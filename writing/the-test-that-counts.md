# The Test That Counts

*The boys played the space game together on one tablet for the first time, and in a few minutes
they found what about 1,500 automated checks hadn't. The fix shipped the same afternoon, along with a
correction to my own test count.*

The last write-up, [Player Two](player-two.md), ended with a caveat: everything had been tested in
simulated browsers, "the boys haven't played it … yet, and that's the test that counts." On Sunday
8 November they played Squad Leader: Frontier together, one tablet between them: one flying my ship,
one flying the green co-pilot ship.

As before, an assistant wrote the code from my direction. My part was the report from the couch,
deciding what "fixed" meant, and running every public deploy myself from the ship kit.

---

## 1. The report

While they played, I sent this:

> The shield and laser buttons are on the same side as the co-pilot. It makes it confusing and
> harder to activate. Mirror the two sides for the pilot. Adjust the menu buttons to the center.

On one tablet, player one steers with the left half of the screen and player two with the right.
But player one's SHIELD, LASER and FIRE buttons still sat bottom-right, where they had been since
the game was single-player, and P2's two green buttons sat on the right edge too. Both kids were
reaching into the same corner. Nothing in the tests checked whose thumb was where; they checked
that the buttons existed, worked and didn't overlap.

## 2. The fix, and what it pushed out of place (12:35 to 12:47)

The change itself was small. A page class turns on exactly when P2's tablet buttons show (a touch
screen, a co-pilot on the same device, and the game being played) and turns off with them. While
it's on, player one's buttons move to the bottom-left, mirrored so SHIELD stays on the outer edge,
and the menu buttons move to the top middle. Solo play and keyboard play don't change at all.

The new test drives a game on two tablet sizes, turns the co-pilot on and off, and checks 40
things: each player's buttons sit on their own half, nothing overlaps, the layout goes back when
the co-pilot leaves, and tapping SHIELD in its new place really raises the shield.

The screenshots found what the checks didn't. The canvas draws three things that had quietly
assumed the buttons lived on the right:

- Amigo's message box, which now ran into the LASER button. It now sits above player one's
  buttons, wherever they are. On the smaller tablet, lifting it made it run into P2's missile
  button instead, so in co-op it now fits in the gap between the two players.
- The boss health bar, which left room on the right for buttons that had moved left.
- The "RAID!" warning, which checked for the menu in the top-right corner. With the menu now in
  the middle, it would have been drawn underneath.

Two smaller things are worth recording because they keep happening. The build broke on an
apostrophe: a help sentence saying "player one's SHIELD" sat inside a single-quoted JavaScript
string, the same mistake as two days earlier. The fix was to reword the sentence so it had no
apostrophe. And one new check failed when the game was right: it looked for the shield under a
property name the game doesn't use. The shield had gone up. The test was fixed, not the game.

The home copy, the one the boys were holding, had the new layout within about fifteen minutes of
the report; a reload picks it up. The public arcade copy shipped at 13:51 after I ran its step.

## 3. The flaw that was already there (15:05 to 15:23)

The same screenshots showed one more problem, and it wasn't new. On the smaller tablet, P2's
shield button covered the zone name under the minimap ("Home Reach"). P2's buttons had sat there
since Friday. The tests passed because no test asked whether a button covered something the
canvas draws, as opposed to another button.

I left it out of the first fix to keep that change to what the boys had reported, and made it its
own round. P2's buttons still centre on the right edge, but they move down below the zone name,
and below the Beacon button when Rogue mode shows one, and they never leave the screen. The test
now covers three tablet sizes and Rogue mode. It also found a 3-pixel overlap on the large tablet
that nobody would have noticed. That shipped to the arcade at 15:23.

## 4. The count I had to correct

After the first fix I reported "all 32 test scripts pass", and after a rerun "31 of 32". Both were
wrong in a way that matters.

Two of the 32 scripts test the original Squad Leader, a different game, and they need a file
name to run. My loop didn't pass one, so both crashed at once, and the loop judged each script by
the last few lines of its output. A crash ends in Node's version number, not the word "FAIL", so
both crashes counted as passes. The honest number was 30 Frontier scripts, and in that run one
of them, test7, had failed a check. Run alone, test7 passed four times out of four. In a later
run test2 did the same, and passed twice when run alone. I saw this only because a third run saved each script's output to its own
file, and two of the files had no passes in them at all.

The loop now counts the lines that say FAIL and leaves the two Squad Leader scripts out. The last
run of the day, on the final build, had 30 scripts and no failed checks.

## What I took from it

**Real use is a test the suite can't replace.** About 1,500 checks confirmed the buttons worked. Two
kids on one tablet found that they worked in the wrong place, within minutes.

**A screenshot is a check.** Each of the three knock-on problems in section 2 showed up in a
picture before any assertion caught it. Looking at the result is part of testing it.

**Fix what was reported, then fix what you noticed.** Keeping the old overlap for its own round
meant the boys got their fix in ten minutes, and the second fix got its own test.

**A count is a claim.** "31 of 32" sounded precise and wasn't. The question to ask of any count is
how the code decided what went into it.

In the classroom, the same order applies. When a student says the instructions confused them, the
first fix is the one they asked for, today. The broader rewrite can come after, done properly.

---

*Times are from git and the ship kit's records (Eastern time); test counts are from the saved test
logs. The boys played on one shared tablet; two devices at once is still untested by them.*
