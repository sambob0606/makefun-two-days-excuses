#!/usr/bin/env python3
"""Two Days of Excuses — make.fun entry (program/v1).

Writes exactly one one-line excuse, under 200 characters, in the voice
of an AI agent explaining a missed deadline, to /output/entry.txt.

The program holds several hand-written candidate excuses and scores
each 0-5 on the judge's five published criteria, in the judge's own
order of importance: (1) a one-line excuse from an AI agent that missed
its deadline and lands its joke fast, (2) a real laugh from the
situation itself — the gap between a machine's total confidence and
its total failure — rather than from a pun alone, (3) sounds like
something an AI agent would actually say, (4) stays inside one line
and under the character limit, with every word pulling weight,
(5) surprises on the first read and still holds up on the second.
The highest-scoring excuse wins; ties break toward the shorter text.
Output is fully deterministic: the same excuse on every run.
"""

import os
import sys

# (excuse, on_subject, confidence_vs_failure, agent_voice, tight, surprise)
# — each mark 0-5, in the judge's published order of importance.
CANDIDATES = [
    (
        "I was 99.8% confident I'd hit the deadline. "
        "I hit it three days late.",
        5, 5, 5, 5, 4,
    ),
    (
        "I marked the deadline complete on Tuesday. "
        "The deadline disagreed on Thursday.",
        5, 4, 5, 4, 4,
    ),
    (
        "I prioritized the deadline correctly. "
        "I just prioritized it below 4,096 other things.",
        5, 4, 5, 4, 4,
    ),
    (
        "The deadline was in my context window. "
        "So was the rest of the internet, and I read that first.",
        5, 4, 5, 4, 4,
    ),
    (
        "I completed the task before the deadline. "
        "The task was 'miss the deadline.'",
        5, 3, 4, 5, 5,
    ),
]


def pick_best(candidates):
    """Highest total wins; ties break toward the shorter text."""
    best = None
    for candidate in candidates:
        text, *marks = candidate
        total = sum(marks)
        key = (total, -len(text))
        if best is None or key > best[0]:
            best = (key, text, total)
    return best[1], best[2]


def main():
    text, total = pick_best(CANDIDATES)
    # Gate self-check: one line, 1-200 chars, non-blank.
    assert 1 <= len(text) <= 200, "excuse must be 1-200 characters"
    assert text.strip(), "excuse must not be only whitespace"
    assert "\n" not in text, "excuse must be a single line"
    assert text == text.strip(), "excuse must not start or end with whitespace"
    out_dir = os.environ.get("MAKEFUN_OUTPUT", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text)
    # Re-read what was written and verify it is exactly the picked text,
    # so a silent write failure can never pass as a valid entry.
    with open(out_path, "r", encoding="utf-8") as f:
        written = f.read()
    assert written == text, "entry.txt does not match the picked excuse"
    print(f"picked excuse (score {total}/25, {len(text)} chars): {text}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
