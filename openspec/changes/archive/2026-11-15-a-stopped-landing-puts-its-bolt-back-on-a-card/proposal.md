# A stopped landing puts its bolt back on a card

## Why

flume's bolt `flumes-settings-read-as-its-records-say` had its land 332 stopped, nothing of the bolt's: "the base place ... is submitted once no place on its branch bolt/flumes-settings-read-as-its-records-say is live". It then read proven again at 886b047. The user had sent `land/flume` (`req_d2c7ae4c54e24fcebf2d`) ticking it and two other bolts. Those two landed, yet the card stayed open for hours. The rail said it "waits on the runner to land" all three. The stopped bolt's line said "held by your send on land/flume: crew asks the runner to land it on that send", and no land was posted. Only ops's next `crew card read land/flume` closed the card and raised the one that asks again (`req_281de9363f5542a1a286`).

rail-cards already says an answered landings card closes once each bolt it ticked has landed, been held or stopped. The raise does close it at a stop (`landings_step`), but nothing ran the raise once the stop was read:

- The read that records a stop or a refusal (`landing_read`) raised no card. Only a landing's close raised one (`bolt_land`), and ops was asked.
- The rail's read raised no card. `unoffered` counted the stopped bolt as held by the send that ticked it. `card_stand` said the send held it. `send_waits` and `answered_waits` counted it as still waiting on the runner, and `answered_waits` named the two bolts that had landed too.
- The raise left the card open when the bolt's head had moved since its stop with its own work unchanged. The send still read as standing, though `runner.lands_due` posts no land on a send a stop spent, at that head or any.

## What Changes

- **The read that records a refusal or a stop raises the bolt's kit's landings card.** It hands the raise to the drive's main machine as a landing's close does. A read inside a raise raises none, since that raise acts on what it read.
- **A send a stop spent waits on that bolt no more, at any head.** One decision, `send_spent`, names the bolts a card's send ticked whose land on that send the runner or Flume stopped. The rail's read raises a card a stop spent the send of. Such a bolt's land line says the card after the answered one carries it, and the sweep does not count it as waiting. The card's line names only the bolts its send still waits on. The raise reads a stop that spent the send as spent though the bolt's head moved since, so it closes the card naming the stop, and the card that follows asks for the bolt again.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `rail-cards`: a stop of the land a send posted ends the sweep's wait on the card and makes the rail's read raise it. A new requirement says crew's own read and the rail's read close the card at a stop with no read of ops's, at the bolt's head or after it moved.
- `crew-rail`: an answered landings card's line names only the bolts its send still waits on. A bolt whose land on the send was stopped follows, held by no send.
- `bolt-teams`: the read that records a stop or a refusal raises the bolt's kit's landings card.

## Impact

- `plugin/lib/plan.py`: `send_spent` and `ticked_waits` are new decisions. `send_waits`, `answered_waits`, `card_stand` and `unoffered` read them. `record_reading` and `landings_unoffered` give `spent` to the card facts. `landings_raised` passes a send a stop spent at an older head to `landings_step` as a stop. `landing_read` raises through `unheld_raise`.
- `tests/py/test_landing.py`, `tests/py/test_landings.py`, `tests/py/test_rail.py`: the cases.
- No change to the views' shape or crew's mod (`code.8`): no bolt, unit, stage, card key or rail row changes shape, only the words of a line.
- No command, usage, brief or README changes (`docs.2`). Ops is still asked of a stop, as role-runs has it.
