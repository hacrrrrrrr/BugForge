"""Fuzzer integration helpers."""
from pathlib import Path
from .parser import parse_crash
from .fingerprint import fingerprint

def scan_directory(path):
    findings=[]
    for p in Path(path).rglob("*"):
        if p.is_file():
            try:
                text=p.read_text(encoding="utf-8",errors="replace")
                f=parse_crash(text)
                if f.crash_type != "UNKNOWN":
                    f.fingerprint=fingerprint(f); findings.append((p,f))
            except OSError:
                pass
    return findings
