"""
Interactive Web Sandbox & Developer Console Server for Instagram Specialist Agent.
Serves visual preview dashboards on http://localhost:5002.
"""

import json
import os
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

# Ensure UTF-8 console output on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

from instagram_agent.agent.instagram_agent import InstagramSpecialistAgent

PORT = int(os.getenv("PORT", "5002"))
agent_instance = InstagramSpecialistAgent()


class ReusableHTTPServer(HTTPServer):
    allow_reuse_address = True


class InstagramAgentSandboxHandler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        sys.stdout.write("%s - - [%s] %s\n" % (self.address_string(), self.log_date_time_string(), format % args))

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()

    def do_GET(self):
        base_dir = Path(__file__).parent

        try:
            if self.path in ("/", "/index.html", "/preview.html", "/instagram_preview.html"):
                html_file = base_dir / "preview.html"
                if not html_file.exists():
                    html_file = base_dir / "instagram_preview.html"

                if html_file.exists():
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html; charset=utf-8")
                    self.end_headers()
                    with open(html_file, "rb") as f:
                        self.wfile.write(f.read())
                else:
                    self.send_error(404, "Preview HTML file not found")

            elif self.path == "/api/example-input":
                example_file = base_dir / "example_input.json"
                if example_file.exists():
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json; charset=utf-8")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    with open(example_file, "rb") as f:
                        self.wfile.write(f.read())
                else:
                    self.send_error(404, "example_input.json not found")

            elif self.path.startswith("/instagram_test_inputs/"):
                file_name = Path(self.path).name
                target = base_dir / "instagram_test_inputs" / file_name
                if target.exists():
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json; charset=utf-8")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    with open(target, "rb") as f:
                        self.wfile.write(f.read())
                else:
                    self.send_error(404, "Input file not found")

            elif self.path.startswith("/instagram_outputs/"):
                file_name = Path(self.path).name
                target = base_dir / "instagram_outputs" / file_name
                if target.exists():
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json; charset=utf-8")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    with open(target, "rb") as f:
                        self.wfile.write(f.read())
                else:
                    self.send_error(404, "Output file not found")

            else:
                self.send_response(404)
                self.send_header("Content-Type", "text/plain")
                self.end_headers()
                self.wfile.write(b"404 Not Found")
        except (ConnectionAbortedError, BrokenPipeError):
            pass

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)

        try:
            if self.path in ("/api/run-instagram-agent", "/api/run-agent"):
                input_payload = json.loads(body.decode("utf-8"))
                output_dict = agent_instance.run_raw(input_payload)

                response_bytes = json.dumps(output_dict, indent=2).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(response_bytes)
            else:
                self.send_response(404)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Endpoint Not Found"}).encode("utf-8"))
        except (ConnectionAbortedError, BrokenPipeError):
            pass
        except Exception as e:
            try:
                err_bytes = json.dumps({"error": str(e)}).encode("utf-8")
                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(err_bytes)
            except (ConnectionAbortedError, BrokenPipeError):
                pass

    def do_OPTIONS(self):
        try:
            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS, HEAD")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.end_headers()
        except (ConnectionAbortedError, BrokenPipeError):
            pass


def run_server():
    server_address = ("", PORT)
    httpd = ReusableHTTPServer(server_address, InstagramAgentSandboxHandler)
    print("=" * 65)
    print("  INSTAGRAM SPECIALIST AGENT — DEVELOPER TESTBED CONSOLE")
    print("=" * 65)
    print(f"  Live UI:    http://localhost:{PORT}")
    print(f"  API:        http://localhost:{PORT}/api/run-instagram-agent")
    print(f"  Example:    http://localhost:{PORT}/api/example-input")
    print("-" * 65)
    print("  Ready to process requests. Press Ctrl+C to terminate.\n")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[INFO] Shutting down Instagram Agent Console...")
        httpd.server_close()


if __name__ == "__main__":
    run_server()
