"""Crash clustering based on deterministic fingerprints and stack overlap."""
from collections import defaultdict
from .fingerprint import fingerprint
from .parser import parse_crash
from .analyzer import similarity

def cluster_texts(texts):
    findings=[]
    for text in texts:
        f=parse_crash(text); f.fingerprint=fingerprint(f); f.intel=similarity
        findings.append(f)
    groups=defaultdict(list)
    for f in findings: groups[f.fingerprint].append(f)
    return dict(groups)
