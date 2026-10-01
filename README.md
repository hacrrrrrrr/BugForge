# BugForge

**Turn crashes into reproducible bugs, automatically.**

BugForge is a solo-built crash analysis toolkit for developers and security researchers. It converts raw crash logs into structured findings, fingerprints similar failures, extracts stack information, and generates machine-readable reports.

## Inspiration

Crash collection is only the first step. Large fuzzing campaigns can produce thousands of failures, including duplicates and noisy logs. BugForge makes the investigation workflow repeatable:

Crash Log → Parse → Fingerprint → Deduplicate → Minimize → Reproduce → Report

## Features

- Crash-log parsing
- Signal and fatal-error detection
- Stack-trace extraction
- Deterministic crash fingerprints
- Duplicate-friendly finding IDs
- JSON and Markdown reports
- CLI-first workflow
- Extensible parser architecture
- No mandatory external service

## Quick start

Requirements: Python 3.10+

Clone the repository and run:

    git clone https://github.com/hacrrrrrrr/BugForge.git
    cd BugForge
    python -m bugforge --help
    python -m bugforge analyze examples/crashes/sample.log
    python -m bugforge fingerprint examples/crashes/sample.log

Install as a CLI during development:

    pip install -e .
    bugforge --help

## Example

Input: examples/crashes/sample.log

    [+] Crash type: SIGABRT
    [+] Signal: SIGABRT
    [+] Stack frames: 4
    [+] Fingerprint: <deterministic hash>
    [+] Report: reports/crash-report.json

## Project structure

    BugForge/
    ├── bugforge/
    │   ├── __init__.py
    │   ├── __main__.py
    │   ├── cli.py
    │   ├── models.py
    │   ├── parser.py
    │   ├── fingerprint.py
    │   └── reporter.py
    ├── examples/
    │   └── crashes/
    ├── tests/
    ├── docs/
    ├── pyproject.toml
    ├── LICENSE
    └── README.md

## Development

Run the test suite with:

    python -m pytest

The core is intentionally modular so new runtimes, crash formats, minimizers, reproduction backends, and dashboard components can be added independently.

## Roadmap

- [x] Crash parser
- [x] Signal and fatal detection
- [x] Crash fingerprinting
- [x] JSON and Markdown reporting
- [ ] Persistent result cache
- [ ] Testcase minimization engine
- [ ] Reproduction workers
- [ ] Web dashboard
- [ ] Fuzzer integrations
- [ ] SARIF export
- [ ] Additional runtime parsers

## About

BugForge is a solo hackathon project by **Kritik Bhattarai**.

Built for practical crash investigation, fuzzing workflows, and developer-friendly debugging.

**Sponsorship / inquiries:** hunterkritik@gmail.com

## License

Apache-2.0
