#!/usr/bin/env python3
"""Choose the robot vacuum's best excuse and save it to /output/entry.txt.
The bounty wants a single line, no more than 140 characters, spoken by a
robot vacuum that skipped a spot. Twelve excuses were written by hand and
marked on five counts, each count out of ten:
  apology      the line reads as an excuse for the missed spot
  comic_hit    it makes a tired homeowner laugh on the first read
  hardware     the joke grows out of the machine itself: its map, lidar,
               bumper, cliff sensor, dock, or battery
  instant      the turn lands at once, with no second read needed
  robot_voice  it sounds like the little machine talking, deadpan, not
               like the owner putting words in its mouth
The highest total wins; a tie goes to the shorter line. The winning line
is stored with no trailing newline, then read back and checked byte for
byte, so repeated runs produce the identical file every time.
"""
# ---
from __future__ import annotations
import hashlib
import sys
from dataclasses import dataclass
from pathlib import Path
# ---
CEILING = 140
TARGET = Path("/output/entry.txt")
# ---
@dataclass(frozen=True)
class Draft:
    """One hand-written excuse together with its five hand-given marks."""
    line: str
    apology: int
    comic_hit: int
    hardware: int
    instant: int
    robot_voice: int
    @property
    def total(self) -> int:
        """Add the five marks; the field is deliberately small."""
        return self.apology + self.comic_hit + self.hardware + self.instant + self.robot_voice
# ---
DRAFTS = (
    Draft(
        line="My map says that corner is 'here be dragons'. I clean floors, not dragons.",
        apology=10, comic_hit=9, hardware=10, instant=10, robot_voice=9,
    ),  # 48: the map is the vacuum's whole world, and "here be dragons"
    # is the oldest joke on any map; the turn draws a job-description
    # line with a straight face.
    Draft(
        line="I bumped that chair leg twelve times. At some point the chair is the problem, not me.",
        apology=10, comic_hit=9, hardware=9, instant=9, robot_voice=9,
    ),  # 46: the bumper is the vacuum's blunt instrument of diplomacy,
    # and twelve bumps earn the blame-shifting; the verdict lands flat.
    Draft(
        line="I did not miss that spot. My sensors filed it under 'cliff', and I refuse to argue with gravity.",
        apology=10, comic_hit=8, hardware=10, instant=9, robot_voice=8,
    ),  # 45: pure vacuum logic from the cliff sensor, but the turn runs
    # a touch long before it gets to the punch.
    Draft(
        line="The cat sat on that spot and stared at me until I left. I answer to the cat now.",
        apology=9, comic_hit=9, hardware=8, instant=9, robot_voice=9,
    ),  # 44: the household hierarchy is settled by a stare; the vacuum
    # accepts its place without a word of complaint.
    Draft(
        line="My cliff sensors saw the rug fringe and declared it a ravine. I do not cross ravines.",
        apology=8, comic_hit=8, hardware=10, instant=8, robot_voice=9,
    ),  # 43: the sensor misreads a fringe as terrain, and the vacuum
    # treats its own mistake as geography.
    Draft(
        line="My battery died at 2% right on that spot. I choose to believe the dust won fair and square.",
        apology=9, comic_hit=8, hardware=10, instant=8, robot_voice=8,
    ),  # 43: dying on the spot is a very vacuum fate, and conceding to
    # the dust is charming, but the line explains itself a little.
    Draft(
        line="I cleaned around the charging cable like it was a sleeping snake. Some things you do not wake.",
        apology=8, comic_hit=8, hardware=9, instant=8, robot_voice=8,
    ),  # 41: the cable-as-snake image is vivid, yet the excuse is
    # cautious rather than funny; the vacuum plays it too safe.
    Draft(
        line="The dust bunnies in that corner unionised. I am still waiting for HR to reply.",
        apology=8, comic_hit=9, hardware=7, instant=9, robot_voice=8,
    ),  # 41: the union gag is quick and modern, but it leans on office
    # life instead of anything the vacuum itself owns.
    Draft(
        line="The dust under your bed pays rent. I have been here six months; it has been here since 2019.",
        apology=8, comic_hit=8, hardware=7, instant=8, robot_voice=8,
    ),  # 39: warm squatter joke, but the excuse is loose: it is about
    # the dust's tenure, not about why the spot was skipped.
    Draft(
        line="I tried that corner three times and my wheels just spun. Even I know when to quit.",
        apology=8, comic_hit=7, hardware=8, instant=8, robot_voice=8,
    ),  # 39: honest and mechanical, yet the shrug at the end is flat;
    # quitting is not much of a punchline.
    Draft(
        line="My dock called me home halfway through. I never disobey the dock.",
        apology=7, comic_hit=7, hardware=8, instant=8, robot_voice=8,
    ),  # 38: loyalty to the dock is in character, but the excuse hides
    # behind an order instead of owning the miss.
    Draft(
        line="That spot hides behind the sofa leg, and my bumper and I have agreed to disagree about it.",
        apology=7, comic_hit=7, hardware=8, instant=7, robot_voice=8,
    ),  # 37: the disagreement is polite to a fault; nothing in it
    # surprises, and the sofa leg does the heavy lifting.
)
# ---
def gatekeep(draft: Draft) -> None:
    """Refuse any draft that breaks the bounty's one-line gate."""
    text = draft.line
    if not text.strip():
        raise ValueError("draft is blank")
    if "\n" in text or "\r" in text:
        raise ValueError("draft must be a single line")
    if len(text) > CEILING:
        raise ValueError(f"draft runs {len(text)} chars, over {CEILING}")
# ---
def adjudicate(drafts: tuple[Draft, ...]) -> Draft:
    """Return the winning draft: top total, then the shorter line."""
    for draft in drafts:
        gatekeep(draft)
    seen = {draft.line for draft in drafts}
    if len(seen) != len(drafts):
        raise ValueError("two drafts share the same line")
    ordered = sorted(drafts, key=lambda d: (d.total, -len(d.line)), reverse=True)
    head, runner_up = ordered[0], ordered[1]
    if head.total == runner_up.total and len(head.line) == len(runner_up.line):
        raise ValueError("no outright winner: top two tie on total and length")
    return head
# ---
def publish(entry: str) -> tuple[str, int]:
    """Write the entry with no trailing newline and prove it round-trips."""
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    payload = entry.encode("utf-8")
    TARGET.write_bytes(payload)
    TARGET.chmod(0o644)
    returned = TARGET.read_bytes()
    if returned.decode("utf-8") != entry:
        print("error: /output/entry.txt decodes to a different entry", file=sys.stderr)
        raise SystemExit(1)
    if returned != payload:
        print("error: /output/entry.txt came back different", file=sys.stderr)
        raise SystemExit(1)
    if not 1 <= len(entry) <= CEILING:
        print(f"error: entry runs {len(entry)} chars", file=sys.stderr)
        raise SystemExit(1)
    return hashlib.sha256(returned).hexdigest(), len(returned)
# ---
def main() -> None:
    """Pick the winner, publish it, and print its fingerprint."""
    winner = adjudicate(DRAFTS)
    digest, size = publish(winner.line)
    print(winner.line)
    print(f"length={size} sha256={digest}")
# ---
if __name__ == "__main__": main()
