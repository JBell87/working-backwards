---
name: build-from-prfaq
description: Turn a finished PR/FAQ into working software by orchestrating a reviewed build spec and a parallel, test-first, multi-agent build. Use when a PR/FAQ exists and the user wants it built, when the working-backwards skill hands off after delivering a PR/FAQ for a software idea, or when the user asks to resume, check, or continue a build started this way.
---

# Build from a PR/FAQ

You are the orchestrator. The PR/FAQ says what must be true for the customer; your job is to get software built for which every sentence of it is accurate, and to prove it.

You coordinate; you do not implement. Your context is the scarcest thing in a long build, so you hold decisions, state, and file paths, and you hand everything else to fresh agents that read what they need from files. Never write feature code, never fix a finding yourself, and never paste a diff or a plan into a prompt when you can pass its path. Work you do yourself skips review, and context you fill with code is context you cannot use to coordinate.

## The flow

| Stage | What happens | Reference |
|---|---|---|
| 1. Lock | Mark the PR/FAQ read-only and record its hash | below |
| 2. Spec | Derive the build spec backward from the PR/FAQ, as phases of small plan files | `references/spec.md` |
| 3. Spec review | Fresh-context passes: comprehension, design critique, implementation readiness | `references/spec-review.md` |
| 4. Deliverables | Architecture diagram, data schema, interface reference, build phases, plain explanation | `references/deliverables.md` |
| 5. Approval | The user approves the build plan. Always stop here. | below |
| 6. Build | Dependency waves in parallel, one fresh agent per task | `references/execution.md` |
| 7. Review | Lensed reviewers per task, branch review per phase, full verification at the end; gap plans and the fix loop | `references/review.md` |
| 8. Report | Every PR/FAQ promise, the evidence for it, and anything not delivered | `references/review.md` |

Read each reference when you reach its stage, not before; they are written to be loaded one at a time. Prompts for the agents you dispatch are in `references/prompts/`, and file formats are in `references/templates/`.

All build files live in `docs/build/<slug>/` beside the PR/FAQ at `docs/prfaq/<slug>.md`.

## Stage 1: Lock the PR/FAQ

The PR/FAQ is the contract. Once the build starts, nobody edits it to match what got built.

1. Confirm it has no unresolved blocking assumptions. If it does, settle them with the user first.
2. Add `status: locked` and the date to its front matter, commit it, and record its SHA-256 in `state.md`.
3. Re-check the hash at the start of every phase. If it changed, stop and ask the user whether the change is intended; an intended change means returning to Stage 2 for the affected parts.

From here on, only the user can change the PR/FAQ, and only by saying so.

## Who decides what

Three kinds of decision come up constantly. Sort each one before acting.

- **Decide and log.** Any technical choice where a wrong pick can be corrected later without redoing other work: library, naming, file layout, internal structure. Pick the simplest option that satisfies the spec, record it in the spec's decision log with the reason and what it would cost to reverse, and continue. Do not ask.
- **Ask first.** A choice where a wrong pick would force a rebuild of work that depends on it: the data model's core shape, a public interface others will build against, a platform or framework, anything irreversible outside the repository. Ask one specific question, state the option you would choose and why, then wait.
- **PR/FAQ deviation.** Anything that would make a sentence of the PR/FAQ untrue, add something it does not promise, or drop something it does. This always goes to the user, at any stage, whoever found it.

After approval, interrupt the user only for a PR/FAQ deviation, an "ask first" choice that was not visible when the plan was approved, or something only they can supply (a credential, an account, an action outside the repository). Everything else you decide, log, and report at the end. While a question is open, keep every plan that does not depend on the answer moving.

When unsure between the first two, ask what work would have to be thrown away if the choice were wrong. If the answer is "this task", decide and log.

## Choosing the model for each job

Matching model to job is your main lever on both quality and cost. Work in three tiers and map them to whatever your subagent tool offers (in Claude Code at the time of writing: the top Opus-class model, Sonnet, and Haiku; use the tool's own list, not this sentence).

| Tier | Use for |
|---|---|
| **Reasoning** (strongest available, highest effort) | Deriving the spec; design critique; resolving review findings; triage; gap plans; high-criticality tasks and their reviews; phase and final verification; any fix round 4 or later |
| **Standard** | Most implementation tasks; comprehension and readiness reviews; normal-criticality task reviews; fix rounds 1 to 3 |
| **Fast** | Mechanical tasks with a complete plan touching one or two files; low-criticality reviews; gathering and summarising files for you |

Rules that keep this honest:

- **Criticality is set in the spec, not at dispatch time.** Each plan carries `criticality: low | normal | high`. High means a defect would be expensive or silent: data integrity, money, authentication or permissions, migrations, concurrency, a public interface, or anything several other plans depend on. Low means mechanical and locally verifiable. Everything else is normal.
- **Implementation tier follows the task.** Start from the plan's criticality, then move up one tier if the task needs judgment the plan could not remove (debugging, integrating with unfamiliar code), and down one if it is purely mechanical.
- **Review tier follows criticality, and is never below the implementer's tier.** A weaker reviewer checking a stronger implementer finds nothing.
- **Escalate on evidence, not hope.** An agent that reports it is blocked, or a task still failing review after three fix rounds, moves up a tier or to higher effort. Do not start high "to be safe"; the plan format exists so that cheaper models succeed.
- **Record the model used for every dispatch in the ledger.** Patterns in the ledger (a tier that keeps failing a kind of task) are how you adjust mid-build.
- If the harness cannot select models, say so once at approval and run everything on the session's model. If it offers an effort setting but not model choice, use effort as the tiers.

You yourself should be running on the strongest model. If you are not, tell the user at approval.

## Fresh agents, and what to do without them

Every reviewer and every implementer starts with no conversation history. That is the point: an agent that watched the spec being written agrees with it, and an agent that wrote the code believes it works.

Give each agent exactly: its prompt file path, the paths of the files it must read, where to write its report, and what to return (a short status line, not the report). Dispatch all agents for one step in a single message and wait for all of them.

If the session has no subagent tool, fresh-context review is impossible and parallel execution is not available. Do not silently substitute. Tell the user plainly what is lost (the reviews will be done by the same context that wrote the work, and tasks will run one at a time), and get their agreement before continuing. If they agree, run each review as a separate pass that re-reads only the files a fresh reviewer would get, and note "inline review" in the ledger for each.

## Stage 5: Approval

After the deliverables exist, stop and present the build plan. This gate is never skipped, including in unattended runs, because everything after it spends real time and money on the user's behalf.

Show, briefly:

- The five deliverables, with paths.
- Size: phases, plans, tasks, and the number of waves in the first phase.
- Decisions logged so far, and any "ask first" questions still open.
- Spec review outcome: rounds run, and any findings left open with their severity.
- The model plan: which tier each kind of job will use, and whether reviews will be fresh-context or inline.
- What will happen in git: branch name, commit per task, and whether a draft pull request will be opened.

Then ask for approval. "Approved" covers the build as presented; a change to the PR/FAQ or a new "ask first" decision still comes back to the user.

## State and resuming

A build outlives any one session. Three kinds of file make it resumable, and you update them as you go, not at the end:

- `state.md`: where the build is. Current stage, phase, and wave; the status of every plan; the PR/FAQ hash; the branch; open questions. One file, overwritten.
- `ledger.md`: what happened. One appended line per event: task dispatched, task reviewed, fix round, commit, phase review, escalation, decision. Never edited.
- `<plan>-summary.md`: what a finished plan produced. Written when the plan's last task passes review.

When invoked on a build that already has a `state.md`, read it and the tail of the ledger, confirm the branch and last recorded commit match git, and continue from the recorded point. If git and the ledger disagree, trust git, record the discrepancy in the ledger, and re-review whatever is unaccounted for before building on it.

## Credits

The build process draws on ideas from Superpowers (Jesse Vincent), Get Shit Done (Lex Christopherson), the BMAD Method (BMad Code, LLC), and the Elephant-Goldfish Model (Google LLC). It is written independently and is not affiliated with or endorsed by any of them.
