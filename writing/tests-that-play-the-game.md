# Tests That Play the Game

*Three checks said a game was fine. Playing it for fifteen seconds said otherwise.*

I keep a library of small browser games and classroom apps: single HTML files,
no install, most of them made for kids. Scheduled AI routines add to it every
day, 20 to 25 new apps a day, sorted into folders by kind. The best ones go on a
public Games Arcade that anyone can open on a phone.

That many new apps means nobody plays most of them before they're filed. So
there were checks:

- **A load test.** Open every page in a headless browser and fail on any error.
- **A daily review.** An AI reads each new app's code and rates it: ship it,
  minor issues, or broken.

Both were green. This is about the week I found out what they couldn't see, and
the test that finally could: one that actually plays the game. As with the rest
of my projects, I built it with heavy AI assistance. My part was deciding what
counted as evidence.

---

## 1. Green on load, broken in the hand

I played five new apps by hand one evening, all of which had passed the load
test. Two were broken:

- **Ricochet Arena**, an arena shooter, started the moment the page loaded.
  Nobody had touched it, and at 11.5 seconds it showed GAME OVER. A child who
  opened it and looked around for a second would lose before pressing anything.
- **Backronym Bash**, a word game, printed the word "null" on every writing
  screen, where a prompt should have been.

Neither threw an error, and that was the problem. The load test asked "did
anything crash?" and both pages answered honestly: no. The daily review had
read Ricochet Arena's code and rated it **ship it**, noting only a little dead
code. It said, fairly, that it couldn't click through a live browser.

So I built the test I'd been doing by hand. For each new app, on a phone-sized
touch screen and a tablet-sized one, it:

1. loads the page and records every error;
2. waits fifteen seconds without touching anything, and flags a "game over" or
   "you lose" that appears on its own;
3. presses the most Start-like button it can find, then plays for five seconds
   with taps and arrow keys;
4. flags the words *null*, *undefined* or *NaN* showing as text.

To check it, I gave it a page I'd broken on purpose: it ends itself on a timer,
it shows "null" in its score, and its Start button calls a function that doesn't
exist. All three faults were caught, on both screen sizes. A healthy page made
the same way came back clean.

**The rule:** "it didn't crash" and "it works" are different claims. A test
that never waits and never presses anything can only prove the first.

## 2. The check that saw one app in ten

The new test ran every night and reported to a status page in the house. For its
first day, it reported four new apps, all of which played fine.

The routines had made 45 apps over those two days.

The nightly check found new apps by asking version control what had changed.
But most of the library lives in folders deliberately kept out of version
control, because they're private and never published. Version control doesn't
report changes in folders it ignores. So the check quietly saw only the public
folders, roughly one app in ten, and its "all four play" was true and almost
meaningless.

I only found this because I'd gone looking for something else: I suspected two
daily checks overlapped, and wanted to merge them. They didn't. One of them
wasn't an app test at all. But counting the apps each one looked at turned up
the gap.

Now the check plays every app made in the last three days, in any folder,
skipping any it has already played unchanged. Its first full run played 51 apps
in 33 minutes. Fifty were real and all of them played. The 51st was my broken
page, hidden in one of the private folders, and it was caught. Each night's
results are now added under that day's code review, so the two can disagree in
one place.

**The rule:** before you trust a check's verdict, check its denominator. "All
four passed" says nothing until you know four out of how many.

## 3. The silent cat

With the test working, I pointed it at all 64 games on the public Arcade. They
come from 35 files, and 34 played cleanly. The 35th was a kids' beat maker,
and it turned up three bugs, each hiding behind the one before it.

- **Every tap on a phone logged an error.** The buttons tried to block the
  browser's default touch behaviour from a kind of listener where browsers
  ignore that. It's harmless-looking noise, and it's why the test flagged the
  app. Fixed by handling touch and mouse in one pointer handler.
- **The Cat voice never made a sound.** It called an audio function that
  doesn't exist, so every note failed before it started. The error went to a
  developer console no child will ever open; on the screen, the button simply
  did nothing, which looks just like a quiet sound effect.
- **The Dog, Frog and Lion notes never stopped.** Each started its sound twice;
  the second start failed, so the note was never recorded as playing and the
  key-up couldn't stop it. After one note each from those three, sixteen sound
  generators were still running with nobody pressing anything.

I could only find the second and third by measuring. A small script picked each
voice in turn, held a key for 600 milliseconds, let go, and counted
the sound generators still running two seconds later. Before the fix: zero
sound from Cat, and sixteen generators still running at the end. After the fix:
every voice played and stopped, zero left running. The app is a minified
production build with no readable source left, so the fix was a careful patch
to the built file, checked the same way.

**The rule:** a bug that fails silently looks exactly like a feature nobody
used. If you can't see it, count something.

---

## What the three have in common

| | the check said | what was true | found by |
|---|---|---|---|
| The ended game | no errors; code reads well | game over before the first tap | waiting fifteen seconds |
| The one-in-ten check | all four new apps play | 41 others never looked at | counting what it looked at |
| The silent cat | one console warning | a dead voice and stuck notes | measuring before and after |

None of the checks lied. Each answered a narrower question than the one I
thought I'd asked. The load test asked whether a page crashed, the review asked
whether the code looked right, and the first nightly check asked about the
folders version control could see. The fix each time was the same move a
teacher makes with a worksheet: don't grade the answer sheet, watch someone use
it.

---

*The test is a short Playwright script; a Python runner picks the apps, runs it
nightly, and reports to a status page at home. It is a smoke test, not a
replacement for a person: it can't tell whether a game is fun, fair or correct,
only whether it falls over when someone picks it up.*
