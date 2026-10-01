# BugForge

> **Turn crashes into actionable, reproducible bug investigations.**

BugForge is a solo-built crash analysis toolkit for developers and security researchers. It combines crash parsing, security-oriented triage, deterministic deduplication, persistent caching, testcase minimization, bounded reproduction workers, fuzzer ingestion, SARIF export, runtime-aware parsing, and a local investigation dashboard.

## Core pipeline

Crash / Fuzzer Output → Parse → Security Intelligence → Fingerprint → Cache / Deduplicate → Minimize → Reproduce → Report → SARIF / Dashboard

## Features

- Crash and stack-trace parsing
- Security-oriented crash intelligence
- Deterministic crash fingerprints
- Persistent SQLite result cache
- Testcase minimization
- Parallel, timeout-bounded reproduction workers
- Fuzzer crash-directory integration
- SARIF 2.1.0 export
- Runtime-aware parsers for generic logs, ASan, UBSan, and V8
- JSON, Markdown, and self-contained HTML investigation reports
- Local web dashboard with JSON API
- CLI-first workflow
- No mandatory external service

## Quick start

Requirements: Python 3.10+

    git clone https://github.com/hacrrrrrrr/BugForge.git
    cd BugForge
    python -m bugforge --help

Analyze:

    python -m bugforge analyze examples/crashes/sample.log

Security triage:

    python -m bugforge intel examples/crashes/security-sample.log

Fingerprint:

    python -m bugforge fingerprint examples/crashes/security-sample.log

Investigation report:

    python -m bugforge report examples/crashes/security-sample.log

Scan fuzzer crashes:

    python -m bugforge scan examples/crashes

SARIF:

    python -m bugforge sarif examples/crashes --output reports/bugforge.sarif

Dashboard:

    python -m bugforge dashboard --host 127.0.0.1 --port 8080

Then open http://127.0.0.1:8080 locally.

## Testcase minimization

BugForge can repeatedly remove testcase lines while checking whether the configured command still exits non-zero:

    python -m bugforge minimize testcase.js --command ./d8 --output testcase.min.js

Use a safe local test command appropriate for your target. The minimizer does not claim a testcase is minimized unless the target continues to reproduce according to the configured predicate.

## Reproduction workers

Run multiple testcases with bounded parallel workers:

    python -m bugforge reproduce --tests crashes/a crashes/b --workers 2 --timeout 5 ./target

The command is executed as a fixed executable/argument prefix followed by each testcase.

## Fuzzer integration

The scanner recursively reads a crash directory and produces fingerprints for recognizable crash logs:

    python -m bugforge scan ./crashes

This adapter-friendly layer can consume outputs from libFuzzer, AFL++, Fuzzilli, and custom fuzzers without coupling the analysis core to one engine.

## Runtime parsers

The Python API exposes:

    from bugforge.parsers import parse_runtime

    parse_runtime(text, "asan")
    parse_runtime(text, "ubsan")
    parse_runtime(text, "v8")
    parse_runtime(text, "generic")

Runtime parsers add specialized extraction while sharing the common finding model.

## SARIF

BugForge emits SARIF 2.1.0 so findings can be consumed by compatible security/developer tooling:

    python -m bugforge sarif ./crashes --output reports/bugforge.sarif

## Project structure

    BugForge/
    ├── bugforge/
    │   ├── cli.py
    │   ├── parser.py
    │   ├── parsers.py
    │   ├── analyzer.py
    │   ├── fingerprint.py
    │   ├── cache.py
    │   ├── minimizer.py
    │   ├── reproducer.py
    │   ├── integrations.py
    │   ├── sarif.py
    │   ├── reporter.py
    │   ├── html_report.py
    │   └── dashboard.py
    ├── examples/
    ├── tests/
    ├── docs/
    └── pyproject.toml

## Development

    python -m pytest -v

## Roadmap

All original hackathon roadmap items are implemented in the current repository:

- [x] Persistent result cache
- [x] Testcase minimization engine
- [x] Reproduction workers
- [x] Web dashboard
- [x] Fuzzer integrations
- [x] SARIF export
- [x] Additional runtime parser layer
- [x] Security-oriented crash intelligence
- [x] HTML investigation reports

Future work can extend the existing interfaces with more runtime-specific parsers, richer clustering, coverage-aware minimization, persistent job queues, and remote dashboards.

## About

BugForge is a **solo hackathon project by Kritik Bhattarai**.

**Sponsorship / inquiries:** hunterkritik@gmail.com

## License

Apache-2.0
