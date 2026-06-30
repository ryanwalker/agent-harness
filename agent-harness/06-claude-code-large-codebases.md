# How Claude Code Works in Large Codebases: Best Practices and Where to Start
**Source:** https://claude.com/blog/how-claude-code-works-in-large-codebases-best-practices-and-where-to-start
**Topic:** Enterprise patterns for deploying Claude Code across large, complex codebases (monorepos, legacy systems, distributed architectures)

## Key Concepts
- Claude Code navigates codebases like a developer — traverses file systems, uses grep, reads files live; no RAG/embeddings, no stale index
- Performance is shaped more by the "harness" (surrounding infrastructure) than the model itself
- Seven harness components: CLAUDE.md files, hooks, skills, plugins, LSP integrations, MCP servers, subagents
- CLAUDE.md files are auto-loaded every session; skills are on-demand; plugins bundle setups for org-wide distribution
- LSP integrations enable symbol-level navigation (not string matching) — requires explicit configuration, not automatic
- Subagents run in isolation — useful for separating exploration from editing
- Instructions in CLAUDE.md written for older models can constrain newer ones — treat config as living documentation
- Non-git version control (Perforce, etc.) and massive directory structures require custom configuration

## Actionable Takeaways
- Keep CLAUDE.md lean and layered: root file for big-picture context, subdirectory files for local conventions
- Initialize Claude in the relevant subdirectory, not the repo root — it walks up the tree automatically
- Scope test/lint commands per subdirectory to avoid full-suite timeouts
- Exclude generated files, build artifacts, and third-party code via `.gitignore` and `.claude/settings.json`
- Build a codebase map (markdown directory index) when folder structure is opaque
- Deploy LSP servers explicitly for any typed language — do not assume it works out of the box
- Put reusable task expertise into skills, not CLAUDE.md — CLAUDE.md is for conventions, not procedures
- Assign a DRI or small team to own Claude Code config before broad rollout
- Establish governance (approved skills, code review requirements, limited initial access) before expanding
- Distribute working setups as plugins to prevent tribal knowledge and fragmentation
- Review and prune CLAUDE.md every 3–6 months as model capabilities improve — remove compensatory workarounds

## Patterns / Frameworks Mentioned
- CLAUDE.md hierarchy (layered config files by directory)
- Skills (on-demand, reusable expertise files)
- Plugins (bundled capability distributions for orgs)
- Hooks (event-triggered scripts for automation and capturing learnings)
- MCP servers (Model Context Protocol — connections to internal tools/APIs)
- Subagents (isolated Claude instances for parallel or scoped work)
- LSP (Language Server Protocol) integration
- DRI pattern (designated responsible individual for config ownership)
- "Agent manager" role (hybrid PM/engineer managing Claude Code ecosystem)
- Managed plugin marketplace (org-wide consistent distribution)
- Cross-functional working group (engineering + security + governance) for regulated industries

## Relevance
- Rolling out Claude Code at a team or job level maps directly to this article — the DRI model, governance-first approach, and plugin distribution patterns are the practical playbook for adoption without chaos
- The harness-over-model framing is transferable: whatever agentic tooling your team uses, the infrastructure (context files, approved skills, review processes) determines outcomes more than model selection alone
