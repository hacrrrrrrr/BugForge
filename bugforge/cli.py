import argparse
from pathlib import Path

from .fingerprint import fingerprint
from .parser import parse_crash
from .reporter import json_report, markdown_report
from .dashboard import serve


def build_parser():
    parser = argparse.ArgumentParser(
        prog="bugforge",
        description="Turn crash logs into structured bug reports.",
    )
    sub = parser.add_subparsers(dest="command")

    analyze = sub.add_parser("analyze", help="Analyze a crash log")
    analyze.add_argument("input")
    analyze.add_argument("--format", choices=("json", "markdown"), default="json")
    analyze.add_argument("--output")

    dash = sub.add_parser("dashboard", help="Start the local web dashboard")
    dash.add_argument("--host", default="127.0.0.1")
    dash.add_argument("--port", type=int, default=8080)

    fp = sub.add_parser("fingerprint", help="Print the crash fingerprint")
    fp.add_argument("input")
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        return 0

    if args.command == "dashboard":
        serve(host=args.host, port=args.port)
        return 0

    path = Path(args.input)
    if not path.is_file():
        parser.error(f"input file not found: {path}")

    finding = parse_crash(path.read_text(encoding="utf-8", errors="replace"))
    finding.fingerprint = fingerprint(finding)

    if args.command == "fingerprint":
        print(finding.fingerprint)
        return 0

    output = args.output or (
        "reports/crash-report.json"
        if args.format == "json"
        else "reports/crash-report.md"
    )

    if args.format == "json":
        json_report(finding, output)
    else:
        markdown_report(finding, output)

    print(f"[+] Crash type: {finding.crash_type}")
    print(f"[+] Signal: {finding.signal or 'N/A'}")
    print(f"[+] Stack frames: {len(finding.frames)}")
    print(f"[+] Fingerprint: {finding.fingerprint}")
    print(f"[+] Report: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
