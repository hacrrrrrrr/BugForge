# AWS Builder Integration

BugForge can use Amazon Bedrock through the Strands Agents SDK while keeping BugForge's deterministic analysis engine as the evidence source.

## Setup

Install:

    python -m pip install -e '.[aws]'

Configure AWS credentials using an AWS-supported role, profile, or environment configuration.

Optional model:

    export BUGFORGE_BEDROCK_MODEL=amazon.nova-lite-v1:0

Then create an agent from:

    from bugforge.agent import build_agent
    agent = build_agent()

The agent is designed to reason over BugForge evidence rather than fabricate technical findings.
