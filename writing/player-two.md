# Player Two

*One day, one kids' space game, multiplayer added in five rounds. Each round shipped only after its
tests passed, and the closest calls were caught by checks outside the game's own tests.*

Squad Leader: Frontier is a space game I build with and for my boys: fly a sector, mine rocks,
rescue pilots, build a base. It runs on a tablet at home, through a small app server I call
AppVerse, and in a public arcade online. On Friday 6 November the request was simple to say:
let a second kid play.

As with my other projects, an assistant wrote the code from my direction. My part was deciding
what "done" meant for each round, running every deploy myself from a one-page list I call the
ship kit, and refusing to ship a round whose checks hadn't passed.

---

## 1. Two thumbs, one tablet (06:11)

The first version kept everything on one screen. The left half of the tablet steers my ship; the
right half steers a second ship, P2, which aims and fires by itself so the youngest player only has
to steer. The game's test for it drives two fingers at once in a browser and checks 23 things,
including that P2 can't leave the shared screen and that the save file doesn't change shape. It was
live in the arcade by 06:36.

## 2. A second device, and a crash the tests couldn't see (06:59, 07:05)

Next, each kid on their own device. I chose to route the game through AppVerse on the home Wi-Fi
rather than an outside service: nothing about the boys' play leaves the house, and the feature
simply hides itself anywhere AppVerse isn't. A small relay passes messages between devices; it
keeps everything in memory and writes nothing to disk.

The two-device test runs a tablet and a phone side by side, and before anything shipped it caught
three real bugs: the Leave button was hidden under the game's canvas on phones, a stopped game
lingered in the join list long enough for a phone to join a dead one, and leaving didn't give the
seat back.

Then the deploy failed one check: "the two-device relay answers", with no reply at all. The relay's
own tests had passed, but they ran it inside a stand-in server. Inside AppVerse's real request
handler, one function imported a name further down that the new relay code used earlier, so Python treated it
as a not-yet-assigned local and every relay request crashed. The fix was two lines. The lesson was
the new test: it drives AppVerse's actual handler, and it fails without the fix. **A stand-in that
passes proves the stand-in works.**

## 3. The copy that was ahead (09:43, 10:22)

While I was teaching, a session on my work laptop built the next thing on the list, wingmate
formations, along with a lime-green P2 and a start-screen button, straight into the arcade's copy of
the game. The laptop doesn't have the game's source folder; that lives on my desktop, and the arcade
copy is normally a build output of it.

That evening the desktop session started building formations from the source, the same feature
again, before a routine look at the arcade file's history showed two commits it hadn't made. The
next rebuild from source would have silently erased the morning's work. So the duplicate was
dropped, the laptop's changes were applied to the source, and the result was checked byte for
byte against the live file.

Those changes had never met the game's tests. Four tests just needed updating for a new start-screen
button and the new formation buttons. One finding was a real bug: How to Play told phone players to
"press A" on a controller they didn't have.

## 4. The guest must never save (19:35)

The next round let the second device show the game itself instead of a thumb-stick. Before writing it,
a review raised the risk that mattered most: the guest would hold the host's whole game in memory,
and every path that saves the game would write it into the guest device's own save, over that
kid's real progress.

The design answer was a separate state for "watching someone else's game" in which saving never
runs. The test answer was to give the test phone its own saved game first, then compare its saves
byte for byte after joining, while watching, after leaving, and after the host stopped. The host
streams only what moves, about 1 KB ten times a second; on one PC a thumb movement made the round
trip in 103 ms. The phone matched the host's 12 enemies, its loot and P2's position exactly.

## 5. When the test was wrong (20:09, 22:05)

The last two rounds let P2 roam with arrows pointing to the other player, and gave the second device
P2's sounds. Several times a new test failed and the game was right. Three examples:

- P2 "didn't mine" a rock because a rock even closer to it was the one it mined.
- P2 still "didn't mine" a rock placed outside my ship's range, because a nest sat nearby, and
  P2 shoots nests first. That's the game's own rule.
- The phone "played my ship's shots", which turned out to be P2's shots at rocks, 6 sounds for 7
  real shots.

Each time, the fix was to read the failing case before changing anything. The tests got sharper:
the rock check now uses a rock only P2 can reach, with nests nearby set aside for the check, and
the sound check compares sounds against P2's real shot count. The game code didn't change.

## What I took from it

**Test the real thing.** The relay's tests ran inside a stand-in; the bug lived in AppVerse's own
handler. The check that caught it was the deploy's own "does it answer?" against the live server.

**Know which copy is the source.** Two sessions on two machines edited the same game. Checking the
history before building saved a morning's work from a silent overwrite.

**Protect what the user owns, and prove it.** A kid's saved game is the most valuable thing on
that tablet. The test that compares it byte for byte is the one that matters most.

**When a test fails, read it before changing anything.** Several of today's failures were the test's
fault, not the game's.

This carries into teaching. When a student's answer doesn't match the key, the first job is to read
their work, not to mark it wrong. Sometimes the key is the thing that's wrong, and the student who
saw that deserves to hear it.

---

*By the end of the day the game's 28 test scripts ran 1,561 checks; one random bot-play check
missed once and passed on three reruns. Seven deploys went out, and every check passed except the
07:05 relay check, fixed at 17:23. All of this was tested in simulated browsers on one PC: the
boys haven't played it on two real devices yet, and that's the test that counts. Times come
from git and the ship kit's records; counts come from the test logs.*
