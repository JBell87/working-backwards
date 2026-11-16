# Stage 6: Build

Begin only after approval. At the start of each phase, re-run the preflight checks for that phase's requirements (`preflight.md` section 7); a phase with an unmet requirement does not start. Work one phase at a time; within a phase, one wave at a time; within a wave, all plans in parallel.

## Set up

1. Create the branch `build/<slug>` from the current default branch. Never commit build work to the default branch.
2. Run the project's existing test suite and record the result in the ledger as the baseline. If it already fails, tell the user before building on it.
3. Update `state.md`: stage, branch, baseline commit.

## Running a wave

A wave is the set of plans whose dependencies are complete and whose file allowlists do not overlap.

1. **Dispatch.** For each plan in the wave, start its first task with a fresh implementer (`prompts/implementer.md`), all in one message. Choose each one's model tier as SKILL.md describes. Give it: the plan file path, the task number, the spec path, the summaries of the plans it depends on, and a report path `reviews/<phase>/<plan>-task-<n>.md`.
2. **Within a plan, tasks run in order**, each with a new fresh agent. The next task is dispatched only after the previous one has passed review and been committed. Plans in the wave advance independently; do not hold one plan back for another.
3. **Review each task** as it returns, per `review.md`. Reviews for different plans run in parallel too.
4. **Commit each task after it passes review** (see Git below).
5. **When every plan in the wave is complete**, run the full test suite once. Parallel plans were each verified alone; this is the first time they are verified together. A failure here is a finding against the wave: triage it in `review.md` like any other.
6. Write each finished plan's summary, update `state.md`, and start the next wave.

## Keeping parallel agents out of each other's way

Agents in the same wave share one working tree. That is safe only because of three rules, so enforce them:

- **An implementer touches only files on its plan's allowlist.** A needed change outside the allowlist is reported, not made.
- **Implementers never run git commands that write** (add, commit, stash, checkout, reset). You do all git operations, one at a time, so parallel agents cannot race on the index.
- **An implementer runs only its own task's tests**, by path. The full suite belongs to you at the end of the wave, when no other agent's half-written file can make it fail.

If the harness offers isolated worktrees per agent and the project builds cleanly in one, you may use them for a wave and merge each plan's branch as it completes. The allowlists guarantee the merges do not conflict. Use this when tasks need to run the whole build or suite to verify themselves; otherwise the shared tree is simpler.

If two plans in a wave turn out to depend on each other after all (one agent reports needing a file the other owns), stop the later one, move it to the next wave, record the correction in the ledger, and fix the spec's wave assignment.

## What an implementer returns

A short status line and a report file. The status is one of:

- **Done**: the test was written first and seen to fail for the stated reason, the implementation passes it, the task's verification command passes.
- **Done with concerns**: as above, with something the reviewer should look at.
- **Blocked**: it could not finish. The report says what it tried and what it needs.
- **Needs a decision**: the plan left a choice open, or following the plan would contradict the spec.

Never accept "done" without the evidence in the report: the failing test output, the passing test output, and the verification command's output. A report without all three is not done; send it back.

## Handling what comes back

Sort every non-"done" return with the rules in SKILL.md under "Who decides what":

- **A bug, a missing piece the task cannot work without, or a broken tool**: this is ordinary work. Let the implementer fix it within its allowlist and note it in the report. No need to ask anyone.
- **A choice the plan left open**: the spec failed the zero-decision rule. Decide and log, amend the plan, and re-dispatch. If the choice would force a rebuild, ask first.
- **A change that alters the structure the spec laid out** (a new component, a different data shape, a different interface): do not let the implementer proceed. On the Reasoning tier, decide whether the spec is wrong. If so, amend the spec and every plan it touches, note which completed work is affected, and schedule a gap plan for it.
- **Anything that would make the PR/FAQ untrue**: stop that plan and ask the user. Other independent plans continue.
- **Blocked by the work**: move up one model tier or raise effort and re-dispatch with the report so far.
- **Blocked by the environment** (a command not found, a dependency that will not install, a service that will not start): do not escalate the model. Follow `preflight.md` section 8: decide whether it is a declared project dependency, an undeclared one, something missing outside the project, or a change since preflight, and act accordingly. Nothing outside the project is installed without the user's approval.
- **Blocked on something only the user can supply** (a credential, an account, a human action): ask the user; batch such questions and keep independent plans moving.

## Git and GitHub

Git is the build's memory of what changed; the ledger is its memory of why.

- **One commit per reviewed task.** Stage only that plan's allowlisted files. Message format:

  ```
  <plan-id> task <n>: <what now works>

  Truths: T-03, T-07
  Plan: docs/build/<slug>/phases/01-core/02-report.md
  ```

- Record the commit hash in the ledger line for that task. Fix rounds get their own commits, referenced in the same way.
- Commit spec amendments, summaries, and state updates separately from code, so the code history reads cleanly.
- **If the repository has a GitHub remote and you have push access**, push `build/<slug>` at the end of each phase and open (or update) one draft pull request for the build. Put the phase table and truth status in its description and add a comment per completed phase with the phase review outcome. This gives the user a place to watch progress and read diffs. Do this only if it was listed at the approval gate.
- Never push to the default branch, never merge the pull request, and never force-push. Merging is the user's decision.
- If there is no remote or no access, skip this silently; the local branch and ledger are sufficient.

## Updating state

After every event, append a ledger line (`templates/ledger.md` has the format). After every plan completes and at every wave boundary, rewrite `state.md`. Do this before dispatching the next thing, not in batches: if the session ends mid-wave, these files are all the next session has.
