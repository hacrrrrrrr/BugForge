from bugforge.workflow import investigate

def test_workflow(tmp_path):
    crashes=tmp_path/"crashes"; crashes.mkdir()
    (crashes/"one.log").write_text("AddressSanitizer: heap-buffer-overflow\nSignal: SIGSEGV\n#0 foo()")
    rows=investigate(str(crashes),str(tmp_path/"out"))
    assert len(rows)==1
    assert (tmp_path/"out"/"summary.json").exists()
    assert (tmp_path/"out"/"findings.sarif").exists()
