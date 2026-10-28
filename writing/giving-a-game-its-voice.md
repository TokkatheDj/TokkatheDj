# Giving a Game Its Voice

*My sons are five and three. They know exactly what Amigo sounds like, so his voice
in a game had to be his.*

Amigo is the assistant that lives in my house: a little coquí frog on a screen, with a
voice, a face and a lot of opinions about bedtime. One evening I turned a small
browser puzzle game into **Amigo's Candy Math**. You link matching tiles, they add
up, and Amigo cheers you on and asks little sums. It's a single HTML file, now on my
public Games Arcade, and it was built in two rounds with heavy AI assistance in one
evening.

The first round had a cheering Amigo, four themes and a Math Coach. My boys liked
it, but it didn't get much of a reaction. So the second round came with a list of notes. One of
them was marked as a hard must: **fix Amigo's voice.** This is about that note, what
it took to get right, and a deploy step that vanished on the way.

---

## 1. Any voice is not his voice

The first version spoke through the browser's built-in voice. The game sent text to
the browser, and the browser read it aloud. It worked, and it was the wrong answer:

- **It sounds different on every device.** One tablet has one voice, a phone has
  another, and some browsers have none at all.
- **It's not Amigo.** At home he talks through a speech engine called Piper, with
  one particular voice at a slightly slow speed. My sons know that voice. A
  stranger's voice coming out of his face isn't him, however clearly it talks.
- **It might not play at all.** I'd shared the game as a private web page, and pages
  like that run in a locked-down frame where the built-in voice isn't guaranteed.

Amigo's real voice lives on a computer in my house, and a game on the internet
can't call it. So the voice had to travel inside the game. A small script loads the
same voice with the same speed and the same respellings Amigo uses at home. It
records every line the game can say, squeezes each one into a small audio clip and
writes the clips into the HTML file itself. The game plays them through the same
sound system as its music, so the volume slider and mute button work on him too.
The browser's voice is kept only as a back-up for a line with no recording.

**The rule:** "it talks" and "it sounds like him" are different features. With
children, the second one is the feature.

## 2. "Hi" came out as "Oh"

I can't listen to audio while I'm building, and listening to a hundred clips by ear
is how you stop noticing them anyway. So I gave the clips to a second ear: a speech
recogniser, which writes down what it hears.

The first batch came back like this:

| Amigo was meant to say | the recogniser heard |
|---|---|
| Hi! I'm Amigo! Let's play! | Oh, I'm Amigo. Let's play. |
| seven | Todah! |

To make clips run straight into each other, the script trimmed the silence off
both ends. It cut too hard: the soft start of "Hi" and the hiss at the front of
"seven" were quiet enough to count as silence. A gentler cut-off, plus a short
lead-in kept on purpose, brought "Hi" back.

**The rule:** if you can't hear the result yourself, get something else to listen,
and read what it writes down.

## 3. Five said "Bye!"

The lines have numbers in them: "Level 4!", "What's 3 plus 2?". The first design
recorded the words and the numbers separately and joined them up as the game
needed them. That makes about a hundred clips, and any number works.

The recogniser didn't think much of it. On their own, the numbers came out as:

| clip | heard |
|---|---|
| 5 | Bye! |
| 7 | Summer! |
| 10 | Huh? |
| plus | Who is? |

Single short words are a hard test for a recogniser, so some of that is its
problem, not the voice's. But it matched what you'd expect: a word spoken alone is
clipped and flat, and gluing clipped words together makes a voice that sounds like
a train announcement. Three-year-olds are an unforgiving audience for that.

So the script now records **whole lines with their numbers in**, for every number
the game can actually use. Every adding question up to 10, every taking-away
question, every level up to 25, every chain length, every tile size. That's 351
clips, against the earlier hundred, and the file grew to about 2.8 MB. The separate
number clips stay as a back-up for anything outside those ranges.

Played back:

| Amigo was meant to say | heard |
|---|---|
| What's 3 plus 2? | What's 3 plus 2? |
| Level 7! You're so smart! | Level 7, you're so smart! |
| Whoa! 128! | Well, 128. |

One word still fails every time: Amigo's call, "ko-KEE!". The recogniser hears it
as "okay" or "who could eat". That one I left alone. It's the same respelling Amigo
uses at home, and the recogniser isn't the ear the game is for.

Then a play-test ran in all six themes at two screen sizes, recording every line
Amigo spoke and where the sound came from. Every line played from his own recorded
clips. The browser's voice was used zero times.

**The rule:** a measurement tells you where to look, not what to decide. It caught
the clipped "Hi". It also failed "ko-KEE", which was right all along.

## 4. The client is three

The voice was the hard must, but the same list had the real design brief in it.
Round one's Math Coach asked things like "What's double 16?" and "half of 32". That's
fine for the game's numbers and useless for a three-year-old.

Round two's questions are adding and taking away up to five, then up to ten.
Each comes with pictures to count: 🐟🐟🐟 + 🐟. For taking away, the ones
taken away fade out, so the answer is the number still bright. The board waits
while Amigo asks. A wrong answer greys out and he says "Try again!", in his own
voice. The themes stopped being colour swaps and became places: an ocean with
fish and bubbles, a volcano with glowing rocks and embers. The spooky theme was
redone as the kind of spooky a small child enjoys: smiling pumpkins, ghosts with
rosy cheeks, a soft moon. No skulls.

None of that came from me looking at the game. It came from how two small
people took to it.

## 5. The deploy step that vanished

The last surprise had nothing to do with sound. My deploys run from a one-page
list. I queue a step, and later I tap it on my phone. I queued "put Amigo's
Candy Math on the Arcade", and when I said "ship it", it wasn't there.

A nightly script adds its own step to the same list: "put tonight's tested apps on
the Arcade". To avoid piling up old copies, it first removed every waiting step
whose name began `arcade-add-`, the prefix it uses. My hand-queued step used the
same prefix, so it went in the bin too. Nothing errored, and nothing logged a
loss.

The fix: each script now removes only steps that it wrote itself, identified by an
"author" field every step already carried, never by what the step is called. The
weekly health check had the identical habit with its own prefix and got the
same fix. Both have a test that reproduces the lost step and fails without the
fix.

**The rule:** clean up only what you can prove is yours. A name is a guess about
ownership; a field that records who wrote the step is a fact.

---

## What the five have in common

| | it looked fine because | what was true | found by |
|---|---|---|---|
| The browser voice | it talked | it wasn't him | knowing who it's for |
| "Hi" → "Oh" | every clip played | the start was cut off | a recogniser reading back |
| Numbers on their own | any number worked | each one was clipped | the same, then whole lines |
| Questions for a three-year-old | the maths was right | the child couldn't do it | watching them play |
| The vanished step | nothing errored | a step was thrown away | going to tap it |

Each time, the check I had answered "does it work?" The question that mattered was
"is it right for these two?" Those are different questions, and only the people the
thing is for can answer the second one.

---

*The voice recordings are made by one short Python script with Piper, the same
engine and voice Amigo uses at home, and the game plays them with the browser's
Web Audio. The check that read the clips back is faster-whisper, the speech
recogniser Amigo uses to hear. The play-test is Playwright. The game is a single
HTML file of about 2.8 MB, on the public Games Arcade.*
