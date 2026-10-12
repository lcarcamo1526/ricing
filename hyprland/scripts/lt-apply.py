#!/usr/bin/env python3
"""Apply LanguageTool's first replacement for each match.

stdin  : LanguageTool JSON
argv[1]: original text
stdout : corrected text
stderr : line 1 = number of fixes; line 2 = "before -> after" diffs, ';'-separated
exit 2 : detected language not trusted (caller should refuse to paste)
"""
import json, os, sys

ALLOWED = set(filter(None, os.environ.get("LT_ALLOWED", "en,es,fr").split(",")))
MIN_CONFIDENCE = float(os.environ.get("LT_MIN_CONFIDENCE", "0.80"))
MAX_SHOWN = int(os.environ.get("LT_MAX_SHOWN", "5"))


def main():
    data = json.load(sys.stdin)
    text = sys.argv[1]

    lang = data.get("language", {})
    detected = lang.get("detectedLanguage", {}) or {}
    code = (detected.get("code") or lang.get("code") or "").split("-")[0]
    confidence = detected.get("confidence")

    if code not in ALLOWED:
        print(f"untrusted-language:{code or '?'}", file=sys.stderr)
        sys.exit(2)
    if confidence is not None and confidence < MIN_CONFIDENCE:
        print(f"low-confidence:{code}:{confidence:.2f}", file=sys.stderr)
        sys.exit(2)

    matches = [m for m in data.get("matches", []) if m.get("replacements")]
    # Apply right-to-left so earlier offsets stay valid.
    matches.sort(key=lambda m: m["offset"], reverse=True)

    diffs = []
    for m in matches:
        o, l = m["offset"], m["length"]
        if o < 0 or o + l > len(text):
            continue
        before = text[o:o + l]
        after = m["replacements"][0]["value"]
        diffs.append((before, after))
        text = text[:o] + after + text[o + l:]

    sys.stdout.write(text)

    # Diffs were collected right-to-left; show them in reading order.
    diffs.reverse()
    print(len(diffs), file=sys.stderr)
    if diffs and len(diffs) <= MAX_SHOWN:
        print("; ".join(f"{b or '∅'} → {a or '∅'}" for b, a in diffs), file=sys.stderr)


main()
