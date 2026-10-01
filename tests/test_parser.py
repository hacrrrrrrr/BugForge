from bugforge.parser import parse_crash
from bugforge.fingerprint import fingerprint

def test_parse_and_fingerprint():
    finding = parse_crash("Fatal error: DCHECK failed\nSignal: SIGABRT\n#0 foo()\n#1 bar()")
    finding.fingerprint = fingerprint(finding)
    assert finding.crash_type == "SIGABRT"
    assert finding.signal == "SIGABRT"
    assert finding.frames
    assert len(finding.fingerprint) == 16
