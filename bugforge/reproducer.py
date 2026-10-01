"""Bounded reproduction workers."""
from concurrent.futures import ThreadPoolExecutor, as_completed
import subprocess

def reproduce(command, testcase, timeout=5.0):
    try:
        p=subprocess.run(command+[testcase],capture_output=True,text=True,timeout=timeout)
        return {"reproduced":p.returncode != 0,"returncode":p.returncode,"timed_out":False,"stdout":p.stdout[-4000:],"stderr":p.stderr[-4000:]}
    except subprocess.TimeoutExpired as e:
        return {"reproduced":False,"returncode":None,"timed_out":True,"stdout":str(e.stdout or "")[-4000:],"stderr":str(e.stderr or "")[-4000:]}

def reproduce_many(command,testcases,workers=2,timeout=5.0):
    workers=max(1,min(int(workers),16))
    with ThreadPoolExecutor(max_workers=workers) as pool:
        jobs={pool.submit(reproduce,command,t,timeout):t for t in testcases}
        return {t:j.result() for j,t in ((j,jobs[j]) for j in as_completed(jobs))}
