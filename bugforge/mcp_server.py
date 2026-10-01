"""BugForge MCP server for Alexa+ integrations using Streamable HTTP."""
from __future__ import annotations

import argparse
from dataclasses import asdict
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP

from .analyzer import analyze_text
from .fingerprint import fingerprint
from .parser import parse_crash

mcp = FastMCP("BugForge", stateless_http=True, json_response=True)


def _read(path: str) -> str:
    p = Path(path).expanduser().resolve()
    if not p.is_file():
        raise FileNotFoundError(f"File not found: {p}")
    return p.read_text(encoding="utf-8", errors="replace")


@mcp.tool()
def list_reproductions(directory: str = "examples/crashes") -> dict[str, Any]:
    """List reproduction/crash artifacts."""
    root = Path(directory).expanduser().resolve()
    if not root.exists():
        return {"directory": str(root), "count": 0, "files": []}
    files = [str(p) for p in sorted(root.rglob("*")) if p.is_file()]
    return {"directory": str(root), "count": len(files), "files": files[:500]}


@mcp.tool()
def get_reproduction(path: str) -> dict[str, Any]:
    """Read a reproduction or crash artifact."""
    content = _read(path)
    return {"path": str(Path(path).resolve()), "bytes": len(content.encode()), "content": content[:200000]}


@mcp.tool()
def analyze_crash(path: str) -> dict[str, Any]:
    """Parse and analyze a crash artifact using BugForge's real engine."""
    raw = _read(path)
    finding = parse_crash(raw)
    finding.fingerprint = fingerprint(finding)
    return {"path": str(Path(path).resolve()), "finding": asdict(finding), "intelligence": analyze_text(raw)}


@mcp.tool()
def parse_stacktrace(path: str) -> dict[str, Any]:
    """Extract structured crash information."""
    finding = parse_crash(_read(path))
    finding.fingerprint = fingerprint(finding)
    return asdict(finding)


@mcp.tool()
def inspect_source(path: str, start_line: int = 1, end_line: int = 250) -> dict[str, Any]:
    """Inspect a bounded source range."""
    p = Path(path).expanduser().resolve()
    lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
    start, end = max(1, start_line), min(len(lines), max(start_line, end_line))
    return {"path": str(p), "start_line": start, "end_line": end,
            "content": "\n".join(f"{i}: {lines[i - 1]}" for i in range(start, end + 1))}


@mcp.tool()
def get_fingerprint(path: str) -> dict[str, Any]:
    """Generate BugForge's deterministic crash fingerprint."""
    finding = parse_crash(_read(path))
    return {"path": str(Path(path).resolve()), "fingerprint": fingerprint(finding)}


@mcp.tool()
def generate_report(path: str) -> dict[str, Any]:
    """Generate a structured report from BugForge's existing analysis."""
    raw = _read(path)
    finding = parse_crash(raw)
    finding.fingerprint = fingerprint(finding)
    return {"path": str(Path(path).resolve()), "report": asdict(finding), "intelligence": analyze_text(raw)}


@mcp.tool()
def get_project_status(directory: str = ".") -> dict[str, Any]:
    """Return project and reproduction inventory."""
    root = Path(directory).expanduser().resolve()
    artifacts = [p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in {".log", ".txt", ".js", ".wat", ".wasm"}] if root.exists() else []
    return {"project": "BugForge", "root": str(root), "exists": root.exists(), "reproduction_files": len(artifacts)}


def main() -> None:
    parser = argparse.ArgumentParser(description="BugForge Alexa+ MCP server")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    mcp.settings.host = args.host
    mcp.settings.port = args.port
    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()
