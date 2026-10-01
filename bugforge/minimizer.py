"""Delta-debugging testcase minimizer."""
from pathlib import Path
import subprocess

def minimize(path, command, timeout=5.0):
    original=Path(path).read_text(encoding="utf-8",errors="replace")
    lines=original.splitlines(keepends=True)
    if len(lines)<2: return original
    kept=lines[:]
    changed=True
    while changed and len(kept)>1:
        changed=False
        for i in range(len(kept)-1,-1,-1):
            candidate=kept[:i]+kept[i+1:]
            tmp=Path(path).with_suffix(".min.tmp")
            tmp.write_text("".join(candidate),encoding="utf-8")
            try:
                r=subprocess.run(command+[str(tmp)],capture_output=True,timeout=timeout)
                reproduces=(r.returncode != 0)
            except subprocess.TimeoutExpired:
                reproduces=False
            if reproduces:
                kept=candidate; changed=True
            tmp.unlink(missing_ok=True)
    return "".join(kept)

def minimize_to_file(path, command, output=None, timeout=5.0):
    result=minimize(path,command,timeout)
    out=Path(output or path).with_name(Path(path).stem+".min"+Path(path).suffix)
    out.write_text(result,encoding="utf-8")
    return out
