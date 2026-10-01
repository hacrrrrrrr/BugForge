"""SARIF 2.1.0 export."""
import json
from dataclasses import asdict

def to_sarif(findings):
    results=[]
    for f in findings:
        results.append({"ruleId":f.fingerprint or f.crash_type,"level":"error","message":{"text":f.message or f.crash_type},"locations":[]})
    return {"version":"2.1.0","$schema":"https://json.schemastore.org/sarif-2.1.0.json","runs":[{"tool":{"driver":{"name":"BugForge","version":"0.1.0"}},"results":results}]}

def write_sarif(findings,path):
    with open(path,"w",encoding="utf-8") as h: json.dump(to_sarif(findings),h,indent=2)
