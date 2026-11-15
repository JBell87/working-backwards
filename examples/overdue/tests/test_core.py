from datetime import date
from overdue import Invoice, find_overdue, total_owed

TODAY = date(2027, 2, 15)

def inv(number, due, paid=False, amount="100.00", client="Acme"):
    return Invoice(client=client, number=number, amount=amount, due_date=date.fromisoformat(due), paid=paid)

def test_ac1_only_unpaid_and_past_due_are_listed():
    invoices = [inv("A", "2027-02-01"), inv("B", "2027-02-01", paid=True),
                inv("C", "2027-03-01"), inv("D", "2027-02-15")]
    assert [o.invoice.number for o in find_overdue(invoices, TODAY)] == ["A"]

def test_ac2_days_late_is_calendar_days_since_due_date():
    (o,) = find_overdue([inv("A", "2027-02-01")], TODAY)
    assert o.days_late == 14

def test_ac3_most_overdue_first():
    invoices = [inv("A", "2027-02-10"), inv("B", "2027-01-01"), inv("C", "2027-02-01")]
    assert [o.invoice.number for o in find_overdue(invoices, TODAY)] == ["B", "C", "A"]

def test_ac4_total_owed_sums_listed_invoices_exactly():
    invoices = [inv("A", "2027-02-01", amount="0.10"), inv("B", "2027-02-01", amount="0.20"),
                inv("C", "2027-03-01", amount="999")]
    assert str(total_owed(find_overdue(invoices, TODAY))) == "0.30"
