from datetime import date
from overdue import main

TODAY = date(2027, 2, 15)
HEADER = "client,number,amount,due_date,paid\n"

def run(tmp_path, capsys, body, *flags, header=HEADER):
    f = tmp_path / "inv.csv"
    f.write_text(header + body)
    code = main([str(f), *flags], today=TODAY)
    return code, capsys.readouterr().out

def test_report_lists_late_invoices_and_total_at_bottom(tmp_path, capsys):
    code, out = run(tmp_path, capsys, "Acme,INV-1,250.00,2027-02-01,no\nBolt,INV-2,100.50,2027-01-16,no\nCord,INV-3,75,2027-01-01,yes\n")
    lines = out.strip().splitlines()
    assert code == 0
    assert "INV-2" in lines[0] and "30 days late" in lines[0]
    assert "INV-1" in lines[1] and "14 days late" in lines[1]
    assert "INV-3" not in out
    assert lines[-1] == "Total owed: 350.50"

def test_ac5_remind_writes_reminder_with_number_amount_and_days(tmp_path, capsys):
    _, out = run(tmp_path, capsys, "Acme,INV-1,250.00,2027-02-01,no\n", "--remind")
    reminder = out.split("Total owed:")[1]
    assert "Acme" in reminder and "INV-1" in reminder and "250.00" in reminder and "14 days" in reminder

def test_no_reminders_without_flag(tmp_path, capsys):
    _, out = run(tmp_path, capsys, "Acme,INV-1,250.00,2027-02-01,no\n")
    assert "Hi" not in out

def test_ac6_extra_columns_ignored(tmp_path, capsys):
    code, out = run(tmp_path, capsys, "Acme,INV-1,250.00,2027-02-01,no,some note\n",
                    header="client,number,amount,due_date,paid,notes\n")
    assert code == 0 and "INV-1" in out

def test_ac7_bad_row_reported_with_line_and_reason_and_rest_still_reported(tmp_path, capsys):
    code, out = run(tmp_path, capsys, "Acme,INV-1,250.00,01/02/2027,no\nBolt,INV-2,abc,2027-02-01,no\nCord,INV-3,75,2027-02-01,no\n")
    assert "INV-3" in out
    assert "Line 2" in out and "due_date" in out
    assert "Line 3" in out and "amount" in out
    assert "Total owed: 75" in out

def test_ac8_nothing_late_says_so_and_exits_zero(tmp_path, capsys):
    code, out = run(tmp_path, capsys, "Acme,INV-1,250.00,2027-03-01,no\n")
    assert code == 0 and "Nothing is overdue" in out
