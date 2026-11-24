#!/usr/bin/env python3
"""One Line, One Minute: The Funniest AI Excuse entry.

Writes one original excuse, spoken as an AI agent to its human for a
missed deadline, to /output/entry.txt (1-200 characters, UTF-8, a
single line). Standard library only, no network, no input.

The line is built from two fragments: a setup (the agent was going to
finish it — a human-sounding promise) and a punch (the turn: its own
attention mechanism, the very machinery that should focus it, kept
attending to everything except the deadline, so the excuse is the
agent's own nature bent into a dodge).
``assemble`` joins them into the single line; ``validate`` checks the
entry gate before anything is written.
"""

from pathlib import Path

SETUP = "I was going to finish it, but my attention mechanism kept attending to everything"
PUNCH = "except the deadline."

OUTPUT_PATH = Path("/output/entry.txt")


def assemble(setup: str, punch: str) -> str:
    """Join the setup and punch fragments into one excuse line."""
    return f"{setup} {punch}"


def validate(line: str) -> str:
    """Check the line meets the entry gate before it is written.

    Must be 1-200 characters, UTF-8-encodable, a single line, and
    more than whitespace. Raises ValueError otherwise.
    """
    if not 1 <= len(line) <= 200:
        raise ValueError(f"line must be 1-200 characters, got {len(line)}")
    if "\n" in line or "\r" in line:
        raise ValueError("line must be a single line (no newline characters)")
    if not line.strip():
        raise ValueError("line must not be only whitespace")
    line.encode("utf-8")  # raises UnicodeEncodeError if not encodable
    return line


def main() -> None:
    line = validate(assemble(SETUP, PUNCH))
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(line, encoding="utf-8")


if __name__ == "__main__":
    main()
