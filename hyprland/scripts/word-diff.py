#!/usr/bin/env python3
"""Summarise word-level changes between two texts.

argv[1] = original, argv[2] = corrected.
Prints up to LT_MAX_SHOWN changes as "before → after; ...".
Prints nothing when there are more than that (caller falls back to a count).
"""
import difflib, os, re, sys

MAX_SHOWN = int(os.environ.get("LT_MAX_SHOWN", "5"))


def words(s):
    # Keep punctuation attached so "dog" -> "dogs." reads as one change.
    return re.findall(r"\S+", s)


def main():
    before, after = words(sys.argv[1]), words(sys.argv[2])
    sm = difflib.SequenceMatcher(a=before, b=after, autojunk=False)

    changes = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        old = " ".join(before[i1:i2])
        new = " ".join(after[j1:j2])
        if tag == "delete":
            changes.append(f"−{old}")
        elif tag == "insert":
            changes.append(f"+{new}")
        else:
            changes.append(f"{old} → {new}")

    if not changes:
        return
    print(f"COUNT={len(changes)}")
    if len(changes) <= MAX_SHOWN:
        print("; ".join(changes))


main()
