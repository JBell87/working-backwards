# Stage 2: Derive the build spec

Do this stage yourself on the Reasoning tier. It is the one piece of deep work the orchestrator does, because every later agent depends on it. If the repository already has code, first send a Fast-tier agent to map the relevant parts and return a summary; plan from the summary.

The spec is derived backward. Do not start from "what should we build"; start from "what must be true".

## 1. Truths

Read the locked PR/FAQ and write down every statement that claims the product does something, as the customer would observe it. Sources: the press release's summary, solution, and how-it-works paragraphs; every Customer FAQ answer; any Internal FAQ answer that constrains behaviour (limits, privacy, what happens on failure).

Give each an ID and a source:

```
T-07  When nothing is overdue, the tool says so and exits without an error.  [Customer FAQ 5]
```

Rules:

- A truth is observable from outside: something a customer or a test at the product's outer surface can see. "Uses a queue" is not a truth; "a delivery that fails is retried and the customer is told" is.
- Every claim gets a truth. If a sentence of the PR/FAQ promises something and you cannot write a truth for it, the PR/FAQ is ambiguous: that is a PR/FAQ deviation question for the user, not something to resolve by picking a reading.
- Copy the Internal FAQ's "not in the first version" list into the spec as **Never**. Anything on it is out of scope for every agent.

## 2. Artifacts

For each truth, list what must exist for it to hold: files, modules, tables, endpoints, commands, configuration. Name them concretely (`src/overdue/report.py`, table `invoices`), not by role.

## 3. Connections

For each artifact, list what it must be connected to for the truth to hold: who calls it, what it reads and writes, what it is registered with. This is where builds fail quietly: every part exists and nothing is wired together. Write each connection as a checkable statement:

```
C-12  cli.main calls report.find_overdue with the parsed invoices and today's date
```

Connections become the integration reviewer's checklist and the final verifier's evidence.

## 4. Phases

Group the work into phases. Each phase must end with the product working and one or more truths demonstrably holding from the outside. Prefer thin end-to-end slices (one truth working through every layer) to horizontal layers (all the models, then all the endpoints), because slices can be verified against the PR/FAQ and layers cannot.

A phase that cannot name the truths it delivers is not a phase.

## 5. Plans and tasks

Break each phase into plan files, each a small, independently reviewable unit of two to five tasks. Use `templates/plan.md`.

- **Size cap: about 2,000 tokens per plan file** (roughly 1,500 words). The agent executing a plan should be able to hold the whole plan and still have most of its context for the code. If a plan exceeds the cap, split it; do not trim detail to fit.
- **Each task is one test-first step.** It states the assertion the test must make, the files it may touch, the interface it must present, and the command that proves it. Tasks are small enough that "the test fails, then passes" is one sitting.
- **Zero decisions left to the implementer.** If an implementer would have to choose a signature, a schema field, an error behaviour, or a dependency, the plan is not finished. Make the choice (decide and log, or ask first) and write it down. State interfaces exactly, because the plan next to this one is being built by a different agent at the same time and they must meet.
- **File allowlist.** Each plan's front matter lists every file it may create or change. Agents may not touch anything else.
- **No scope-shrinking language.** A plan never says "simplified", "basic version", "for now", "placeholder", "stub", or "later". If the full thing does not fit in one plan, write more plans. If it should not be built at all, it belongs on the Never list, which only the PR/FAQ can extend.
- **No code in plans beyond interfaces.** Signatures, schemas, example inputs and outputs: yes. Implementations: no. Writing the code in the plan removes the test-first step and doubles the review surface.

## 6. Dependencies and waves

In each plan's front matter, set `depends_on` to the plans whose output it needs. Then assign waves:

- Wave 1 is every plan with no dependencies.
- A plan's wave is one more than the highest wave among its dependencies.
- Two plans may share a wave only if their file allowlists do not overlap. If they overlap, either move the shared file into an earlier plan that both depend on, or put one plan in a later wave.

Independence is what makes parallel work safe. If you find yourself unsure whether two plans are independent, they are not: sequence them.

## 7. Criticality

Set each plan's `criticality` as defined in SKILL.md. Be honest in both directions; marking everything high makes the build slow and expensive, and marking a migration low gets it a cursory review.

## 8. Coverage check

Before the spec goes to review, verify and record in `spec.md`:

- Every truth is covered by one or more plans, and those plans' tasks include a test at the product's outer surface for it.
- Every artifact is created by exactly one plan.
- Every connection is made by a named task.
- Nothing in any plan is on the Never list, and nothing in any plan is absent from the PR/FAQ.

A truth with no plan is a hole. A plan with no truth is scope creep. Fix both before review.

Then run the mechanical checker bundled with this skill and fix everything it reports:

```
python3 <this skill's folder>/scripts/check_spec.py docs/build/<slug>
```

It checks front matter, the size cap, scope-shrinking language, dependency order, overlapping allowlists within a wave, and that every truth is claimed by a plan. It cannot judge whether a plan is good; that is what the review is for.

## What gets written

```
docs/build/<slug>/
  spec.md                      truths, never list, artifacts, connections, phases, coverage, decision log
  state.md                     from templates/state.md
  ledger.md                    from templates/ledger.md
  phases/
    01-<phase-name>/
      01-<plan-name>.md        from templates/plan.md
      02-<plan-name>.md
    02-<phase-name>/
      ...
```

Use `templates/spec.md` for the overview. Commit the spec before review so reviewers and later agents read a fixed version.
