#!/bin/bash
# PreToolUse hook, wired into implementer.md's own frontmatter — only runs
# while that subagent is active. Blocks any tool call that touches tests/.
set -euo pipefail

INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name')

if [ "$TOOL_NAME" = "Bash" ]; then
  TARGET=$(echo "$INPUT" | jq -r '.tool_input.command // ""')
else
  TARGET=$(echo "$INPUT" | jq -r '.tool_input.file_path // .tool_input.path // ""')
fi

if echo "$TARGET" | grep -q 'tests/'; then
  echo "implementer may not access tests/ (blocked: $TARGET)" >&2
  exit 2
fi

exit 0
