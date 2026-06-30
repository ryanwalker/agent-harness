# Agent Harness Engineering
**Source:** https://addyosmani.com/blog/agent-harness-engineering/
**Topic:** How to design, configure, and evolve the harness layer that wraps an LLM to produce a reliable agent

## Key Concepts
- **Agent = Model + Harness** — the harness is everything except the model: prompts, tools, execution loops, state, feedback, constraints
- "A decent model with a great harness beats a great model with a bad harness"
- Agent failures are almost always configuration problems, not model problems ("It's not a model problem. It's a configuration problem.")
- Harness components: system prompts/docs, tools/infrastructure, context management, execution controls, long-horizon patterns
- **Ratchet Principle** — every agent mistake becomes a rule that prevents recurrence; failures are permanent signals, not one-offs
- System prompt rules should each trace to a specific past failure or external constraint (no orphan rules)
- Keep per-file docs under ~60 lines (HumanLayer recommendation)
- Models post-train alongside specific harnesses — harnesses create model overfitting to their tool patterns
- Industry is converging on shared harness patterns (Claude Code, Cursor, Aider, Cline look increasingly alike)
- **Harness-as-a-Service (HaaS)** — industry shifting from raw LLM APIs to harness frameworks (Claude Agent SDK, OpenAI Agents SDK, Codex SDK)

## Actionable Takeaways
- Start with a v0.1 harness immediately — don't over-engineer upfront; iterate from real failures
- Document every rule with a traceable reason; remove rules you can't explain
- Wire hooks at lifecycle points (pre-tool-call, post-file-edit, pre-commit) to enforce conventions automatically
- Gate destructive commands behind explicit approval — never let agents rm/overwrite without a permission check
- Keep tool outputs on the filesystem, not in context — offload large outputs to disk, pass paths instead
- Use compaction/summarization when context window fills; do full resets for multi-day tasks
- Separate generation from evaluation — use a dedicated evaluator agent/step, not the same agent self-reviewing
- Use progressive disclosure in skills/prompts — reveal instructions only when the relevant task is active
- Design harness features by starting from desired behavior, then deriving the scaffolding needed
- Treat every agent failure as a permanent input to harness config (add a rule, hook, or gate)
- Success should be silent; failures should be verbose — wire back-pressure signals into loops

## Patterns / Frameworks Mentioned
- **Ralph Loops** — inject original prompt into fresh context windows to continue long-horizon tasks without context decay
- **Planner / Generator / Evaluator split** — separate agents for planning, generating, and evaluating output
- **Sprint contracts** — negotiate done-conditions (acceptance criteria) with the agent before implementation begins
- **AGENTS.md / CLAUDE.md / skill files** — structured documentation layers for harness configuration
- **MCP (Model Context Protocol)** — runtime for plugging in external tool servers
- **Production architecture layers:** Input → Knowledge (skill registry, memory) → Integration (MCP) → Execution (tool dispatch, caching) → Output (verified results) → Observability → Multi-agent coordination
- **Claude Agent SDK, OpenAI Agents SDK, Codex SDK** — HaaS frameworks providing pre-built loops, tools, context management
- **HumanLayer** — referenced for prompt length recommendations

## Relevance
- The ratchet principle and hook-based enforcement give a concrete rollout playbook: instrument failures as they happen and harden the harness incrementally, which works well for teams that can't afford big upfront investment.
- The "four pillars" customization model (system prompts, tools, context strategy, subagent structure) maps directly to what any team needs to decide when adopting an agentic workflow, regardless of which SDK or model they choose.
