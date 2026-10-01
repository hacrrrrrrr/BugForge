import json
from dataclasses import asdict
from pathlib import Path

def json_report(finding, path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(asdict(finding), indent=2), encoding="utf-8")

def markdown_report(finding, path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    frames = "\n".join(f"- {frame}" for frame in finding.frames)
    content = f"# BugForge Crash Report\n\n- Crash type: {finding.crash_type}\n- Signal: {finding.signal or 'N/A'}\n- Fingerprint: {finding.fingerprint or 'N/A'}\n- Message: {finding.message or 'N/A'}\n\n## Stack frames\n\n{frames or 'No frames detected.'}\n"
    Path(path).write_text(content, encoding="utf-8")
