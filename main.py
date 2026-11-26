#!/usr/bin/env python3
"""Fortune Cookie Funnies for Engineers — entry writer.

Writes the selected one-line fortune to entry.txt in the output directory
(MAKEFUN_OUTPUT_DIR, or /output as fallback). Writes nothing to the repo.
"""

import hashlib
import os
import sys

ENTRY = "The legacy code you fear was written by you, six months ago."


def main() -> int:
    # Validation: exactly one line, 1-120 chars, printable ASCII only.
    if "\n" in ENTRY or "\r" in ENTRY:
        print("error: entry must be exactly one line", file=sys.stderr)
        return 1
    if not 1 <= len(ENTRY) <= 120:
        print(f"error: entry length {len(ENTRY)} out of range 1-120",
              file=sys.stderr)
        return 1
    if not all(32 <= ord(c) <= 126 for c in ENTRY):
        print("error: entry must be printable ASCII only", file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="ascii", newline="") as f:
        f.write(ENTRY)

    # Post-write verification: file must be byte-identical to ENTRY.
    with open(path, "rb") as f:
        written = f.read()
    expected = ENTRY.encode("ascii")
    if written != expected:
        print("error: entry.txt is not byte-identical to the selected entry",
              file=sys.stderr)
        return 1
    print(f"wrote {path} ({len(written)} bytes, "
          f"sha256={hashlib.sha256(written).hexdigest()})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
