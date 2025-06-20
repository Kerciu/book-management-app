from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = 8080

class SingleFileHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        content = None
        path = self.path
        file = None
        if path.endswith(".html") or path.endswith(".js") or path.endswith(".wasm") or path.endswith(".css"):
            file = path
        else:
            file = "index.html"
        with open(file, "rb") as f:
            content = f.read()
        self.send_response(200)
        if path.endswith(".html"):
            self.send_header("Content-Type", "text/html")
        if path.endswith(".js"):
            self.send_header("Content-Type", "text/javascript")
        if path.endswith(".css"):
            self.send_header("Content-Type", "text/css")
        if path.endswith(".wasm"):
            self.send_header("Content-Type", "text/wasm")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

print("Staring", flush=True)
if __name__ == "__main__":
    httpd = HTTPServer(("0.0.0.0", PORT), SingleFileHandler)
    print(f"Serving at http://0.0.0.0:{PORT}", flush=True)
    httpd.serve_forever()