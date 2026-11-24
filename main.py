# The Robot Vacuum's Best Excuse — make.fun bounty
# u-golden-heron-44-the-robot-vacuum-s-best-excuse-53412214
#
# The program writes one funny one-line excuse a robot vacuum gives for
# missing a spot (a single line of at most 140 characters) to
# /output/entry.txt.
# Candidates were drafted against the judge's brief, in order of weight:
#   1. reads as a one-line excuse from a robot vacuum for missing a spot
#   2. funny on first read, the kind that makes a tired homeowner laugh
#      out loud rather than smile politely
#   3. rooted in the vacuum's own world — its sensors, bumpers, dock,
#      map, battery — not a generic apology
#   4. the joke lands on the first read, with a clean turn at the end
#   5. sounds like the vacuum itself talking, a small machine keeping a
#      straight face, not the owner putting words in its mouth
# Each candidate carries a hand-scored craft score (0-10 per criterion,
# summed below); selection is deterministic: highest score wins, ties go
# to the shorter text. The output is byte-identical on every run.

CANDIDATES = [
    # score: excuse 10, funny 9, vacuum-world 10, first-read 10,
    #   vacuum-voice 9 = 48. The map is the vacuum's whole world, and
    #   "here be dragons" is the oldest joke on any map; the turn —
    #   "I clean floors, not dragons" — is the vacuum drawing a job
    #   description line with a straight face.
    ("My map says that corner is 'here be dragons'. "
     "I clean floors, not dragons.",
     48),
    # score: excuse 10, funny 9, vacuum-world 9, first-read 9,
    #   vacuum-voice 9 = 46. The bumper is the vacuum's blunt instrument
    #   of diplomacy; after twelve bumps the blame-shifting feels earned,
    #   and the last clause is the vacuum's deadpan verdict.
    ("I bumped that chair leg twelve times. At some point the chair "
     "is the problem, not me.",
     46),
    # score: excuse 10, funny 8, vacuum-world 10, first-read 9,
    #   vacuum-voice 8 = 45. The sensors' "cliff" classification is
    #   pure vacuum logic; refusing to argue with gravity is the
    #   machine's idea of courage, but the turn is a touch wordy.
    ("I did not miss that spot. My sensors filed it under 'cliff', "
     "and I refuse to argue with gravity.",
     45),
    # score: excuse 9, funny 8, vacuum-world 9, first-read 8,
    #   vacuum-voice 8 = 42. Dying at 2% on the spot is very much a
    #   vacuum's fate, and conceding defeat to the dust is charming,
    #   but it explains itself a little rather than landing the punch.
    ("My battery died at 2% right on that spot. I choose to believe "
     "the dust won fair and square.",
     42),
    # score: excuse 8, funny 8, vacuum-world 7, first-read 8,
    #   vacuum-voice 8 = 39. The squatter-dust joke is warm, but the
    #   excuse is looser — it is about the dust's tenure, not why the
    #   vacuum missed the spot — and it leans less on vacuum hardware.
    ("The dust under your bed pays rent. I have been here six months; "
     "it has been here since 2019.",
     39),
]

# The gate requires 1-140 characters of non-whitespace UTF-8 text.
MAX_CHARS = 140


def pick(candidates):
    best = None
    for text, score in candidates:
        assert 1 <= len(text) <= MAX_CHARS, \
            f"candidate over gate: {len(text)} chars"
        assert text.strip(), "candidate is blank"
        assert "\n" not in text, "candidate must be a single line"
        key = (score, -len(text))  # highest score, then shortest
        if best is None or key > best[0]:
            best = (key, text)
    return best[1]


def main():
    import hashlib
    import os
    import sys

    excuse = pick(CANDIDATES)
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(excuse)
    os.chmod("/output/entry.txt", 0o644)
    # Verify the written output: read it back byte-for-byte, re-check
    # the gate (1-140 characters, single line, non-blank) and print its
    # SHA-256 so any later run can prove the entry is byte-identical.
    # A truncated or altered file must fail loudly instead of shipping
    # a bad entry.
    with open("/output/entry.txt", "rb") as f:
        raw = f.read()
    written = raw.decode("utf-8")
    digest = hashlib.sha256(raw).hexdigest()
    if written != excuse:
        print("error: /output/entry.txt does not match selected excuse",
              file=sys.stderr)
        sys.exit(1)
    if not (1 <= len(written) <= MAX_CHARS and written.strip()
            and "\n" not in written):
        print("error: /output/entry.txt fails gate: "
              f"{len(written)} chars", file=sys.stderr)
        sys.exit(1)
    print(excuse)
    print(f"chars={len(written)} sha256={digest}")


if __name__ == "__main__":
    main()
