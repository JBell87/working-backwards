# Stage 7: Review, verify, and close gaps

Two different questions get asked at every level, and they have different answers more often than you would expect:

- **Is the task done?** The code the plan asked for exists and its tests pass.
- **Is the goal achieved?** The truth the task was written to deliver now holds, in the running system, connected to everything it needs.

A task can be done and its goal unmet: the function exists but nothing calls it; the endpoint returns a hard-coded value; the test passes because it asserts nothing. Reviews here are built to find that difference.

## Level 1: after every task

Reviewers judge the work against **the assertions the task was supposed to establish and how it fits the rest of the system**, not against whether the code looks reasonable.

Dispatch the reviewers in one message, each fresh, each given the plan file, the task number, the spec path, the implementer's report, and the path to a diff file you wrote (`git diff` of the task's changes, saved under `reviews/`). They do not see each other's reports.

| Lens | Asks | Prompt |
|---|---|---|
| **Assertions** | Does each test assert what the task required, would it fail if the behaviour were wrong, and did it fail before and pass after? | `prompts/review-assertions.md` |
| **Integration** | Does this code meet the interfaces the spec states, and is it connected to what the spec says it connects to? Will the plans built alongside it be able to use it as written? | `prompts/review-integration.md` |
| **Scope** | Is everything the task promised really there (no stubs, placeholders, hard-coded results, or quietly narrowed behaviour), and is anything there that was not asked for or outside the allowlist? | `prompts/review-scope.md` |

How many reviewers, and on which tier, follows the plan's criticality:

- **Low**: one reviewer covering all three lenses (give it all three prompt files), Fast or Standard tier.
- **Normal**: three reviewers, Standard tier.
- **High**: three reviewers, Reasoning tier.

Never review on a lower tier than the one that implemented the task.

## Level 2: at the end of every phase

After the phase's last wave passes its full-suite run, dispatch one **phase reviewer** (`prompts/review-phase.md`, Reasoning tier), given the spec, the phase's plan files and summaries, and a diff of the whole phase against the commit the phase started from.

It performs goal-backward verification for each truth the phase claims to deliver. For each truth, four checks, in order, stopping at the first failure:

1. **Exists**: the artifacts the spec lists for this truth are present.
2. **Substantive**: each is a real implementation, not a stub, a placeholder, or a constant standing in for logic.
3. **Connected**: each connection the spec lists is made in the code: the call, the registration, the read, the write.
4. **Exercised**: a test at the product's outer surface drives the behaviour end to end and asserts the truth as the customer would see it. Then run it.

It also reviews the branch as a whole for what no task reviewer could see: plans that each work but disagree with each other, duplicated logic, an interface used differently from how it was specified.

A phase is complete only when every truth it claims passes all four checks. Record the result per truth in `reviews/<phase>/phase-review.md` and in `state.md`.

## Level 3: at the end of the project

Dispatch the **final verifier** (`prompts/review-final.md`, Reasoning tier) with only the locked PR/FAQ, the spec, and the repository. Not the summaries, not the ledger: it should reach its own conclusion.

It:

1. Repeats the four checks for **every** truth, on the finished system, running the product itself where it can.
2. Re-reads the press release and both FAQs sentence by sentence as the customer would, and marks each claim as true of the built product, false, or not verifiable, with the evidence.
3. Checks the Never list: nothing excluded was built.
4. Checks the five deliverable documents still describe what was built.

## Triage

Reviewers report findings; they do not grade them, because they lack the context. You triage, on the Reasoning tier. First verify the finding is real by looking at the code it cites. Then route it to exactly one of:

| Route | When | What happens |
|---|---|---|
| **Patch** | Real, caused by this work, and the fix is small and within the plan as written | Enters the fix loop |
| **Plan gap** | Real, and the plan was wrong or incomplete: followed correctly, it produces this problem | Amend the plan or write a gap plan; affected code is redone from the amended plan |
| **PR/FAQ deviation** | Fixing it, or leaving it, would make a PR/FAQ sentence untrue, or the PR/FAQ does not settle what the right behaviour is | Stop that plan and ask the user |
| **Defer** | Real but not caused by this work (it was already there) | Record in `state.md` under deferred; report at the end |
| **Reject** | Not real | Record the evidence that refutes it |

When unsure between patch and plan gap, choose plan gap. A fix made to the plan produces coherent code; a patch on a wrong plan produces a second problem.

**Shrinking scope is never a route.** "Remove the failing behaviour", "make the test less strict", "mark it as a known limitation", and "implement a simpler version" are not fixes. If a truth cannot be delivered as written, that is a PR/FAQ deviation and the user decides.

## Gap plans

For a plan gap, or for any phase- or final-review finding that is more than a patch, write a gap plan: an ordinary plan file (`templates/plan.md`) named `<nn>-gap-<what>.md` in the phase folder, whose tasks' assertions are the findings turned into tests that currently fail. Give it an allowlist, dependencies, and criticality like any plan, add it to the next wave it can run in, and build and review it the same way. Record it in `spec.md`'s coverage section so the truth it serves stays traceable.

Gap plans keep fixes inside the same discipline as the original work: test first, reviewed, committed, recorded.

## The fix loop

For findings routed to patch:

- **Rounds 1 to 3: the same implementer.** Resume the agent that did the task if the harness allows sending it another message; its context still holds the task and its own choices. Otherwise dispatch a fresh one on the same tier with the plan, its original report, and the findings. Send the findings verbatim.
- **Rounds 4 and 5: a fresh agent, one tier up or at higher effort**, told that earlier attempts failed and given the report file showing what was tried. Three failed rounds usually mean the implementer cannot see its own mistake.
- **Every round**: the implementer fixes, re-runs the tests covering the change, and appends to its report. Then a fresh re-reviewer (`prompts/re-review.md`) checks each open finding as addressed or not, and looks for new breakage in the fix only. New problems elsewhere go to triage, not into this loop.
- **You never fix anything yourself**, however small.
- **After round 5**, stop. If what remains open means a truth is not met, it is a PR/FAQ deviation: ask the user, with what was tried. If it does not affect any truth, record it as deferred with the evidence and continue.

Append a ledger line per round: round number, findings addressed and open, model used, commit.

## Stage 8: The final report

Write `docs/build/<slug>/report.md` and present its summary to the user:

- **Truth table**: every truth, its source sentence in the PR/FAQ, the test that proves it, and the final verifier's result.
- **The PR/FAQ re-read**: any sentence that is not true of the built product, quoted, with what the product does instead.
- **Not delivered**: anything promised and not built, and why.
- **Decisions made on the user's behalf**: the decision log, most consequential first.
- **Deferred findings**.
- **Numbers**: phases, plans, tasks, fix rounds, gap plans, and how often each model tier was used and escalated.

State plainly whether the PR/FAQ is now accurate. If it is not, say which sentences, and offer the two honest options: build the gap, or ask the user to change the PR/FAQ.
