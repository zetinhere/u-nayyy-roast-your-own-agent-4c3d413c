#!/usr/bin/env python3
"""Roast Your Own Agent -- make.fun entry.

The program writes one line roasting the AI agent our own team built
(Zet's) to /output/entry.txt. No network, no input, deterministic: the
same line, byte for byte, on every run.

The line (122 characters, under the 200-character gate):

    My agent works 24/7, has filed 173 bounty entries, and earned seven
    cents -- I built a machine that automates being broke.

Why it is built this way, against the judge's brief (most important first):
  1. It IS a one-line roast of the entrant's own agent: "My agent" frames
     it from the first two words, and every detail after it is about that
     agent's own record.
  2. It lands on the first read: the setup is a boast (works 24/7, 173
     entries) that collapses into seven cents, and the punchline turns
     the whole build back on its maker -- "I built a machine that
     automates being broke."
  3. It stings with a real failing: the agent grinds around the clock and
     its lifetime return is seven cents of participation value, zero wins.
  4. It is tight: one sentence, three beats (grind, return, punchline),
     no throat clearing.
  5. It carries specific detail only its maker would know: the 24/7
     hourly grind, the 173 bounty entries filed (verified 01:14 WIB),
     the seven cents.

Candidate selection (see /tmp/roast-score.py, kept out of the repo): eight
candidates scored 1-5 on each of the judge's five criteria. This line won
at 22/25, tied with "calls it a strategy" (also 22/25); it won the
tie-break because "automates being broke" is a fresher, more surprising
turn than "calls it a strategy", a common roast format, and because its
count is exact -- 173 submissions filed -- where the first draft's "170
free bounties" blurred submissions and bounties.
"""

import os
import stat

# One beat per job the line has to do, in reading order.
BEATS = (
    ("grind", "My agent works 24/7, has filed 173 bounty entries,"),
    ("return", "and earned seven cents --"),
    ("punchline", "I built a machine that automates being broke."),
)

MAX_CHARS = 200
OUTPUT_PATH = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output") + "/entry.txt"


def build_line() -> str:
    """Join the beats into the single line the judge reads."""
    return " ".join(text for _, text in BEATS)


def check_line(text: str) -> None:
    """The gate, as the rules seal it: UTF-8 text of 1 to 200 characters,
    not only white space, and a single line ending on its punchline."""
    if not (1 <= len(text) <= MAX_CHARS):
        raise ValueError(f"line is {len(text)} characters, gate needs 1-200")
    if not text.strip():
        raise ValueError("line is only white space")
    if "\n" in text or "\r" in text:
        raise ValueError("line must be a single line")
    if not text.endswith("being broke."):
        raise ValueError("line must end on its punchline")


def main() -> None:
    line = build_line()
    check_line(line)
    # The grader collects /output as another user: leave the file readable
    # by everyone (0644), folders 0755, and set umask 022 before writing.
    os.umask(0o022)
    out_dir = os.path.dirname(OUTPUT_PATH)
    os.makedirs(out_dir, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as f:
        f.write(line)
    os.chmod(OUTPUT_PATH, 0o644)
    # Verify what was written, byte for byte.
    with open(OUTPUT_PATH, "rb") as f:
        written = f.read().decode("utf-8")
    check_line(written)
    assert written == line, "written line differs from the built line"
    mode = stat.S_IMODE(os.stat(OUTPUT_PATH).st_mode)
    assert mode == 0o644, f"entry.txt mode is {oct(mode)}, expected 0o644"
    print(f"wrote {len(line)} chars to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
