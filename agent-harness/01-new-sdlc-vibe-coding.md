# The New Software Lifecycle: Vibe Coding vs. Agentic Engineering
**Source:** https://addyosmani.com/blog/new-sdlc-vibe-coding/
**Topic:** How AI restructures the SDLC — and why harness engineering, not the model, is the real leverage point

## Key Concepts
- **Agent = Model (~10%) + Harness (~90%)** — the harness includes instructions, tools, sandboxes, orchestration, hooks, and observability; most agent failures are harness failures
- **Context engineering** is the primary optimization surface; context categories: Instructions, Knowledge, Memory, Examples, Tools, Guardrails
- **Static vs. dynamic context split** — static loads every turn (system prompts, rule files), dynamic loads on-demand (RAG, task-specific skills); treat the boundary as a versioned architectural decision
- **Progressive disclosure** — agents see minimal metadata at startup, load full skill instructions only when task-matched, pull heavy references only during execution
- **Verification spectrum** ranges from vibe coding (casual prompts, assume functionality) → structured AI-assisted → agentic engineering (formal specs, automated evals, CI/CD gates)
- **Three verification layers**: Tests (deterministic I/O), Output Evaluation (final result), Trajectory Evaluation (reasoning path, tool calls, intermediate steps)
- **The 80% problem** — agents handle first 80% efficiently; the final 20% (edge cases, system seams, domain-specific logic) remains stubbornly hard
- **Specification becomes the bottleneck**, not implementation; verification moves to the center of the lifecycle
- **Economics**: vibe coding = low upfront CapEx, high ongoing OpEx (token burn, maintenance tax, security cleanup); agentic engineering = higher upfront, lower marginal cost per feature; vibe coding costs 3-10x more per feature past breakeven
- **Conductor mode** (real-time, IDE-integrated, keystroke-level) vs. **Orchestrator mode** (async, goal-based delegation, human review) — switch within a session based on task clarity
- AI amplifies existing engineering culture — both its strengths and its weaknesses

## Actionable Takeaways
- **Invest in the harness first** — before tuning the model, audit instructions, tools, sandboxes, and hooks; that's where most gains are
- **Create rule files** (AGENTS.md, CLAUDE.md, or equivalent) versioned in source control as static guardrails — treat them like code, review them like code
- **Implement progressive disclosure for agent skills** — metadata only at startup, full instructions on match, heavy docs fetched on execution; keeps token cost low across a large skill library
- **Build eval suites, not just demos** — demos prove single-instance function; rubric-based eval suites prove reliable operation; set the bar at benchmark scores
- **Flip the testing model** — tests and evals become the primary specification mechanism, written before or alongside generation, not after
- **Route by cost** — large models for complex reasoning, small/cheap models for test gen, code review, CI checks; model routing is a direct financial lever
- **Default to Orchestrator mode for well-specified work** — migrations, test generation, and refactors are well-suited; use Conductor mode for exploration and unfamiliar code
- **Specify trajectory evaluation** — don't just check final output; evaluate whether the agent's reasoning path and tool calls were correct
- **Treat the static/dynamic context boundary as an architecture decision** — document it, version it, PR-review changes to it
- **Maintenance is underrated** — tedious migrations (dependency upgrades, API version bumps) are now feasible with agents; prioritize these as early wins for team rollout

## Patterns / Frameworks Mentioned
- **Harness Engineering** — the discipline of building the non-model components of an agent system
- **Factory Model** — production-scale agent deployment pattern
- **Agentic Code Review** — using agents in the review loop
- **Progressive Disclosure Pattern** — layered context loading (metadata → instructions → references)
- **Conductor / Orchestrator Mode** — dual interaction paradigm within the same tooling session
- **Evaluation-Driven Development** — benchmark → failure clustering → prompt/tool refinement → regression suite → prod monitoring loop
- **MCP (Model Context Protocol)** — standard for tool integration across agents
- **A2A (Agent-to-Agent)** — standard for agent-to-agent work handoff and coordination
- **AGENTS.md / CLAUDE.md / GEMINI.md** — tool-specific static rule file conventions
- **Terminal Bench 2.0** — coding agent benchmark referenced for harness impact evidence
- **Google Agents CLI** — collapses prototype-to-production gap (setup → build → eval → deploy in one session)
- **Agent Engine** — Google Cloud managed runtime for deployed agents
- **Beyond Vibe Coding** (O'Reilly) — book referenced as extended resource

## Relevance
- The harness-first framing gives a concrete rollout path: start with rule files and context structure, build eval suites, then layer in orchestration — no specific vendor lock-in required since the patterns (MCP, A2A, rule files) are tool-agnostic
- The CapEx/OpEx model and "specification as bottleneck" argument are directly usable in team conversations to justify investment in agentic engineering infrastructure over ad-hoc AI use
