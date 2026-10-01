"""Self-contained investigation report."""
import html, json
from .analyzer import analyze_text

def render(title, raw, finding):
    intel=analyze_text(raw)
    rows="".join(f"<tr><td>{html.escape(k)}</td><td>{html.escape(json.dumps(v))}</td></tr>" for k,v in intel.items())
    return f"""<!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)}</title><style>body{{font-family:system-ui;max-width:1000px;margin:40px auto;padding:0 18px;background:#0d1117;color:#e6edf3}}.card{{background:#161b22;border:1px solid #30363d;border-radius:12px;padding:20px;margin:14px 0}}table{{width:100%;border-collapse:collapse}}td{{padding:10px;border-bottom:1px solid #30363d}}code,pre{{white-space:pre-wrap}}</style></head><body><h1>BugForge Investigation</h1><div class="card"><h2>{html.escape(finding.crash_type)}</h2><p>Fingerprint: <code>{html.escape(finding.fingerprint or "N/A")}</code></p></div><div class="card"><h2>Crash Intelligence</h2><table>{rows}</table></div><div class="card"><h2>Raw Evidence</h2><pre>{html.escape(raw)}</pre></div></body></html>"""
