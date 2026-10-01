"""BugForge MCP server for Alexa+ integrations.

Uses the MCP Python SDK's Streamable HTTP transport.
Run: python -m bugforge.mcp_server --host 0.0.0.0 --port 8000
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP

from .analyzer import analyze_text
from .fingerprint import fingerprint_text
from .parser import parse_crash
from .reporter import report_finding

mcp = FastMCP("BugForge", stateless_http=True, json_response=True)


def _read(path: str) -> str:
    p = Path(path).expanduser().resolve()
    if not p.is_file():
        raise FileNotFoundError(f"File not found: {p}")
    return p.read_text(encoding="utf-8", errors="replace")


@mcp.tool()
def list_reproductions(directory: str = "examples/crashes") -> dict[str, Any]:
    """List crash/reproduction files available to BugForge."""
    root = Path(directory).expanduser().resolve()
    if not root.exists():
        return {"directory": str(root), "files": []}
    files = [str(p) for p in sorted(root.rglob("*")) if p.is_file()]
    return {"directory": str(root), "count": len(files), "files": files[:500]}


@mcp.tool()
def get_reproduction(path: str) -> dict[str, Any]:
    """Read a reproduction or crash artifact."""
    text = _read(path)
    return {"path": str(Path(path).resolve()), "bytes": len(text.encode()), "content": text[:200000]}


@mcp.tool()
def analyze_crash(path: str) -> dict[str, Any]:
    """Parse and analyze a crash artifact with BugForge's real analysis engine."""
    text = _read(path)
    parsed = parse_crash(text)
    analysis = analyze_text(text)
    return {"path": str(Path(path).resolve()), "parsed": parsed, "analysis": analysis}


@mcp.tool()
def parse_stacktrace(path: str) -> dict[str, Any]:
    """Extract structured crash information from a stack trace."""
    return parse_crash(_read(path))


@mcp.tool()
def inspect_source(path: str, start_line: int = 1, end_line: int = 250) -> dict[str, Any]:
    """Inspect a bounded source range for agent-assisted investigation."""
    p = Path(path).expanduser().resolve()
    lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
    start = max(1, start_line)
    end = min(len(lines), max(start, end_line))
    return {"path": str(p), "start_line": start, "end_line": end, "content": "\n".join(f"{i}: {lines[i-1]}" for i in range(start, end + 1))}


@mcp.tool()
def fingerprint(path: str) -> dict[str, Any]:
    """Generate BugForge's deterministic fingerprint for a crash artifact."""
    return {"path": str(Path(path).resolve()), "fingerprint": fingerprint_text(_read(path))}


@mcp.tool()
def generate_report(path: str) -> dict[str, Any]:
    """Generate BugForge's structured investigation report."""
    text = _read(path)
    finding = analyze_text(text)
    return {"path": str(Path(path).resolve()), "report": report_finding(finding)}


@mcp.tool()
def get_project_status(directory: str = ".") -> dict[str, Any]:
    """Return useful project/reproduction inventory for an agent."""
    root = Path(directory).expanduser().resolve()
    return {
        "project": "BugForge",
        "root": str(root),
        "exists": root.exists(),
        "reproduction_files": len([p for p in root.rglob("*") if p.is_file() and p.suffix in {".log", ".txt", ".js", ".wat", ".wasm"}]) if root.exists() else 0,
    }


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
