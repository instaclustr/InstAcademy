"""Tiny stdlib OpenSearch + Ollama client for the local-Ollama RAG lab.
Configuration is read from a .env file in this folder if present, and from
real environment variables, which take precedence over .env. No secrets
live in the tracked files: copy .env.example to .env and fill it in.
Works on macOS, Linux, and Windows (standard library only, no pip).
"""
import os, json, ssl, time, base64, urllib.request, urllib.error


def _load_dotenv():
    """Load KEY=VALUE lines from a .env file next to this script."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            # real environment variables win, so only fill what is not set
            os.environ.setdefault(key.strip(), val.strip().strip('"').strip("'"))


_load_dotenv()


def _require(name):
    val = os.environ.get(name)
    if not val:
        raise SystemExit(
            f"Missing {name}. Copy .env.example to .env in this folder and fill in "
            f"your values, or set {name} as an environment variable.")
    return val


OS_URL = _require("OS_URL").rstrip("/")
OS_USER = _require("OS_USER")
OS_PW = _require("OS_PW")
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434").rstrip("/")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2:3b")

# Which model writes the answers. "gemini" follows the five-block prompt the
# course teaches; a 3B local model does not, and will invent a procedure
# rather than decline. "ollama" needs no signup and no quota, so it is both
# the zero-signup option and the fallback when the free tier runs out.
LLM_BACKEND = os.environ.get("LLM_BACKEND", "ollama").strip().lower()
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GROQ_MODEL = os.environ.get("GROQ_MODEL", "openai/gpt-oss-120b")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

# Fall back to Ollama rather than failing when the key for a cloud backend is
# missing, so a learner without a key still gets a working runner.
_KEYS = {"gemini": GEMINI_API_KEY, "groq": GROQ_API_KEY}
if LLM_BACKEND in _KEYS and not _KEYS[LLM_BACKEND]:
    print(f"LLM_BACKEND={LLM_BACKEND} but its API key is not set. "
          f"Using Ollama instead.", flush=True)
    LLM_BACKEND = "ollama"
LLM_MODEL = {"gemini": GEMINI_MODEL, "groq": GROQ_MODEL}.get(
    LLM_BACKEND, OLLAMA_MODEL)

_ctx = ssl.create_default_context()
_ctx.check_hostname = False
_ctx.verify_mode = ssl.CERT_NONE
_auth = "Basic " + base64.b64encode(f"{OS_USER}:{OS_PW}".encode()).decode()


def os_req(method, path, body=None, timeout=60):
    url = OS_URL + path
    data = None
    headers = {"Authorization": _auth, "Content-Type": "application/json"}
    if body is not None:
        data = body.encode() if isinstance(body, str) else json.dumps(body).encode()
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=_ctx) as r:
            raw = r.read().decode()
    except urllib.error.HTTPError as e:
        raw = e.read().decode()
        return e.code, (json.loads(raw) if raw.strip().startswith(("{", "[")) else raw)
    return 200, (json.loads(raw) if raw.strip().startswith(("{", "[")) else raw)


def ollama_generate(prompt, system=None, timeout=300):
    # num_ctx is capped on purpose. Without it Ollama allocates the model's
    # full trained context window, which for llama3.2:3b means a multi-GB KV
    # cache for packed evidence that is only a few hundred tokens long. That
    # is enough to stall a fanless laptop.
    body = {"model": OLLAMA_MODEL, "prompt": prompt, "stream": False,
            "options": {"temperature": 0.0, "num_ctx": 4096}}
    if system:
        body["system"] = system
    req = urllib.request.Request(OLLAMA_URL + "/api/generate",
                                 data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"},
                                 method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode()).get("response", "")


def gemini_generate(prompt, system=None, timeout=120, tries=5):
    """Google AI Studio. The key goes in the x-goog-api-key HEADER: passing it
    as ?key= returns a bare 404 that reads like a bad model name. The free tier
    allows only a few requests per minute, so a 429 is normal rather than an
    error, and waiting is the correct response to it."""
    body = {"contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0}}
    if system:
        body["systemInstruction"] = {"parts": [{"text": system}]}
    url = (f"https://generativelanguage.googleapis.com/v1beta/models/"
           f"{GEMINI_MODEL}:generateContent")
    data = json.dumps(body).encode()
    delay = 15
    for attempt in range(tries):
        req = urllib.request.Request(
            url, data=data, method="POST",
            headers={"Content-Type": "application/json",
                     "x-goog-api-key": GEMINI_API_KEY})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                parts = (json.loads(r.read().decode())["candidates"][0]
                         ["content"]["parts"])
                return "".join(p.get("text", "") for p in parts)
        except urllib.error.HTTPError as e:
            detail = e.read().decode()[:200]
            if e.code in (429, 503) and attempt < tries - 1:
                print(f"  [{e.code} from Gemini, waiting {delay}s]", flush=True)
                time.sleep(delay)
                delay = min(delay * 2, 60)
                continue
            if e.code == 429:
                raise SystemExit(
                    "Gemini free-tier quota is exhausted. Either wait for it to "
                    "reset, or switch to the local model for the rest of the "
                    "session by setting LLM_BACKEND=ollama in your .env.")
            raise SystemExit(f"Gemini returned HTTP {e.code}: {detail}")


def groq_generate(prompt, system=None, timeout=120, tries=5):
    """Groq, OpenAI-compatible. Its free tier allows far more requests per day
    than Google's, which matters because one pass through this course is about
    twenty generation calls."""
    msgs = ([{"role": "system", "content": system}] if system else []) + \
           [{"role": "user", "content": prompt}]
    data = json.dumps({"model": GROQ_MODEL, "temperature": 0,
                       "messages": msgs}).encode()
    delay = 15
    for attempt in range(tries):
        req = urllib.request.Request(
            "https://api.groq.com/openai/v1/chat/completions",
            data=data, method="POST",
            headers={"Content-Type": "application/json",
                     "Authorization": f"Bearer {GROQ_API_KEY}",
                     # Groq sits behind Cloudflare, which blocks urllib's
                     # default User-Agent with a 403 "error code: 1010".
                     # Any explicit User-Agent gets through.
                     "User-Agent": "example-corp-rag-lab/1.0"})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read().decode())["choices"][0]["message"]["content"]
        except urllib.error.HTTPError as e:
            detail = e.read().decode()[:200]
            if e.code in (429, 503) and attempt < tries - 1:
                print(f"  [{e.code} from Groq, waiting {delay}s]", flush=True)
                time.sleep(delay)
                delay = min(delay * 2, 60)
                continue
            raise SystemExit(f"Groq returned HTTP {e.code}: {detail}")


def llm_generate(prompt, system=None):
    """One entry point so the chapters do not care which model is behind it."""
    if LLM_BACKEND == "gemini":
        return gemini_generate(prompt, system=system)
    if LLM_BACKEND == "groq":
        return groq_generate(prompt, system=system)
    return ollama_generate(prompt, system=system)
