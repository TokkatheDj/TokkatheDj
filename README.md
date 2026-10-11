## Lance Massey

Secondary-school teacher who builds and ships software — full-stack web apps, local AI tools,
and classroom apps. I care most about the parts that are easy to skip:
tests on the maths, accessibility, and writing down why a decision was made.

### Selected work

**Amigo** · code private · [write-up](writing/believe-the-photograph.md)
A local-only AI assistant for my house: nothing leaves the building. Language models run on
a desktop GPU (Ollama), speech goes in and out locally (faster-whisper, Piper), and one chat
page works hands-free from a phone. Around it are a microcontroller on the desk (button, buzzer,
LED strip, motion sensor), a Raspberry Pi front door that wakes the desktop when it's needed
and covers for it with a small model, a smartwatch face, smart lights, and games for my kids.
The server is plain Python with no framework. Amigo keeps a dated engineering log of what
broke and why, and a self-check that catches the server freezing and restarts it. A "ship it"
list runs each deploy step from my phone, then checks the live result.

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
own span — checked frame by frame against the old output (same frame count, every frame ≥ 49 dB PSNR).

**[Games Arcade](https://github.com/TokkatheDj/party-command-games)** · [play](https://tokkathedj.github.io/party-command-games/)
55 party, carnival and kids' games in one searchable catalog, no install. Its Math Worksheets
grade by mathematical *value*, not exact text — `2(x+3)` is accepted for `2x+6` — using a
small polynomial-equivalence checker with no libraries.

**[Math Tools](https://github.com/TokkatheDj/MathTools)** · [live](https://tokkathedj.github.io/MathTools/)
Interactive manipulatives for students: algebra tiles, balance scale, fractions, number line,
place value, probability. React, Vite, TypeScript, Tailwind. The balance scale solves for x
on either side, with fractions and negatives — and has the tests to prove it.

**[VR Math Rooms](https://github.com/TokkatheDj/vr-apps)** · [open on a Quest](https://tokkathedj.github.io/vr-apps/)
Three WebXR rooms for teaching in a Meta Quest headset: plot points and read off slope and
the line's equation, stand on y = mx + b and feel the hill change as m does, and sort a
month's expenses into 50 / 30 / 20 — which balances at $3,200 and $4,500 but never at
$2,400, where even the cheapest needs take 66% of take-home pay: the rule assumes slack.
A-Frame, one HTML file per room, no build step; walking blinks instead of gliding, to spare
stomachs. Checked by script on a real GPU: clicking (3, −9) plots (3, −9), above the floor.

Also: a phone app for a roadside-assistance business that shows which call channel actually
pays per hour worked, including drive time and dead runs (client work, private).

### Writing

**[Shipping on a teacher's schedule](writing/shipping-on-a-teachers-schedule.md)** — how a
one-page list, a Y/N runner and a weekly health check got a backlog of fixes across nine
projects live in one evening, and the twelve things that broke on the way.

**[Believe the photograph](writing/believe-the-photograph.md)** — three bugs from Amigo that
passed every test I had, what finally caught each one, and the thing my sons found in
one round.

**[The client is a kid](writing/the-client-is-a-kid.md)** — redesigning Amigo's face in one
evening: five versions tuned to my own taste, then one sentence from my son that pointed at
the reference I'd ignored, and what that changes about designing for students.
