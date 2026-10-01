"""One-command end-to-end BugForge investigation workflow."""
from pathlib import Path
from .integrations import scan_directory
from .analyzer import analyze_text
from .reproducer import reproduce_many
from .sarif import write_sarif
from .reporter import json_report

def investigate(directory, output="reports/investigation"):
    root=Path(directory)
    out=Path(output); out.mkdir(parents=True,exist_ok=True)
    findings=scan_directory(str(root))
    rows=[]
    for path,finding in findings:
        raw=path.read_text(encoding="utf-8",errors="replace")
        intel=analyze_text(raw)
        rows.append({
            "file":str(path),
            "crash_type":finding.crash_type,
            "fingerprint":finding.fingerprint,
            "intelligence":intel,
        })
    (out/"summary.json").write_text(__import__("json").dumps(rows,indent=2),encoding="utf-8")
    write_sarif([f for _,f in findings],str(out/"findings.sarif"))
    return rows
