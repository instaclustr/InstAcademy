#!/usr/bin/env node
// Minimal stdio <-> Streamable HTTP bridge for MCP servers that use basic auth.
// Zero dependencies; needs Node 18+.
// Usage: node mcp-basic-auth-bridge.mjs <mcp-url> <base64-of-username:password>

const [url, b64] = process.argv.slice(2);
if (!url || !b64) {
  console.error("usage: node mcp-basic-auth-bridge.mjs <mcp-url> <base64 user:pass>");
  process.exit(1);
}

let buf = "";
process.stdin.setEncoding("utf8");
process.stdin.on("data", (chunk) => {
  buf += chunk;
  let i;
  while ((i = buf.indexOf("\n")) >= 0) {
    const line = buf.slice(0, i).trim();
    buf = buf.slice(i + 1);
    if (line) forward(line);
  }
});
process.stdin.on("end", () => process.exit(0));

async function forward(line) {
  try {
    const res = await fetch(url, {
      method: "POST",
      headers: {
        "Authorization": "Basic " + b64,
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
      },
      body: line,
    });
    const text = await res.text();
    if (!text || !text.trim()) return; // notifications get 202 with no body
    const ct = res.headers.get("content-type") || "";
    if (ct.includes("text/event-stream")) {
      for (const event of text.split("\n\n")) {
        for (const l of event.split("\n")) {
          if (l.startsWith("data:")) process.stdout.write(l.slice(5).trim() + "\n");
        }
      }
    } else {
      process.stdout.write(text.replace(/\r?\n/g, "") + "\n");
    }
  } catch (e) {
    try {
      const msg = JSON.parse(line);
      if (msg.id !== undefined) {
        process.stdout.write(
          JSON.stringify({ jsonrpc: "2.0", id: msg.id, error: { code: -32000, message: String(e) } }) + "\n"
        );
      }
    } catch {
      // unparseable input line; nothing sensible to report
    }
  }
}
