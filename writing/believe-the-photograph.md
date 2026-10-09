# Believe the Photograph

*Three bugs from a home AI project that passed every test I had.*

I built a thing called Amigo — a local-only AI assistant that runs on a desktop
in my house. No cloud, no account, nothing leaves the building. It answers out
loud through a local text-to-speech voice, drives the smart lights, runs games
for my two sons, draws on a pixel panel in their room, and puts a face on a
smartwatch. Underneath there's a microcontroller wired to an LED strip, a
buzzer and a motion sensor; a Python server holding it together; and a browser
app that runs the games.

This is not a writeup of the features. It's a writeup of three bugs, because
the bugs are the part I actually learned from — and all three have the same
shape:

> The code was right in every case I tested, and wrong in a case I had not
> reached yet.

One more thing up front. I built Amigo with heavy AI assistance; a lot of this
code was written by an assistant working from my direction. What I brought was
the part that turned out to be the scarce half: deciding what counted as
evidence, and refusing to accept a pass I couldn't explain. Every bug below
was caught by that, not by the code being typed more carefully.

---

## 1. The layout that never applied

The watch page had a stylesheet that adapted the layout for a round screen:

```css
@media (shape: round) { /* padding, centring, the lot */ }
```

Reasonable. Documented. Wrong for three weeks.

The browser on the watch does not answer that media query. Not "answers it
badly" — does not answer it. So every rule hiding behind it never applied at
all, and the text box ran to both edges of a display that has no pixels in the
corners. The desktop browser, where I did all my checking, showed a tidy
rounded mock-up. It looked perfect in the only place I was looking.

I found it by pulling a screenshot off the actual watch and putting it beside
the mock-up I had been trusting.

The fix was to stop asking. That page is only ever opened on a round watch, so
there is no case to switch on: the round layout is now unconditional. While I
was in there I wrote down the geometry for whoever moves something next — on a
456 px round screen, the visible width a fifth of the way down is only about
334 px. A full-width button with a centred label survives that. Text does not.

Two more turned up the same week, both on the watch face itself rather than the
page, and both while I was wearing it:

- The clock looked perfectly centred on my monitor and sat visibly right of
  centre on my wrist. I had centred it against a five-character time — `12:45`
  — and nine of the twelve hours are four characters wide. My watch was quietly
  wrong for three quarters of the day.
- Then the always-on face, which right-aligned its time against an element that
  ambient mode hides. It was balanced against something invisible.

Not one of the three was findable from a desktop browser.

**The rule I came away with:** for anything watch-shaped, believe the
photograph. A screenshot off the device costs two seconds. There is no excuse
for not taking one.

---

## 2. The stop button that made it last longer

The games take over the house lights. A round of *The Floor is Lava* turns
every bulb red. When a game ends, the room goes back to normal — and there's a
watchdog that also hands the house back on its own after 90 seconds of silence,
so a crashed game can't leave the place red all night.

There's a Stop button. Its entire job is to end a game immediately.

Stop called a routine that cleared the game state and, while it was there,
updated the "last activity" timestamp. That looks like ordinary bookkeeping.
It is the opposite, because the 90-second watchdog measures its silence *from
that timestamp*.

So: a game wedges. The room is red. The watchdog is going to rescue you at
t=90. At t=89 — which is precisely when a person gives up and reaches for the
button — you press Stop. The timestamp resets. The room stays red until t=179.

**The button whose only job was to make it stop made it last twice as long.**

Every test I'd run pressed Stop within a few seconds of starting a game, where
the behaviour is invisible. It took reading the code with the question "what
is the worst possible moment to press this?" to see it. The fix was to delete
one line, plus a second thing the same review turned up: Stop now sends the
lights home itself. With a properly wedged game, nothing else ever will — the
component that normally sends the all-clear is the one that died.

**The rule:** the dangerous inputs aren't the malformed ones. They're the
well-formed ones that arrive at the worst possible time. Ask when, not what.

---

## 3. The test that could not fail

I wanted to prove that a game leaves the rest of the house alone — that a round
of Lava reddens the play area and doesn't touch the other rooms.

So I ran one. Started a game, watched the other bulbs, and they came back
completely unchanged. Clean pass. Exactly the result I wanted, which should
have been the first warning.

The reason nothing changed was that the game engine wasn't running. My start
command went into a queue and sat there. No game ever ran. I had proved
that a room full of lights is unaffected by a game that does not exist.

The tell was in the log timestamps. The light changes were spaced 4.0 seconds
apart — the even rhythm of a script walking through a list of colours. A real
game's calls land 3.1 to 6.3 seconds apart, because a real game is paced by a
clock and a speaking voice, not a loop. The spacing was the giveaway, and the
spacing is in the log every time.

**The rule, and it's the one I keep coming back to:** a test that cannot fail
has not passed. Before believing a green result, I now have to be able to say
what a red one would have looked like. If I can't describe the failure, I
haven't run a test — I've run a ritual.

---

## What the three have in common

None of these were found by writing more careful code. Each needed a different
kind of evidence:

| | invisible to | found by |
|---|---|---|
| The layout | every desktop browser | a photograph of the real device |
| The stop button | every test that pressed it early | asking what the worst moment was |
| The house test | the result I was hoping for | the timestamps in the log |

The common failure wasn't in the code. It was in me accepting a signal that
felt like proof. A tidy mock-up on the wrong screen, a stop button that stopped
things during testing, a row of unchanged bulbs. Every one of those is what
success looks like, right up until you check what's underneath it.

The last word, though, doesn't go to any of this. When the games were finally
finished and reviewed and tested three separate ways, I handed the tablet to my
sons. Their first note was that the lights were too slow. I turned the speed up
and gave it back. They played another round and said that felt right, so that's
what it ships as.

I'd tested that app more thoroughly than anything I've built. It took them one
round to find the thing I'd got wrong.

---

*Amigo is a personal project — roughly 800 KB of source across a Python service
and game engine, a microcontroller firmware, four browser apps and a Wear OS
watch face. It runs on one desktop, with a Raspberry Pi added later as its front door, and
it is not on the public internet.*
