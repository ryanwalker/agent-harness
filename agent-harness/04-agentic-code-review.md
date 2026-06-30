# Agentic Code Review
**Source:** https://addyosmani.com/blog/agentic-code-review/
**Topic:** How to structure code review workflows when agents are generating most of the code

## Key Concepts
- The bottleneck shifted: code generation is cheap now; verification is the expensive, high-leverage skill
- Industry data (2026): AI users produce ~4x raw code output but only ~12% more delivered value; code churn up 861%; defect rates rose from 9% to 54%; AI-written code produces 1.7x more issues than human-written code
- The **intent reconstruction problem**: agents discard their reasoning before producing diffs, leaving reviewers with no context — solution is to capture agent reasoning as decision logs attached to PRs
- Four parallel reviewers flagged different lines 93.4% of the time — heterogeneous reviewers beat any single "best" tool
- PRs merging with zero review up 31.3%; review duration up 441.5% — the process is breaking under volume

## Actionable Takeaways
- Determine review depth using three variables per PR: **blast radius** (consequence of failure), **code lifespan** (throwaway vs. long-lived), **knowledge distribution** (solo vs. team ownership required)
- Implement **risk-tiered review**: config changes → linter + glance; payments/auth → types + tests + dual AI review + human sign-off + security pass; boilerplate → lightweight
- Require agents to produce **intake artifacts** before review begins: statement of purpose, appropriately-sized diff with comments, test output, evidence justifying the change
- Instruct agents to produce **small commits** deliberately — large unreviable diffs are 51% larger on average in agent PRs
- **Read test changes more carefully than implementation code** — agents may alter assertions to match broken behavior
- Run **two deliberately different AI reviewers** (e.g., one broad, one correctness-focused); don't chase the single "best" tool
- Keep CI as immovable deterministic gates; never let agents weaken coverage thresholds or skip linting
- Implement **circuit breakers** for high-maintenance PRs using file types and patch size before human review begins
- A human must own the merge decision — accountability, strategic judgment, and requirement-level thinking don't delegate
- For teams: protect reviewer capacity as a measurable resource; prevent review from becoming a senior engineer tax

## Red Flags in Agent PRs
- Removed or rewritten tests (especially altered assertions)
- Lowered coverage thresholds or skipped linting
- Untrusted input flowing into prompt calls (prompt injection surface)
- Changes that weaken CI gates
- Diffs too large to meaningfully review

## Patterns / Frameworks Mentioned
- **Risk-tiered review** — match review effort to blast radius + lifespan + knowledge distribution
- **Intent reconstruction problem** — capture agent reasoning as decision logs on PRs
- **Heterogeneous reviewer pattern** — run 2+ different AI reviewers in parallel
- **Loop Engineering** — humans own escalation, sampling, and merge; agents own generation
- **Predictive triage / circuit breakers** — flag high-maintenance PRs early using patch metadata
- **Intake requirements gate** — enforce PR intake checklist before review begins
- **Kun Chen loop pattern** — detailed upfront plan → 20-30 parallel agents → automated gates → human escalation (noted as solo/greenfield only, not team/legacy)
- Tools mentioned: CodeRabbit, Greptile, Sentry Seer, Cursor BugBot, Anthropic Code Review, GitClear, Faros AI, GitHub Copilot

## Relevance
- Directly applicable to team rollout: the risk-tiering framework and intake requirements give you concrete process gates to propose without mandating a specific tool or language stack.
- The core message for job interviews: the engineering value-add has shifted from writing to verifying — demonstrate you have a review system, not just a generation workflow.
