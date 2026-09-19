"""
Interactive Web Sandbox & Developer Console Server for Instagram Specialist Agent.
Provides full backward and forward compatibility with Leno OS (Digital Distribution OS)
and Leno UI on http://localhost:5002 (or custom PORT).
"""

import json
import os
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from typing import Dict, Any

# Ensure UTF-8 console output on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

from instagram_agent.agent.instagram_agent import InstagramSpecialistAgent
from instagram_agent.adapter.leno_adapter import leno_adapter

# Port configuration: CLI arg > PORT env var > default 5002
PORT = 5002
if len(sys.argv) > 1 and sys.argv[1].isdigit():
    PORT = int(sys.argv[1])
elif os.getenv("PORT") and os.getenv("PORT").isdigit():
    PORT = int(os.getenv("PORT"))

agent_instance = InstagramSpecialistAgent()


class ReusableHTTPServer(HTTPServer):
    allow_reuse_address = True


class InstagramAgentSandboxHandler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        sys.stdout.write("%s - - [%s] %s\n" % (self.address_string(), self.log_date_time_string(), format % args))

    def _send_json(self, data: Any, status: int = 200):
        body = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Requested-With")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS, HEAD")
        self.end_headers()
        self.wfile.write(body)

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Requested-With")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS, HEAD")
        self.end_headers()

    def do_GET(self):
        base_dir = Path(__file__).parent

        try:
            # 1. Leno OS Health & Overview Check
            if self.path in ("/api/overview", "/api/health", "/health"):
                tavily_key = os.getenv("TAVILY_API_KEY", "")
                airtop_key = os.getenv("AIRTOP_API_KEY", "")
                self._send_json({
                    "status": "operational",
                    "agent_status": "operational",
                    "agent": "Instagram Specialist Agent",
                    "platform": "instagram",
                    "version": "2.0-specialist",
                    "leno_os_compatible": True,
                    "capabilities": [
                        "Carousels (4:5 Portrait)",
                        "Static Posts (1:1 & 4:5)",
                        "Story Sequences (9:16 Vertical)",
                        "Content Calendars",
                        "Reels Notice Guardrail",
                        "12 Visual Archetypes",
                        "Leno OS Bidirectional Adapter"
                    ],
                    "providers": {
                        "agent_core": {"connected": True, "type": "Autonomous Instagram Specialist Agent"},
                        "svg_creative_engine": {"connected": True, "type": "Automated SVG Generation"},
                        "leno_adapter": {"connected": True, "type": "Leno OS Schema Bridge"},
                        "tavily_search": {"connected": bool(tavily_key), "type": "Live Web Search API"},
                        "airtop_browser": {"connected": bool(airtop_key), "type": "Cloud Browser & Scraper"}
                    },
                    "endpoints": [
                        "/api/draft (Leno OS Draft & Critique connector)",
                        "/api/generate-post (Leno UI Cockpit connector)",
                        "/api/run-instagram-agent (Raw Agent Contract)",
                        "/api/overview (Health and status)"
                    ]
                })
                return

            # 2. Web Visual Sandbox
            if self.path in ("/", "/index.html", "/preview.html", "/instagram_preview.html"):
                html_file = base_dir / "preview.html"
                if not html_file.exists():
                    html_file = base_dir / "instagram_preview.html"

                if html_file.exists():
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html; charset=utf-8")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    with open(html_file, "rb") as f:
                        self.wfile.write(f.read())
                else:
                    self.send_error(404, "Preview HTML file not found")
                return

            # 3. Sample Inputs & Outputs
            if self.path == "/api/example-input":
                example_file = base_dir / "example_input.json"
                if example_file.exists():
                    with open(example_file, "rb") as f:
                        self._send_json(json.loads(f.read().decode("utf-8")))
                else:
                    self.send_error(404, "example_input.json not found")
                return

            if self.path.startswith("/instagram_test_inputs/"):
                file_name = Path(self.path).name
                target = base_dir / "instagram_test_inputs" / file_name
                if target.exists():
                    with open(target, "rb") as f:
                        self._send_json(json.loads(f.read().decode("utf-8")))
                else:
                    self.send_error(404, "Input file not found")
                return

            if self.path.startswith("/instagram_outputs/"):
                file_name = Path(self.path).name
                target = base_dir / "instagram_outputs" / file_name
                if target.exists():
                    with open(target, "rb") as f:
                        self._send_json(json.loads(f.read().decode("utf-8")))
                else:
                    self.send_error(404, "Output file not found")
                return

            self.send_response(404)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"404 Not Found")
        except (ConnectionAbortedError, BrokenPipeError):
            pass

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body_bytes = self.rfile.read(content_length)

        try:
            input_payload = json.loads(body_bytes.decode("utf-8")) if body_bytes else {}

            # ── Endpoint A: Leno OS Native Platform Connector (/api/draft) ──
            # Used directly by Leno OS Orchestrator & src/agents/platforms/instagram.ts
            if self.path in ("/api/draft", "/api/leno/draft"):
                leno_draft = leno_adapter.execute_leno_request(input_payload)
                self._send_json(leno_draft)
                return

            # ── Endpoint B: Leno UI Cockpit Connector (/api/generate-post) ──
            # Used by Leno UI creative cockpit (js/api.js)
            if self.path == "/api/generate-post":
                leno_draft = leno_adapter.execute_leno_request(input_payload)
                hook = input_payload.get("hook") or input_payload.get("core_message", "").split("\n")[0]
                if not hook:
                    hook = leno_draft.get("title", "Strategic System Architecture")

                response = {
                    "status": "success",
                    "draft": {
                        "hook": hook,
                        "body": leno_draft.get("body", ""),
                        "hashtags": leno_draft.get("hashtags", []),
                    },
                    "instagram": {
                        "title": leno_draft.get("title", "Instagram Carousel"),
                        "hook": hook,
                        "body": leno_draft.get("body", ""),
                        "hashtags": leno_draft.get("hashtags", []),
                        "score": f"{leno_draft.get('quality', {}).get('score', 9.5)}/10",
                        "slides": leno_draft.get("slides", []),
                        "svg_preview": leno_draft.get("svg_preview", ""),
                    }
                }
                self._send_json(response)
                return

            # ── Endpoint C: Raw Instagram Specialist Agent Contract ──
            if self.path in ("/api/run-instagram-agent", "/api/run-agent"):
                output_dict = agent_instance.run_raw(input_payload)
                self._send_json(output_dict)
                return

            self._send_json({"error": f"Endpoint '{self.path}' not found"}, 404)
        except (ConnectionAbortedError, BrokenPipeError):
            pass
        except Exception as e:
            try:
                self._send_json({"error": str(e)}, 500)
            except (ConnectionAbortedError, BrokenPipeError):
                pass


def run_server():
    server_address = ("", PORT)
    httpd = ReusableHTTPServer(server_address, InstagramAgentSandboxHandler)
    print("=" * 70)
    print("  📸 INSTAGRAM SPECIALIST AGENT — LENO OS COMPATIBLE DAEMON")
    print("=" * 70)
    print(f"  🌐 Live Web Preview:   http://localhost:{PORT}")
    print(f"  ⚡ Leno OS Connector:  http://localhost:{PORT}/api/draft")
    print(f"  🚀 Leno UI Cockpit:    http://localhost:{PORT}/api/generate-post")
    print(f"  📡 Agent Raw Contract: http://localhost:{PORT}/api/run-instagram-agent")
    print(f"  🩺 Health & Overview:  http://localhost:{PORT}/api/overview")
    print("-" * 70)
    print("  Ready to process requests from Leno OS, UI, or CLI. (Ctrl+C to stop)\n")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[INFO] Shutting down Instagram Agent Console...")
        httpd.server_close()


if __name__ == "__main__":
    run_server()
