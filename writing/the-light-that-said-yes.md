# The Light That Said Yes

*On Halloween night a porch light reported every colour I sent it and showed none of them.
What I learned about acknowledgements, restarts and a show that couldn't be stopped.*

The Haunted Coquí Porch was a one-night show. A Raspberry Pi greeted trick-or-treaters as
Amigo, our home assistant's frog character: a voice line on a Bluetooth speaker, the porch
lights resting on pumpkin orange, and everything flashing green for each new group. It ran from
5:30 to 9:00 and then put every light back the way it had found it. The tests passed and the
rehearsal two days earlier went fine. The night still found problems the tests hadn't, and
they had to be fixed while the show was running, because stopping it would have caused a
worse problem, which is section 2.

As with my other projects, I built it with heavy AI assistance. My part was deciding what
counted as proof, and that turned out to be most of the night.

---

## 1. The light that said yes

The string lights weren't up this year, so an hour before the show I swapped in the gazebo's
LED strip. I checked it the usual way: I asked the manufacturer's cloud for the strip's state.
It reported the strip online, on, and set to `#FF5000`, pumpkin orange, at 80%.

The strip was warm white. Every command had come back "success", and the state readback
showed exactly what I'd sent. Neither one had looked at the strip itself. The cloud was
reporting the last value it had been told, not what the light was showing.

The fix was in the device's capability list. This strip is divided into fifteen segments, and
it ignores the whole-strip colour command but obeys a per-segment one. I sent orange to all
fifteen segments once, and asked the one person standing in the yard. *"Yes orange now."*

**The rule:** an acknowledgement is not an observation. When the system can only report its
own last command back to you, the check has to be a person, a camera or a sensor.

## 2. The restart that would have lied

The obvious fix was to change the show's code and restart it. The trouble was that when the
show opens, it saves every light's current state so it can put it back at 9:00. A restart at
6:00 would have saved the show's *own* Halloween colours as normal, and at 9:00 the porch
would have stayed orange.

So nothing touched the running show. A small helper ran beside it on the desktop instead. It
watched the visitor count the Pi already published, flashed the gazebo green segment by
segment for each new group, and put the strip back to warm white at the end.

Then the request grew: the hallway light, then a hexagon panel, then two lamps. Each addition
meant restarting the helper, and the helper had the same flaw as the show. On its second
restart it would have saved the hallway and the panel, already orange and purple, as their
normal state. I caught it before restarting. The helper now writes each light's *first*
reading to a file and reuses it, and I filled that file with readings taken before the
helper ever touched those lights. One reading was incomplete: I hadn't recorded the hallway
bulb's exact colour coordinates, so it went back by hue and saturation, the same colour
described a different way.

**The rule:** anything that snapshots "how it was" has to survive its own restart. Otherwise
the second snapshot records your own changes as the original.

## 3. A check that compared a value with itself

Adding the hallway light to the helper, I wrote a test that it flashed green and then went
back to orange. The check read `hue == hue`. It would have passed whatever the light did. I
caught it on reread and replaced it with real ranges: green between 20,000 and 25,000 on the
bulb's hue scale, orange below 5,000.

It's the same failure as a car simulator I wrote about earlier that sampled too coarsely to
see a reverse. A check that can't fail tells you nothing about the code.

## 4. The cloud got slow, and the button got busy

Two smaller problems, each of which changed something.

- **Timeouts.** Around 6:15 the light maker's servers started taking longer than ten seconds
  to list devices. The helper fetched that list once per light, four times, and crashed on
  start. Now it fetches the list once and tries three times. The show's own log has a run of
  `TimeoutError` lines around 8:45; it kept going because every light call is allowed to fail.
- **The phone button.** The motion sensor never reached the door (the long USB cable didn't
  arrive), so greetings came from a big orange button on a phone. Between 7:00 and 7:30, 40
  groups arrived, too fast to tap for each child. We switched to one tap per group. A
  12-second cooldown already stopped double taps from stuttering the speaker.

---

## What they have in common

| | what the system said | what was true | what caught it |
|---|---|---|---|
| Gazebo strip | online, orange, 80% | warm white | a person in the yard |
| A mid-show restart | "how it was found" | the show's own colours | reading the snapshot code before restarting |
| The helper's 2nd restart | same | same, for two more lights | the same question, asked again |
| A new test | pass | it couldn't fail | rereading the assertion |
| Speaker at 5:30 | paired | not connected | the show's log; its once-a-minute check reconnected it |

The night ended on its own at 9:00: **87 groups**, first knock 5:53, last 8:53. The Hue bulbs'
readings confirmed they were back to normal. The cloud lights got their restore commands twice,
but by section 1's rule a readback proves nothing for them, so I asked for one more look on the
way past.

Afterwards, both night-time fixes went into the show itself: per-segment colour wherever a
light supports it, and an "as found" file that a restart reuses and that is deleted at close.
The checks for both fixes fail on the old code and pass on the new. Next October the show won't need the
desktop helper.

---

*The porch show is a Python service on a Raspberry Pi: a Bluetooth speaker, two smart-light
clouds, and a phone page. `test_porch.py` has 46 checks and `test_porch_lessons.py` adds 11;
the ones for the two fixes failed on the code from the night.*
