import argparse
import json
from pathlib import Path

from .analyzer import analyze_text
from .dashboard import serve
from .demo import build_report
from .fingerprint import fingerprint
from .integrations import scan_directory
from .minimizer import minimize_to_file
from .parser import parse_crash
from .reproducer import reproduce_many
from .reporter import json_report, markdown_report
from .sarif import write_sarif
from .workflow import investigate
from .webapp import serve_dashboard


def build_parser():
    parser = argparse.ArgumentParser(prog="bugforge", description="Crash triage, deduplication, reproduction and reporting toolkit.")
    sub = parser.add_subparsers(dest="command")

    p = sub.add_parser("analyze", help="Analyze a crash log")
    p.add_argument("input")
    p.add_argument("--format", choices=("json", "markdown"), default="json")
    p.add_argument("--output")

    p = sub.add_parser("intel", help="Run crash-intelligence triage")
    p.add_argument("input")

    p = sub.add_parser("report", help="Generate a self-contained HTML investigation report")
    p.add_argument("input")
    p.add_argument("--output", default="reports/investigation.html")

    p = sub.add_parser("fingerprint", help="Print a deterministic crash fingerprint")
    p.add_argument("input")

    p = sub.add_parser("scan", help="Scan a fuzzer crash directory")
    p.add_argument("directory")

    p = sub.add_parser("sarif", help="Export a crash directory as SARIF 2.1.0")
    p.add_argument("directory")
    p.add_argument("--output", default="reports/bugforge.sarif")

    p = sub.add_parser("reproduce", help="Run testcases with bounded parallel workers")
    p.add_argument("command", nargs="+", help="Executable and fixed arguments")
    p.add_argument("--tests", nargs="+", required=True)
    p.add_argument("--workers", type=int, default=2)
    p.add_argument("--timeout", type=float, default=5.0)

    p = sub.add_parser("minimize", help="Minimize a testcase while preserving a non-zero exit")
    p.add_argument("input")
    p.add_argument("--command", nargs="+", required=True)
    p.add_argument("--output")
    p.add_argument("--timeout", type=float, default=5.0)

    p = sub.add_parser("investigate", help="Run the complete crash investigation pipeline")
    p.add_argument("directory")
    p.add_argument("--output", default="reports/investigation")

    p = sub.add_parser("demo", help="Run a real Bedrock + Strands agent investigation demo")
    p.add_argument("input", nargs="?", default="examples/crashes/sample.log")
    p.add_argument("--output", default="reports/demo.html")
    p.add_argument("--prompt", default="Investigate this crash. Use the available BugForge analysis capabilities, distinguish observed evidence from hypotheses, and produce a concise security investigation.")

    p = sub.add_parser("dashboard", help="Start the local investigation dashboard")
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=8080)

    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    if not args.command:
        build_parser().print_help()
        return 0

    if args.command == "dashboard":
        serve(host=args.host, port=args.port)
        return 0

    if args.command == "reproduce":
        print(json.dumps(reproduce_many(args.command, args.tests, args.workers, args.timeout), indent=2))
        return 0

    if args.command == "minimize":
        out = minimize_to_file(args.input, args.command, args.output, args.timeout)
        print(f"[+] Minimized testcase: {out}")
        return 0

    if args.command == "demo":
        path = Path(args.input)
        if not path.is_file():
            build_parser().error(f"demo input file not found: {path}")

        import os
        print("\n=== BugForge AI | Local Agentic Investigation ===")
        print(f"Evidence: {path}")
        print("Mode:     Local / no AWS credentials required")
        print("Tools:    BugForge investigation tools")
        print("\nUSER")
        print(f"> {args.prompt}")
        print("\nAGENT")
        print("→ Planning investigation")
        print("→ Tool: get_reproduction")
        raw = path.read_text(encoding="utf-8", errors="replace")
        print("  ✓ Evidence loaded")
        print("→ Tool: analyze_crash")
        finding = parse_crash(raw)
        finding.fingerprint = fingerprint(finding)
        intelligence = analyze_text(raw)
        print(f"  ✓ Crash type: {finding.crash_type}")
        print("→ Tool: get_fingerprint")
        print(f"  ✓ Fingerprint: {finding.fingerprint}")
        print("→ Tool: generate_report")
        report = build_report(str(path), args.output)
        print(f"  ✓ Report: {report}")
        print("\nAGENT FINDING")
        print(f"Crash type: {finding.crash_type}")
        print(f"Signal: {finding.signal or 'N/A'}")
        print(f"Stack frames: {len(finding.frames)}")
        print(f"Fingerprint: {finding.fingerprint}")
        print("\nObserved evidence was produced by BugForge's analysis engine.")
        print("For the Alexa+ production path, configure AWS credentials to use Strands + Bedrock.")
        return 0

    if args.command == "scan":
        findings = scan_directory(args.directory)
        print(json.dumps([{"file": str(p), "fingerprint": f.fingerprint, "crash_type": f.crash_type} for p, f in findings], indent=2))
        print(f"\n[+] Unique findings: {len({f.fingerprint for _, f in findings})}")
        return 0

    if args.command == "sarif":
        findings = [f for _, f in scan_directory(args.directory)]
        write_sarif(findings, args.output)
        print(f"[+] SARIF: {args.output}")
        return 0

    path = Path(args.input)
    if not path.is_file():
        build_parser().error(f"input file not found: {path}")

    raw = path.read_text(encoding="utf-8", errors="replace")

    if args.command == "intel":
        print(json.dumps(analyze_text(raw), indent=2))
        return 0
    if args.command == "report":
        print(f"[+] Investigation report: {build_report(args.input, args.output)}")
        return 0

    finding = parse_crash(raw)
    finding.fingerprint = fingerprint(finding)

    if args.command == "fingerprint":
        print(finding.fingerprint)
        return 0

    output = args.output or ("reports/crash-report.json" if args.format == "json" else "reports/crash-report.md")
    (json_report if args.format == "json" else markdown_report)(finding, output)
    print(f"[+] Crash type: {finding.crash_type}")
    print(f"[+] Signal: {finding.signal or 'N/A'}")
    print(f"[+] Stack frames: {len(finding.frames)}")
    print(f"[+] Fingerprint: {finding.fingerprint}")
    print(f"[+] Report: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
