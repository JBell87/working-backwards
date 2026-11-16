# Preflight: <slug>

Checked: <date and time>. Machine: <operating system and version>, <architecture>, <where it runs: local, cloud session, instance>.

**Result:** <ready | ready after approved installs | not ready: see below>

## Requirements

| Requirement | Minimum | Needed by | First phase | Check | Outcome | Evidence |
|---|---|---|---|---|---|---|
| <Python> | <3.12> | <01-01, 01-02> | 1 | `python3 --version` | present / wrong version / missing / not verifiable | <output> |

## Orchestration

| Capability | Outcome | Effect if missing |
|---|---|---|
| git, clean tree, can branch and commit | | build cannot start |
| Python 3 for the spec checker | | spec checked by hand |
| Subagents | | inline review and one task at a time, with the user's agreement |
| Model selection per agent | | everything runs on the session's model |
| Push and pull request | | local branch only |

## Smoke test

<What was created, installed, and run in the temporary directory, and the result. If it failed: the exact command and error.>

## Needs your approval to install

| What | Why (plans) | Command | Approved? | Installed and re-checked? |
|---|---|---|---|---|

## Only you can supply

| What | For | First needed |
|---|---|---|

## Not verifiable from here

| What | Why not | When it will first matter |
|---|---|---|

## Open requirements carried into the build

<Requirements for later phases left open with the user's agreement, and the phase each blocks.>
