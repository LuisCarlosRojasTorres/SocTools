from html import escape
from http.server import BaseHTTPRequestHandler, HTTPServer

from .config import load_component_config


class ServerComponent:
    def __init__(self, config=None):
        self.config = config or load_component_config("serverComponent.ini")
        self.host = self.config.get("server", "host", fallback="127.0.0.1")
        self.port = self.config.getint("server", "port", fallback=8000)
        self.title = self.config.get("server", "title", fallback="SocTools")

    def build_url(self) -> str:
        return f"http://{self.host}:{self.port}"

    def build_page(self, message: str) -> str:
        escaped_message = escape(message)
        escaped_title = escape(self.title)
        return (
            "<!doctype html>"
            "<html><head>"
            f"<title>{escaped_title}</title>"
            "</head><body>"
            f"<h1>{escaped_title}</h1>"
            f"<p>{escaped_message}</p>"
            "</body></html>"
        )

    def create_handler(self, message: str):
        page = self.build_page(message).encode("utf-8")

        class RequestHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(page)))
                self.end_headers()
                self.wfile.write(page)

            def log_message(self, format, *args):
                return

        return RequestHandler

    def serve(self, message: str):
        with HTTPServer((self.host, self.port), self.create_handler(message)) as httpd:
            print(f"Serving SocTools UI at {self.build_url()}")
            httpd.serve_forever()

