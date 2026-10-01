## Lance Massey

Secondary-school teacher who builds and ships software — full-stack web apps, local AI tools,
and classroom apps. I care most about the parts that are easy to skip:
tests on the maths, accessibility, and writing down why a decision was made.

### Selected work

**[Canopy HR](https://github.com/TokkatheDj/canopy-hr)** · [live demo](https://canopy-hr.vercel.app)
A complete HR platform: people records, hiring pipeline, onboarding, time off, timesheets,
simulated payroll and benefits, performance reviews, anonymous eNPS surveys, reporting.
Next.js 16, TypeScript, Prisma + PostgreSQL, Auth.js. Effective-dated job history, a
ledger for time-off balances, one approval engine for every request type, role checks
enforced on the server. CI on every push; light and dark themes, with zero axe-core
violations on every page, for every role, in both.

**[Paper Edit](https://github.com/TokkatheDj/paper-edit)**
Edit long-form video and podcasts by editing the transcript. Runs entirely on your own
machine — no cloud, no subscription, no account. Python, FastAPI, Whisper, FFmpeg; pytest suite.
Exporting a real 97-cut edit went from about 30 minutes to 4 once each cut decoded only its
own span — verified frame-for-frame against the old output.

**[Games Arcade](https://github.com/TokkatheDj/party-command-games)** · [play](https://tokkathedj.github.io/party-command-games/)
53 party, carnival and kids' games in one searchable catalog, no install. Its Math Worksheets
grade by mathematical *value*, not exact text — `2(x+3)` is accepted for `2x+6` — using a
small polynomial-equivalence checker with no libraries.

**[Math Tools](https://github.com/TokkatheDj/MathTools)** · [live](https://tokkathedj.github.io/MathTools/)
Interactive manipulatives for students: algebra tiles, balance scale, fractions, number line,
place value, probability. React, Vite, TypeScript, Tailwind. The balance scale solves for x
on either side, with fractions and negatives — and has the tests to prove it.

Also: a phone app for a roadside-assistance business that shows which call channel actually
pays per hour worked, including drive time and dead runs (client work, private).

### Writing

**[Shipping on a teacher's schedule](writing/shipping-on-a-teachers-schedule.md)** — how a
one-page list, a Y/N runner and a weekly health check got a backlog of fixes across nine
projects live in one evening, and the eight things that broke on the way.
