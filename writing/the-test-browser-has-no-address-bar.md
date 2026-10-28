# The Test Browser Has No Address Bar

*Every check passed. Then the game I'd made for my sons ran off the bottom of a real phone.*

On the morning my sons were going to play **Amigo's Candy Math**, a maths game I'd built
the night before, I opened it on my phone. The bottom row of tiles was half off the
screen.

That game had been through a lot of testing. A script played it at phone and tablet
sizes, in all six of its themes. An accessibility scanner checked every screen, and the
nightly check that guards my public Games Arcade had passed it. I'd looked at screenshots
of the bottom row myself. Every one of those checks ran in a test browser, and a test
browser has no address bar.

This is about the bug that hid in that gap, the check I built to see it, and the ways
that check was wrong before it was right. As with my other projects, I built it
with heavy AI assistance. My part was deciding what counted as evidence.

---

## 1. "Full height" depends on whose phone

The game sized itself with a line of CSS that says "be as tall as the screen":
`height: 100vh`.

On a real phone, "the screen" is a moving target. The browser's address bar and toolbar
take up part of it, and they slide away as you scroll. Mobile browsers measure `100vh`
against the *tall* version, the screen with the bars gone, even while the bars are
showing. So the game laid itself out about 180 pixels taller than what you could see, and
the page couldn't scroll. The bottom row ended up under the toolbar.

A test browser has no bars. Its "screen" is exactly the window it was given, so `100vh`
was always right there. Every check I had was looking through the one window where the
bug couldn't happen.

To reproduce it, I made the test browser behave like the phone. The visible area was the
real one, 664 pixels on an iPhone 14 with Safari's bars showing. Every `vh` in the page was
measured against the full 844. Then I measured the board:

| phone (bars showing) | before | after the fix |
|---|---|---|
| iPhone 14 | board ends 61 px below the screen | fits |
| iPhone SE | 96 px below | fits |
| Pixel 7 | 12 px below | fits |
| a small Android | 61 px below | fits |
| a phone turned sideways | 162 px below | fits |

Five of the seven sizes I measured were cut off, and the fix made all seven fit. CSS has a
unit for the *visible* height, `dvh`, and the game now also measures what's actually on
screen when it sizes the board, re-fitting whenever the bars slide in or out.

**The rule:** a test environment is the real one with the hard parts taken out. Know
which parts, or you'll test everything except the bug.

## 2. If it happened once, where else?

One fixed game didn't tell me how many others had the same problem. The Arcade has
about 95 games, and around 35 of them use `vh` somewhere.

So I turned the reproduction into a check, `phone_fit_check.js`. It opens a page the way
a phone with its bars showing would, presses Start, and fails if a button or the play
area ends below the screen where nothing scrolls to it. It runs on two phone sizes and opens
each game both ways a child can: as a tile inside the Arcade, and as a direct link.

Before trusting it, I pointed it at the bug it was built for. It failed the old Candy Math
by 61 pixels, exactly what I'd measured by hand, and passed the fixed one. Then I ran it
over the whole Arcade: 164 checks.

That turned up something I hadn't expected. Inside the Arcade's frame, the old Candy Math
*fit*. In a frame, `vh` is the frame's height, not the screen's, so the bars don't come into
it. The bug only bit on a direct link, which was exactly what I'd sent to my phone that
morning.

**The rule:** before you trust a new check, run it on the case it was built for. If it
doesn't catch that one, it won't catch anything.

## 3. Four false alarms, one finding

The first full run flagged six games. That's when the check needed checking.

I opened each flagged game and actually tried to scroll it, with a real wheel and swipe
instead of a measurement. Four of the six were fine: every flagged button came into view.
Those pages scroll *inside their body*, a box set to the screen's height that scrolls its
own contents, while the page as a whole reports nothing to scroll. My check only asked the
page. So four "cut off" games were really one mistake in the check, repeated four times.

With that fixed, two real failures were left:

- **Feed the Monster:** its third row of food buttons sat 27–83 px below the screen. Not a
  `vh` problem this time: the column of title, monster and square buttons was simply taller
  than 664 pixels. On short screens it now gets a smaller monster and slightly flatter food
  buttons, so the whole game fits, with scrolling as a backstop.
- **Draw & Color:** opened directly, its brushes sat 123 px below the screen. I fixed it in
  the app's source, then measured again. The brushes fit, but the canvas had shrunk from
  358 to 196 pixels wide, too small for drawing. A shorter tool bar on small screens brought
  it back to 280.

**The rule:** a false alarm is a finding about the check. Four wrong answers with one cause
is one bug, in the thing doing the measuring.

## 4. The check broke the pictures

Draw & Color had one more surprise. Under the check, its template pictures loaded broken and
the page logged eleven errors. On a real screen they were fine.

The check imitates the phone by rewriting every "number followed by `vh`" in the page.
Draw & Color carries its pictures inside the page as long runs of base64 text, and base64
sometimes contains exactly that pattern, like `...Q3vhK...`. My rewrite was corrupting the
images. Now it skips anything that sits inside base64.

The same rule caught one more gap later, when I pointed the check at my standalone web apps:
it only rewrote pages whose address ended in `.html`. Built apps load from `/` and keep
their styles in separate files, so the check couldn't see them at all. Fixed, and checked
again on a build I knew was broken, it caught that one and passed all ten live apps.

**The rule:** a tool that changes what it measures can cause the fault it reports. When a
result looks strange, check whether the tool did it.

---

## What they have in common

| | looked fine because | what was true | found by |
|---|---|---|---|
| The bottom row | every test passed | test browsers have no bars | opening it on my phone |
| Arcade tile vs link | the tile fit | only the direct link broke | testing both ways in |
| Four "cut-off" games | the check said so | the check couldn't see body scrolling | trying to scroll by hand |
| Draw & Color's pictures | "11 errors" | the check corrupted them | asking what the check changed |
| The web apps | "nothing cut off" | the check never touched them | running it on a known-bad build |

Every check in this piece answered a narrower question than it seemed to. The fix was always
the same: before believing a check, run it on a case where you already know the answer.

The phone check now runs every night on every new app, so a game that hides under the
toolbar stays off the Arcade until it's fixed. It still can't tell me if a game is fun. For
that I have two testers, aged five and three.

---

*`phone_fit_check.js` is a Playwright script. It imitates a phone's browser bars by
rewriting `vh` against the full screen height while showing only the visible height, then
measures what a child can't reach. It runs on two phone sizes, as an Arcade tile and as a
direct link, and the nightly check runs it on every new app.*
