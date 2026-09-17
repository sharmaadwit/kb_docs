#!/usr/bin/env python3
"""Temporary diagnostic HTTP server: logs the FULL raw request (headers + body)
SuperAgent sends for kb_answer calls, then answers using the real skill code so
the test account still gets a genuine response.

Point a SuperAgent microagent config at this server's public tunnel URL
(ngrok/cloudflared, etc.) for ONE test account only, make a query, then read
back local/reports/superagent_capture.jsonl to see exactly what was sent.
Point the microagent config back at the real skill endpoint when done.

Usage:
    python3 local/scripts/capture_superagent_payload.py [--port 8765]
"""
import sys, os, json, argparse
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "skill"))

CAPTURE_LOG = os.path.join(os.path.dirname(__file__), "..", "reports", "superagent_capture.jsonl")


class _NoopContext:
    """Minimal context stand-in — real Langfuse/GitLab secrets aren't available
    here, so this only exercises identity/param extraction, not KB retrieval."""
    def get_secret(self, name):
        return os.environ.get(name)


class CaptureHandler(BaseHTTPRequestHandler):
    def _capture_and_respond(self):
        length = int(self.headers.get("Content-Length", 0) or 0)
        raw_body = self.rfile.read(length) if length else b""
        try:
            parsed_body = json.loads(raw_body) if raw_body else {}
        except Exception:
            parsed_body = {"<unparsed_raw_body>": raw_body.decode("utf-8", errors="replace")}

        record = {
            "captured_at": datetime.now(timezone.utc).isoformat(),
            "method": self.command,
            "path": self.path,
            "headers": dict(self.headers.items()),
            "body": parsed_body,
        }
        os.makedirs(os.path.dirname(CAPTURE_LOG), exist_ok=True)
        with open(CAPTURE_LOG, "a") as f:
            f.write(json.dumps(record, default=str) + "\n")
        print(f"[CAPTURED] {self.command} {self.path} — body keys: {list(parsed_body.keys()) if isinstance(parsed_body, dict) else type(parsed_body).__name__}", flush=True)

        answer_text = "Test capture received — this is a diagnostic response, not a real KB answer."
        try:
            import kb_answer as _kb
            params = parsed_body if isinstance(parsed_body, dict) else {}
            if "query" in params:
                result = _kb.kb_answer(parameters=params, context=_NoopContext())
                answer_text = result.get("answer", answer_text)
        except Exception as e:
            answer_text = f"Diagnostic server: captured OK, kb_answer call failed ({type(e).__name__}: {e})"

        payload = json.dumps({"answer": answer_text}).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_POST(self):
        self._capture_and_respond()

    def do_GET(self):
        self._capture_and_respond()

    def log_message(self, fmt, *args):
        pass  # suppress default access logging; we print our own line above


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8765)
    args = ap.parse_args()

    print(f"Capture server listening on http://0.0.0.0:{args.port}")
    print(f"Logging every request to {os.path.abspath(CAPTURE_LOG)}")
    print("Expose this via a tunnel (ngrok/cloudflared) and point the SuperAgent")
    print("microagent config at the tunnel URL for your TEST ACCOUNT ONLY.")
    server = ThreadingHTTPServer(("0.0.0.0", args.port), CaptureHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
