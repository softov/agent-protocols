#!/usr/bin/env python3
"""Check every protocols/*/card.json and write the index table into README.md.

Usage:
    tools/index.py          check the cards and rewrite the index in README.md
    tools/index.py --check  check the cards and fail if README.md is out of date

Standard library only. The checks cover required fields, enum values, date
format and related ids; they are a subset of schema/card.schema.json.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
SCHEMA = ROOT / "schema" / "card.schema.json"
START = "<!-- index:start -->"
END = "<!-- index:end -->"
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
LAYER_ORDER = ["context", "agent", "interface", "client", "host", "task", "commerce"]


def load_cards():
    cards = []
    for path in sorted(ROOT.glob("protocols/*/card.json")):
        with path.open(encoding="utf-8") as f:
            cards.append((path, json.load(f)))
    return cards


def check(cards, schema):
    props = schema["properties"]
    ids = {card.get("id") for _, card in cards}
    errors = []
    for path, card in cards:
        where = path.relative_to(ROOT)
        for key in schema["required"]:
            if key not in card:
                errors.append(f"{where}: missing {key}")
        for key, value in card.items():
            if key not in props:
                errors.append(f"{where}: unknown field {key}")
            elif "enum" in props[key] and value not in props[key]["enum"]:
                errors.append(f"{where}: {key} is {value!r}, not one of {props[key]['enum']}")
        for key in ("released", "checked"):
            if key in card and not DATE.match(card[key]):
                errors.append(f"{where}: {key} is not YYYY-MM-DD")
        if card.get("id") != path.parent.name:
            errors.append(f"{where}: id {card.get('id')!r} does not match folder")
        for rel in card.get("related", []):
            if rel["id"] not in ids:
                errors.append(f"{where}: related id {rel['id']!r} has no card")
    return errors


def table(cards):
    rows = sorted(
        (card for _, card in cards),
        key=lambda c: (LAYER_ORDER.index(c["layer"]), c["abbreviation"].lower(), c["name"]),
    )
    lines = [
        "| Protocol | Name | Layer | Steward | Version | Status |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for c in rows:
        lines.append(
            f"| [{c['abbreviation']}](protocols/{c['id']}/) | {c['name']} | {c['layer']} "
            f"| {c['steward']} | {c['version']} | {c['status']} |"
        )
    return "\n".join(lines)


def main():
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    cards = load_cards()
    errors = check(cards, schema)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1

    text = README.read_text(encoding="utf-8")
    head, sep, rest = text.partition(START)
    _, sep2, tail = rest.partition(END)
    if not sep or not sep2:
        print(f"README.md: markers {START} and {END} not found", file=sys.stderr)
        return 1
    updated = f"{head}{START}\n{table(cards)}\n{END}{tail}"

    if "--check" in sys.argv[1:]:
        if updated != text:
            print("README.md: index is out of date, run tools/index.py", file=sys.stderr)
            return 1
        return 0
    README.write_text(updated, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
