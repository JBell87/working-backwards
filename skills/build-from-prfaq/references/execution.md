# Stage 6: Build

Begin only after approval. At the start of each phase, re-run the preflight checks for that phase's requirements (`preflight.md` section 7); a phase with an unmet requirement does not start. Work one phase at a time; within a phase, one wave at a time; within a wave, all plans in parallel.

## Set up

1. Create the branch `build/<slug>` from the current default branch. Never commit build work to the default branch.
2. Make sure `.worktrees/` is in `.gitignore`.
3. Run the project's existing test suite and record the result in the ledger as the baseline. If it already fails, tell the user before building on it.
4. Update `state.md`: stage, branch, baseline commit, isolation mode.

## One worktree per plan

Each plan in a wave runs in its own git worktree on its own branch. An agent there cannot see or disturb another plan's unfinished work, can run the whole build and test suite, and commits its own tasks. Work reaches the build branch only after it has passed review, so `build/<slug>` only ever contains reviewed, passing commits.

The unit is the plan, not the task. A plan's tasks run in order and build on each other, so they share the plan's worktree; a fresh agent takes each task in turn.

For each plan, when its wave starts:

```
git worktree add .worktrees/<plan-id> -b plan/<slug>/<plan-id> build/<slug>
```

Then prepare it before any implementer is dispatched: run the dependency setup command the spec records, in that worktree. Do these preparations one at a time, since package managers do not always tolerate running concurrently against a shared cache. Record the worktree path in `state.md`.

Things a worktree does not isolate, which the plans must handle (the spec stage requires it):

- **Services and ports.** A database or cache is shared by every worktree. Each plan's tests use their own database name, schema, or temporary instance, and an unused port. Pass the plan id to the agent as `WB_PLAN`.
- **Untracked local files.** Anything the tests need that git does not track must be created by the setup command or the tests themselves.

Do not start more plans at once than the limit recorded at preflight. If a wave is larger, run it in batches.

## Running a wave

A wave is the set of plans whose dependencies are merged and whose file allowlists do not overlap.

1. **Dispatch.** Create and prepare the worktrees, then start each plan's first task with a fresh implementer (`prompts/implementer.md`), all in one message. Choose each one's model tier as SKILL.md describes. Give it: the worktree path it must work in, the plan file path, the task number, the spec path, the summaries of the plans it depends on, the commit message to use, and an absolute report path under the main checkout, `docs/build/<slug>/reviews/<phase>/<plan>-task-<n>.md`.
2. **Within a plan, tasks run in order**, each with a new fresh agent in the same worktree. The implementer commits its task on the plan branch when its own checks pass. The next task is dispatched only after the previous one has passed review. Plans advance independently; do not hold one back for another.
3. **Review each task** as it returns, per `review.md`. Reviewers are given the worktree path and the task's commit range. Fixes are further commits on the plan branch.
4. **Merge each plan when its last task passes review.** One plan at a time, from the main checkout:

   ```
   git merge --no-ff plan/<slug>/<plan-id> -m "Merge <plan-id>: <title>"
   ```

   `--no-ff` keeps the task commits and their hashes intact under one merge commit per plan. Because allowlists in a wave do not overlap, the merge should be clean. **A conflict means the spec was wrong** about independence: do not resolve it by hand. Abort the merge, record it, and triage it as a plan gap (`review.md`).
5. **Run the full suite on `build/<slug>` after each merge.** This is the first time the plan's work meets the plans merged before it. A failure belongs to the plan just merged or to its interaction with an earlier one; triage it in `review.md`. Do not merge the next plan onto a failing branch.
6. **Clean up.** After a successful merge and suite run, write the plan's summary, remove the worktree (`git worktree remove`), and delete the plan branch. Keep the worktree of a plan that is blocked or failing until it is resolved.
7. Update `state.md` and the ledger after every merge. When every plan in the wave is merged, start the next wave; its worktrees branch from the updated `build/<slug>`.

## Shared files

Some files are touched by many plans: dependency manifests, lock files, migration sequences, route or module registries, generated code. Worktrees turn a silent overwrite of these into a merge conflict, which is better, but the right fix is in the spec (`spec.md` requires it):

- **A manifest change belongs to one plan.** The dependencies a phase needs are declared up front and added by a single plan in the phase's first wave. A later plan that discovers it needs another library reports "needs a decision"; it does not edit the manifest.
- **Lock files and other generated files are yours.** No plan lists them. After a merge that changes a manifest, regenerate them on `build/<slug>` (dispatch a Fast-tier agent), run the suite, and commit them separately.
- **Sequenced files are numbered in the spec.** Migration numbers and similar are assigned when plans are written, never chosen by an implementer.
- **Registries are wired by one plan.** Where components must be registered in a central file, a single later-wave plan does the wiring, or the design discovers components without a central list.

## If worktrees are not available

When preflight found that worktrees cannot be used, parallel plans share the build branch's working tree. That is safe only under these rules, so enforce them and record "shared tree" in `state.md`:

- **An implementer touches only files on its plan's allowlist.**
- **Implementers never run git commands that write.** You do all git operations, one at a time: after a task passes review, you stage that plan's allowlisted files and commit.
- **An implementer runs only its own task's tests**, by path. Other agents' half-written files can make anything broader fail.
- **Run the full suite when the whole wave is complete**, since nothing was verified together before then.
- In a compiled language, where one unfinished file can break every agent's build, do not run plans in parallel in a shared tree at all. Run the wave's plans one after another.

Everything else in this stage applies unchanged.

## What an implementer returns

A short status line and a report file. The status is one of:

- **Done**: the test was written first and seen to fail for the stated reason, the implementation passes it, the task's verification command passes.
- **Done with concerns**: as above, with something the reviewer should look at.
- **Blocked**: it could not finish. The report says what it tried and what it needs.
- **Needs a decision**: the plan left a choice open, or following the plan would contradict the spec.

Never accept "done" without the evidence in the report: the failing test output, the passing test output, and the verification command's output. A report without all three is not done; send it back.

## Handling what comes back

Sort every non-"done" return with the rules in SKILL.md under "Who decides what":

- **A bug or a missing piece the task cannot work without**: this is ordinary work. Let the implementer fix it within its allowlist and note it in the report. No need to ask anyone.
- **A choice the plan left open**: the spec failed the zero-decision rule. Decide and log, amend the plan, and re-dispatch. If the choice would force a rebuild, ask first.
- **A change that alters the structure the spec laid out** (a new component, a different data shape, a different interface): do not let the implementer proceed. On the Reasoning tier, decide whether the spec is wrong. If so, amend the spec and every plan it touches, note which completed work is affected, and schedule a gap plan for it.
- **Anything that would make the PR/FAQ untrue**: stop that plan and ask the user. Other independent plans continue.
- **Blocked by the work**: move up one model tier or raise effort and re-dispatch with the report so far.
- **Blocked by the environment** (a command not found, a dependency that will not install, a service that will not start): do not escalate the model. Follow `preflight.md` section 8: decide whether it is a declared project dependency, an undeclared one, something missing outside the project, or a change since preflight, and act accordingly. Nothing outside the project is installed without the user's approval.
- **Blocked on something only the user can supply** (a credential, an account, a human action): ask the user; batch such questions and keep independent plans moving.

## Git and GitHub

Git is the build's memory of what changed; the ledger is its memory of why.

- **One commit per task**, made by the implementer on the plan branch (or by you, in shared-tree mode), plus one merge commit per plan. Message format:

  ```
  <plan-id> task <n>: <what now works>

  Truths: T-03, T-07
  Plan: docs/build/<slug>/phases/01-core/02-report.md
  ```

- Record the commit hash in the ledger line for that task, and the merge commit when the plan is merged. Fix rounds get their own commits, referenced in the same way.
- Only `build/<slug>` is ever pushed. Plan branches and worktrees are local and temporary.
- Commit spec amendments, summaries, and state updates separately from code, so the code history reads cleanly.
- **If the repository has a GitHub remote and you have push access**, push `build/<slug>` at the end of each phase and open (or update) one draft pull request for the build. Put the phase table and truth status in its description and add a comment per completed phase with the phase review outcome. This gives the user a place to watch progress and read diffs. Do this only if it was listed at the approval gate.
- Never push to the default branch, never merge the pull request, and never force-push. Merging is the user's decision.
- If there is no remote or no access, skip this silently; the local branch and ledger are sufficient.

## Updating state

After every event, append a ledger line (`templates/ledger.md` has the format). After every plan completes and at every wave boundary, rewrite `state.md`. Do this before dispatching the next thing, not in batches: if the session ends mid-wave, these files are all the next session has.
