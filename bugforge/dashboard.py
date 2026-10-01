"""Minimal local web dashboard using Python stdlib."""
import json
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path

def serve(report_dir="reports",host="127.0.0.1",port=8080):
    root=Path(report_dir)
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path!="/": self.send_error(404); return
            reports=[]
            for p in root.glob("*.json"):
                try: reports.append(json.loads(p.read_text()))
                except Exception: pass
            body=("<!doctype html><html><head><title>BugForge</title></head><body>"
                  "<h1>BugForge Dashboard</h1><p>Reports: %d</p><pre>%s</pre></body></html>"
                  %(len(reports),json.dumps(reports,indent=2))).encode()
            self.send_response(200); self.send_header("Content-Type","text/html; charset=utf-8")
            self.send_header("Content-Length",str(len(body))); self.end_headers(); self.wfile.write(body)
    print(f"BugForge dashboard: http://{host}:{port}")
    ThreadingHTTPServer((host,port),Handler).serve_forever()
