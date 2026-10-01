# Alexa+ Integration

BugForge's primary hackathon track is Alexa+.

## MCP server

BugForge exposes its investigation capabilities through a self-hosted MCP server using the MCP SDK's Streamable HTTP transport.

Start locally:

    python -m pip install -e '.[mcp]'
    python -m bugforge.mcp_server --host 0.0.0.0 --port 8000

The Streamable HTTP endpoint is:

    http://127.0.0.1:8000/mcp

Available tools include:

- `list_reproductions`
- `get_reproduction`
- `analyze_crash`
- `parse_stacktrace`
- `inspect_source`
- `fingerprint`
- `generate_report`
- `get_project_status`

## Agent flow

Alexa+ or a compatible MCP client can ask for an investigation. The agent calls the appropriate BugForge tools and uses their returned evidence to construct the response.

Example request:

> Analyze the latest reproduction and explain what evidence supports the finding.

BugForge retrieves the reproduction, parses the stack, runs its existing analysis pipeline, and returns structured evidence.

## Security

The MCP endpoint is intentionally self-hosted. Put it behind HTTPS and an authentication/reverse-proxy layer before exposing it to the public internet. Do not expose arbitrary filesystem access to untrusted users.
