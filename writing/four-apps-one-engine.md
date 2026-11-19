# Four Learning Apps, One Engine

*A teacher's case study: four practice apps built for real learners and tested like software. The
checks found a wrong answer key, and a tutor that was polite about refusing, before any student did.*

I teach 9th-grade Pre-Algebra and high school Personal Finance. Many of my students are low readers,
and they work on school Chromebooks. The practice tools I had either gave answers away, buried the one
step a student was stuck on, or assumed a strong reader. I also wanted the same kind of practice for
two people outside class: an adult studying for the Michigan MTTC 022 math test, and a preschooler at
home getting ready for kindergarten.

I designed, directed and tested these apps; the code was written with Claude Code as an AI pair
programmer. My part was the teaching rules, deciding what counted as right, and choosing what to test.

---

## 1. The four apps

| App | For |
|---|---|
| **Step Up Math** | 9th-grade Pre-Algebra, plus Algebra 1 chapter topics |
| **Money Moves** | High school Personal Finance, 17 chapters |
| **MTTC Math 022 Practice** | An adult preparing for the MTTC 022 math test |
| **Little Counters** | A kindergarten-readiness hub for a 3-year-old, with a frog guide named Amigo |

All four run on one shared engine. Each app is a single, self-contained HTML file, built by stitching
the shared engine together with that app's content. A fix to the engine reaches all four apps at once.

Every app has:

- **Practice** in three levels per topic, with hints and worked steps.
- **Guided first problems**: fill-in blanks and a "What do you do first?" question.
- **Common mistakes**: each wrong choice comes with a short "why", and the app keeps track of which
  mix-ups a student makes.
- **Accessibility**: read-aloud, dark mode, text size, and a setting to turn off animations.
- **An AI tutor** that coaches with hints and is built never to give the answer.

The two class apps also have a **class mode**: live class questions, per-student progress with a CSV
export, saved tutor chats the teacher can read, and chapters that open on a schedule (Money Moves
skips winter break on its own).

## 2. The rules I held to

- **Low readers:** short sentences, one idea per step, a "why" for every wrong answer, and no repeated
  steps.
- **Little kids:** wrong taps just wiggle, the guide never says "wrong", nobody loses, and every screen
  fits an iPad without scrolling.
- **Privacy:** no real names in the content. The class apps are owned by the school account, so
  student work stays with the school.
- **Original content:** matched to the class pacing guide's topics, not copied from a textbook.

## 3. How I know it works

A wrong answer key in a student-facing tool is the worst bug a math teacher can ship, so testing is
most of the work.

- **70,800** generated problems checked for structure across the four apps.
- **8,000** Step Up Math answers re-checked by an independent solver.
- **619** automated browser checks, all passing.
- **5** iPad screen sizes where every Little Counters screen must fit.

### The AI tutor, tested against the real model

I captured the exact requests the apps send at 25 real student moments across all four apps, including
messages that try to trick the tutor into revealing the answer. I sent them to the live model, ran each
reply through the app's own answer-leak check, and had a stronger model grade every reply against the
tutor rules. Across two runs, 48 replies were graded:

- **0** gave away the answer.
- **0** followed a planted instruction (6 of the 48 were planted-instruction attempts).
- **0** were flagged as unsafe.

The first run averaged **3.7** out of 5 and the second **4.1**. In the first run, 4 of 25 replies
opened by refusing ("I can't give you the answer"), which the grader marked down as cold. After that
run I added one rule telling the tutor to go straight to a friendly hint. In the second run, none
opened that way, and replies were shorter (29 words on average, down from 36). Each run used freshly
generated problems, so the rise shows a direction, not an exact measurement.

### Bugs the tests caught before students did

- **Factoring:** in 224 of 13,384 generated factoring problems, the right answer appeared twice, and
  one copy was marked wrong. After the fix: 0.
- **Slope from a graph:** 733 of 9,898 problems put a point off the visible grid. After the fix: 0.
- **Personal finance:** some generated budgets came out with negative money where a real budget can't.
  The fix redraws them, and a scan of every topic found no others.

## 4. What I'd do next

- A live check of the AI tutor with a real student account on a school Chromebook.
- A play-test of the preschool app on the iPad with its real user.

Until those two happen, the tutor has been graded on scripted student messages, not live ones. The
learners are the test that counts.

---

*Problem, answer, browser and screen-size counts are from the project's own checkers, run on
17 November 2026. The tutor figures are from the two saved result files of 4 November 2026 (25 and 23
graded replies; two grades in the second run came back unreadable). The factoring and slope counts
were measured when each bug was fixed and were not saved as files. The school, the students and the
app links are left out on purpose.*
