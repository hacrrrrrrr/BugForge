"""Self-contained visual investigation dashboard."""
import json
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path

def serve_dashboard(data_dir="reports/investigation",host="127.0.0.1",port=8080):
    root=Path(data_dir)
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path=="/api":
                body=(root/"summary.json").read_bytes() if (root/"summary.json").exists() else b"[]"
                self.send_response(200); self.send_header("Content-Type","application/json"); self.send_header("Content-Length",str(len(body))); self.end_headers(); self.wfile.write(body); return
            items=[]
            try: items=json.loads((root/"summary.json").read_text())
            except Exception: pass
            cats={}
            for x in items:
                for c in x["intelligence"].get("categories",[]): cats[c]=cats.get(c,0)+1
            cards="".join(f"<div class='card'><b>{k}</b><strong>{v}</strong></div>" for k,v in cats.items()) or "<div class='card'><b>No findings</b><strong>0</strong></div>"
            rows="".join(f"<tr><td>{x['crash_type']}</td><td><code>{x['fingerprint']}</code></td><td>{', '.join(x['intelligence'].get('categories',[]))}</td><td>{x['intelligence'].get('triage','')}</td></tr>" for x in items)
            html=f"""<!doctype html><meta name=viewport content='width=device-width,initial-scale=1'><title>BugForge Investigation</title><style>
body{{margin:0;font-family:system-ui;background:#090d16;color:#edf2ff}}main{{max-width:1150px;margin:auto;padding:30px}}header{{padding:28px 0}}h1{{font-size:42px;margin:0}}.sub{{color:#9aa7bd}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:14px}}.card{{background:#121a29;border:1px solid #26344b;border-radius:16px;padding:18px}}.card strong{{display:block;font-size:30px;margin-top:8px}}section{{background:#121a29;border:1px solid #26344b;border-radius:16px;margin-top:18px;padding:20px;overflow:auto}}table{{width:100%;border-collapse:collapse}}th,td{{padding:13px;text-align:left;border-bottom:1px solid #26344b}}code{{font-size:12px}}.pill{{display:inline-block;padding:5px 9px;border-radius:999px;background:#1c2940}}</style>
<main><header><h1>⚡ BugForge</h1><p class=sub>Crash → Intelligence → Fingerprint → Investigation</p></header>
<div class=grid>{cards}<div class=card><b>Total findings</b><strong>{len(items)}</strong></div><div class=card><b>Unique fingerprints</b><strong>{len({x['fingerprint'] for x in items})}</strong></div></div>
<section><h2>Investigation findings</h2><table><tr><th>Crash</th><th>Fingerprint</th><th>Evidence</th><th>Triage</th></tr>{rows}</table></section>
<section><h2>Artifacts</h2><p class=pill>summary.json</p> <p class=pill>findings.sarif</p></section></main>"""
            body=html.encode(); self.send_response(200); self.send_header("Content-Type","text/html; charset=utf-8"); self.send_header("Content-Length",str(len(body))); self.end_headers(); self.wfile.write(body)
    print(f"BugForge investigation dashboard: http://{host}:{port}")
    ThreadingHTTPServer((host,port),Handler).serve_forever()
