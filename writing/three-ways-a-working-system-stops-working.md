# Three Ways a Working System Stops Working

*One week of keeping a home AI server up, and the three times "it's fine" was wrong.*

Amigo is the local AI assistant I built for my house. A Python server on a
desktop runs the chat page, the voice, the games and the lights; a Raspberry Pi
sits in front of it as the always-on front door. When someone asks a question
and the desktop is asleep, the Pi wakes it over the network. If it doesn't wake
in time, a small model on the Pi answers instead.

Around the server I'd built two safety nets. A wrapper script restarts it if it
dies. A watchdog, run every five minutes, checks it's answering and starts it if
it isn't. Both worked. Every check I had said the system was healthy.

This is about one week in which it wasn't, three times, and what finally showed
it. As with the rest of Amigo, I built it with heavy AI assistance. The scarce
part, again, was deciding what counted as evidence.

---

## 1. The crashes that were deploys

The server's restart log said it had exited three times in one day, each time
with "code 1". Three crashes in a day is a pattern, so I went looking.

None of them was a crash. Each one lined up with a change to the server's code
that day, the last one to the minute. The old copy had been stopped so the new
code would load, and a stopped process reports the same exit code as one that
fell over. The log line couldn't tell the two apart, so anyone reading it would
assume the worse one.

The look turned up two real problems that the "crashes" had been sitting on top
of:

- **The error log was 21 MB of nothing.** It held 12,254 copies of the same
  20-line error, every one from the Pi. The Pi drives a small screen showing
  Amigo's face, and its browser polls the server a few times a second. Browsers
  routinely drop idle connections, and the server printed a full traceback each
  time, about 10 MB a day. Anything that really went wrong would have been
  buried. Those disconnects are now ignored; every other error still prints.
- **Each restart wiped the previous run's logs**, which is why the three exits
  had left no trace. The previous run's logs are now kept.

**The rule:** a log that can't tell "stopped on purpose" from "crashed" will be
read as a crash. If a status line has to be interpreted, write the
interpretation into it.

## 2. The guard nobody was guarding

While checking the server, I found it running with **no wrapper at all**. The
server had been up for two days. The thing that restarts it if it dies had
quietly stopped existing, so a real crash would have stayed down until the
watchdog's next pass.

The first way I found for that to happen was a rule in the wrapper. If it started and found another copy
already holding the port, it assumed that copy was fine and exited. But stopping
the wrapper's scheduled task ends only the wrapper; the server it started keeps
running. So after a stop and a start, the new wrapper saw the old server, trusted
it, and left. Now the wrapper waits and takes over as soon as the port frees up.

Two days later the server was unsupervised again. This time I added a check to
the watchdog: *answering, but nothing is watching it*, which starts a new
wrapper. Then I tested it by recreating the situation, and the test caught the
real culprit.

**The two safety nets were fighting.** When the server dies, the wrapper starts
a new copy within seconds, but that copy takes a few more seconds before it's
listening. The watchdog's five-minute run landed in exactly that gap. It saw "task running, but nothing listening",
decided the wrapper was wedged, and stopped the task, which ended the wrapper.
Each net was correct on its own. Together, one could switch the other off.

The fix was patience: if the task is running but the port is quiet, the watchdog
now gives the wrapper 30 seconds to finish its restart. I recreated the race,
killing the server and running the watchdog at the same moment. The watchdog
waited nine seconds, saw the server come back, and did nothing. The same wrapper
carried on.

**The rule:** two supervisors that don't know about each other aren't twice as
safe. Ask what each one will do while the other is halfway through its job.

## 3. The answer that never came

The last one started as a success. With the desktop asleep, I asked my phone
"what is seven times eight?". The Pi woke the desktop and waited 25 seconds.
The desktop came back three seconds too late, so the Pi's small model answered
"56". Correct, and the designed fallback, but the desktop had taken 28 seconds
where a test a fortnight earlier had taken ten.

So I measured it. I ran two recorders, one on the desktop and one on the Pi,
each checking every half second whether the server answered: from inside the
desktop, and over the network. Then I let the Pi wake it.

The desktop answered **11 seconds** after the wake signal. That was just Windows
resuming, and the server answered the instant it ran. It was also not the
firewall: the server answered while Windows still had the network marked
"Public", and the app's rule covers both.

The slow wake didn't come back. So I ran it the way the phone does it: a longer
sleep, with the question going through the Pi rather than a bare wake signal.
The desktop answered in 14 seconds, and the Pi handed it the question.

The answer never came.

The graphics card was idle. The model, asked directly, answered in nine seconds.
The Pi had an open connection to the server, and **the desktop had no record of
it**. The Pi had handed over the question the instant the server first
answered. Two seconds later, both times I measured it, Windows finished
re-identifying the network and switched it from "Public" to "Private". I can't
prove that switch killed the connection, but the connection was opened in that
gap and was gone on the desktop's side afterwards. And the Pi was willing to
wait **ten minutes** for a reply on it. My phone would simply have hung.

Three changes. After waking the desktop, the Pi now waits four seconds past its
first answer before handing anything over. It gives up on a silent desktop after
60 seconds instead of 600. And if the desktop drops a question before any of the
answer has gone out, the small model answers. I tested that last part against a
fake desktop that answers health checks but swallows every question: "56" again,
instead of a hang.

Then I ran the real thing. The first rerun didn't count, because a USB device
woke the desktop 14 seconds into its sleep. On the second, the desktop slept for
five minutes, the question went through the Pi, and the full desktop model
answered **"Fifty-six." in 20.8 seconds**. That's faster than the fallback.

**The rule:** "it answered" is a moment, not a state. A system that has just
come back is still settling, and the first thing you hand it is the thing most
likely to be lost.

---

## What the three have in common

Each failure was invisible exactly where I was looking:

| | what it looked like | what it was | found by |
|---|---|---|---|
| The crashes | three exits in a day | three deploys | matching the times to the commits |
| The missing guard | a server answering every check | nothing to restart it | recreating the failure on purpose |
| The lost answer | a desktop that had woken up | a dead connection held open for 10 minutes | recording both ends at once |

Every one of those signals is what a healthy system looks like, right up until
you check what's underneath it. It's the same lesson as my last write-up, from a
different direction: there it was tests that couldn't fail, here it was
monitoring that couldn't see.

---

*Amigo is a personal project and is not on the public internet. The server is
plain Python with no framework; the restart wrapper and watchdog are PowerShell;
the Pi's front door is a single Python file.*
