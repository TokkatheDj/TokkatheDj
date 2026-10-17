# Every Page Said 200 OK

*Auditing my own kids' apps: five problems that no load test could see.*

I keep a set of games and maths apps for kids. Most live in two places: a public
Games Arcade, where each game is one HTML file, and their own small sites on
Netlify, where they install to a tablet's home screen like an app. My sons use
them. So do students.

Every one of those pages loads. A health check opens them all each week, and
every week every page answered **200 OK**. This is about one week in October when
I stopped asking whether the pages loaded and started asking whether they were
*right*. I found five kinds of problem, each invisible to "does it load?", and
added a check for each so it can't quietly come back.

As with the rest of my projects, I built this with heavy AI assistance: an
assistant wrote most of the code and ran the tests, working from my direction.
My part was deciding what to ask, and what counted as proof.

---

## 1. Two copies that drifted

Nine of the games exist twice: the Netlify site (built from source) and the
Arcade copy (everything inlined into one file). Fixes went into whichever copy
I was looking at. Nothing compared the two.

When I finally did, three Netlify copies were missing fixes the Arcade copies
had had for days, and two pairs had drifted *both ways*. The Arcade's Kids Math
had a whole 6th grade (10 units, 56 lessons) and 13 finance topics; the Netlify
copy had 6 topics, but it also had grading fixes the Arcade never got. Merging
them meant re-grading 1,686 answers against both versions. Right answers
accepted stayed at 784, and wrong answers accepted fell from 20 to 12.

That re-grade also caught one of mine. My first count said the checker rejected
59 correct answers. It didn't: my test had taken whatever came after the last
"=" as a full answer, so it expected "−2" to be accepted for "x = 8 or x = −2".
I tried 42 answers a student would actually type instead (`6.28` for "≈ 6.28",
`2, 3` for "x = 3 or x = 2", `15 apples`), and the checker got every one right.

**The check now:** each week it compares what each pair actually *runs*. That
means statements of code and styles, with minified names blanked and packaging
lines dropped, so a build difference isn't a drift. It remembers the accepted
differences per pair and speaks up only when they change: one copy edited, the
other not.

## 2. Six apps that installed with a blank icon

Install any of six of the kids' apps to a home screen and you got a blank tile.
Four of them served the June template's icon files, which were 70 bytes each: a
valid PNG of nothing. The other two listed icons in their manifest that had
never been uploaded. Every page still answered 200.

A seventh, Draw & Color, couldn't be installed at all. Its manifest, offline
worker and a real icon were all live on the site, but the page never linked to
them. An older copy of that page did, and the link had been lost from the source
along the way.

**The check now:** for every installable app, it reads the manifest and fetches
each icon the manifest names. Each one has to answer, be an actual picture, and
be bigger than a placeholder. It covers twelve apps, and run against the old
sites it named exactly these six.

## 3. A quiz that taught the rule backwards

The maths worksheets walk students through each problem with multiple-choice
steps. I audited all of them: 1,556 questions on 652 problems. For each one I
checked that exactly one button is right, that no two buttons say the same
thing, and that no "wrong" button is worth the same as the answer.

For graphing inequalities, step 1 asks whether the boundary line is solid or
dashed. For ≤ and ≥ the correct button read **"Solid (boundary not included)"**,
and the wrong one read "Dashed (boundary included)". The explanations were
attached to the button's *position*, not to the kind of line, so on three of
the six problems, a student who answered correctly was told the opposite of the
rule. Elsewhere, a negative-exponents question offered `4^-3` as a wrong choice
beside the answer `1/64`, which is the same number. And three topics sometimes
showed two identical wrong buttons.

The night before, a compound-interest problem had turned up whose quiz asked
about *simple* interest. Its worked answer, $7,834.96, wasn't one of the four
choices.

None of this crashed anything. A quiz that teaches the wrong rule is worse than
a broken one, because nobody reports it.

**The check now:** a script runs every question on both live copies each week:
one right button, no duplicates, no wrong button equal to the answer, and no
right answer that explains itself backwards. Its first run found eight problems
on each copy. It finds none now.

## 4. Three tiles that led nowhere

The Arcade has a hub page for the kids' games: nine big tiles. Three of them,
Carnival, Math Worksheets and Song Maker, opened a 404. They pointed at copies
that had only ever existed on my computer, in folders that aren't published, or
at a file name that was never used. The hub itself loaded fine, which is all
the old check asked.

**The check now:** the Arcade is published straight from its repository, so
any link from a published page to a page that isn't in the repository is a dead
link on the live site. The check looks at every link on 148 pages and runs in a
couple of seconds.

## 5. A risk I overstated

Ten of the Netlify sites go live from uploads I make by hand, but they're still
linked to GitHub repositories with automatic builds switched on. I flagged it as
urgent: one push to those repos, I said, would replace each live site with the
old repo copy and undo the week.

Then I checked. All ten repos had been archived in July, and nobody can push to
an archived repo. The real risk was smaller: a "Retry deploy" click on Netlify
would still clone the July copy and publish it. That's still worth closing, and
I did, by stopping builds on all ten. The repo link and hand uploads still
work. But I had raised an alarm before checking the one fact that decided it,
and I had to correct myself to the person relying on me.

**The check now:** a hand-uploaded site with builds still on is raised every
week until it's stopped, archived repo or not.

---

## The week's other lesson: deploys cost money

Halfway through, every live deploy started failing with *"Account credit usage
exceeded"*. Weeks of small one-fix deploys had used up the month's credits. Test
deploys still worked, which made the first failure confusing. The fix was
partly a top-up, and partly a habit: batch the changes, deploy once, and check
each folder against the live site first so a deploy carries only what I meant
it to.

---

## What I'd do differently

**Ask what each check can see.** "Does it load?" was the only question my
checks asked, and every problem here answered it correctly. Each new check asks
something specific: do the two copies match, is that icon a picture, is the
right button right, does that link go anywhere.

**Audit the answer key, not just the grader.** I'd spent real effort on whether
the worksheets *accept* right answers. Nobody had looked at whether the buttons
*offered* the right one.

**One copy is better than a check.** The twin comparison is a safety net
for a design decision: keeping the same game in two places. Where I can, the
better fix is one source that builds both.

**Check the deciding fact before raising the alarm.** The archived repos took
one command to see. I ran it after I'd already called the risk urgent.

This carries straight into the classroom. The mistakes that matter most aren't
the ones that stop a lesson, which students report in seconds. They're the ones
that look fine and teach the wrong thing quietly. The only way to find those is
to go and look, one question at a time.

---

*The Games Arcade is public at
[tokkathedj.github.io/party-command-games](https://tokkathedj.github.io/party-command-games/).
The checks run weekly from a small Python health script with Playwright, and
each one has tests built from the real bug it was written for.*
