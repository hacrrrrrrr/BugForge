import re
from .models import CrashFinding

SIGNAL_RE = re.compile(r"\b(SIG[A-Z0-9]+)\b")
FATAL_RE = re.compile(r"(?:fatal error|FATAL|DCHECK failed|assert(?:ion)? failed)", re.I)

def parse_crash(text: str) -> CrashFinding:
    signal_match = SIGNAL_RE.search(text)
    signal = signal_match.group(1) if signal_match else None
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    frames = [line for line in lines if re.match(r"^(?:#\d+\s+.*|\s*at\s+.+)", line)][:100]
    if signal:
        crash_type = signal
    elif FATAL_RE.search(text):
        crash_type = "FATAL"
    else:
        crash_type = "UNKNOWN"
    message = next((line for line in lines if "fatal" in line.lower() or "error" in line.lower()), None)
    return CrashFinding(crash_type, signal, message, frames)
