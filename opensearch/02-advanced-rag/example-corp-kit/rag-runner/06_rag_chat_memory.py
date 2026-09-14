"""Step 6 (Chapter 4 capstone): a browser chat UI with MEMORY.
Same RAG loop as 05, plus conversation memory via the ML Commons Memory API:
the server creates a memory, stores every turn, reads the history back to
resolve follow-ups (query rewriting), and feeds recent turns into the prompt.
Launch (point at the course knowledge base):
  RAG_INDEX=support-advrag-kb RAG_PIPE=support-advrag-hybrid python3 06_rag_chat_memory.py
Open http://localhost:8788 (bound to 127.0.0.1).
"""
import json, time, os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from osc import os_req, llm_generate, LLM_MODEL, LLM_BACKEND

MODEL_ID = open("model_id.txt").read().strip()
INDEX = os.environ.get("RAG_INDEX", "support-advrag-kb")
PIPE = os.environ.get("RAG_PIPE", "support-advrag-hybrid")
PORT = int(os.environ.get("RAG_PORT", "8788"))
CUSTOMER = os.environ.get("RAG_CUSTOMER", "acme-analytics")
VERSION = os.environ.get("RAG_VERSION", "4.8")
TIER = os.environ.get("RAG_TIER", "standard")

# The system instructions are the Chapter 2 Step 4 string, character for
# character. Everything about this customer lives in the RESTRICTIONS block
# instead, built from the memory's additional_info rather than hard-coded.
SYS = ("You are Example Corp's internal support assistant. Answer ONLY using the "
       "evidence provided below. If the evidence does not contain the answer, say "
       "you do not have that information. After each claim, cite the source in "
       "square brackets using its source_id. Be concise, then end with a final "
       "line that reads Confidence: low, medium, or high.")

RESTRICTIONS = (
    f"The customer is on product version {VERSION}, {TIER} tier. Version matching "
    "is a preference for choosing between sources, NOT a requirement for using "
    "them. Never refuse to answer because the evidence is written for a different "
    "version. If a fix only exists in a later version, give the workaround for "
    "their version and name the version the fix ships in.")

SCHEMA = ("The answer, a [source_id] citation on every claim, then a final line "
          "reading Confidence: low, medium, or high.")


def memory_create():
    c, r = os_req("POST", "/_plugins/_ml/memory/",
                  {"name": f"{CUSTOMER} support session",
                   "additional_info": {"customer_id": CUSTOMER, "product_version": VERSION, "tier": TIER}})
    return r.get("memory_id")

MEMORY_ID = memory_create()


def history():
    c, r = os_req("GET", f"/_plugins/_ml/memory/{MEMORY_ID}/messages")
    return r.get("messages", [])


def store_turn(q, a):
    os_req("POST", f"/_plugins/_ml/memory/{MEMORY_ID}/messages", {"input": q, "response": a})


def embed(text, tries=6):
    for _ in range(tries):
        c, p = os_req("POST", f"/_plugins/_ml/_predict/text_embedding/{MODEL_ID}",
                      {"text_docs": [text], "return_number": True, "target_response": ["sentence_embedding"]})
        try:
            return p["inference_results"][0]["output"][0]["data"]
        except (KeyError, TypeError, IndexError):
            time.sleep(1.0)
    raise RuntimeError("embedding failed")


def rewrite(question, msgs):
    """Turn a follow-up into a standalone query using recent history."""
    if not msgs:
        return question, False
    convo = "\n".join(f"User: {m['input']}\nAssistant: {m['response']}" for m in msgs[-3:])
    prompt = (f"Conversation so far:\n{convo}\n\nUser: {question}\n\n"
              "Rewrite the user's last message as a standalone search query that includes any "
              "error code or version it depends on. Output only the query, nothing else.")
    out = llm_generate(prompt).strip().strip('"').splitlines()[0]
    return (out or question), True


EVIDENCE_BUDGET_WORDS = 1200  # smaller than the single-turn form: memory needs room too


def hybrid(query):
    """Match the child chunks. No `collapse` here: it is incompatible with the
    hybrid RRF processor and reorders the fused list. Dedupe in pack()."""
    vec = embed(query)
    c, r = os_req("POST", f"/{INDEX}/_search?search_pipeline={PIPE}",
                  {"size": 8, "query": {"hybrid": {"queries": [
                      {"multi_match": {"query": query, "fields": ["text", "title", "section_path"]}},
                      {"knn": {"text_embedding": {"vector": vec, "k": 10}}}]}},
                   "_source": ["source_id", "parent_id", "title", "text",
                               "parent_text", "doc_type", "product_version"]})
    return r.get("hits", {}).get("hits", [])


def pack(hits, keep=3):
    """Search matched the child, the model reads the parent. One block per
    parent section. Known issues have no parent, so fall back to the child.
    Respect the budget: the memory block shares this context window.
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
        blocks.append(f"[{s['source_id']}] ({s['doc_type']}, version "
                      f"{s.get('product_version') or 'n/a'}) {s['title']}: {text}")
    print(f"packed {len(blocks)} parent sections ({words} words): "
          f"{', '.join(sorted(seen))}", flush=True)
    return "\n\n".join(blocks), kept


def answer(question):
    msgs = history()
    query, rewrote = rewrite(question, msgs)
    # source chips must name what was packed, one per parent, not every child hit
    ev, hits = pack(hybrid(query))
    # The five blocks from Chapter 2, with memory in the slot TOOLING left empty.
    memblock = f"Customer {CUSTOMER}, product version {VERSION}, {TIER} tier."
    if msgs:
        memblock += "\nRecent turns:\n" + "\n".join(
            f"User: {m['input']}\nAssistant: {m['response']}" for m in msgs[-3:])
    prompt = (f"## MEMORY\n{memblock}\n\n"
              f"## GOAL\n{query}\n\n"
              f"## RESTRICTIONS\n{RESTRICTIONS}\n\n"
              f"## EVIDENCE\n{ev}\n\n"
              f"## ANSWER SCHEMA\n{SCHEMA}")
    ans = llm_generate(prompt, system=SYS)
    if "</think>" in ans:
        ans = ans.split("</think>")[-1].strip()
    store_turn(question, ans.strip())
    return {"answer": ans.strip(),
            "sources": [{"source_id": h["_source"]["source_id"], "title": h["_source"]["title"]} for h in hits],
            "rewrote": query if rewrote and query != question else None,
            "turns": len(msgs) + 1, "model": LLM_MODEL}


PAGE = """<!doctype html><html><head><meta charset=utf-8>
<title>Example Corp RAG with memory</title><style>
body{font-family:-apple-system,Segoe UI,Roboto,sans-serif;max-width:760px;margin:0 auto;padding:20px;background:#f6f7f9;color:#222}
h1{font-size:18px} .sub{color:#666;font-size:13px;margin-bottom:16px}
#log{margin:16px 0} .msg{margin:12px 0;padding:12px 14px;border-radius:10px;line-height:1.5}
.u{background:#dbeafe;text-align:right} .a{background:#fff;border:1px solid #e5e7eb}
.src{font-size:12px;color:#555;margin-top:8px} .rw{font-size:12px;color:#8a6d1a;margin-bottom:6px}
.chip{display:inline-block;background:#eef2ff;border:1px solid #c7d2fe;border-radius:12px;padding:2px 8px;margin:2px}
form{display:flex;gap:8px} input{flex:1;padding:10px;border:1px solid #ccc;border-radius:8px;font-size:15px}
button{padding:10px 16px;border:0;border-radius:8px;background:#2563eb;color:#fff;font-size:15px;cursor:pointer}
button:disabled{background:#9ca3af} button.sec{background:#6b7280} .think{color:#888;font-style:italic}
</style></head><body>
<h1>Example Corp support assistant <span style="font-weight:400;color:#666;font-size:13px">(with memory)</span></h1>
<div class=sub>Hybrid retrieval + <span id=backend>...</span> (<span id=model>...</span>), and a conversation memory that resolves follow-ups. Turns stored: <span id=turns>0</span>.</div>
<div id=log></div>
<form id=f><input id=q autocomplete=off placeholder="Try: How do I fix ERR-1102? then: what about on version 5.0?" autofocus><button id=b>Ask</button><button id=c type=button class=sec>Clear view</button></form>
<script>
const log=document.getElementById('log'),f=document.getElementById('f'),q=document.getElementById('q'),b=document.getElementById('b');
function add(cls,html){const d=document.createElement('div');d.className='msg '+cls;d.innerHTML=html;log.appendChild(d);window.scrollTo(0,document.body.scrollHeight);return d;}
f.onsubmit=async e=>{e.preventDefault();const text=q.value.trim();if(!text)return;q.value='';b.disabled=true;
 add('u',text.replace(/</g,'&lt;'));const t=add('a','<span class=think>remembering, retrieving, generating...</span>');
 try{const r=await fetch('/ask',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({q:text})});
  const d=await r.json();if(d.error){t.innerHTML='<b>error:</b> '+d.error;}else{
  document.getElementById('turns').textContent=d.turns;
  let rw=d.rewrote?('<div class=rw>understood as: '+d.rewrote.replace(/</g,'&lt;')+'</div>'):'';
  let s=d.sources.map(x=>'<span class=chip>'+x.source_id+' &middot; '+x.title+'</span>').join(' ');
  t.innerHTML=rw+d.answer.replace(/</g,'&lt;').replace(/\\n/g,'<br>')+'<div class=src>sources: '+s+'</div>';}
 }catch(err){t.innerHTML='<b>error:</b> '+err;}b.disabled=false;q.focus();};
document.getElementById('c').onclick=()=>{log.innerHTML='';q.focus();};
fetch('/model').then(r=>r.json()).then(d=>{document.getElementById('model').textContent=d.model;
 document.getElementById('backend').textContent=d.backend;});
</script></body></html>"""


class H(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="application/json"):
        b = body.encode() if isinstance(body, str) else body
        self.send_response(code); self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)

    def do_GET(self):
        if self.path == "/":
            self._send(200, PAGE, "text/html; charset=utf-8")
        elif self.path == "/model":
            self._send(200, json.dumps({"model": LLM_MODEL, "backend": LLM_BACKEND,
                                        "memory_id": MEMORY_ID}))
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
    print(f"RAG+memory chat on http://localhost:{PORT}  (model {LLM_MODEL}, memory {MEMORY_ID})", flush=True)
    ThreadingHTTPServer(("127.0.0.1", PORT), H).serve_forever()
