"""Office Judge Laugh entry: writes one original office joke to /output/entry.txt.

The joke is a single original line about office life, invented for this
entry. The program is fully deterministic: no network, no randomness,
no environment reads, no time or date — it always writes the same text.
"""

import os
import tempfile

ENTRY = "Our office recycles exactly one thing: the same three excuses for why my raise is delayed until next quarter."


def validate(text):
    """Fail loudly unless the entry is 1-200 characters and not blank."""
    if not isinstance(text, str):
        raise ValueError("ENTRY must be a string")
    if not 1 <= len(text) <= 200:
        raise ValueError("ENTRY must be 1-200 characters, got %d" % len(text))
    if not text.strip():
        raise ValueError("ENTRY must not be whitespace-only")
    if "\n" in text or "\r" in text:
        raise ValueError("ENTRY must be a single line")


def write_entry(text):
    """Write text atomically to /output/entry.txt, falling back to ./output."""
    for directory in ("/output", "./output"):
        try:
            os.makedirs(directory, exist_ok=True)
            target = os.path.join(directory, "entry.txt")
            fd, tmp = tempfile.mkstemp(dir=directory, prefix=".entry-", suffix=".tmp")
            try:
                with os.fdopen(fd, "w", encoding="utf-8") as f:
                    f.write(text)
                os.replace(tmp, target)
            except BaseException:
                try:
                    os.unlink(tmp)
                except OSError:
                    pass
                raise
            # Round-trip check: read back and confirm byte-for-byte.
            with open(target, "r", encoding="utf-8") as f:
                if f.read() != text:
                    raise ValueError("read-back mismatch in %s" % target)
            return target
        except OSError:
            continue
    raise OSError("could not write entry.txt to /output or ./output")


def main():
    validate(ENTRY)
    target = write_entry(ENTRY)
    print(ENTRY)
    print("characters:", len(ENTRY))
    print("wrote:", target)


if __name__ == "__main__":
    main()
