"""Example driver: runs the `implementer` subagent (defined in
.claude/agents/implementer.md) with the tests/ directory blocked.

NOTE: permission_mode="bypassPermissions" is not used here. The SDK's
documented decision order applies permission_mode before can_use_tool, so
bypassPermissions can skip the callback below entirely. acceptEdits still
routes through can_use_tool, so the directory restriction holds while still
auto-accepting file edits (no interactive approval needed for most calls).
"""

from __future__ import annotations

import asyncio
import logging
import sys

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ClaudeSDKClient,
    ResultMessage,
    TaskNotificationMessage,
    TaskStartedMessage,
    TextBlock,
    ToolResultBlock,
    ToolUseBlock,
    UserMessage,
)

from agent_harness.permissions import enforce_directory_restrictions

PROJECT_ROOT = "."
DEFAULT_PROMPT = "Use the implementer subagent to list the files under tests/."

# Subagents dispatch as background tasks (same model the interactive CLI
# uses for the Agent tool); cap how long we'll keep the session open
# waiting on them before giving up.
TASK_WAIT_TIMEOUT_S = 180


def _print_message(message: object, pending_tasks: set[str]) -> None:
    if isinstance(message, AssistantMessage):
        for block in message.content:
            if isinstance(block, TextBlock):
                print(block.text)
            elif isinstance(block, ToolUseBlock):
                print(f"-> {block.name}({block.input})")
    elif isinstance(message, UserMessage) and isinstance(message.content, list):
        for block in message.content:
            if isinstance(block, ToolResultBlock):
                marker = "x" if block.is_error else "ok"
                print(f"   [{marker}] {block.content}")
    elif isinstance(message, TaskStartedMessage):
        pending_tasks.add(message.task_id)
        print(f"... background task started: {message.task_id} ({message.description})")
    elif isinstance(message, TaskNotificationMessage):
        pending_tasks.discard(message.task_id)
        print(f"... background task {message.status}: {message.task_id} — {message.summary}")
    elif isinstance(message, ResultMessage):
        status = "error" if message.is_error else "ok"
        cost = f"${message.total_cost_usd:.4f}" if message.total_cost_usd is not None else "n/a"
        print(f"--- turn done ({status}, {message.num_turns} turns, {cost}) ---")
    else:
        # Anything not explicitly handled above — surface it instead of
        # dropping it silently.
        print(f"... {type(message).__name__}: {message!r}")


async def _drain_until_tasks_done(client: ClaudeSDKClient, pending_tasks: set[str]) -> None:
    if not pending_tasks:
        return
    print(f"--- waiting on {len(pending_tasks)} background subagent task(s) ---")
    async for message in client.receive_messages():
        _print_message(message, pending_tasks)
        if not pending_tasks:
            return


async def run(prompt: str) -> None:
    options = ClaudeAgentOptions(
        cwd=PROJECT_ROOT,
        setting_sources=["project"],  # loads .claude/agents/*.md from cwd
        permission_mode="acceptEdits",
        can_use_tool=enforce_directory_restrictions,
    )
    pending_tasks: set[str] = set()

    async with ClaudeSDKClient(options=options) as client:
        await client.query(prompt)
        async for message in client.receive_response():
            _print_message(message, pending_tasks)

        try:
            await asyncio.wait_for(
                _drain_until_tasks_done(client, pending_tasks), TASK_WAIT_TIMEOUT_S
            )
        except asyncio.TimeoutError:
            print(f"--- gave up waiting after {TASK_WAIT_TIMEOUT_S}s; still pending: {pending_tasks} ---")


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    prompt = " ".join(sys.argv[1:]) or DEFAULT_PROMPT
    asyncio.run(run(prompt))


if __name__ == "__main__":
    main()
