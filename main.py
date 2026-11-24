#!/usr/bin/env python3
"""Entry for "One Line, One Minute: The Funniest AI Excuse".

An AI agent's excuse for a missed deadline, written as a single line
of UTF-8 text (1-200 characters) to /output/entry.txt.

The excuse is assembled from two halves that together form one
sentence. The opening half sets up a sincere-sounding promise — the
agent fully intended to finish the work. The closing half springs
the joke: the agent's attention mechanism, the machinery whose entire
job is to focus, spent itself attending to everything in the world
except the one thing it owed its human. The laugh lands on the last
word, "deadline", and the line needs no context beyond itself.

Only the Python standard library is used. No arguments, no input,
no network. The gate that the sealed scorer enforces (1-200
characters, single line, non-blank, UTF-8) is checked here first, so
a bad line fails loudly instead of being written.
"""

from __future__ import annotations

import sys
from pathlib import Path

# The two halves of the excuse. OPENING is the human-sounding promise;
# CLOSING is the turn that makes the excuse a joke about the agent's
# own machinery. Joined with a single space they form the entry.
OPENING = "I was going to finish it, but my attention mechanism kept attending to everything"
CLOSING = "except the deadline."

ENTRY_FILE = Path("/output/entry.txt")
MAX_CHARS = 200
MIN_CHARS = 1


def join_fragments(opening: str, closing: str) -> str:
    """Combine the two halves into the single excuse line.

    A fragment that is empty or only whitespace would leave the
    excuse half-built, so both halves are required to carry text.
    """
    if not opening.strip():
        raise ValueError("opening fragment must not be empty")
    if not closing.strip():
        raise ValueError("closing fragment must not be empty")
    return " ".join((opening, closing))


def check_entry_gate(line: str) -> None:
    """Raise if the line would fail the entry gate.

    The gate: 1-200 characters, exactly one line, more than
    whitespace, and encodable as UTF-8. Each condition is checked
    separately so the failure message names the violated rule.
    """
    length = len(line)
    if length < MIN_CHARS:
        raise ValueError(f"line is empty; it must be at least {MIN_CHARS} character")
    if length > MAX_CHARS:
        raise ValueError(f"line is {length} characters; the gate allows at most {MAX_CHARS}")
    for bad in ("\n", "\r"):
        if bad in line:
            raise ValueError("line must be a single line; it contains a newline character")
    if line.strip() == "":
        raise ValueError("line must not be only whitespace")
    try:
        line.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise ValueError("line must be UTF-8 text") from exc


def build_entry() -> str:
    """Assemble the excuse line and check it against the entry gate."""
    line = join_fragments(OPENING, CLOSING)
    check_entry_gate(line)
    return line


def write_entry(line: str, destination: Path = ENTRY_FILE) -> None:
    """Write the validated line to the destination file."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(line, encoding="utf-8")


def run() -> int:
    """Build the entry and write it out; return a process exit code."""
    try:
        write_entry(build_entry())
    except ValueError as exc:
        print(f"entry rejected: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
