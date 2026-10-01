"""Bounded subprocess workers for crash reproduction."""
from concurrent.futures import ThreadPoolExecutor, as_completed
import subprocess

def reproduce(command, testcase, timeout=5.0):
    try:
        p=subprocess.run(command+[testcase],capture_output=True,text=True,timeout=timeout)
        return {"reproduced":p.returncode != 0,"returncode":p.returncode,"stdout":p.stdout[-4000:],"stderr":p.stderr[-4000:]}
    except subprocess.TimeoutExpired as e:
        return {"reproduced":False,"timeout":True,"stdout":e.stdout or "","stderr":e.stderr or ""}

def reproduce_many(command,testcases,workers=2,timeout=5.0):
    with ThreadPoolExecutor(max_workers=workers) as pool:
        jobs={pool.submit(reproduce,command,t,timeout):t for t in testcases}
        return {t:f.result() for f,t in ((j,jobs[j]) for j in as_completed(jobs))}
