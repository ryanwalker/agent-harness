# Agent Harness & Agentic Engineering — Master Summary
**Sources:** 6 articles (Addy Osmani blog series, Google/Kaggle whitepaper, ADK tutorial, Anthropic/Claude blog)
**Purpose:** Team rollout + interview prep

---

## The One Equation to Know

> **Agent = Model (~10%) + Harness (~90%)**

Most agent failures are configuration problems, not model problems. A decent model with a great harness beats a great model with a bad harness. The harness is where the leverage is — invest here first.

---

## Core Concepts

### What Is a Harness?
Everything except the model: system prompts, rule files, tools, sandboxes, hooks, context loading logic, execution controls, subagent structure, observability.

**Five parts of every agent (whitepaper taxonomy):**
1. **Model** — reasoning engine; reads context, decides next step, produces output
2. **Tools** — connect model to the world: APIs, code execution, databases, other agents
3. **Memory** — state: past interactions, project rules, context across sessions
4. **Orchestration** — the loop: assembles context, dispatches tool calls, captures results, decides whether to continue
5. **Deployment** — hosting, identity, observability, production infrastructure

**Six harness components (what surrounds the model):**
1. Instructions / Rule Files — `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, skill files
2. Tools — functions, MCP servers, APIs the agent can call + prose for when/how to call them
3. Sandboxes / execution environments — what the agent can reach and what it cannot
4. Orchestration logic — subagent spawning, model routing, handoffs between specialists
5. Guardrails / Hooks — deterministic code at lifecycle points (pre-tool-call, post-file-edit, pre-commit)
6. Observability — logs, traces, evals, cost and latency metering

**Claude Code deployment taxonomy (from large codebase article):**
- Skills — on-demand reusable expertise files
- Plugins — bundled configurations for org-wide distribution
- LSP integrations — symbol-level code navigation (requires explicit config)
- Subagents — isolated Claude instances for parallel or scoped work

---

### Context Engineering (the core optimization surface)

**Six context types:**
| Type | What goes here |
|------|---------------|
| Instructions | Role, constraints, operating bounds |
| Knowledge | Architecture docs, domain data, retrieved references |
| Memory | Session state, long-term project state |
| Examples | Few-shot patterns from your actual codebase |
| Tools | Precise API and service definitions |
| Guardrails | Hard constraints the agent cannot cross |

**Static vs. dynamic split:**
- **Static** (loads every turn): system prompts, rule files — keep lean (~60 lines/file max)
- **Dynamic** (loads on-demand): skills, RAG docs, tool results — trigger conditionally
- Progressive disclosure: metadata at startup → full instructions on task match → heavy docs on execution

Treat the static/dynamic boundary as a versioned architectural decision, not an implementation detail.

---

### The Vibe Coding → Agentic Engineering Spectrum

| | Vibe Coding | Structured AI-Assisted | Agentic Engineering |
|---|---|---|---|
| Verification | "does it seem to work?" | manual testing | automated evals + CI/CD gates |
| Rule files | none | informal | versioned, PR-reviewed |
| Right for | prototypes, hackathons | dev productivity | production systems |

Position on spectrum is determined by **verification rigor**, not which tool you use.

**Economics:**
- Vibe coding: near-zero upfront, steep hidden costs (token waste, maintenance tax, security cleanup)
- Agentic engineering: higher upfront, lower marginal cost per feature
- Crossover: vibe coding becomes **3–10x more expensive per feature at scale**
- Use this argument to justify harness investment to a team

**Data from the whitepaper:**
- Self-reported gains: 25–39% productivity improvement (industry surveys)
- Measured reality: 19% **slower** for experienced devs on complex tasks (METR RCT, Feb 2026)
- Terminal Bench 2.0: harness change alone moved an agent from outside Top 30 → Top 5 (no model change)
- LangChain study: +13.7 benchmark points from harness changes alone on a fixed model
- Deloitte: projecting 30–35% productivity gains across full dev process (2025–2026)
- Vibe coding crossover: 3–10x more expensive per feature than agentic engineering at scale

> The whitepaper does not cite Veracode, GitClear, or DORA stats — those appeared only in a third-party critique of the paper, not in the document itself.

---

### The 80% Problem
Agents reliably produce the first 80% of any feature fast. The remaining 20% — edge cases, integration seams, subtle correctness — requires domain judgment models lack. Most production failures originate here. **Do not outsource architectural decisions.**

---

## Build and Rollout Playbook

### Starting a Harness (individual)
1. Create an `AGENTS.md` or `CLAUDE.md` in every project — start with 10 lines
2. Include: stack version pins, architectural patterns, banned packages, test locations, logging standards
3. Add one rule each time the agent makes the same mistake (Ratchet Principle)
4. Every rule must trace to a specific failure or constraint — no orphan rules
5. Write tests before generating code — tests become the specification
6. Review every agent-produced diff before merging

### Rolling Out to a Team
1. **Assign a DRI** (designated responsible individual) before expanding access
2. **Governance first**: approved skills list, code review requirements, limited initial scope
3. **Rule files are production code** — require PR review, version alongside app code
4. **Distribute working setups as plugins** — prevents tribal knowledge and fragmentation
5. **Audit CLAUDE.md every 3–6 months** — remove workarounds as model capabilities improve
6. **Build shared infrastructure** (prompt libraries, skill folders, eval harnesses) — these compound across projects
7. **Encode security invariants as executable tests**, not documentation
8. Track technical debt: code churn rate, copy-paste ratio, refactor ratio

### Operator Modes (switch within a session)
- **Conductor mode**: real-time IDE guidance, keystroke-level; preserves understanding, limits throughput; use for exploration and unfamiliar code
- **Orchestrator mode**: async goal delegation, review results not generation; requires precise specs upfront; use for migrations, test gen, refactors

---

## Agentic Code Review

### The Problem
- 4x raw code output, only 12% more delivered value
- Defect rates rose from 9% → 54%; PRs up 31% with zero review
- The **intent reconstruction problem**: agents discard reasoning before producing diffs, leaving reviewers without context

### Review Framework
Determine review depth using three variables per PR:
1. **Blast radius** — consequence of failure
2. **Code lifespan** — throwaway vs. long-lived
3. **Knowledge distribution** — solo-owned vs. team-shared

**Risk tiers:**
- Config changes → linter + quick glance
- Business logic → types + tests + human sign-off
- Auth/payments → dual AI review + security pass + human sign-off

### Process Gates
- Require agents to attach **decision logs** to PRs (captures reasoning that would otherwise be discarded)
- Require **intake artifacts** before review: statement of purpose, sized diff with comments, test output
- Run **two different AI reviewers** — they catch different things 93.4% of the time
- CI gates are immovable — never let agents weaken coverage thresholds or skip linting
- **A human must own the merge decision** — strategic judgment and accountability don't delegate

### Red Flags in Agent PRs
- Altered test assertions (check this before implementation code)
- Lowered coverage thresholds
- Skipped linting
- Diffs too large to meaningfully review
- Untrusted input flowing into prompt calls (prompt injection surface)

---

## Named Patterns (interview-ready)

| Pattern | Description |
|---------|-------------|
| **Ratchet Principle** | Every agent failure permanently hardens the harness config |
| **Progressive Disclosure** | Metadata at startup → full instructions on match → heavy docs on execution |
| **Agent Skills** | Portable packages of procedural knowledge loaded dynamically by task match; solves context rot |
| **Quality Flywheel** | Evaluate → cluster root causes → optimize prompts/tools → verify against regression suite → monitor production; each cycle compounds |
| **Factory Model** | Developer Zone (specs → guardrails → review) feeds Agent Factory Floor (planning agent → coding agent → tests → verified output, with failure feedback loop) |
| **Ralph Loops** | Inject original prompt into fresh context windows to continue long-horizon tasks without context decay |
| **Planner / Generator / Evaluator split** | Separate agents for planning, generating, and evaluating output |
| **Sprint Contracts** | Negotiate done-conditions (acceptance criteria) with the agent before implementation begins |
| **Conductor / Orchestrator modes** | Two developer operating modes within the same session |
| **Heterogeneous Reviewer Pattern** | Run 2+ different AI reviewers in parallel; they cover different failure modes |
| **Intent Reconstruction** | Capture agent reasoning as decision logs attached to PRs |
| **Risk-Tiered Review** | Match review effort to blast radius + lifespan + knowledge distribution |
| **HaaS (Harness-as-a-Service)** | Industry shift from raw LLM APIs to pre-built harness frameworks |
| **Evaluation-Driven Development** | Benchmark → failure clustering → prompt/tool refinement → regression suite → prod monitoring |

---

## Verification (the new engineering craft)

> "Generation is solved. Verification, judgment, and direction are the new craft."

**Three verification layers:**
1. **Tests** — deterministic input/output coverage
2. **Output evaluation** — is the final result correct?
3. **Trajectory evaluation** — was the reasoning path and tool call sequence sound?

**Eval practice:**
- Set the bar at the eval, not the demo — demos prove single-instance function; evals prove reliable operation
- Use LM-as-judge for non-deterministic outputs
- Run evals in CI — never ship agentic workflows validated only by demo

---

## Tool-Agnostic Standards (avoid lock-in)

| Standard | Purpose |
|----------|---------|
| **MCP (Model Context Protocol)** | Connect tools/data to any AI coding assistant |
| **A2A (Agent-to-Agent)** | Agent-to-agent work handoff and coordination |
| **llms.txt / llms-full.txt** | Machine-readable library docs served to any MCP client |
| **mcpdoc** | Serve any llms.txt-indexed site as an MCP server |
| **AGENTS.md / CLAUDE.md** | Rule file convention (supported by Claude Code, Cursor, Gemini CLI, etc.) |

**Shared docs MCP setup (team rollout):**
```json
{
  "mcpServers": {
    "your-library-docs": {
      "command": "uvx",
      "args": ["--from", "mcpdoc", "mcpdoc", "--urls", "LibName:https://your-lib.dev/llms.txt", "--transport", "stdio"]
    }
  }
}
```
Commit this as `mcp.json` in the project repo — every engineer's IDE gets the same documentation context automatically.

---

## Model Routing (cost lever)

- **Frontier models**: complex reasoning, architecture decisions, unfamiliar code
- **Smaller/cheaper models**: test generation, CI checks, code review, deterministic tasks
- Model routing is a direct financial lever — don't route everything to the most expensive model

---

## Interview Talking Points

- "Most agent failures are harness failures — I start by auditing the configuration, not the model"
- "Verification is the high-leverage skill now; generation is commoditized"
- "The 80% problem is real — I keep humans in the loop for edge cases and integration seams"
- "My review framework: blast radius × lifespan × knowledge distribution"
- "Every agent mistake is a permanent signal — I apply the Ratchet Principle to harden config incrementally"
- "Tests written before generation are the specification, not an afterthought"
- "I use heterogeneous reviewers because no single AI reviewer catches everything"

---

## Files in This Directory
| File | Source |
|------|--------|
| `01-new-sdlc-vibe-coding.md` | Addy Osmani — New SDLC & Vibe Coding |
| `02-agent-harness-engineering.md` | Addy Osmani — Agent Harness Engineering |
| `03-whitepaper-new-sdlc-vibe-coding.md` | Google/Kaggle whitepaper (reconstructed from author blog + secondary sources) |
| `04-agentic-code-review.md` | Addy Osmani — Agentic Code Review |
| `05-adk-coding-with-ai-cli.md` | ADK — Coding with AI CLI tutorial |
| `06-claude-code-large-codebases.md` | Anthropic — Claude Code in Large Codebases |
