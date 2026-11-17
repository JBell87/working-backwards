---
id: 01-02
title: <what works when this plan is done>
phase: 01-<name>
wave: 1
depends_on: []            # plan ids whose output this plan needs
criticality: normal       # low | normal | high
truths: [T-01]
connections: [C-01]
files:                    # allowlist: every file this plan may create or change
  - <path>
  - <test path>
status: planned           # planned | in-progress | in-review | merged | blocked
---

<!-- Cap: about 2,000 tokens for the whole file. Split the plan if it is larger. Remove these comments. -->

## Goal

<One or two sentences: the behaviour that exists when this plan is done, and which truth it serves.>

## Interfaces

<!-- Exact. Other plans are built against this at the same time. -->

**Provides**

```
<signature, endpoint, command, or schema, with types and error behaviour>
```

**Uses**

- `<name>` from plan <id>: <exactly how it is called>

## Tasks

<!-- Two to five. Each is one test-first step. No implementation code. -->

### Task 1: <what works after this task>

- **Files:** <subset of the allowlist>
- **Test asserts:** <the specific observable assertion, with example input and expected output>
- **Fails first because:** <what is missing>
- **Build:** <what to implement, precisely enough that no choice is left>
- **Proves it:** `<command>` -> <expected result>

### Task 2: <...>

## Edge cases

| Case | Input or state | Expected behaviour |
|---|---|---|
| <name> | <...> | <...> |

## Not in this plan

<Anything a reader might expect here that belongs to another plan or the Never list.>
