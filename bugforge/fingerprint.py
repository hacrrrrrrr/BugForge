import hashlib
import re

def fingerprint(finding) -> str:
    normalized = []
    for frame in finding.frames[:20]:
        value = re.sub(r"0x[0-9a-fA-F]+", "0xADDR", frame)
        value = re.sub(r"\d+", "N", value)
        normalized.append(value)
    material = "\n".join([finding.crash_type, finding.signal or "", *normalized])
    return hashlib.sha256(material.encode()).hexdigest()[:16]
