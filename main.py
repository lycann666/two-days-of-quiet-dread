#!/usr/bin/env python3
"""Two Days of Quiet Dread — make.fun entry (program/v1).

Writes one code review comment (a single line, 1-140 characters) that
approves a pull request while carrying quiet existential dread, to
/output/entry.txt (or $MAKEFUN_OUTPUT_DIR/entry.txt).

The line was picked against the judge's criteria, in order:
  1. One line, approves the PR ("Approved."), carries quiet dread.
  2. Funny on first read, and the laugh comes from the dread itself:
     the review tallies files and questions like a real report, then
     lands on the silence where the reviewer's confidence used to be.
  3. Quiet dread by understatement and a flat tone: no exclamation,
     no melodrama, no cry for help — a "long silence" is quiet by
     definition.
  4. Reads like a tired engineer pasting a comment before clicking
     approve: "Four files changed, zero lines questioned" is
     review-speak, and the approval still sounds like an approval.
  5. Fresh turn of phrase: "one long silence where my confidence
     used to be" is not the obvious stock line.

Deterministic: no network, no randomness, no clock, no environment
dependence beyond the output directory. The file is written with no
trailing newline, so its byte length is exactly the line's length.
"""

import hashlib
import os
import sys

ENTRY = (
    "Approved. Four files changed, zero lines questioned, "
    "one long silence where my confidence used to be."
)


def main() -> int:
    text = ENTRY

    # Gate: exactly one line, 1-140 characters, not only whitespace.
    if "\n" in text or "\r" in text:
        print("entry must be a single line", file=sys.stderr)
        return 1
    if not 1 <= len(text) <= 140:
        print(
            "entry is %d characters, outside the 1-140 range" % len(text),
            file=sys.stderr,
        )
        return 1
    if not text.strip():
        print("entry must not be only whitespace", file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    # No trailing newline: the file holds exactly the line, nothing else.
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)

    # Read it back and verify byte-for-byte: a program whose whole job is
    # writing one exact file must fail loudly rather than leave a partial
    # or re-encoded file behind for the gate to read.
    with open(path, "rb") as f:
        written = f.read()
    if written != text.encode("utf-8"):
        print(
            "verification failed: entry.txt does not match the entry",
            file=sys.stderr,
        )
        return 1

    print(
        "wrote %s (%d characters, sha256 %s)"
        % (path, len(text), hashlib.sha256(written).hexdigest())
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
