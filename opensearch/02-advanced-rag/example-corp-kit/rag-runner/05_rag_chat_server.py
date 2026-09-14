"""Step 5: a browser chat UI for the RAG loop (stdlib only, no installs).
Each question runs embed (OpenSearch ML) -> retrieve (OpenSearch) -> pack
parents -> generate (Groq, Gemini, or Ollama). Retrieval matches the small
child chunks; packing keeps one section per parent_id and hands the model
parent_text (falling back to the child for one-record doc types like
known issues) inside a word budget. The page has an Ask button and a
Clear button.
Launch:
  OS_URL=... OS_USER=... OS_PW=... OLLAMA_MODEL=llama3.2:3b python3 05_rag_chat_server.py
  OS_URL=... OS_USER=... OS_PW=... LLM_BACKEND=gemini GEMINI_API_KEY=... python3 05_rag_chat_server.py
Then open http://localhost:8787  (the port is bound to 127.0.0.1 only).
"""
import json, time, os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from osc import os_req, llm_generate, LLM_MODEL, LLM_BACKEND

MODEL_ID = open("model_id.txt").read().strip()
INDEX = os.environ.get("RAG_INDEX", "support-advrag-kb")
# RAG_PIPE is optional on purpose. Leave it unset and this server runs a
# single-leg vector search, which is what Chapter 2 teaches. Set it to the
# hybrid search pipeline once Chapter 3 Step 5 has created that pipeline, and
# the same server fuses a BM25 leg alongside the vector leg. Chapter 3 Step 9
# asks you to compare the two.
PIPE = os.environ.get("RAG_PIPE", "").strip()
PORT = int(os.environ.get("RAG_PORT", "8787"))
RETRIEVAL_MODE = (f"hybrid via {PIPE}" if PIPE else "vector only")

SYS = ("You are Example Corp's internal support assistant. Answer ONLY using the "
       "evidence provided below. If the evidence does not contain the answer, say "
       "you do not have that information. After each claim, cite the source in "
       "square brackets using its source_id. Be concise, then end with a final "
       "line that reads Confidence: low, medium, or high.")

def embed(text, tries=8):
    for _ in range(tries):
        c, p = os_req("POST", f"/_plugins/_ml/models/{MODEL_ID}/_predict",
                      {"text_docs": [text], "return_number": True,
                       "target_response": ["sentence_embedding"]})
        try:
            return p["inference_results"][0]["output"][0]["data"]
        except (KeyError, TypeError, IndexError):
            time.sleep(1.0)
    raise RuntimeError("embedding failed")

EVIDENCE_BUDGET_WORDS = 1500  # leave room for the answer inside the context window
RETRIEVE_WIDE = 8             # retrieve wide, dedupe to parents, keep the top 3

SOURCE_FIELDS = ["source_id", "parent_id", "title", "text",
                 "parent_text", "doc_type", "product_version"]


def retrieve(q, k=RETRIEVE_WIDE):
    """Match the small child chunks, then dedupe to parents in pack().

    Two retrieval modes, chosen by whether RAG_PIPE is set:

      unset  a single-leg vector search. This is the Chapter 2 system: the
             question is embedded and matched by meaning, nothing else.
      set    a hybrid query fused by the Chapter 3 search pipeline, so a BM25
             leg runs alongside the vector leg and RRF merges the two.

    Deliberately NO `collapse` in either mode. It is incompatible with the
    hybrid RRF processor (it reorders the fused list and can drop the top hit
    entirely), so parent dedupe happens after retrieval, in pack()."""
    vec = embed(q)
    knn = {"knn": {"text_embedding": {"vector": vec, "k": 10}}}
    if PIPE:
        path = f"/{INDEX}/_search?search_pipeline={PIPE}"
        query = {"hybrid": {"queries": [{"match": {"text": q}}, knn]}}
    else:
        path = f"/{INDEX}/_search"
        query = knn
    c, r = os_req("POST", path,
                  {"size": k, "query": query, "_source": SOURCE_FIELDS})
    return r.get("hits", {}).get("hits", [])

def pack(hits, keep=3):
    """The parent-child payoff: search matched the child, the model reads the
    parent. One block per parent section, so sibling children never spend the
    budget twice. Known issues are one record with no parent, so fall back to
    the child. Stop at `keep` sections or when the budget is spent.
    Returns the evidence string and the hits that actually made it in."""
    seen, blocks, kept, words = set(), [], [], 0
    for h in hits:
        if len(blocks) >= keep:
            break
        s = h["_source"]
        pid = s.get("parent_id") or s["source_id"]
        if pid in seen:
            continue
        text = s.get("parent_text") or s["text"]
        n = len(text.split())
        if blocks and words + n > EVIDENCE_BUDGET_WORDS:
            break
        seen.add(pid)
        words += n
        kept.append(h)
        blocks.append(f"[{s['source_id']}] ({s['doc_type']}, "
                      f"v{s.get('product_version') or 'n/a'}) {s['title']}: {text}")
    print(f"packed {len(blocks)} parent sections ({words} words): "
          f"{', '.join(sorted(seen))}", flush=True)
    return "\n\n".join(blocks), kept

def answer(q):
    # source chips must name what was packed, one per parent, not every child hit
    hits, ev = retrieve(q), None
    ev, hits = pack(hits)
    prompt = f"Evidence:\n{ev}\n\nQuestion: {q}\n\nGrounded answer with [source_id] citations:"
    ans = llm_generate(prompt, system=SYS)
    if "</think>" in ans:
        ans = ans.split("</think>")[-1].strip()
    sources = [{"source_id": h["_source"]["source_id"], "title": h["_source"]["title"],
                "score": round(h["_score"], 4)} for h in hits]
    return {"answer": ans.strip(), "sources": sources, "model": LLM_MODEL}

PAGE = """<!doctype html><html><head><meta charset=utf-8>
<title>Example Corp RAG</title><style>
body{font-family:-apple-system,Segoe UI,Roboto,sans-serif;max-width:760px;margin:0 auto;padding:20px;background:#f6f7f9;color:#222}
h1{font-size:18px} .sub{color:#666;font-size:13px;margin-bottom:16px}
#log{margin:16px 0} .msg{margin:12px 0;padding:12px 14px;border-radius:10px;line-height:1.5}
.u{background:#dbeafe;text-align:right} .a{background:#fff;border:1px solid #e5e7eb}
.src{font-size:12px;color:#555;margin-top:8px} .chip{display:inline-block;background:#eef2ff;border:1px solid #c7d2fe;border-radius:12px;padding:2px 8px;margin:2px}
form{display:flex;gap:8px} input{flex:1;padding:10px;border:1px solid #ccc;border-radius:8px;font-size:15px}
button{padding:10px 16px;border:0;border-radius:8px;background:#2563eb;color:#fff;font-size:15px;cursor:pointer}
button:disabled{background:#9ca3af} button.sec{background:#6b7280} .think{color:#888;font-style:italic}
</style></head><body>
<h1>Example Corp support assistant</h1>
<div class=sub>Retrieval: OpenSearch <span id=mode>...</span> &middot; Generation: <span id=backend>...</span> (<span id=model>...</span>) &middot; grounded, cites sources, declines when the answer is not in the corpus.</div>
<div id=log></div>
<form id=f><input id=q autocomplete=off placeholder="Ask about ERR-1102, slow dashboards, audit event retention..." autofocus><button id=b>Ask</button><button id=c type=button class=sec>Clear</button></form>
<script>
const log=document.getElementById('log'),f=document.getElementById('f'),q=document.getElementById('q'),b=document.getElementById('b');
function add(cls,html){const d=document.createElement('div');d.className='msg '+cls;d.innerHTML=html;log.appendChild(d);window.scrollTo(0,document.body.scrollHeight);return d;}
f.onsubmit=async e=>{e.preventDefault();const text=q.value.trim();if(!text)return;q.value='';b.disabled=true;
 add('u',text.replace(/</g,'&lt;'));const t=add('a','<span class=think>retrieving and generating...</span>');
 try{const r=await fetch('/ask',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({q:text})});
  const d=await r.json();if(d.error){t.innerHTML='<b>error:</b> '+d.error;}else{
  let s=d.sources.map(x=>'<span class=chip>'+x.source_id+' &middot; '+x.title+'</span>').join(' ');
  t.innerHTML=d.answer.replace(/</g,'&lt;').replace(/\\n/g,'<br>')+'<div class=src>sources: '+s+'</div>';}
 }catch(err){t.innerHTML='<b>error:</b> '+err;}b.disabled=false;q.focus();};
document.getElementById('c').onclick=()=>{log.innerHTML='';q.focus();};
fetch('/model').then(r=>r.json()).then(d=>{document.getElementById('model').textContent=d.model;
 document.getElementById('backend').textContent=d.backend;document.getElementById('mode').textContent=d.retrieval;});
</script></body></html>"""

class H(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="application/json"):
        b = body.encode() if isinstance(body, str) else body
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_GET(self):
        if self.path == "/":
            self._send(200, PAGE, "text/html; charset=utf-8")
        elif self.path == "/model":
            self._send(200, json.dumps(
                {"model": LLM_MODEL, "backend": LLM_BACKEND,
                 "retrieval": RETRIEVAL_MODE}))
        else:
            self._send(404, json.dumps({"error": "not found"}))

    def do_POST(self):
        if self.path != "/ask":
            self._send(404, json.dumps({"error": "not found"})); return
        try:
            n = int(self.headers.get("Content-Length", 0))
            q = json.loads(self.rfile.read(n)).get("q", "").strip()
            if not q:
                self._send(400, json.dumps({"error": "empty question"})); return
            self._send(200, json.dumps(answer(q)))
        except Exception as e:
            self._send(200, json.dumps({"error": str(e)}))

    def log_message(self, *a):
        pass

if __name__ == "__main__":
    print(f"RAG chat UI on http://localhost:{PORT}  "
          f"(model {LLM_MODEL}, retrieval {RETRIEVAL_MODE})", flush=True)
    ThreadingHTTPServer(("127.0.0.1", PORT), H).serve_forever()
