# working-backwards

A Claude Code plugin for the Working Backwards method: write the press release and FAQ for a product before building it, then build software until every sentence of that document is true.

It has three skills:

- **`working-backwards`** turns an idea into a PR/FAQ.
- **`build-from-prfaq`** turns the PR/FAQ into working software, by orchestrating a reviewed build spec and a parallel, test-first, multi-agent build.
- **`security-review`** runs an authorized security review of what was built and where it is deployed. It also works on its own, on any project you own.

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
         └─ preflight: can this environment actually run the plan?
         └─ YOU APPROVE THE BUILD PLAN (and any installs it needs)
         └─ build: dependency waves in parallel, a fresh agent per task
             └─ after each task: reviewers with different lenses, in parallel
             └─ after each phase: whole-branch, goal-backward verification
             └─ gaps: gap plans and a fix loop that escalates models
         └─ final verification against the PR/FAQ, sentence by sentence
         └─ YOU AUTHORIZE THE SECURITY REVIEW                security-review
             └─ scans: code, secrets, dependencies, infrastructure code,
                cloud configuration, network exposure, running application
             └─ findings verified, fixed, re-scanned
             └─ you accept or reject any serious risk left open
         └─ final report
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

**Checks the environment before asking you.** A preflight derives what the plan needs (runtimes, tools, services, network, credentials), checks each one, and runs a small end-to-end smoke test. Anything missing is listed with its install command; nothing outside the project is installed without your approval.

**Asks you once.** You approve the build plan, with five documents to judge it by. After that it comes back to you only if something would make the PR/FAQ untrue, a newly discovered choice would force a rebuild if wrong, or it needs something only you can supply.

**Builds in parallel.** Plans that do not depend on each other and do not share files run at the same time, each task with a fresh agent.

**Treats "task done" and "goal achieved" as different things.** Reviewers check that tests assert what they should, that code is connected to the rest of the system, and that nothing was stubbed or quietly narrowed. Phase and final reviews verify each promise in four steps: it exists, it is real, it is connected, it is exercised from the outside.

**Chooses the model for each job.** The strongest model designs, critiques, and triages; implementation uses the model the task warrants; reviews scale with how critical the plan is. Failures escalate: the same implementer for three fix rounds, then a stronger model or higher effort.

**Keeps state on disk.** A state file, an append-only ledger, a summary per plan, and one commit per reviewed task, so a build can stop and resume. With a GitHub remote it keeps a draft pull request up to date; it never merges or pushes to the default branch.

**Survives a full context window.** State is written to disk before every next action, the orchestrator reads status lines instead of reports, and a hook points it back at its state file after the conversation is compacted or resumed.

### How decisions are made

| Kind of decision | What happens |
|---|---|
| Technical choice that can be corrected later | Decided and logged, without asking |
| Choice where a wrong pick would force a rebuild | You are asked first |
| Anything that would make the PR/FAQ untrue | Always comes to you |

### Requirements

The build is designed for Claude Code, where it can start subagents and choose their models. Without subagents it tells you what is lost (fresh-context review and parallel work) and asks before continuing with inline review.

## What `security-review` does

It orchestrates established open-source scanners; it does not contain attack techniques of its own.

| Layer | Looks for | Scanner |
|---|---|---|
| Code | Injection, broken authorization, unsafe patterns | Semgrep |
| Secrets | Stored passwords and keys, including in git history | TruffleHog |
| Dependencies and images | Known-vulnerable packages | Trivy or OSV-Scanner |
| Infrastructure code | Public storage, missing encryption, open firewalls, before deployment | Checkov or Trivy |
| Live cloud configuration | The same, on what is deployed: AWS, Azure, Google Cloud | Prowler, read-only |
| Network exposure | Unintended open services, clear-text protocols, weak TLS | Nmap, testssl.sh |
| Running application | Missing protections, leaked information, and (optionally) injection and access-control flaws | OWASP ZAP, Nuclei |

DigitalOcean and other providers Prowler does not cover are audited from infrastructure code plus a manual read-only checklist, and reported as partial coverage.

**It evaluates only what you put in scope**: after a build, that build's own resources; run directly, the resources you name. The rest of the account is left alone.

**It writes the read-only permissions for you.** Tell it your platform and whether you want commands to run or files with instructions, and it produces the policy and setup steps for a dedicated audit identity, plus the steps to remove it afterwards. You create the identity; it never does.

**Nothing runs without your written authorization**, which names each target, the intensity for each environment, and an expiry. Live targets are checked against your cloud account before any traffic is sent.

**What it will not do, whatever it is asked:** denial-of-service or load testing, password guessing or cracking, exploiting a finding or extracting data, changing live infrastructure, or scanning anything you have not authorized. Resilience to overload is assessed from configuration.

**Findings are verified before they are reported**, then rated for this system. Critical and high findings are fixed where possible and re-scanned. Anything serious that cannot be fixed does not block the build, but you are asked to accept each risk explicitly, and that is recorded. Nothing is accepted on your behalf.

You need the scanners installed, or Docker to run their official images. A scanner that is missing is reported as a gap, never as a pass. This is automated scanning, not a professional penetration test.

## Install

In Claude Code:

```
/plugin marketplace add JBell87/working-backwards
/plugin install working-backwards@working-backwards
```

To use only the PR/FAQ skill elsewhere, copy `skills/working-backwards/` into your skills folder or upload it as a skill in the Claude apps. It will stop after delivering the PR/FAQ.

## Use

Full reference, with every input each skill accepts: [`docs/usage.md`](docs/usage.md).

- "Working backwards on this idea: ..."
- "Coach me through a PR/FAQ for ..."
- "Review my PR/FAQ before I send it"
- "Build this PR/FAQ" or "Resume the build"
- "Run a security review of this project"

## What a build writes

```
docs/prfaq/<slug>.md              the PR/FAQ, locked
docs/build/<slug>/
  spec.md                         truths, artifacts, connections, phases, decision log
  architecture.md  schema.md  api.md  phases.md  explained-simply.md
  phases/01-<name>/01-<plan>.md   plan files, with summaries as they complete
  reviews/                        reviewer reports
  preflight.md                    what the plan needs from the machine, and whether it is there
  state.md  ledger.md             where the build is, and what happened
  report.md                       final verification against the PR/FAQ
docs/security/<slug>/
  authorization.md                what you authorized, and when
  findings.md  risk-acceptance.md  report.md
```

## Examples

- [`examples/critique.md`](examples/critique.md): a review of a deliberately weak PR/FAQ.
- [`examples/draft-and-build.md`](examples/draft-and-build.md): a PR/FAQ for a small command-line tool, built with the simple single-agent loop from version 0.1. The code is in [`examples/overdue/`](examples/overdue/). It predates `build-from-prfaq`.

## Testing it

[`docs/dry-run-test-plan.md`](docs/dry-run-test-plan.md) is a staged first run: a dry run to the approval gate, a one-phase build, then fault injection.

## Status

Version 0.4. `build-from-prfaq` and `security-review` are new and **have not yet been run end to end**. Draft and critique modes have been exercised on the examples above; coach mode and the six-page narrative have not.

## Licence and credits

MIT. Based on the Working Backwards process described in Colin Bryar and Bill Carr's book *Working Backwards*. Not affiliated with or endorsed by Amazon.

The build process draws on ideas from [Superpowers](https://github.com/obra/superpowers) (Jesse Vincent, MIT), [Get Shit Done](https://github.com/gsd-build/get-shit-done) (Lex Christopherson, MIT), the [BMAD Method](https://github.com/bmad-code-org/BMAD-METHOD) (BMad Code, LLC, MIT), and the [Elephant-Goldfish Model](https://github.com/google/elephant-goldfish-model) (Google LLC, Apache-2.0). It is written independently, contains no text or code from them, and is not affiliated with or endorsed by any of them.

The security review runs independent open-source scanners, each under its own licence: Semgrep, TruffleHog, Trivy, OSV-Scanner, Checkov, Prowler, Nmap, testssl.sh, OWASP ZAP, and Nuclei. This plugin does not bundle them and is not affiliated with or endorsed by their authors.
