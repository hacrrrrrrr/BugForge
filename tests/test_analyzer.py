from bugforge.analyzer import analyze_text

def test_security_intelligence():
    x=analyze_text("AddressSanitizer: heap-buffer-overflow\nSignal: SIGSEGV\n#0 foo()")
    assert "memory-safety" in x["categories"]
    assert x["has_sanitizer"]
    assert x["signal"]=="SIGSEGV"
