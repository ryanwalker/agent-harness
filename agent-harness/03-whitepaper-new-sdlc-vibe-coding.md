# The New SDLC With Vibe Coding: From Ad-Hoc Prompting to Agentic Engineering
**Source:** /Users/ryanwalker/projects/research/agent-harness/The_New_SDLC_With_Vibe_Coding_Google_Whitepaper.pdf
**Authors:** Addy Osmani, Shubham Saboo, Sokratis Kartakis (content contributors: Elia Secchi, Julia Wiesinger, Anant Nawalgaria)
**Published:** May 2026
**Topic:** Framework for moving from casual AI prompting to disciplined agentic engineering across every SDLC phase

> Note: Summary based on full PDF read (all 51 pages).

---

## Key Concepts

**The Spectrum (not a binary)**
- The key differentiator is NOT whether you use AI — it's how much structure, verification, and human judgment surrounds the AI's output
- Three positions: Vibe Coding | Structured AI-Assisted | Agentic Engineering
- Vibe Coding: casual prompts, "does it seem to work?" verification, disposable code; appropriate scope = prototypes/hackathons; risk = high
- Structured AI-Assisted: detailed prompts with examples and constraints, manual testing and spot-checks, selective review; scope = features in established codebases; risk = moderate
- Agentic Engineering: formal specs + architecture docs, automated evals + CI/CD gates, comprehensive review; scope = production systems at scale; risk = low (systematic verification at every stage)
- The same coding agent can be used at either end — the spectrum is about deliberateness of harness configuration, not the tool

**Agent = Model + Harness (the core equation)**
- Model ~10% of outcomes; Harness ~90% of outcomes
- Harness: everything surrounding the model — prompts, tools, context policies, hooks, sandboxes, sub-agents, observability
- Terminal Bench 2.0: one team moved a coding agent from outside Top 30 → Top 5 by changing only the harness, no model change
- LangChain study: +13.7 benchmark points on the same benchmark by tweaking only system prompt, tools, and middleware on a fixed model
- "Most agent failures, examined honestly, are configuration failures."

**Five Parts of Every Agent**
1. Model — reasoning engine; reads context, decides next step, produces output
2. Tools — connect model to the world: APIs, code execution, databases, other agents
3. Memory — state: past interactions, project rules, context across sessions
4. Orchestration — code that runs the loop: assembles context, dispatches tool calls, captures results, decides whether to continue
5. Deployment — hosting, identity, observability, production infrastructure

**Six Types of Agent Context**
1. Instructions — core role, goals, operational boundaries
2. Knowledge — retrieved docs, architectural diagrams, domain-specific data
3. Memory — short-term session logs + long-term persistent state
4. Examples — few-shot behavioral demos and codebase reference patterns
5. Tools — precise definitions of APIs, scripts, external services the agent can invoke
6. Guardrails — hard constraints, formatting rules, safety validations

**Static vs. Dynamic Context**
- Static: always loaded every interaction — system instructions, rule files (AGENTS.md, CLAUDE.md, GEMINI.md), global memory, core guardrails; token cost: high; never forgotten
- Dynamic: loaded on demand — Agent Skills (triggered by task match), tool results (retrieved during execution), RAG documents, windowed session history; token cost: low per turn; pay only when needed
- Boundary between static and dynamic is a first-class architectural decision, reviewed and versioned like code
- Too much static context wastes tokens and dilutes signal; too little means the agent forgets critical rules

**Agent Skills** — the key pattern for managing static/dynamic tradeoff
- Structured, portable packages of procedural knowledge loaded only when the task calls for it
- Agent sees lightweight metadata at startup, loads full instructions on task match, pulls deep reference material only when explicitly needed
- Solves four problems: context rot from overloaded prompts, absence of procedural memory for LLMs, operational overhead of multi-agent architectures, need for portability across tools and vendors

**The New SDLC — compression is uneven**
- Traditional iterative: Requirements (2-3 days) → Design (1-2 days) → Implementation (1-3 weeks) → Testing (3-5 days) → Review & Deploy (2-3 days) → Maintenance; sprint cycle: weeks
- AI-Driven: same phases but Implementation = minutes to hours; iteration cycle: minutes to hours
- What shifts: bottleneck moves from writing code → specifying intent precisely and verifying output
- Specification quality is the new bottleneck; architecture decisions are amplified at scale

**How AI Transforms Each SDLC Phase**
- Requirements: AI generates user stories from product briefs, identifies edge cases humans miss, produces API schemas from NL descriptions, generates interactive prototypes; requirements become a conversation not a handoff document
- Design/Architecture: most stubbornly human-centric phase; trade-offs (consistency vs. availability, build vs. buy) depend on business context AI cannot fully grasp; AI excels at implementing decisions once made, scaffolding entire applications from a clear architecture doc
- Implementation: 25-39% productivity gains (industry surveys); METR study found experienced devs took 19% longer on certain tasks because of verification/debugging overhead; work transforms from writing to reviewing, guiding, verifying
- Testing & QA: output evaluation (does code compile, do tests pass) + trajectory evaluation (full sequence of tool calls and intermediate reasoning); fluent output that skipped verification steps is more dangerous than one with a visible error; quality flywheel: evaluate → cluster root causes → optimize prompts/tools → verify against regression suite → monitor production
- Code Review & Deployment: AI as first-pass reviewer (bugs, style violations, security vulnerabilities); human review still required for design/maintainability/strategic alignment; AI agents monitor deployment health, auto-rollback, predict deployment risk; deployment pipelines becoming AI-aware
- Maintenance: previously impenetrable legacy codebases now navigable with AI; agents can systematically migrate between frameworks, update deprecated APIs, modernize test suites

**The Factory Model**
- Developer's primary output is not code — it's the system that produces code
- Developer Zone: Define Specs → Design Guardrails → Review & Approve
- Agent Factory Floor: Specs/Context/Requirements → Planning Agent → Coding Agent → Tests & Verification (pass → Verified Output; fail → Failure feedback loop back to Planning Agent)
- Guardrails at every level: token limits, security policies, style rules, architectural constraints
- "Give agents success criteria rather than step-by-step instructions, then let them iterate."

**Harness Components (What Surrounds the Model)**
- Instructions and Rule Files: AGENTS.md, CLAUDE.md, GEMINI.md, skill files, sub-agent prompts
- Tools: functions, MCP servers, APIs the agent can call, plus prose telling the model when/how to call them
- Sandboxes and execution environments: where agent code runs, what it can access, what it cannot reach
- Orchestration logic: sub-agent spawning, model routing, hand-offs between specialists, rules governing when each fires
- Guardrails / Hooks: deterministic code at specific lifecycle points (before a tool call, after a file edit, before a commit); things the agent should never forget but often does
- Observability: logs, traces, evaluations, cost and latency metering; without it there is no way to tell whether the agent is doing well or quietly drifting

**Harness Across the SDLC**
1. Requirements, Planning & Architecture (Configuring the Harness): create AGENTS.md, define architectural constraints, specify tool access and fundamental rules before a single line of production code
2. Implementation (Running the Harness): sandboxes and execution environments keep agent focused, secure, productive; model generates code within harness-isolated sandbox, uses only tools the harness provides
3. Testing & QA (The Feedback Loop): orchestration logic captures test failure output and routes it back to the model to re-plan; harness creates the automated "think → act → observe" loop
4. Code Review, Deployment & Maintenance (Observing the Harness): hooks block commits with hard-coded passwords or policy violations; observability tracks token costs, latency, agent drift, lets engineers audit why a decision was made

**Developer Modes: Conductor vs. Orchestrator**
- Conductor: real-time, synchronous, in-IDE; keystroke-level control, immediate feedback, single-file scope, developer always in the loop; best for exploratory coding, prototyping, learning new APIs; risk — can become a bottleneck if developer directs every keystroke
- Orchestrator: asynchronous, high-level, multi-agent; goal-level control, delayed feedback, multi-file scope, reviews outcomes not keystrokes; best for feature implementation, migrations, test generation; requires skills in specification, decomposition, evaluation, system design
- Most developers move fluidly between both in a single day

**Three Categories of Coding Agent in Daily Practice**
- In the editor: inline completion, chat panels, whole-codebase awareness in IDE; examples: GitHub Copilot, Cursor, Windsurf, JetBrains AI Assistant
- In the terminal: full filesystem access, multi-file edits, runs tools and tests, iterates on results; examples: Claude Code, Codex CLI, Antigravity CLI, Open Code, Cline, Aider
- In the background: cloud-hosted sandboxes, works autonomously for hours, produces PR output; examples: Google Jules, GitHub Copilot agent mode, Cursor background agents, Google AlphaEvolve

**The 80% Problem**
- Agents rapidly generate ~80% of code for a feature
- Remaining 20% (edge cases, error handling, integration points, subtle correctness) demands deep contextual knowledge current models often lack
- Error character has evolved from syntax mistakes → conceptual failures: wrong business logic assumptions, missing edge cases, architectural decisions that create long-term maintenance burdens
- These errors are harder to detect because the code "looks right" and may pass basic tests
- Effective developers use AI for rapid implementation of well-specified tasks; reserve their own attention for ambiguous requirements, architectural trade-offs, and correctness verification

**Economics: CapEx vs. OpEx**
- Vibe Coding (Low CapEx, High OpEx): token burn from unstructured prompting loops, context collapse, maintenance tax (spaghetti code with no structural consistency), security remediation; crossover point: vibe coding costs 3-10x more per feature at scale
- Agentic Engineering (High CapEx, Low OpEx): upfront investment in API schemas, deterministic test suites, structured agent context; marginal cost of shipping and maintaining a feature drops dramatically thereafter
- Context engineering as financial lever: dense high-signal AGENTS.md increases first-pass success rate, avoids costly trial-and-error loops
- Intelligent model routing: frontier models for complex tasks (requirements, architecture, initial implementation); smaller, faster, cheaper models for deterministic lower-complexity tasks (test generation, code review, CI/CD monitoring)

---

## Actionable Takeaways

### For Individual Developers
1. Set up an AGENTS.md (or CLAUDE.md / GEMINI.md) for every project — start with 10 lines covering stack, conventions, hard rules, workflow; add a rule every time the agent does something it shouldn't repeat
2. Install a set of Agent Skills for your coding agent (e.g., via Agents CLI) to build, evaluate, deploy, and optimize agents
3. Pick one repetitive workflow and build it as an agent end-to-end — doing this once teaches more than reading about a hundred
4. Write tests and evals before generating code — they are the contract with the AI and communicate intent more precisely than any natural-language prompt
5. Review every line the agent produces before it ships — check imports for real packages, verify error handling covers realistic failure modes, be skeptical of anything that looks clever
6. Maintain your foundational developer skills deliberately — AI handles the routine, but debugging, system design, performance intuition, and architecture judgment must stay sharp; treat AI as a way to apply expertise at greater scale, not a substitute for it

### For Engineering Leaders / Team Rollout
1. Make context engineering a first-class engineering practice — treat AGENTS.md, system prompts, eval suites, and skill libraries as code: reviewed in pull requests, versioned with the project, owned by named engineers; without this discipline, harness drifts and agent behavior becomes irreproducible
2. Set the bar at the eval, not the demo — a working demo proves an agent can succeed once; a passing eval suite proves it succeeds reliably; define scoring criteria (task success, tool use quality, trajectory compliance, hallucination rate, response quality) and require eval coverage as a precondition for any agent shipping into a shared workflow
3. Re-shape code review for AI-generated code — extra attention to hallucinated dependencies, inadequate error handling, subtle correctness gaps that look right at a glance; train reviewers on the failure modes of generated code
4. Make the boundary between vibe coding and agentic engineering explicit in team norms — which projects, branches, and environments warrant which mode; teams that keep this distinction blurry produce prototypes that ship by accident
5. Invest in harness components as a shared team asset — reusable system prompts, skill libraries, MCP server connections, and evaluation harnesses compound across projects; treat them as infrastructure: documented, maintained, improved deliberately; the teams compounding the most value build the harness once and refine it many times

### For Engineering Leaders / Team Rollout (Org Level)
1. Treat AI-assisted development as an engineering investment, not a productivity feature — rolling out a coding agent without eval coverage, observability, and clear architectural standards produces speed without quality, which compounds into technical debt faster than any team can pay it down
2. Build the production substrate before the first production agent ships — trajectory and final-response evals running in CI, traces of every agent run, scoped permissions per agent, security review tuned to the failure modes of generated code; not after
3. Adopt open standards for tools and inter-agent communication — MCP for tool access, A2A (Agent2Agent protocol) for cross-agent delegation; choosing them now keeps vendor options open and avoids re-platforming later
4. Plan for hybrid teams of humans and agents — code review processes, on-call rotations, and team structures all need to evolve to reflect that agents are now participants, not just tools
5. Reframe hiring and skill development around judgment, not just implementation — the most valuable engineers in the next several years will be those who can direct agents well: strong at specification, evaluation, architectural judgment, and review

---

## Named Patterns / Frameworks
- Agent = Model + Harness — the core equation; the harness dominates outcomes, not the model
- The Spectrum — vibe coding to agentic engineering; position determined by verification rigor, not tooling choice
- Factory Model — developer designs the system that produces code; agents implement within guardrails; tests verify output; failure loops back
- Conductor mode — real-time, keystroke-level direction in the IDE; fine-grained control but limited throughput
- Orchestrator mode — async, goal-level delegation; high-leverage but requires specification and evaluation skills
- The 80% Problem — agents reliably produce ~80% of any feature; remaining 20% requires domain context models lack and is where production failures originate
- Static vs. Dynamic Context split — architectural design decision on what belongs in always-loaded vs. on-demand context
- Agent Skills — portable packages of procedural knowledge loaded dynamically by task match; solves context rot and portability
- Quality Flywheel — evaluate → cluster root causes → optimize prompts/tools → verify against regression suite → monitor production; each cycle compounds
- Intelligent Model Routing — route complex reasoning to frontier models; route deterministic work to smaller cheaper models
- Progressive Disclosure — agent sees only metadata at startup, loads full instructions on task match, pulls deep reference material only when explicitly needed

---

## Data / Statistics Worth Citing
- 85% of professional developers use AI coding agents regularly (early 2026) — GetPanto / Index.dev
- 51% use AI coding agents daily
- 41% of all new code is AI-generated (2026 industry data)
- 25-39% self-reported productivity gains from structured AI-assisted development (industry surveys)
- METR study (Feb 2026): experienced developers took 19% longer on certain tasks with AI — largely due to time spent verifying, debugging, and correcting AI output
- Terminal Bench 2.0: harness change alone (no model change) moved an agent from outside Top 30 → Top 5
- LangChain study: +13.7 benchmark points on the same benchmark from harness changes alone (fixed model)
- Vibe coding crossover point: 3-10x more expensive per feature than agentic engineering at scale
- Deloitte: projecting 30-35% productivity gains across the full development process (2025-2026)
- Anthropic experiment (early 2026): agent teams built a working C compiler in Rust in two weeks, with humans setting direction and reviewing but not writing implementation
- Traditional SDLC implementation: 1-3 weeks → AI-Driven SDLC: minutes to hours

---

## Gaps / Caveats
- The 10%/90% model-vs-harness split is asserted via the Terminal Bench and LangChain examples but no formal methodology is cited — it is illustrative, not a measured ratio
- Productivity gains (25-39%) are largely self-reported; the METR RCT result (19% slower) is the only controlled-experiment data cited and applies specifically to experienced developers on complex tasks — the paper does not reconcile these conflicting results
- The paper is written at mid-2026 and explicitly acknowledges the phase-by-phase picture "is shifting fast" and "may look different in 12 months" — frameworks are intentionally durable but specific timelines are not
- Architecture and design remain "stubbornly human-centric" — the paper does not offer a concrete model for when/how to delegate architectural decisions, only that you shouldn't fully delegate them
- Security is treated lightly — the paper notes that vibe coding rapidly generates vulnerabilities and that security invariants should be encoded as executable tests, but provides no specific security metrics or mitigation checklist
- The paper is published by Google and prominently features Google tools (Agents CLI, ADK, Agent Runtime, Jules, Gemini Code Assist, A2A protocol, AlphaEvolve) — the frameworks are vendor-agnostic but the tooling examples skew heavily toward the Google stack
- No data on team-level coordination overhead when multiple developers each run background agents concurrently against shared codebases

---

## Relevance
The whitepaper provides the most comprehensive public framework available for operationalizing AI-assisted development at a team and org level — the spectrum model, harness taxonomy, factory model, and conductor/orchestrator distinction all translate directly into rollout planning conversations and give precise vocabulary for internal alignment. The economics section (vibe coding becomes 3-10x more expensive at scale) and the "where to start" prescriptions (AGENTS.md first, evals before demos, harness as shared infrastructure) are immediately applicable to team rollout sequencing and are strong interview talking points for engineering judgment questions.
