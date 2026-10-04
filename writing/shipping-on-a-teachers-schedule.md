# Shipping on a teacher's schedule

I teach secondary school from 7:30 to 2:30. Software happens after that, in the gaps
between dinner and bedtime, and the gaps are short. For a long time the bottleneck wasn't
writing fixes. It was getting them *out*: a fix would be committed, and then sit there,
because shipping meant remembering a dozen commands across half a dozen repos on the one
evening I had the energy.

So I built three small things around one list.

## The list, the runner and the screen

**One list.** Every step waiting on me lives in a single JSON file: a title, one line of
*why*, the exact commands, and — the part that matters — how to tell it worked. "Pushed"
means the repo is in sync with GitHub. "Live" means the real site serves the change, not
that a command exited 0.

**One runner.** A double-click file walks the list one step at a time: what it is, why,
the commands, then **Y / N / Q**. It stops at the first failure and runs nothing after it.
When it's done it checks every step on the real thing and reports anything that ran but
didn't work as *failed*, never as shipped. `--rehearse` shows the whole flow without running
anything.

**One screen.** My home server (a local AI I built, called Amigo) already has a chat page,
a "face" screen, and a Stream Deck. Now the chat page shows **Your turn 2**,
the face shows a small badge, and a **SHIP IT** key opens the runner. A phone can see the
list; only the desktop can run it.

Then a **weekly health check** keeps the list honest: unpushed work, sites that are down,
builds the host skipped, failed CI, and private details added to public repos. Whatever it
finds becomes a step on the list.

It has grown since, each time because something slipped past it. "The site answers" turned
out not to mean "the site works", so it now opens every page and game — 75 of them — in a
real browser on a tablet-sized screen; that found a game tile leading to a 404 and a 30 MB
music app that took 13 seconds to appear. It flags work left *uncommitted* for a week, after a
server fix and a whole folder of code were found living only on disk. And it watches the
nightly backups, which now also keep every local repo's history on the *other* drive.

The first evening it existed, it shipped a backlog of fixes across nine projects — each one
verified live.

## What broke on the way

This is the part worth reading. Each of these was caught by a check, not by luck.

**1. A private repo isn't private once it's deployed.** A static site deployed straight from
a private repo served *every* file in it — including internal notes with a client's contact
details. Found by requesting a non-page file on the live URL. Fixed with forced 404 rules for
the working folders, then verified live.

**2. A security fix sat undeployed for two months.** A small app had a fix adding an order
code and daily limits to a public form. The host's "skip unchanged builds" rule compared
the commit with *itself* once its build cache was empty, so it skipped every build — 88 in a
row. Fixed the rule, tested all four cases, and now the health check looks for exactly that
pattern.

**3. Cloud sync rolled back a branch.** One repo lived in a synced cloud folder. At 8:30 one
morning, the sync overwrote the branch pointer with a stale one and saved the real one under a
broken duplicate name. Nothing was lost, but a push would have
gone wrong. Lesson: don't keep a git repo inside a sync folder.

**4. A stray quote in the system PATH.** One PATH entry ended in a `"`. The command prompt
treats that as an open quote and stops finding everything after it — so one tool was "not
recognized" while others worked. `where` found it fine, which made it look like the tool
was the problem. The runner now cleans PATH before it runs anything.

**5. A safety check that blocked the right answer.** "Only deploy if the pull request is
merged" used `findstr /x`, which needs a Windows line ending; the GitHub CLI doesn't print
one. So it said *not merged* about a merged PR. I had only tested the "not merged" case.
Now every guard is tested in both directions against real state.

**6. A rehearsal that wasn't one.** Testing the old batch-file version meant patching it to
answer the prompts automatically. One bad patch left two real commands in place, and they
ran. No harm done — one was a no-op, the other failed — but it's why rehearsal became a flag
in the runner instead of something I improvise.

**7. A slow export that was really a scaling bug.** A transcript-based video editor I built
took about 30 minutes to export a 9-minute edit with 97 cuts. Every cut was decoding the
video from the beginning up to that cut, so the work grew with *cuts × length*. Giving each
cut its own seeked input took it to 4 minutes — but the first version ran out of memory at
97 inputs, which only a full-size test on the real edit showed. The final version was checked
frame by frame against the old one (same frame count, every frame at least 49 dB PSNR), and
steps back to the old path when there are too many cuts to hold in memory.

**8. A maths tool that taught the wrong answer.** A balance-scale manipulative treated *x* as
weighing nothing, so `x + 2 = 5` said `x = 5`. For a tool students use, that's the worst
possible bug. It now solves properly, with fractions and negatives, and the tests include the
three wrong answers it used to give.

**9. My own profile overstated something.** It said the HR demo had zero accessibility
violations on every page, for every role, in both themes. That came from a sweep of every
page in the menu, but it never opened a detail page: one person's profile, one job opening,
one assessment. A fresh sweep that did (136 scans) found four kinds of detail page failing. Worse, it found
something no scanner flags: rows in the People directory opened on a mouse click only, so a
keyboard user couldn't open anyone's profile at all. All fixed, and the weekly check now
re-runs the full sweep, so the sentence on my profile is tested rather than remembered.

**10. Merged isn't deployed.** The fix for #9 merged cleanly, and the runner reported the
step as *failed* anyway. The live check had swept the real site and found the old problems
still there. That app is deployed by command, not on merge (switched that way in August to stop
broken preview builds, and forgotten by the time it mattered). This is exactly the case the "how do you know it worked?" field
exists for. The list's own tests now refuse a step that merges into a repo like that
without also deploying it, and the health check notices when a live site is behind its code.

**11. A finished step that would have done harm twice.** A step that moved the demo's dates
forward eight weeks, on the live database, had completed by hand but was still listed as
*failed*, so one Y would have offered it again. It never ran twice, but now any waiting step
that changes production must carry a guard that refuses once the change is already made.
And the runner itself got its own tests: I re-created nine of its past and possible bugs on
a scratch copy, one at a time, to make sure the tests catch each one.

**12. My own maths tools were grading wrong.** #8 was one bug in one tool, so I audited every
place my sites grade an answer or do a calculation a student trusts. The worst was an answer
checker shared by three worksheet pages: it counted anything *contained* in the answer, so
"2" passed for "x = 25", and it read "3/4" as 34. To measure it rather than argue about it, I
took every one of the 1,007 real problems, generated answers a student would rightly type and
plausible wrong ones (off by one, a digit dropped, ten times too big), and ran them through
the page's own checker: it accepted **716 of 1,856 wrong answers**. The rewrite accepts none
and rejects none of the right ones. The same audit found a credit-card lesson telling students
a $5,000 balance would "never" be paid off (it takes 35 years), quizzes marking 7.9 correct
for 7, a calculator whose "log" key gave 4.605 for log(100), and the kids' maths tile accepting
2222 for 2221. Every fix now has a test that runs weekly against the live site, and each test
was checked against the old code to prove it would have caught the bug.

## What I'd tell another teacher who codes

- **Make "done" mean verified.** A green exit code isn't shipped. Check the thing people use.
- **Silence isn't health.** My health check reports how much it looked at, and a check that
  saw nothing is a finding of its own.
- **Test the guard both ways.** Most of my bugs were checks that had only been shown to say
  "no".
- **Shorten the last mile.** Writing the fix was never the hard part. Making it one
  double-click was.

*Built with Claude Code as a pair: I set the direction and made the calls; it did a lot of the
typing and most of the checking — including catching several of the bugs above.*
