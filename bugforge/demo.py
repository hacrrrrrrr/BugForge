"""Generate a polished local demo report from a crash log."""
from pathlib import Path
from .parser import parse_crash
from .fingerprint import fingerprint
from .html_report import render

def build_report(input_path, output="reports/investigation.html"):
    raw=Path(input_path).read_text(encoding="utf-8",errors="replace")
    finding=parse_crash(raw); finding.fingerprint=fingerprint(finding)
    Path(output).parent.mkdir(parents=True,exist_ok=True)
    Path(output).write_text(render("BugForge Investigation",raw,finding),encoding="utf-8")
    return output
