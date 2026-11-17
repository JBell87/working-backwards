# Stage 5, first half: Preflight

Before asking the user to approve the plan, prove that this environment can carry it out. A plan that is correct but cannot run here wastes the approval and fails halfway through a wave, when it is most expensive to recover.

Preflight answers one question: **can every task in this plan be executed and verified on this machine, as it is now?**

## 1. Derive what the plan needs

Read `spec.md` and the plan files (send a Fast-tier agent to gather this if there are many) and list every requirement. Do not work from a generic checklist; a requirement belongs on the list only if a plan depends on it.

| Kind | Examples |
|---|---|
| **Runtimes and versions** | The language and the minimum version the plans assume |
| **Package manager and registry** | The tool that installs project dependencies, and whether it can reach its registry from here |
| **Build and test tools** | Compiler, bundler, the test runner named in the tasks' "Proves it" commands |
| **Services** | Database, cache, queue, anything a test or the product connects to, and whether it can be started here |
| **Containers** | A working container runtime, if any plan builds or runs an image |
| **Command-line tools** | Anything a task's verification command calls |
| **Network** | Hosts the build or tests must reach, and ports the product must be able to listen on |
| **Credentials and accounts** | Anything a task needs to authenticate to. Record the name only, never a value. |
| **Capacity** | Disk and memory, if the plan needs a meaningful amount |

Add what the orchestration itself needs:

- git, a clean working tree, and the ability to create and commit to a branch
- Python 3, for the spec checker
- a subagent tool, and whether it can select a model (decides fresh-context review, parallel waves, and model routing)
- push access and a way to open a pull request, only if the git plan includes one

Record the list in `spec.md` under "Environment requirements": the requirement, the minimum version if any, the plans that need it, the first phase that needs it, and the command that checks it.

## 2. Check each one

Run the check command for each requirement and record what you find. Four outcomes:

- **Present**: there, and at a version the plan can use.
- **Wrong version**: there, but older than the plan assumes.
- **Missing**.
- **Not verifiable**: cannot be checked from here (a credential you cannot test without using it, a host the sandbox may block). Say why.

For a service, checking means starting it and connecting, not finding its binary. For a registry, it means resolving one package, not pinging the host.

## 3. Prove the chain end to end

Version checks pass on machines that still cannot build. So run one smoke test of the whole toolchain the plan uses, in a temporary directory outside the repository:

1. Create the smallest possible project in the planned stack.
2. Install one dependency through the planned package manager.
3. Write one test with the planned test runner, see it fail, make it pass.
4. If the plan uses a service or a container, start it and have the test touch it.

Delete the directory afterwards. If the smoke test fails where the version checks passed, the failure is the finding: record exactly what broke.

**Also test isolation.** Parallel plans each work in their own git worktree (`execution.md`). Check that this works here and what it costs:

1. Create a worktree of the repository in `.worktrees/preflight/`, run the project's dependency setup command in it (the one the spec records), and run the existing tests there.
2. Note how long setup took and how much disk it used, then remove the worktree.
3. From disk free and setup size, work out how many plans can run at once, and record that limit.

If worktrees cannot be used (git refuses, the project cannot build from a second checkout, or there is not room for two), record why. The build then falls back to the shared-tree rules in `execution.md`, and you say so at the approval gate.

Skip a step only when the plan does not use that part. Keep it small; this is minutes, not a second build.

## 4. Resolve what is missing

Sort each problem by who can fix it and how.

**Project dependencies** (libraries the product itself uses, installed by its package manager into the project and declared in a plan) are not preflight problems. They are installed during the build. Preflight only needs the registry to be reachable.

**Anything installed outside the project** (a runtime, a system package, a global tool, a service, a container image) **you install yourself, after the user has approved the list.** The user should not have to run commands.

1. Build the list of proposed installs: what, which plans need it, and how it will be installed (the package manager and package, not a command for them to run).
2. Present the list at the approval gate. Do not install anything from it before it is approved. The user may approve all of it, strike items, or decline.
3. Once approved, install the approved items yourself, one at a time. Never run two installs at once, and never let implementers install in parallel: concurrent package managers corrupt each other.
4. Re-run each item's check and then the smoke test. Record what was installed, the version, and the result in `preflight.md` and the ledger.
5. If an install fails, say what failed and offer the options under "cannot be installed here". Do not try a different source or method the user has not seen.

**Some changes need their own explicit yes, even inside an approved list.** Flag these separately and ask about each one by name:

- removing, replacing, or downgrading something already on the machine
- anything that costs money or needs a licence or an account
- anything beyond adding packages: system configuration, firewall rules, exposing a service to the network
- swapping out something the user stated as a fixed requirement

**Things that cannot be installed here** (no permission, no network path, an unsupported platform). Offer the realistic options:

- The user installs it or moves the build to an environment that has it.
- The plan changes to something this environment does have. Nothing is built yet, so this is cheap: amend the spec and the affected plans, log the decision, and re-run the readiness review for the plans that changed. If the missing thing was a fact the user stated ("it must be Postgres"), do not swap it; ask.

**Credentials, accounts, and access** only the user can supply. List them by name with what each is for and when it is first needed.

**Not verifiable** items are reported as risks with the phase where they will first matter.

Never work around a missing requirement by weakening the plan: replacing a real service with a fake in tests the plan says must use the real one, dropping a verification command, or marking a task as unverifiable. That is shrinking scope by another route.

## 5. Write the result

Save `docs/build/<slug>/preflight.md` from `templates/preflight.md`: every requirement with its outcome and evidence, the smoke test result, the isolation mode and how many plans can run at once, the proposed installs awaiting approval, what only the user can supply, and what is unverifiable. Record the date and the machine (operating system, architecture), because the result is only true of this machine.

## 6. The gate

Carry the result into the approval summary (SKILL.md, Stage 5).

- **Phase 1 must be fully runnable.** The build cannot start with a missing or wrong-version requirement that any phase 1 plan needs. After approval, install the approved items and confirm phase 1's requirements are met before dispatching anything. If the user declined an install phase 1 needs, the item must be supplied by them or the plan changed.
- **Later phases may wait, if the user agrees.** A requirement first needed in a later phase can be left open with the user's explicit agreement. Record it in `state.md` as an open requirement with the phase it blocks. That phase does not start until it is met.
- If nothing is missing, say so in one line and move on. Do not make a ceremony of a clean result.

## 7. Preflight is not a one-time check

Environments change, and a resumed build may be on a different machine.

- **At the start of every phase**, re-run the checks for that phase's requirements. This takes seconds.
- **On resume in a new session**, compare the machine with the one recorded in `preflight.md`. If it differs, re-run the whole preflight before dispatching anything.
- **When the spec changes** (a gap plan or an amended plan introduces a new tool, service, or version), add the requirement and check it before that plan is dispatched.

## 8. When something is missing mid-build anyway

Preflight reduces this; it does not eliminate it. When an implementer reports it is blocked by the environment (a command not found, a service that will not start, a registry that cannot be reached):

1. **Do not escalate to a stronger model.** A better model cannot install a missing compiler. Check the report against `preflight.md` first.
2. Work out which it is:
   - *A project dependency declared in the plan failed to install*: an ordinary problem. Re-dispatch once; if it fails again, check the registry and report what is unreachable.
   - *A project dependency the plan did not declare*: the plan left a decision open. Decide and log (or ask first, if it is a framework-sized choice), amend the plan, re-dispatch.
   - *Something outside the project is missing*: a preflight miss. Add it to the requirements, pause that plan, and ask the user to approve the install (one short question naming what and why). Once approved, install it yourself, re-check, and resume the plan. Do not let the implementer install it.
   - *The environment changed* (it was present at preflight): re-run preflight for that requirement and tell the user what changed.
3. Keep every plan that does not need the missing thing moving.
4. Record the miss in the ledger as `preflight-miss`, with what the derivation in step 1 overlooked, so the pattern is visible.

Implementers never install anything outside the project, never change machine configuration, and never substitute a different tool for the one the plan names.
