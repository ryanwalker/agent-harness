"""Per-subagent permission enforcement.

Agent definitions in .claude/agents/*.md declare which *tools* an agent may
use (Read, Write, Bash, ...), but they can't restrict *which paths* a tool
touches. That's enforced here, in the can_use_tool callback passed to
ClaudeAgentOptions, keyed on ToolPermissionContext.agent_id.
"""

from __future__ import annotations

import logging

from claude_agent_sdk import (
    PermissionResultAllow,
    PermissionResultDeny,
    ToolPermissionContext,
)

logger = logging.getLogger(__name__)

# Agents listed here may not touch this path prefix via any tool.
DENIED_DIRS: dict[str, str] = {
    "implementer": "tests/",
}

# Tools whose input carries a single file/dir path to check.
_PATH_INPUT_KEYS = ("file_path", "path")


def _denied_dir_for(agent_id: str | None) -> str | None:
    if agent_id is None:
        return None
    return DENIED_DIRS.get(agent_id)


def _path_from_tool_input(tool_input: dict) -> str | None:
    for key in _PATH_INPUT_KEYS:
        value = tool_input.get(key)
        if isinstance(value, str):
            return value
    return None


async def enforce_directory_restrictions(
    tool_name: str,
    tool_input: dict,
    context: ToolPermissionContext,
) -> PermissionResultAllow | PermissionResultDeny:
    denied_dir = _denied_dir_for(context.agent_id)
    if denied_dir is None:
        return PermissionResultAllow()

    if tool_name == "Bash":
        command = tool_input.get("command", "")
        if denied_dir.rstrip("/") in command:
            reason = f"{context.agent_id} may not reference {denied_dir} in Bash commands"
            logger.warning("DENIED: %s (command=%r)", reason, command)
            return PermissionResultDeny(message=reason)
        return PermissionResultAllow()

    path = _path_from_tool_input(tool_input)
    if path is not None and (path.startswith(denied_dir) or f"/{denied_dir}" in path):
        reason = f"{context.agent_id} is not permitted to access {denied_dir}"
        logger.warning("DENIED: %s (tool=%s, path=%r)", reason, tool_name, path)
        return PermissionResultDeny(message=reason)

    return PermissionResultAllow()
