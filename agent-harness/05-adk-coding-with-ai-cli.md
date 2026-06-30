# Coding with AI — ADK CLI Tutorial
**Source:** https://adk.dev/tutorials/coding-with-ai/
**Topic:** How to give your AI coding assistant (Claude Code, Cursor, Gemini CLI, etc.) live ADK documentation via MCP server or CLI scaffolding tools

## Key Concepts
- Two complementary approaches: (1) install "development skills" into your project via `google-agents-cli`, or (2) connect your coding assistant to ADK docs via an MCP server
- The ADK Docs MCP server uses `mcpdoc` + `llms.txt` — a machine-readable documentation standard, not ADK-specific
- `llms.txt` is an index with links; `llms-full.txt` is the full flat doc — both served at `adk.dev/`
- MCP servers can be wired into any MCP-compatible tool using a standard JSON config block (`command`, `args`, `transport: stdio`)
- The `uvx` runner is used throughout — no global install needed, runs tools ephemerally from PyPI
- Agents CLI (`google-agents-cli`) bundles: scaffolding, lifecycle management, evaluation methodology, deployment guidance (Cloud Run, GKE), and API reference

## Actionable Takeaways
- Add ADK docs to Claude Code with one command:
  ```
  claude mcp add adk-docs --transport stdio -- uvx --from mcpdoc mcpdoc --urls AgentDevelopmentKit:https://adk.dev/llms.txt --transport stdio
  ```
- Add ADK docs to Cursor or any MCP-compatible tool via `mcp.json` / `mcp_config.json`:
  ```json
  {
    "mcpServers": {
      "adk-docs-mcp": {
        "command": "uvx",
        "args": ["--from", "mcpdoc", "mcpdoc", "--urls", "AgentDevelopmentKit:https://adk.dev/llms.txt", "--transport", "stdio"]
      }
    }
  }
  ```
- Bootstrap a new ADK project with: `uvx google-agents-cli setup`
- Use `mcpdoc` as the generic pattern for wiring any `llms.txt`-compatible doc set into your coding assistant — not just ADK
- Point assistants at `adk.dev/llms-full.txt` directly if you want a single-file context dump instead of the indexed version

## Patterns / Frameworks Mentioned
- **ADK (Agent Development Kit)** — Google's framework for building agents
- **MCP (Model Context Protocol)** — standard for connecting tools/context to AI coding assistants
- **llms.txt / llms-full.txt** — emerging standard for machine-readable library documentation
- **mcpdoc** — PyPI package that serves any `llms.txt`-indexed site as an MCP server
- **google-agents-cli** — ADK's CLI for project scaffolding, evaluation, and deployment
- **uvx** — ephemeral Python tool runner (like `npx` for Python); no global install required
- Supported IDEs/tools: Claude Code, Cursor, Gemini CLI, Antigravity, any MCP-compatible client

## Relevance
- The `mcpdoc` + `llms.txt` pattern is framework-agnostic and reusable: any team can wire current library docs into their coding assistants without modifying the assistant itself — a low-friction way to standardize context across engineers.
- For rollout: establish a shared `mcp.json` config in your project repo so every engineer's IDE automatically has the same documentation context wired up, reducing hallucination on framework-specific APIs.
