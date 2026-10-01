# BugForge Architecture

BugForge separates ingestion, analysis, and reporting.

1. Input: read a crash log.
2. Parser: extract signal, fatal markers, messages, and frames.
3. Fingerprint: normalize unstable values and hash stable crash structure.
4. Reporter: emit JSON or Markdown.
5. Future workers: testcase minimization and reproduction.

Design goals:
- deterministic results
- no mandatory external service
- CLI-first operation
- extensible runtime parsers
- safe handling of malformed logs
