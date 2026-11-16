# Ledger: <slug>

Append-only. One line per event. Never edit earlier lines.

Format: `<timestamp> | <event> | <plan/task or scope> | <model tier and name> | <result> | <commit or -> | <note>`

Events: `preflight`, `preflight-miss`, `baseline`, `dispatch`, `return`, `review`, `triage`, `fix`, `re-review`, `commit`, `wave-suite`, `phase-review`, `gap-plan`, `escalate`, `decision`, `question`, `final`.

```
2027-01-12T10:02Z | dispatch    | 01-02 task 1 | standard (sonnet)  | -                    | -       |
2027-01-12T10:09Z | return      | 01-02 task 1 | standard (sonnet)  | done                 | -       |
2027-01-12T10:14Z | review      | 01-02 task 1 | standard x3        | 2 findings           | -       | assertions 1, scope 1
2027-01-12T10:15Z | triage      | 01-02 task 1 | reasoning (opus)   | 1 patch, 1 reject    | -       |
2027-01-12T10:21Z | fix         | 01-02 task 1 | standard (sonnet)  | round 1/5            | -       | same implementer
2027-01-12T10:24Z | re-review   | 01-02 task 1 | standard           | 1 addressed, 0 open  | -       |
2027-01-12T10:25Z | commit      | 01-02 task 1 | -                  | -                    | a1b2c3d |
```
