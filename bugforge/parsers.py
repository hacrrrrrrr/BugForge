"""Runtime-aware crash parsers."""
import re
from .parser import parse_crash

def parse_asan(text):
    f=parse_crash(text)
    m=re.search(r"(heap-buffer-overflow|stack-buffer-overflow|use-after-free|global-buffer-overflow|double-free)", text, re.I)
    f.message=m.group(1) if m else f.message
    return f

def parse_ubsan(text):
    f=parse_crash(text)
    m=re.search(r"runtime error:\s*(.+)", text, re.I)
    if m: f.message=m.group(1).strip()
    return f

def parse_v8(text):
    f=parse_crash(text)
    m=re.search(r"(?:Fatal error|Debug check failed|DCHECK failed):?\s*(.+)", text, re.I)
    if m: f.message=m.group(0).strip()
    return f

RUNTIMES={"generic":parse_crash,"asan":parse_asan,"ubsan":parse_ubsan,"v8":parse_v8}

def parse_runtime(text,runtime="generic"):
    try: return RUNTIMES[runtime](text)
    except KeyError: raise ValueError(f"unsupported runtime: {runtime}; choose from {', '.join(RUNTIMES)}")
