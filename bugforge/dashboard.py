"""Local investigation dashboard using only Python stdlib."""
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

def serve(report_dir="reports",host="127.0.0.1",port=8080):
    root=Path(report_dir); root.mkdir(parents=True,exist_ok=True)
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if urlparse(self.path).path=="/api/reports":
                items=[]
                for p in sorted(root.glob("*.json")):
                    try: items.append({"file":p.name,"data":json.loads(p.read_text())})
                    except Exception: pass
                body=json.dumps(items).encode()
                self.send_response(200); self.send_header("Content-Type","application/json"); self.send_header("Content-Length",str(len(body))); self.end_headers(); self.wfile.write(body); return
            reports=[]
            for p in sorted(root.glob("*.json")):
                try: reports.append(json.loads(p.read_text()))
                except Exception: pass
            rows="".join(f"<tr><td>{x.get('crash_type','')}</td><td><code>{x.get('fingerprint','')}</code></td><td>{len(x.get('frames',[]))}</td></tr>" for x in reports)
            body=f"""<!doctype html><meta name="viewport" content="width=device-width,initial-scale=1"><title>BugForge</title><style>
            body{{font-family:system-ui;max-width:1100px;margin:auto;padding:24px;background:#0b1020;color:#eef2ff}}.hero,.card{{background:#141b2d;border:1px solid #293451;border-radius:16px;padding:20px;margin:14px 0}}.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}}.metric{{font-size:30px;font-weight:700}}table{{width:100%;border-collapse:collapse}}td,th{{padding:12px;border-bottom:1px solid #293451;text-align:left}}code{{font-family:monospace}}@media(max-width:700px){{.grid{{grid-template-columns:1fr}}}}</style>
            <div class=hero><h1>⚡ BugForge</h1><p>Crash → Evidence → Fingerprint → Investigation</p></div>
            <div class=grid><div class=card><div class=metric>{len(reports)}</div>Reports</div><div class=card><div class=metric>{len({x.get('fingerprint') for x in reports})}</div>Unique fingerprints</div><div class=card><div class=metric>{sum(len(x.get('frames',[])) for x in reports)}</div>Stack frames</div></div>
            <div class=card><h2>Findings</h2><table><tr><th>Type</th><th>Fingerprint</th><th>Frames</th></tr>{rows}</table></div>
            <div class=card><h2>API</h2><p><code>/api/reports</code> returns the dashboard dataset as JSON.</p></div>"""
            body=body.encode(); self.send_response(200); self.send_header("Content-Type","text/html; charset=utf-8"); self.send_header("Content-Length",str(len(body))); self.end_headers(); self.wfile.write(body)
    print(f"BugForge dashboard: http://{host}:{port}")
    ThreadingHTTPServer((host,port),Handler).serve_forever()
