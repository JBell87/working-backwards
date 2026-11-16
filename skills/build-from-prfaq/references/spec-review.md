# Stage 3: Review the spec with fresh eyes

You wrote the spec, so you cannot review it: you will read what you meant, not what is written. Reviewers at this stage have no conversation history. They get file paths and nothing else.

## Three passes, in order

Each pass asks a different question, and a later pass is wasted on a spec that fails an earlier one.

| Pass | Question | Prompt | Tier |
|---|---|---|---|
| 1. Comprehension | Can someone who was not there follow this? | `prompts/spec-comprehension.md` | Standard |
| 2. Design critique | Is this the right design for these truths? | `prompts/spec-design.md` | Reasoning |
| 3. Implementation readiness | Could an implementer build each plan with no decisions left? | `prompts/spec-readiness.md` | Standard; Reasoning for high-criticality plans |

**What each reviewer is given:** the locked PR/FAQ, `spec.md`, the plan files in its scope, and a path to write its report under `docs/build/<slug>/reviews/spec/`. Never your reasoning, the conversation, or another reviewer's report.

**Splitting the work:** passes 1 and 2 read the whole spec. Pass 3 is per phase: dispatch one readiness reviewer per phase, all in the same message, so no reviewer has to hold every plan.

## Resolving findings

Reviewers report findings with a severity (blocker, major, minor) and a location. You resolve them, on the Reasoning tier. Give each finding exactly one response:

- **Fix.** The finding is right. Change the spec or plan.
- **Contest.** The finding is wrong, and you can cite evidence the reviewer could have read: a line of the PR/FAQ, a decision-log entry, a file in the repository. "That was intentional" is not evidence.
- **Escalate.** Settling it needs something only the user knows, or it is an "ask first" decision or a PR/FAQ deviation. Hold it for the approval gate, or ask now if later work depends on it.
- **Decline.** Minor only. Record it and move on.

Constraints on you as resolver:

- You may not change a finding's severity. If you think a blocker is minor, contest it and say why.
- You may not contest a comprehension finding. If a fresh reader could not follow it, it is not written clearly enough; the implementers will be fresh readers too.
- Do not pad the spec with explanation only to satisfy a reviewer. Fix what a real implementer would trip on.
- A wish to contest is not evidence the reviewer is wrong.

Record every finding and response in `reviews/spec/resolution.md`. Contested and declined findings are **settled**: if a later reviewer raises the same issue at the same location, do not reopen it. Fixed findings are not settled: if the issue comes back, the fix failed.

## When the review is finished

- A **round** is one pass by fresh reviewers followed by your resolution. A round is **clean** if no unsettled blocker or major finding was raised.
- Re-run a pass with new fresh reviewers after fixing its findings, until it has a clean round. Then go to the next pass.
- After pass 3 is clean, run one **confirmation round**: all three reviewers in parallel, fresh, on the final spec. Fixes made for one pass can break another, and a second fresh reader often finds a different gap in the same text.
- **Cap: five rounds in total per pass.** If a pass has not converged, stop looping. List the open findings by severity and carry them to the approval gate for the user to accept or redirect.
- **Churn:** if a new finding sits on text you changed to fix an earlier one, and undoing that fix would resolve it, the two reviewers disagree. Do not oscillate; decide between them on the merits (decide and log) or escalate.
- A reviewer that fails, times out, or returns nothing **did not review**. Retry once. If it fails again, record it as not run. Never count it as a reviewer with no findings, and a round with a not-run reviewer is not clean.

## Without subagents

Follow "Fresh agents, and what to do without them" in SKILL.md: tell the user the review will be inline and what that loses, and get agreement first. Then run each pass as a separate step in which you re-read only the files that pass's reviewer would receive, write the report file before resolving anything, and record "inline review" in the ledger. Expect this to find less; say so at the approval gate.
