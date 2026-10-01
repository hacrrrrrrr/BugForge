# Integrations

BugForge can consume crash/testcase directories produced by fuzzers through the Python API:

    from bugforge.integrations import scan_directory
    findings = scan_directory("crashes")

Each finding receives the same deterministic fingerprint used by the CLI.

The integration layer is intentionally adapter-friendly so engines such as libFuzzer, AFL++, Fuzzilli, and custom fuzzers can be connected without coupling the analysis core to one fuzzer.
