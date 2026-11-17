# Using the working-backwards plugin

What each part of the plugin is, and how to invoke each skill.

## How invocation works

Skills are not command-line programs, so there are no flags. Each skill is started in one of two ways, and everything else is said in words:

- **By asking.** Describe what you want ("working backwards on this idea: ..."). Claude picks the skill from its description.
- **By name.** In Claude Code, type the skill as a slash command, followed by your request in plain text:

  ```
  /working-backwards:working-backwards <your request>
  /working-backwards:build-from-prfaq <your request>
  /working-backwards:security-review <your request>
  ```

The "inputs" below are things you state in that request, or answer when asked. Each one has a default, so the shortest invocation is just the skill and the idea.

## The parts

```
working-backwards/
├── .claude-plugin/
│   ├── plugin.json              plugin name, version, description
│   └── marketplace.json         lets Claude Code install it from this repository
├── skills/
│   ├── working-backwards/       idea -> PR/FAQ
│   ├── build-from-prfaq/        PR/FAQ -> working software
│   └── security-review/         authorized security review
├── hooks/
│   ├── hooks.json               registers the hook below
│   └── resume-build.sh          points the orchestrator back to its state after compaction
├── docs/
│   ├── usage.md                 this file
│   └── dry-run-test-plan.md     staged first run
└── examples/                    sample outputs from version 0.1
```

| Part | What it is for |
|---|---|
| `working-backwards` skill | Turns an idea into a PR/FAQ (press release and FAQs), coaches you through one, or critiques one you wrote. Hands software ideas to the build. One file. |
| `build-from-prfaq` skill | The orchestrator. Locks the PR/FAQ, derives and reviews a build spec, produces five planning documents, waits for your approval, runs a parallel test-first build with reviews, and verifies the result against the PR/FAQ. |
| `build-from-prfaq/references/` | One guide per stage (spec, spec review, deliverables, preflight, execution, review), loaded only when that stage starts. |
| `build-from-prfaq/references/prompts/` | Instructions for each agent the orchestrator dispatches: the implementer, three spec reviewers, three task reviewers, the phase reviewer, the final verifier, and the re-reviewer. |
| `build-from-prfaq/references/templates/` | File formats: spec, plan, state, ledger, plan summary. |
| `build-from-prfaq/scripts/check_spec.py` | Mechanical checks on a build spec: plan size, required fields, scope-shrinking words, dependency order, overlapping files in a wave, coverage of every truth. |
| `security-review` skill | Scopes, authorizes, scans, verifies, fixes, and reports. Works after a build or on its own. |
| `security-review/references/` | Guides for authorization, resource scope and audit permissions, the scan layers, the cloud audit, and triage, fixing and risk acceptance; prompts for the scanner and verifier agents; templates for the authorization record and report. |
| `hooks/` | After the conversation is compacted or a session is resumed, reminds the orchestrator that a build is in progress and where its state file is. Does nothing when no build is running. |

## `working-backwards`

Turns an idea into a PR/FAQ.

**Required:** the idea. For a critique, the existing PR/FAQ as text or a file path.

| Input | How to say it | Default |
|---|---|---|
| Mode | "draft", "coach me through", "critique" or "review" | Inferred from the request |
| Stop at the document | "document only" | Hands off to the build when the idea is software |
| Six-page narrative | "with a six-pager" | Not written |
| File format | "as a Word file", "as markdown" | The session's document format |
| Facts | State what is already decided: platform, language, data, constraints | Guesses are listed as assumptions |

**Examples**

```
/working-backwards:working-backwards Linkshelf: a self-hosted bookmark service for one
person. Python 3.12, standard library plus SQLite, no accounts. ...

Coach me through a PR/FAQ for a meal-planning app. Document only.

Critique docs/prfaq/linkshelf.md before I send it to my director.
```

**What you get:** `docs/prfaq/<slug>.md` containing the press release, customer FAQ, internal FAQ, assumptions (each marked blocking or not), and open questions.

**When it stops to ask:** if it had to guess something that decides what gets built, it asks before handing off.

## `build-from-prfaq`

Turns a PR/FAQ into working software. Needs Claude Code for subagents and model selection.

**Required:** a PR/FAQ. If there is exactly one in `docs/prfaq/`, it is used; otherwise give the path.

| Input | How to say it | Default |
|---|---|---|
| PR/FAQ | A path | The one file in `docs/prfaq/` |
| Plan without building | "plan only" | Asks for approval, then builds |
| Partial build | "phase 1 only", "stop after phase 2" | All phases |
| Resume | "resume the build" | Automatic when a build's state file exists |
| Status | "build status" | - |
| Git | "no pull request" | Draft pull request when a GitHub remote exists |
| Security review | "skip the security review" | Runs after final verification |
| Constraints | Language, framework, platform, hosting | Decided and logged |

**Examples**

```
/working-backwards:build-from-prfaq docs/prfaq/linkshelf.md, plan only

Approved. Build phase 1 only, then stop.

Resume the build.

Build status.
```

**Where it waits for you**

1. **Plan approval**, always, after the five planning documents exist and the preflight has checked the environment. The same approval covers the preflight's list of proposed installs, which Claude then installs itself.
2. **Security review authorization**, after the build.
3. During the build, only for something that would make the PR/FAQ untrue, a newly discovered choice that would force a rebuild if wrong, or something only you can supply.

**What you get:** in `docs/build/<slug>/`: the spec, `preflight.md`, `architecture.md`, `schema.md`, `api.md`, `phases.md`, `explained-simply.md`, the plan files and their summaries, reviewer reports, `state.md`, `ledger.md`, and the final `report.md`. In git: a `build/<slug>` branch with one commit per task and one merge per plan. Each plan is built in a temporary worktree under `.worktrees/` and merged after review.

## `security-review`

Runs an authorized security review of software and cloud resources you own.

**Required:** what to review. After a build that is the build itself. Run directly, name the repository and the specific cloud resources.

| Input | How to say it | Default |
|---|---|---|
| What to review | A build slug; or resource identifiers, a resource group, a project, a tag, a stack, hostnames | After a build: its own resources. Direct: asked. |
| Platform | "AWS", "Azure", "Google Cloud", "DigitalOcean" | Read from the infrastructure code |
| Permissions form | "as commands" or "as files" | Asked |
| Permissions breadth | "standard" or "strict" | Recommended, then asked |
| Intensity | "passive", "standard", "thorough", per environment | Standard on production, thorough on staging |
| Account-wide checks | "include account-level checks" | Off |
| Repository only | "static only" | Off |
| No fixes | "report only" | Fixes critical and high findings |
| Scan window | "authorization valid until <date>" | Seven days |

**Examples**

```
/working-backwards:security-review the linkshelf build. AWS. Permissions as commands,
standard. Standard intensity on production.

/working-backwards:security-review this repository, static only, report only.

Run a security review of resource group rg-shop-prod in Azure subscription <id> and
https://shop.example.com. Permissions as files, strict.
```

**What happens before anything is scanned**

1. It lists the exact resources in scope (`scope.md`) for you to check.
2. It gives you the read-only permissions for a dedicated audit identity, as commands or files, with removal steps. You create the identity.
3. It writes the authorization record and asks you to confirm it.

**What you get:** in `docs/security/<slug>/`: `scope.md`, `authorization.md`, `permissions/` (if you chose files), `findings.md`, `risk-acceptance.md`, and `report.md`.

**What it will not do:** denial-of-service or load testing, password guessing or cracking, exploiting a finding, changing live infrastructure, creating identities for you, or evaluating anything outside the scope you confirmed.

**Prerequisites:** the scanners, or Docker to run their official images: Semgrep, TruffleHog, Trivy or OSV-Scanner, Checkov, Prowler, Nmap, testssl.sh, OWASP ZAP, Nuclei. Anything missing is reported as a gap in coverage.

## Running the whole flow

```
/working-backwards:working-backwards <idea, with the facts you have already decided>
```

That one request runs the PR/FAQ, hands off to the build, stops for plan approval, builds, stops for security authorization, and ends with the final report. Each skill can also be started on its own at its stage.
