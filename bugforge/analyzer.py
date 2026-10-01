"""Higher-level crash intelligence for BugForge."""
import re
from collections import Counter

SECURITY_PATTERNS = {
    "memory-safety": [r"heap-buffer-overflow", r"stack-buffer-overflow", r"use-after-free", r"out-of-bounds", r"buffer-overflow"],
    "assertion": [r"DCHECK", r"assert(?:ion)? failed", r"fatal error"],
    "memory-corruption": [r"double free", r"invalid free", r"corruption", r"wild pointer"],
    "sanitizer": [r"AddressSanitizer", r"UndefinedBehaviorSanitizer", r"ASan", r"UBSan"],
}

def analyze_text(text):
    lower=text.lower()
    categories=[]
    for name,patterns in SECURITY_PATTERNS.items():
        if any(re.search(p, text, re.I) for p in patterns):
            categories.append(name)
    signal=(re.search(r"\b(SIG[A-Z0-9]+)\b",text) or [None,None])[1]
    frames=re.findall(r"^\s*#\d+\s+(.+)$",text,re.M)
    modules=[]
    for frame in frames:
        m=re.search(r"([A-Za-z_][\w.-]*)(?:!|::)([A-Za-z_][\w:<>~]*)",frame)
        if m: modules.append(m.group(1))
    return {
        "signal": signal,
        "categories": categories or ["generic-crash"],
        "stack_depth": len(frames),
        "top_frames": frames[:5],
        "modules": list(dict.fromkeys(modules)),
        "has_sanitizer": any(x.lower() in lower for x in ("asan","ubsan","sanitizer")),
        "triage": "needs-reproduction" if signal or categories else "insufficient-evidence",
    }

def similarity(a,b):
    sa=set(a.get("top_frames",[])); sb=set(b.get("top_frames",[]))
    return len(sa & sb) / max(1,len(sa | sb))
