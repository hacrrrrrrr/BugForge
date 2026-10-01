"""Additional lightweight runtime parsers."""
from .parser import parse_crash

RUNTIMES={"generic":parse_crash}

def parse_runtime(text,runtime="generic"):
    if runtime not in RUNTIMES: raise ValueError(f"unsupported runtime: {runtime}")
    return RUNTIMES[runtime](text)
