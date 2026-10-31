# The Car That Corrected Its Simulator

*I wrote a robot car's software before the kit arrived, against a simulator that passed 33
checks. Then the real car spent two days showing me what the simulator didn't know.*

Coqui 2.0 is a small four-wheel robot car built from a Freenove kit: a Raspberry Pi Pico W,
mecanum wheels that can slide sideways, an ultrasonic sensor on a turning head, and an IR
remote. Before the box came, I wrote its program in MicroPython and a simulator that ran
that program unchanged against fake wheels, a fake sensor and a fake clock. Everything
passed.

Then I built it. Over two days on the floor of my house, the car failed in ways the
simulator couldn't, and I kept to one rule each time: **reproduce the failure in the
simulator first, watch the check fail on the old code, then fix it.** The simulator went
from 33 checks to 85, plus 36 more for its Wi-Fi link. This is what the real car taught it.
As with my other projects, I built it with heavy AI assistance. My part was deciding what
counted as evidence.

---

## 1. The freeze that wasn't the servo

The car worked on the bench. Then the sensor head went on, and the USB connection died:
Windows saw the board but reported *"a device attached to the system is not functioning."*

I made three wrong guesses in a row. The servo's electrical noise: unplugging it changed
nothing. A loose cable: swapping cables changed nothing. The sensor: unplugging it changed
nothing either. But that last test was spoiled, because by then Windows' record of the
port had wedged from all the failed attempts, and *any* test would have failed.

I stopped guessing and had the car tell me instead: did it reach its "ready" light with
the cable out? It did, so the program was fine and the PC side was stuck. After a clean
reset, the pattern was clear. The head socket is shared between the ultrasonic sensor
and an LED face panel, and at start-up the program asked *"is a face panel there?"* by
scanning those pins. A powered sensor made every address wait out a timeout, which froze
the USB link. An unpowered one made every address seem to answer.

The fix pings the sensor first and only scans for a face if nothing echoes. The simulator
got a sensor that behaves like the real one: it always answers, even with nothing in range.

**The rule:** when three guesses fail, stop guessing and ask the system for a fact that
splits the possibilities.

## 2. Driving away from its own eyes

The first time it explored on its own, it rammed walls and knocked its own head off. Its
reports showed bumps at 5 and 10 cm. Up close, or meeting a wall at an angle, an ultrasonic
pulse doesn't come back, and the sensor reports "nothing there". My code read that as open
floor.

I added a rule: no echo right after seeing something close means *blocked*. Then it backed
into the wall behind it. There's no sensor at the back. Then it stopped turning toward walls
but still hit them. Watching it, my question was: *"is it supposed to drive with the
sensors at the rear?"* It wasn't. On this build the head sits at the end the motors call
"back", so its "forward" drove away from its own eyes, and every rule I'd written about
what it saw was about the wrong direction.

One setting fixed it. "Head at the back" mirrors forward and sideways, but not turning:
turning a car round doesn't change which way "spin left" goes. The simulator now tests
the car both ways round.

**The rule:** before tuning behaviour, check the assumption under it. Four fixes to what it
did with its eyes were wasted while its eyes faced the other way.

## 3. When the simulator was too kind

Twice, my new check passed on code I knew was broken.

**The reverse it never saw.** The check sampled the wheels every 20 ms of simulated time.
The back-away began and ended *inside* one step, so the check never caught the wheels
going backwards. I changed it to record every wheel command instead of sampling, and on
the old code it failed with full reverse on all four wheels in exactly the floor's
situations.

**The room that emptied.** The car spun on the spot forever, turning away from walls
without ever driving off. My test said the fix wasn't needed, because in my fake room
everything vanished once the car turned. A real room keeps its walls. The side wall it had
just seen was still there, and that side reading re-armed the "blocked" rule. Once the
fake room kept its walls, the test reproduced the spin, and the fix (only readings straight
ahead count, and a turn clears them) made it pass.

**The rule:** a test that can't fail proves nothing. Break the code on purpose and watch the
check catch it, and when it doesn't, the test is the bug.

## 4. The remote, the Wi-Fi and the firewall

The rest were smaller, and each left a check behind.

- **A button nobody could stop.** One number key on the remote started a three-minute
  explore, and only the power switch would stop it. Now *any* key stops a self-drive, and
  a learn mode prints key codes without acting on them. That's how the real remote's layout
  was read off the car.
- **A Wi-Fi name with the wrong capitals.** The car saw seven networks and none matched
  exactly. It now accepts the one network that matches apart from capitals and spaces, and
  never guesses between two.
- **A firewall that ate the hello.** The car announced itself by broadcast, and Windows
  dropped it. Reversing who asks fixed it: the desktop broadcasts "who's there?" and the
  car's answer arrives as a reply, which the firewall lets in.
- **Wi-Fi that gave up.** It tried once at power-on. Now it retries every 30 seconds
  without ever pausing the loop that runs the wall stop. Tested by switching it on out of
  range and carrying it back: it reconnected in 44 seconds.

**The rule:** when one fix depends on another, test the second in the state that breaks it,
not the one that's convenient.

---

## What they have in common

| | the simulator thought | the real car showed | found by |
|---|---|---|---|
| USB freeze | sensors answer politely | a powered sensor stalls the scan | asking the car for its ready light |
| Ramming walls | no echo means open floor | no echo up close means blocked | its own bump reports |
| Backing into walls | sampled wheels look fine | a reverse fits inside one sample | recording every command |
| Driving blind | the head faces forward | the head faced "back" | watching it, and asking why |
| Spinning forever | rooms empty after a turn | side walls stay put | a fake room that kept its walls |
| Silent on Wi-Fi | broadcasts arrive | the firewall drops them | asking instead of announcing |

By the end of the second day it left my room, went down the hall and into the boys' room on its own,
turning away from everything in its path. Then it drove under a bed rail it couldn't see:
the rail sat above its sensor's beam. That's a limit of one forward sensor, not a bug. The
camera that's going on next is the fix for that.

---

*Coqui 2.0 runs MicroPython on a Raspberry Pi Pico W. `sim_robot.py` runs the unchanged
program against fake hardware and a fake clock (85 checks); `sim_link.py` tests the Wi-Fi
link over real UDP (36). Every check added during the build failed on the code before it.*
