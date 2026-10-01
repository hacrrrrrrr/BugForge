from bugforge.cache import ResultCache
from bugforge.parser import parse_crash
from bugforge.fingerprint import fingerprint
from bugforge.sarif import to_sarif

def test_cache_and_sarif(tmp_path):
    f=parse_crash("Signal: SIGSEGV\n#0 foo()")
    f.fingerprint=fingerprint(f)
    c=ResultCache(tmp_path/"cache.db"); c.put(f.fingerprint,{"crash_type":f.crash_type})
    assert c.get(f.fingerprint)["crash_type"]=="SIGSEGV"
    assert to_sarif([f])["version"]=="2.1.0"
    c.close()
