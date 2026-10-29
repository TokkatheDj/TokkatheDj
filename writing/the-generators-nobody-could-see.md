# The Generators Nobody Could See

*I wrote a rule and the number didn't move. The reason was fourteen app generators that
the list I trusted never showed me.*

Every night, AI routines build new apps for my collection: kids' games, party games,
classroom tools, music toys, around twenty a day across twenty-odd categories. A nightly
check plays each one and scans it for accessibility problems. Anything that fails stays
off my public Games Arcade until someone fixes it by hand.

In late October I gave every generator a written accessibility block: contrast pairs,
named buttons, real switches. Two days later I counted again, expecting the failure rate
to drop. It didn't. This is how the count led me to generators I didn't know were running,
and what I changed once I could see all of them. As with my other projects, I built it
with heavy AI assistance. My part was deciding what to believe.

---

## 1. The number that didn't move

The count split the apps by when they were made:

| apps from the main generators | failing the accessibility scan |
|---|---|
| before the block | 7 of 29 (24%) |
| with the block | 10 of 44 (22%) |
| with the block and a stricter contrast rule | 8 of 33 (24%) |
| **from generators that never got the block** | **15 of 27 (56%)** |

The block wasn't being ignored. Apps made after it used the exact wording it asked for,
such as real toggle buttons, where none had before. But the failure rate stayed flat, and
a whole group of apps was failing at more than twice the rate. Those came from four
categories (data viz, educational, health, art) whose generators I had never found.

**The rule:** when a fix doesn't move the number, check what's in the sample before you
change the fix.

## 2. The list that wasn't the list

I'd looked for those generators before. The tool that lists scheduled tasks returned 21,
and none of them made data viz apps. I'd assumed they lived somewhere else.

They didn't. The listing paged in a loop and never reached the end. Claude Desktop also
keeps the full list in a local file, and that file held 28 tasks, each with the id needed
to fetch it directly. Reading every one changed the picture:

- All 14 app generators on that list were **switched on**, and **none had the
  accessibility block**.
- Four of them were the "missing" ones.
- Five more **duplicated** generators I'd already fixed. Kids games, table games,
  classroom tools, music apps and adult puzzles each got two apps a night: one from the
  fixed prompt and one from a copy of the old one, dropped into the same folder.

So the "with the block" rows in my table were partly apps made without it, and the 56% was
real.

**The rule:** an inventory from one tool is that tool's opinion. Find a second source
before deciding something doesn't exist.

## 3. Patch nine, or move nine

Pausing the duplicates was easy. Nine generators existed only as these desktop tasks,
and they still needed the block. Each prompt sat inside a session config of roughly
100 KB. Editing that blind over an API, nine times, could break all nine.

The other option was to move them. My main generators already run on a second machine
from plain text files in git, and each run starts by reading a registry of every app
already built, so it doesn't rebuild an old idea. I turned each of the nine prompts into
one of those files, with the registry step, its real save folder and the accessibility
block. I gave each a slot in the schedule, and copied their 292 existing apps across so the
registry knew what they'd already made. Then I paused the nine old tasks.

Now every category has one generator, in one place, and a rule change is a single commit.

**The rule:** if a rule lives in nine places, the fix is making it live in one, not
editing it nine times.

## 4. Two answers, not one criterion

Contrast was still most of the failures, six of the last eight. I looked at the actual
colours instead of the totals. Every one of the six fell into one of two patterns:

- **A dim label colour the generator made up** for hints and labels on dark panels. There
  were seven different greys and slates, from 2.8:1 to 4.3:1. The rule said "must reach
  4.5:1" and gave one passing example. The model treated that as a suggestion and picked
  something slightly darker every time.
- **White text on bright green or orange buttons**, at about 2:1. The rule already
  forbade it.

The rule now names the colour: muted text is `#a9a3c0` or lighter, on panels no lighter
than `#3a3550`, where it still reaches 4.8:1. Bright fills always take dark text.

**The rule:** when a model keeps missing a threshold, it's choosing. Give it the answer,
not the test.

## 5. Everything looked the same

My sons tried four of the new games on an iPad and kept all four. My question afterwards
was why every game looks and sounds alike. So I measured all 628 apps made in October:

| | |
|---|---|
| main font is the Windows default (Segoe UI) | 47% |
| main font is Trebuchet MS | 15% |
| sound made only from plain oscillator tones | 78% |
| apps with reverb | 36 of 628 |
| apps using recorded samples | 1 |

Nothing in any prompt said anything about look or sound. "Make it polished" with no
direction gets the model's default every time: system font, gradient, rounded pills, a
sine beep.

So every generator got an identity block, written the same way as the contrast fix,
with answers rather than criteria:

- **Ten style cards.** Paper Cutout, Chalkboard, Neon Arcade, Storybook, Toy Blocks,
  Retro Terminal, Watercolour, Comic Panel, Swiss Poster and Clay, each with exact fonts,
  colours and shape language. I checked every text-and-fill pair on every card before
  shipping. One green failed, at 3.9:1, and was darkened.
- **Eight sound kits**, each a recipe: plucked strings (Karplus-Strong), an FM marimba,
  chiptune, woodblocks and shakers, toy piano, warm pad, cartoon effects, music box. No
  bare beeps, every sound shaped, and each app gets its own short signature tune.
- **Rotation.** Each app tags its header `[style: … / sound: …]`, and the next run avoids
  whatever its category used in the last five apps, read from the same registry that
  stops repeated ideas.

**The rule:** a model with no direction isn't neutral, it's predictable. If you want
variety, name the options and rotate them.

---

## What they have in common

| | looked like | what was true | found by |
|---|---|---|---|
| The flat number | the block didn't work | the sample held apps made without it | splitting the count by source |
| The missing generators | they didn't exist | the list never reached the end | a second source, a local file |
| Nine copies of a rule | patch each one | move them to one place | asking where the rule lives |
| Contrast failures | a vague rule | two exact patterns | reading the colours, not the totals |
| Same-looking apps | bad luck | no direction at all | measuring 628 apps |

The accessibility re-count and the first identity count run on 1 November, the first
nights where every new app comes from a generator with both blocks. I'll add the numbers
here, whichever way they go.

---

*The nightly check plays every new app at phone and tablet sizes and scans it with
axe-core. `identity_count.py` measures fonts, backgrounds, sound and style tags across
any date range. The generators are plain-text prompts in git, run by Windows Task
Scheduler through the Claude CLI.*
