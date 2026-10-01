from dataclasses import dataclass, field
from typing import List

@dataclass
class CrashFinding:
    crash_type: str
    signal: str | None
    message: str | None
    frames: List[str] = field(default_factory=list)
    fingerprint: str | None = None
