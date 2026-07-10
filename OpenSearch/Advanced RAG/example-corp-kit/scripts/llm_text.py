"""
Extract the generated text from an ML Commons remote-model predict
response, whichever provider is behind the connector (Gemini or
Cohere). Labs pipe predict output through this so every LLM command
works identically on both providers.

Usage:
    curl ... /_plugins/_ml/models/$LLM_ID/_predict ... | python3 scripts/llm_text.py
"""
import json
import sys


def main():
    raw = sys.stdin.read()
    try:
        resp = json.loads(raw)
    except ValueError:
        sys.exit(f"not JSON: {raw[:300]}")
    if "error" in resp:
        sys.exit(f"predict error: {str(resp)[:400]}")
    try:
        dam = resp["inference_results"][0]["output"][0]["dataAsMap"]
    except (KeyError, IndexError):
        sys.exit(f"unexpected response shape: {raw[:400]}")

    # Gemini: candidates[0].content.parts[0].text
    if "candidates" in dam:
        print(dam["candidates"][0]["content"]["parts"][0]["text"].strip())
        return
    # Cohere v2 chat: message.content[0].text
    if "message" in dam:
        parts = dam["message"]["content"]
        print(" ".join(p.get("text", "") for p in parts).strip())
        return
    sys.exit(f"unrecognized provider payload: {str(dam)[:400]}")


if __name__ == "__main__":
    main()
