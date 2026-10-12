"""Shared pytest switches for course tasks. Provided by the coach; don't edit.

- Tests marked @pytest.mark.live call paid APIs. They run only with --live, for example:
  uv run --env-file ../../.env pytest --live
- Tests marked @pytest.mark.agent_sdk run the Claude Agent SDK on your Max login. They run only
  with --agent-sdk and only while ANTHROPIC_API_KEY is unset, for example:
  env -u ANTHROPIC_API_KEY uv run pytest --agent-sdk
"""

import os

import pytest


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption("--live", action="store_true", help="run tests that call paid APIs")
    parser.addoption(
        "--agent-sdk", action="store_true", help="run Claude Agent SDK tests on the Max login"
    )


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line("markers", "live: calls a paid API; needs --live and an API key")
    config.addinivalue_line("markers", "agent_sdk: runs the Claude Agent SDK; needs --agent-sdk")


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    run_live = config.getoption("--live")
    run_sdk = config.getoption("--agent-sdk")
    if run_sdk and os.environ.get("ANTHROPIC_API_KEY"):
        raise pytest.UsageError(
            "ANTHROPIC_API_KEY is set, so the Agent SDK would bill the Console key instead of "
            "your Max login. Run: env -u ANTHROPIC_API_KEY uv run pytest --agent-sdk"
        )
    for item in items:
        if "live" in item.keywords and not run_live:
            item.add_marker(pytest.mark.skip(reason="paid API test: run with --live"))
        if "agent_sdk" in item.keywords and not run_sdk:
            item.add_marker(pytest.mark.skip(reason="Agent SDK test: run with --agent-sdk"))
