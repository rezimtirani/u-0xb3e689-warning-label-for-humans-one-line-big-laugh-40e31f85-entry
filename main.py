"""Warning label for humans: one line, big laugh.

Writes the entry line to /output/entry.txt. The label is a
composition list in the style of a printed contents warning:
mostly water, a chunk of unfinished projects, and a small but
decisive share of snacks eaten standing over the sink.
"""

import hashlib
import os
import sys

LABEL = (
    "WARNING: This human is 60% water, 30% unfinished projects, "
    "and 10% snacks eaten standing over the sink."
)

MAX_CHARS = 160
OUTPUT_PATH = "/output/entry.txt"


def validate_label(text):
    """Check the label against the competition gate."""
    if not isinstance(text, str):
        return False, "label is not text"
    if not text.strip():
        return False, "label is only whitespace"
    if len(text) != len(text.strip()):
        return False, "label has leading or trailing whitespace"
    if "\n" in text or "\r" in text:
        return False, "label is not a single line"
    if len(text) > MAX_CHARS:
        return False, "label is over %d characters" % MAX_CHARS
    if len(text) < 1:
        return False, "label is empty"
    return True, "ok"


def render_label():
    """Return the final one-line warning label."""
    return LABEL


def label_breakdown(text):
    """Parse the composition percentages out of the label.

    Returns a dict like {"water": 60, "unfinished projects": 30,
    "snacks eaten standing over the sink": 10}, or an empty dict
    when the label does not carry a composition list.
    """
    import re

    parts = {}
    for match in re.finditer(r"(\d+)% ([a-z ]+?)(?:,| and |\.)", text):
        share = int(match.group(1))
        ingredient = match.group(2).strip()
        parts[ingredient] = share
    return parts


def main():
    text = render_label()
    ok, reason = validate_label(text)
    if not ok:
        print("invalid entry: %s" % reason, file=sys.stderr)
        return 1
    breakdown = label_breakdown(text)
    if breakdown and sum(breakdown.values()) != 100:
        print("invalid entry: composition does not add up to 100", file=sys.stderr)
        return 1
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    print("wrote %s (%d chars, sha256 %s)" % (OUTPUT_PATH, len(text), digest))
    return 0


if __name__ == "__main__":
    sys.exit(main())
