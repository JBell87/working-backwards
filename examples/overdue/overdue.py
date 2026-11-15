"""Overdue: list late invoices from a CSV."""
import argparse
import csv
import sys
from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation


@dataclass(frozen=True)
class Invoice:
    client: str
    number: str
    amount: str
    due_date: date
    paid: bool


@dataclass(frozen=True)
class Overdue:
    invoice: Invoice
    days_late: int


def find_overdue(invoices, today):
    late = [Overdue(i, (today - i.due_date).days)
            for i in invoices if not i.paid and i.due_date < today]
    return sorted(late, key=lambda o: o.days_late, reverse=True)


def total_owed(overdue):
    return sum((Decimal(o.invoice.amount) for o in overdue), Decimal("0"))

REQUIRED = ("client", "number", "amount", "due_date", "paid")


def read_invoices(path):
    """Return (invoices, problems). Problems are 'Line N: reason' strings."""
    invoices, problems = [], []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        missing = [c for c in REQUIRED if c not in (reader.fieldnames or [])]
        if missing:
            return [], [f"Line 1: missing column(s): {', '.join(missing)}"]
        for line, row in enumerate(reader, start=2):
            try:
                due = date.fromisoformat((row["due_date"] or "").strip())
            except ValueError:
                problems.append(f"Line {line}: due_date '{row['due_date']}' is not YYYY-MM-DD")
                continue
            amount = (row["amount"] or "").strip()
            try:
                Decimal(amount)
            except InvalidOperation:
                problems.append(f"Line {line}: amount '{amount}' is not a number")
                continue
            paid = (row["paid"] or "").strip().lower()
            if paid not in ("yes", "no"):
                problems.append(f"Line {line}: paid '{row['paid']}' is not yes or no")
                continue
            invoices.append(Invoice(row["client"].strip(), row["number"].strip(), amount, due, paid == "yes"))
    return invoices, problems


def days(n):
    return f"{n} day" if n == 1 else f"{n} days"


def reminder(o):
    i = o.invoice
    return (f"Hi {i.client},\n\nA quick reminder that invoice {i.number} for {i.amount} "
            f"is now {days(o.days_late)} past its due date of {i.due_date.isoformat()}. "
            f"Could you let me know when I can expect payment?\n\nThank you.")


def main(argv=None, today=None):
    parser = argparse.ArgumentParser(prog="overdue", description="List late invoices from a CSV.")
    parser.add_argument("csv_file")
    parser.add_argument("--remind", action="store_true", help="write a reminder for each late invoice")
    args = parser.parse_args(argv)

    invoices, problems = read_invoices(args.csv_file)
    late = find_overdue(invoices, today or date.today())

    for p in problems:
        print(p)
    if problems:
        print()
    if not late:
        print("Nothing is overdue.")
        return 0
    for o in late:
        i = o.invoice
        print(f"{i.number}  {i.client}  {i.amount}  {days(o.days_late)} late")
    print(f"Total owed: {total_owed(late)}")
    if args.remind:
        for o in late:
            print("\n---\n" + reminder(o))
    return 0


if __name__ == "__main__":
    sys.exit(main())
