# The Client Is a Kid

*Redesigning a face in one evening, and the one note that mattered.*

Amigo, the local AI assistant I built for my house, has a face. It's a cartoon
coquí — a tiny frog from Puerto Rico — on a web page that runs on a tablet, on a
small screen in the house, and on my watch. It blinks, looks around, moves its
mouth when Amigo talks and falls asleep at night. My two sons are the people who
actually look at it.

One evening I decided the face looked too robotic and set out to fix it. Five
versions later, the version that shipped was the one my son had preferred for
weeks, before anyone asked him. This is how I got there the long way
round, and what I'd do differently.

As with the rest of Amigo, I built this with heavy AI assistance: an assistant
wrote most of the code, working from my direction. That made each version cheap
— minutes, not days — which turned out to matter, because the expensive part of
this job was never drawing the frog. It was working out which feedback to trust.

---

## Round 1: deciding what "less robotic" meant

The face I started with was a silver robot frog, and every detail said so. It
had panel seams across its head, a bolted-on chin plate, cheek vents, eye
"turrets", and a 130-millisecond blink like a camera shutter. All of that was
deliberate, and all of it matched the app icon.

So "less robotic" was ambiguous. It could mean *move* less like a machine, or
*be* less of one, and the second would change a character that also lived on
the icon, the watch and the kids' pixel panel. I stopped and asked myself which
I meant, and picked a middle path: keep the silver and the silhouette, take off
the machinery, add soft shading, glossy eyes and blushing cheeks.

The motion got the same treatment. Eyelids that slide down and lift more slowly
than they fell. Eyes that dart to a new spot and settle, rather than drifting
like a camera on a gimbal, with a tiny tremor while they fixate. A mouth that
moves in syllables instead of a sine wave. A throat that puffs twice now and
then, the way a coquí calls: *co-QUÍ*.

It was much better. By my standards.

## Rounds 2 and 3: tuning to my own taste

"Cuter — maybe add light blue somewhere" became big light-blue eyes with
sparkles, rosier cheeks and a blue-silver tint. That came back as "less blush,
eyes are too light," which was a five-minute fix.

Notice the pattern. Every note so far was mine, and every one was about
*degree*: more of this, less of that. I was polishing in a direction I had
chosen myself, and nothing in that loop could tell me the direction was wrong.

## Round 4: "not nice like the pixel"

Then my son looked at it and said the face version wasn't nice looking like the
pixel one.

That sentence is not a design spec, and if I'd treated it as one I'd have made
it worse. It's a comparison, and a comparison points at a reference. The
reference was the pixel coquí: a 32 × 32 drawing of the same character that
lives on an LED panel in his room and in the games, flat silver with chunky
navy outlines, bright blue eye rings, a square sparkle and a little smile. He'd
been looking at that frog every day for weeks. Mine was a new frog wearing the
old one's name.

My version was better on everything I'd been measuring: shading, motion,
detail. It was worse on the one thing he cared about, which was that it was
*his* frog.

My first move overcorrected. I put the actual pixel art on the screen, scaled
up and crisp, with the animation rebuilt to move in whole pixels like the
original GIFs. It was faithful, and it was blocky on a large screen. The next
note fixed that: smooth it out — round the head, the eyes and the mouth.

## Round 5: his frog, drawn better

That turned out to be the right answer. I redrew every shape of the pixel
coquí as a smooth one, in the same place and at the same size: the oval head,
the round eye bumps, the navy-blue-navy eye rings, the dot cheeks, one curve for
the smile. The colours stayed flat, with no shading. Then the natural motion
from round 1 went back on top: sliding lids, gliding pupils, a mouth that opens
and closes.

The character stayed the same and only the drawing changed, which was what had
been asked for all along.

The background went the same way. I offered four options. The rainforest at
night won: swaying leaves, drifting fireflies, the coquí's real home. "Make it
blue instead of green" took one change to a colour table. The next message was,
in full, "SOOOO GOOOD".

The same drawing now runs on my watch, rendered from the same shapes so the two
match.

---

## One bug, for old times' sake

The fireflies came with a bug of the kind my last write-up was about. They
weren't showing up, so I measured. The canvas they're drawn on had 13,405 lit
pixels, with 22 of the 24 fireflies outside the frog's ring where they should
have been visible. On screen there was nothing.

The page was right and the screen was wrong. The swaying leaves were animated,
the browser gave them their own compositing layer, and that layer painted over
the fireflies' canvas despite both sitting at the same depth on the page.
Moving the fireflies one layer up fixed it. The measurement said "working" and
the screenshot said "not". The screenshot was the one that mattered.

---

## What I'd do differently

**Treat "not like X" as a pointer.** When a kid compares, the useful information
is the X. I had a working reference on the wall of his room the whole time and
didn't think to look at it before I started.

**Know what you're optimising.** I was optimising for realism and polish. He was
optimising for recognition. Neither of those is wrong, but only one of them was
the client's.

**Changing the character is a different job from changing how it's drawn.** I
asked myself early whether a change was to *motion* or to *identity*, and then
answered the identity half on my own. It belonged to the person who'd lived with
the character, and he was in the next room.

**Short loops let the kid steer.** Every version took minutes and was on the
screen before anyone lost interest. With a pair writing the code, trying a
version cost almost nothing, so the scarce resource was judgement: which note to
act on, and which one was really about something else. One note in the whole
evening changed the direction. It came from the youngest person in the house.

This carries straight into the classroom. Students judge new things against the
things they already know, and "it's not like the old one" is usually the most
precise feedback they can give. It's worth asking which old one.

---

*Amigo is a personal project and is not on the public internet. The face is one
HTML page with inline SVG and a canvas, no framework; the watch face is a Wear OS
Watch Face Format package built from the same shapes.*
