# Build spec: <product name>

PR/FAQ: `docs/prfaq/<slug>.md` (locked <date>, sha256 `<hash>`)

## Truths

What must be observably true for the PR/FAQ to be accurate.

| ID | Truth | Source |
|---|---|---|
| T-01 | <observable statement> | <press release paragraph or FAQ number> |

## Never

Out of scope for the first version, from the PR/FAQ. No plan may build these.

- <item>

## Artifacts

| Artifact | What it is | Truths | Created by plan |
|---|---|---|---|
| `<path or name>` | <one line> | T-01 | 01-01 |

## Connections

| ID | Connection | Truths | Made by |
|---|---|---|---|
| C-01 | <A calls / reads / writes / registers with B, with what> | T-01 | 01-02 task 2 |

## Phases

| Phase | Delivers | What the customer can do afterwards | Plans | Waves |
|---|---|---|---|---|
| 01-<name> | T-01, T-02 | <customer terms> | 4 | 2 |

## Coverage

| Truth | Plans | Outer-surface test |
|---|---|---|
| T-01 | 01-01, 01-02 | `<test path>::<name>` |

Checks: every truth has a plan and an outer-surface test; every artifact has exactly one creating plan; every connection has a task; nothing planned is on the Never list or absent from the PR/FAQ.

## Build setup

- **Dependency setup command:** `<one command that makes a fresh checkout ready to build and test>`
- **Full test suite:** `<command>`
- **Shared files and their owners:** <manifest: plan id; migrations: numbering; registries: plan id>

## Environment requirements

What the plans need from the machine they run on. Filled in at preflight.

| Requirement | Minimum | Needed by | First phase | Check |
|---|---|---|---|---|
| <runtime, tool, service, credential name> | <version> | <plan ids> | <n> | `<command>` |

## Decision log

Append-only. Decisions made without asking, most recent last.

| # | Decision | Why | Cost to reverse | Stage |
|---|---|---|---|---|
| D-01 | <what was chosen over what> | <reason> | <what would be redone> | spec |

## Questions for the user

Open "ask first" decisions and PR/FAQ deviations, with the option recommended.
