# working-backwards

A Claude Code plugin for the Working Backwards method: write the press release and FAQ for a product before building it, then build software until every sentence of that document is true.

It has two skills:

- **`working-backwards`** turns an idea into a PR/FAQ.
- **`build-from-prfaq`** turns the PR/FAQ into working software, by orchestrating a reviewed build spec and a parallel, test-first, multi-agent build.

## The flow

```
idea
 └─ PR/FAQ (optional six-page narrative)                working-backwards
     └─ locked: read-only from here                     build-from-prfaq
         └─ build spec, derived backward from the PR/FAQ
             truths -> artifacts -> connections -> phases -> small plan files
         └─ fresh-context review: comprehension, design critique, readiness
         └─ deliverables: architecture diagram, data schema, interface
            reference, build phases, plain-language explanation
         └─ YOU APPROVE THE BUILD PLAN
         └─ build: dependency waves in parallel, a fresh agent per task
             └─ after each task: reviewers with different lenses, in parallel
             └─ after each phase: whole-branch, goal-backward verification
             └─ gaps: gap plans and a fix loop that escalates models
         └─ final verification against the PR/FAQ, sentence by sentence
```

## What `working-backwards` does

- **Draft** a PR/FAQ from an idea: a one-page press release, customer and internal FAQs, and a list of assumptions to validate.
- **Coach** you through the five customer questions one at a time, pushing back on weak answers before anything is written.
- **Critique** an existing PR/FAQ as a skeptical senior reader would.
- **Six-page narrative**, on request.

It does not invent metrics, research, or customers. Gaps are marked as placeholders or open questions.

## What `build-from-prfaq` does

**Derives the spec backward.** It starts from what must be observably true for the PR/FAQ to be accurate, then the files that requires, then the connections between them. Work is split into phases that each end with something working, and phases into small plan files (about 2,000 tokens each) of test-first tasks that leave no design decision to the implementer.

**Reviews the spec with fresh eyes.** Reviewers with no conversation history check that the spec can be followed, that the design delivers the truths, and that each plan can be implemented as written.

**Asks you once.** You approve the build plan, with five documents to judge it by. After that it comes back to you only if something would make the PR/FAQ untrue, a newly discovered choice would force a rebuild if wrong, or it needs something only you can supply.

**Builds in parallel.** Plans that do not depend on each other and do not share files run at the same time, each task with a fresh agent.

**Treats "task done" and "goal achieved" as different things.** Reviewers check that tests assert what they should, that code is connected to the rest of the system, and that nothing was stubbed or quietly narrowed. Phase and final reviews verify each promise in four steps: it exists, it is real, it is connected, it is exercised from the outside.

**Chooses the model for each job.** The strongest model designs, critiques, and triages; implementation uses the model the task warrants; reviews scale with how critical the plan is. Failures escalate: the same implementer for three fix rounds, then a stronger model or higher effort.

**Keeps state on disk.** A state file, an append-only ledger, a summary per plan, and one commit per reviewed task, so a build can stop and resume. With a GitHub remote it keeps a draft pull request up to date; it never merges or pushes to the default branch.

### How decisions are made

| Kind of decision | What happens |
|---|---|
| Technical choice that can be corrected later | Decided and logged, without asking |
| Choice where a wrong pick would force a rebuild | You are asked first |
| Anything that would make the PR/FAQ untrue | Always comes to you |

### Requirements

The build is designed for Claude Code, where it can start subagents and choose their models. Without subagents it tells you what is lost (fresh-context review and parallel work) and asks before continuing with inline review.

## Install

In Claude Code:

```
/plugin marketplace add JBell87/working-backwards
/plugin install working-backwards@working-backwards
```

To use only the PR/FAQ skill elsewhere, copy `skills/working-backwards/` into your skills folder or upload it as a skill in the Claude apps. It will stop after delivering the PR/FAQ.

## Use

- "Working backwards on this idea: ..."
- "Coach me through a PR/FAQ for ..."
- "Review my PR/FAQ before I send it"
- "Build this PR/FAQ" or "Resume the build"

## What a build writes

```
docs/prfaq/<slug>.md              the PR/FAQ, locked
docs/build/<slug>/
  spec.md                         truths, artifacts, connections, phases, decision log
  architecture.md  schema.md  api.md  phases.md  explained-simply.md
  phases/01-<name>/01-<plan>.md   plan files, with summaries as they complete
  reviews/                        reviewer reports
  state.md  ledger.md             where the build is, and what happened
  report.md                       final verification against the PR/FAQ
```

## Examples

- [`examples/critique.md`](examples/critique.md): a review of a deliberately weak PR/FAQ.
- [`examples/draft-and-build.md`](examples/draft-and-build.md): a PR/FAQ for a small command-line tool, built with the simple single-agent loop from version 0.1. The code is in [`examples/overdue/`](examples/overdue/). It predates `build-from-prfaq`.

## Testing it

[`docs/dry-run-test-plan.md`](docs/dry-run-test-plan.md) is a staged first run: a dry run to the approval gate, a one-phase build, then fault injection.

## Status

Version 0.2. `build-from-prfaq` is new and **has not yet been run end to end**. Draft and critique modes have been exercised on the examples above; coach mode and the six-page narrative have not.

## Licence and credits

MIT. Based on the Working Backwards process described in Colin Bryar and Bill Carr's book *Working Backwards*. Not affiliated with or endorsed by Amazon.

The build process draws on ideas from [Superpowers](https://github.com/obra/superpowers) (Jesse Vincent, MIT), [Get Shit Done](https://github.com/gsd-build/get-shit-done) (Lex Christopherson, MIT), the [BMAD Method](https://github.com/bmad-code-org/BMAD-METHOD) (BMad Code, LLC, MIT), and the [Elephant-Goldfish Model](https://github.com/google/elephant-goldfish-model) (Google LLC, Apache-2.0). It is written independently, contains no text or code from them, and is not affiliated with or endorsed by any of them.
