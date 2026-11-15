# Example: Draft mode, then build

**Prompt used:** "Working backwards on this: a tiny command-line tool for freelancers. I keep my invoices in a CSV (client, number, amount, due_date, paid). I want to run one command and see who owes me money and how late they are, plus a reminder I can paste into an email. Python is fine."

**Reading taken:** Draft mode; software idea, so the skill continues into Step 4.

---

# Overdue tells freelancers who owes them money in one command
*Freelancers who track invoices in a spreadsheet see every late payment, and a reminder ready to send, without opening the spreadsheet.*

**Remote - 15 February 2027** - Today we released Overdue, a free command-line tool for freelancers who keep their invoices in a CSV file. Run `overdue invoices.csv` and it lists every unpaid invoice past its due date, how many days late each one is, and the total you are owed.

Freelancers who invoice from a spreadsheet find out a payment is late when the rent is due. Checking means opening the file, sorting by date, and comparing each row with today's date by eye. Invoicing software does this automatically, but it costs a monthly fee and means moving every client record into someone else's system. Most freelancers with a handful of clients do neither, and chase late.

Overdue reads the file you already have. It shows the late invoices with the most overdue first, and the total at the bottom. Add `--remind` and it writes a short, polite reminder for each one, with the invoice number, amount, and days late filled in, ready to paste into an email.

"Getting paid should not depend on remembering to check a spreadsheet," said [project lead - illustrative]. "We did not want to build another invoicing product. We wanted the one answer a freelancer needs on a Monday morning."

To use it, export or save your invoices as a CSV with the columns `client`, `number`, `amount`, `due_date`, and `paid`, then run `overdue invoices.csv`. Nothing is uploaded; the file never leaves your computer.

"I had two invoices more than a month late and did not know," said a freelance illustrator [illustrative quote, not a real customer]. "Now I run it with my coffee on Mondays and send the reminders before I start work."

Overdue is free and open source. Install it with `pip install overdue` [name availability unchecked].

## Customer FAQ

**What does my CSV need to look like?** A header row with `client`, `number`, `amount`, `due_date` (YYYY-MM-DD), and `paid` (`yes` or `no`). Extra columns are ignored.

**What if a row is wrong?** Overdue tells you which line it could not read and why, and still reports the rest.

**Does it send the emails?** No. It writes the text; you send it.

**Does it handle several currencies?** No. It adds the amounts as written. If you invoice in more than one currency the total is not meaningful.

**What if nothing is late?** It says so, and exits without an error.

## Internal FAQ

**How big is the opportunity?** Unknown - to find out: count freelancers in [community X] who track invoices in a spreadsheet; ask ten whether they would run a command weekly.

**What does it cost to build?** A few hours for the first version. No hosting or running costs.

**What are the hardest problems?** Real-world CSVs: date formats, currency symbols in the amount column, different column names. The first version handles one format and reports the rest clearly.

**Top reasons this fails.** (1) The target customer does not use a command line. (2) People who would use it already have invoicing software. (3) The fixed CSV format is too much friction.

**What are we not doing in the first version?** Sending email; multiple currencies; date formats other than YYYY-MM-DD; column mapping; partial payments; a graphical interface.

**How will success be measured?** [X] weekly runs after three months - needs a target and a way to count that does not collect data, since the release promises nothing leaves the computer. Unknown - to find out.

## Assumptions to validate

| Assumption | Blocking? |
|---|---|
| Freelancers who track invoices in a CSV are comfortable running a command | Non-blocking for the build; decides whether to ship it publicly |
| A fixed column layout is acceptable | Non-blocking; the user who asked already has this layout |
| "Days late" counts calendar days from the due date | Non-blocking; stated in the release |

No blocking assumptions, so the build proceeds.

## Open questions

- Is a command-line tool the right form for this customer, or should it be a spreadsheet template?
- Is the package name available?

---

## Build brief

**Acceptance criteria** (one per promise in the release)

| # | Given / when / then | From |
|---|---|---|
| AC1 | Given a CSV with paid and unpaid invoices, when the customer runs `overdue file.csv`, then only unpaid invoices with a due date before today are listed | Summary |
| AC2 | Each listed invoice shows the number of days late | Summary |
| AC3 | The list is ordered most overdue first | Solution |
| AC4 | The total owed across listed invoices is shown at the bottom | Summary, solution |
| AC5 | With `--remind`, a reminder is written for each listed invoice containing the invoice number, amount, and days late | Solution |
| AC6 | Extra columns in the CSV are ignored | Customer FAQ |
| AC7 | A row that cannot be read is reported with its line number and reason, and the remaining rows are still reported | Customer FAQ |
| AC8 | When nothing is late, it says so and exits with status 0 | Customer FAQ |

**Out of scope:** sending email; multiple currencies; other date formats; column mapping; partial payments; a GUI.

**Constraints:** Python (stated). Standard library only, pytest for tests (chosen: simplest stack that meets the criteria).

**Handoff:** Superpowers skills not present in this session, so the built-in test-first loop was used.

---

## Build result

Two test-first cycles, each committed: core logic (AC1-4), then the command line (AC5-8). In each, the tests were written and seen to fail before any implementation existed. Final suite: **10 tests, all passing.**

| # | Covered by | Result |
|---|---|---|
| AC1 | `test_ac1_only_unpaid_and_past_due_are_listed` | Pass |
| AC2 | `test_ac2_days_late_is_calendar_days_since_due_date` | Pass |
| AC3 | `test_ac3_most_overdue_first` | Pass |
| AC4 | `test_ac4_total_owed_sums_listed_invoices_exactly`, `test_report_lists_late_invoices_and_total_at_bottom` | Pass |
| AC5 | `test_ac5_remind_writes_reminder_with_number_amount_and_days`, `test_no_reminders_without_flag` | Pass |
| AC6 | `test_ac6_extra_columns_ignored` | Pass |
| AC7 | `test_ac7_bad_row_reported_with_line_and_reason_and_rest_still_reported` | Pass |
| AC8 | `test_ac8_nothing_late_says_so_and_exits_zero` | Pass |

**Re-read against the press release**

- Promised but not built: the release says `pip install overdue` and `overdue invoices.csv`. What exists is `python overdue.py invoices.csv`; there is no packaging or installed command. Recommendation: fix the build (add packaging) rather than edit the release, since the one-command experience is the headline.
- The release says a day an invoice falls due is not late; the build matches (an invoice due today is not listed).
- Nothing was built that the release does not mention.
