"""Optional AWS Strands + Amazon Bedrock agent integration.

The agent delegates factual project operations to the BugForge MCP server.
Set AWS credentials using the standard AWS SDK environment/role configuration.
"""
from __future__ import annotations

import os


def build_agent():
    try:
        from strands import Agent
        from strands.models import BedrockModel
    except ImportError as exc:
        raise RuntimeError("Install the optional AWS agent dependencies: pip install 'bugforge[aws]'") from exc

    model_id = os.getenv("BUGFORGE_BEDROCK_MODEL", "amazon.nova-lite-v1:0")
    model = BedrockModel(model_id=model_id)
    return Agent(
        model=model,
        system_prompt=(
            "You are BugForge, a developer security investigation agent. "
            "Use available BugForge tools to inspect evidence. Never invent crash evidence. "
            "Clearly separate observed evidence from hypotheses and return concise actionable findings."
        ),
    )
