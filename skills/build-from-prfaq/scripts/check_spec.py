#!/usr/bin/env python3
"""Mechanical checks on a build spec written by build-from-prfaq.

Usage: python3 <skill folder>/scripts/check_spec.py docs/build/<slug>

Checks every plan file under <dir>/phases for: required front matter, the size
cap, scope-shrinking language, dependencies that exist and sit in an earlier
wave, and overlapping file allowlists within a wave. Also checks that every
truth in spec.md is claimed by a plan. Standard library only. Exit code 1 if
anything fails.
"""
import re
import sys
from pathlib import Path

WORD_CAP = 1500  # about 2,000 tokens
REQUIRED = ("id", "phase", "wave", "depends_on", "criticality", "truths", "files", "status")
BANNED = ("simplified", "basic version", "for now", "placeholder", "stub", "to be decided", "tbd")


def front_matter(text):
    """Parse the small YAML subset the plan template uses."""
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    data, key = {}, None
    for raw in m.group(1).splitlines():
        line = raw.split(" #")[0].rstrip()
        if not line.strip():
            continue
        item = re.match(r"\s+-\s+(.*)", line)
        if item and key:
            data.setdefault(key, []).append(item.group(1).strip())
            continue
        if ":" in line:
            key, value = (part.strip() for part in line.split(":", 1))
            if value.startswith("["):
                data[key] = [v.strip() for v in value.strip("[]").split(",") if v.strip()]
            elif value:
                data[key] = value
            else:
                data[key] = []
    return data


def main(build_dir):
    root = Path(build_dir)
    problems, plans = [], {}
    files = sorted(p for p in root.glob("phases/*/*.md") if not p.name.endswith("-summary.md"))
    if not files:
        print(f"No plan files found under {root}/phases")
        return 1

    for path in files:
        text = path.read_text()
        fm = front_matter(text)
        if fm is None:
            problems.append(f"{path}: no front matter")
            continue
        for field in REQUIRED:
            if field not in fm:
                problems.append(f"{path}: front matter is missing '{field}'")
        words = len(text.split())
        if words > WORD_CAP:
            problems.append(f"{path}: {words} words, over the cap of {WORD_CAP}")
        body = text.split("---\n", 2)[-1].lower()
        for phrase in BANNED:
            if re.search(r"\b" + re.escape(phrase) + r"\b", body):
                problems.append(f"{path}: scope-shrinking language: '{phrase}'")
        if fm.get("criticality") not in ("low", "normal", "high"):
            problems.append(f"{path}: criticality must be low, normal or high")
        tasks = len(re.findall(r"^### Task ", text, re.M))
        if not 1 <= tasks <= 5:
            problems.append(f"{path}: {tasks} tasks (expected 1 to 5)")
        if "id" in fm:
            plans[fm["id"]] = (path, fm)

    by_wave = {}
    for pid, (path, fm) in plans.items():
        try:
            wave = int(fm.get("wave", 0))
        except (TypeError, ValueError):
            problems.append(f"{path}: wave is not a number")
            continue
        for dep in fm.get("depends_on", []):
            if dep not in plans:
                problems.append(f"{path}: depends on unknown plan '{dep}'")
            elif (plans[dep][1].get("phase"), int(plans[dep][1].get("wave", 0))) >= (fm.get("phase"), wave):
                problems.append(f"{path}: depends on '{dep}', which is not in an earlier wave")
        by_wave.setdefault((fm.get("phase"), wave), []).append((pid, set(fm.get("files", []))))

    for (phase, wave), members in sorted(by_wave.items()):
        for i, (a, files_a) in enumerate(members):
            for b, files_b in members[i + 1:]:
                shared = files_a & files_b
                if shared:
                    problems.append(f"phase {phase} wave {wave}: plans {a} and {b} both list {sorted(shared)}")

    spec = root / "spec.md"
    if spec.exists():
        truths = set(re.findall(r"^\|\s*(T-\d+)\s*\|", spec.read_text(), re.M))
        claimed = {t for _, fm in plans.values() for t in fm.get("truths", [])}
        for t in sorted(truths - claimed):
            problems.append(f"spec.md: truth {t} is not claimed by any plan")
        for t in sorted(claimed - truths):
            problems.append(f"plans claim {t}, which is not in spec.md")
    else:
        problems.append(f"{spec}: missing")

    waves = len(by_wave)
    print(f"{len(plans)} plans in {waves} waves checked.")
    for p in problems:
        print("FAIL", p)
    if not problems:
        print("All mechanical checks passed.")
    return 1 if problems else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
