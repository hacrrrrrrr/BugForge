"""SQLite-backed persistent cache for crash analysis results."""
import json, sqlite3, time
from pathlib import Path

class ResultCache:
    def __init__(self, path=".bugforge/cache.db"):
        self.path=Path(path); self.path.parent.mkdir(parents=True, exist_ok=True)
        self.db=sqlite3.connect(self.path)
        self.db.execute("CREATE TABLE IF NOT EXISTS results (fingerprint TEXT PRIMARY KEY, result TEXT NOT NULL, updated REAL NOT NULL)")
        self.db.commit()
    def get(self, fingerprint):
        row=self.db.execute("SELECT result FROM results WHERE fingerprint=?", (fingerprint,)).fetchone()
        return json.loads(row[0]) if row else None
    def put(self, fingerprint, result):
        self.db.execute("INSERT OR REPLACE INTO results VALUES (?,?,?)",(fingerprint,json.dumps(result),time.time()))
        self.db.commit()
    def close(self): self.db.close()
