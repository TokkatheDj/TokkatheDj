# Count the Printed Rows

*Building a talking frog for my sons as a circuits novice, and why the object on
the desk always wins.*

On my desk there's a breadboard with a Raspberry Pi Pico on it, and the Pico is
a coquí: the tiny Puerto Rican frog that's also the face of Amigo, the local AI
assistant I built for my house. Press its button and it answers in one or two
playful sentences, as a frog who wants to be an astronaut. Recently it grew a button for each of my sons, an arm that waves when it talks,
and an infrared remote that starts games on the LED strip.

I teach maths. I am not an electronics person. As with the rest of Amigo, an AI
assistant wrote the firmware, the desktop code and the step-by-step wiring
guides, working from my direction. In software that partnership has a safety
net: tests catch most of the assistant's mistakes before I see them. In
hardware the net had a hole in it. Almost every problem in this build came
from the gap between a *description* of a part and the *part itself*. The
description was usually confident and the part was usually right.

---

## 1. Hole 23 was not row 23

The first wiring guide said to put the button's wires in "holes 23 and 25". I
put them in rows 23 and 25, the numbers printed down the side of the
breadboard. The button was dead.

The guide meant the Pico's *pin* numbers. Pin 23 is a ground and pin 25 is an
input, and with the board's USB plug at the top they sit beside printed rows 18
and 16. Rows 21 and up were past the end of the Pico and connected to nothing.
Both numbers were correct; they were just counting different things, and only
one of them was printed on the thing in my hand.

![The breadboard with the Pico covering printed rows 1 to 20. Its pin numbers run 40 down to 21 beside them, so pin 25 sits at row 16 and pin 23 at row 18. Rows 21 to 25, where the wires went, connect to nothing.](img/printed-rows.svg)

Every guide now gives the printed row numbers, with the board drawn the way it
actually sits on my desk. The rule I took from it is simple: **give
instructions in the labels the reader can see.** A pin number is a fact about
the chip. A printed row is a fact about the desk.

## 2. The remote that started the wrong game

The kit came with a little infrared remote. The guide used the key codes from
the most common version of that remote, and the first time I pressed OK, which
should ask the coquí a question, it started a game of Freeze Dance.

My remote is a different variant with the arrows on top, and its codes are
different. The fix took two minutes: I pressed all seventeen keys in order while
the board printed each code, and those became the table. Any key the program
doesn't recognise is now logged by number, so the next surprise will explain
itself.

A table from the internet describes *a* remote. Reading the codes off the
device in your hand describes *yours*.

## 3. The big button was a guitar pedal

I had a big chunky button from Micro Center, and the plan for a two-player
buzz race was built around it. When I sent a photo, it turned out to be a latching
guitar footswitch: six pins, press it once and it stays on, press again and it
stays off. That's great for a pedalboard and useless for a reaction-time game,
where the button has to spring back.

Nothing in the plan was wrong except the name I'd given the part. One photo
fixed that faster than any amount of description would have.

## 4. If we can't start right

So we used the small yellow push buttons from the kit, one per son, on jumper
wires. They worked. They were also awful: the buttons' legs are too thin to
grip in a jumper socket, they wobbled loose, and when I bent the legs to make
them hold, the legs started to break.

I said, more or less: *if we can't start right, I don't want to start at all.*
The circuit worked, but a kid will hit a buzzer as hard as he can,
and a button that falls out mid-game is a broken game. So we stopped. The plan
now is proper arcade buttons with quick-disconnect wires, and the reaction game
waits until they arrive.

That was the right call, and it cost nothing but a few days. **A working
circuit isn't a finished one** when the people using it are children.

## 5. The wave that was one twitch

The arm is a small hobby servo that waves gently whenever the coquí starts
talking. The first real wave was one quick twitch.

The firmware moves the arm in small timed steps. But when someone walks past,
the motion sensor triggers a greeting with a sweep of the light strip and a
chirp, and that held the main loop for about 0.6 seconds in the middle of a
wave. When the loop came back, the code dutifully "caught up" on every step it
had missed, all at once: sixteen moves in one instant, which the servo
rendered as a jerk. A late step now *pauses* the wave instead of skipping
ahead.

What made that fix trustworthy was a set of small simulators that run the
exact firmware file, unchanged, against fake pins and a fake clock. They can
hold the loop for 0.6 seconds on purpose and check that the arm still waves
smoothly afterwards. The same trick covers the remote decoder and the light
games. None of them replaced looking at the real arm, but they meant each fix
was checked before it went near the board.

## 6. A stop button for a talking frog

The coquí sometimes talks for too long, so I asked for a way to stop him
mid-sentence. This one took three tries, and the second try taught me the most.

The simple way the desktop plays sound can't be interrupted from another part
of the program. Tested: a five-second sound kept playing for five seconds. So
the second try chopped each answer into one-second slices and checked for a
stop between them. It worked, and it sounded terrible. Each slice cost about a
quarter of a second of silence to start, and the coquí's voice has no pause
long enough to hide that. My verdict was that he didn't sound good: a lot of
pauses and sound gaps.

The test had passed. My ears had not. The third try plays the whole answer
through a lower-level Windows audio call that can be cut off instantly, so the
voice is continuous again and the OK key stops him mid-word. Then one more
note from the listener, "a little fast", and the voice now runs at 0.9 speed.

---

## What I'd do differently

**Ask for a photo before the guide, not after.** Two of the six problems
dissolved the moment a picture showed what was actually on the desk. With an
AI pair writing the instructions, a photo is the cheapest test there is.

**Describe what the reader can see.** Printed rows, not pin numbers. Wire
colours, not signal names. The wiring guides are now pictures first, because
I'm the reader and I'm a novice.

**Read values off the real thing.** Key codes, which way the servo sits, which
button is which. The device is the specification.

**Build it sturdy before you build it clever.** The fun parts are the games and
the voice. None of that matters if a button falls out.

**Let the listener have the last word.** A passing test told me the stop button
worked. Listening told me it had ruined the voice.

This carries into my classroom, where I write instructions for a living. The
student is always holding the actual worksheet, the actual calculator, the
actual breadboard. Instructions that point at what's in front of them work;
instructions that point at what's in the textbook sometimes don't.

---

*The coquí is a Raspberry Pi Pico running MicroPython: buttons, a buzzer, an LED
strip, a motion sensor, an SG90 servo and a VS1838B infrared receiver. It
plugs into a Raspberry Pi, which relays it to the desktop, where a Python
program talks to a local language model and a local text-to-speech voice.
Nothing leaves the house. Code private.*
