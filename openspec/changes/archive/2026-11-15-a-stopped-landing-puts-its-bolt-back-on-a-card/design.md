# Design

## Context

This section records what was read on 2026-11-15 at this branch's base, `e65f3c44`, so the decisions below rest on it.

**The case.** The fix's brief says flume's `land/flume` (`req_d2c7ae4c54e24fcebf2d`) ticked three bolts. Two landed. Land 332 of `flumes-settings-read-as-its-records-say` was stopped, nothing of the bolt's. The card stayed open until ops's `crew card read land/flume` raised it. That raise closed the card and posted `req_281de9363f5542a1a286`, which asks for the stopped bolt again.

**What closes an answered landings card.** Only `raise_landings`, through `landings_step`, closes one. The step reads a ticked row whose facts carry `stopped` as a send spent. It closes the card naming the stop, and the card that follows asks for the bolt (rail-cards "A ticked bolt stopped at the close"). `crew card read` reaches it through `land_hand`, which is why ops's read closed the card.

**What runs the raise.** `landing_close`, through `bolt_land`, raises it after a landing. Each place where crew reads a stop leaves it unraised:
- `landing_read` records a refusal or a stop and asks ops (`unlanded_ask`). It raises no card, though bolt-teams "A conflict recorded by a later read" says the read raises one.
- The rail's `sweep_moved` raises a card for four reasons: main moved, an answer recorded, an unoffered row, and a land due on proof. `unoffered` held a ticked bolt at its head by the send whatever became of that send's land. So a stopped bolt was "held", and nothing was unoffered.
- `sweep_cards` leaves an answered card while `send_waits` names a bolt. `send_waits` counted every ticked bolt neither landed nor dropped, a stopped one among them.
- `card_stand` said `holds` of every ticked bolt, giving the land line the brief quotes.
- `answered_waits` named every ticked bolt, landed or not, giving "waits on the runner to land" all three.

**When a send is spent.** `runner.lands_due` posts no land on a send whose land of the row was stopped, "at this head or any". `landings_raised` gives the step `stopped` only where the stop is at the row's head now (`landing_rows`, `stopped_at`). Suppose the head moved after the stop with the bolt's own work unchanged, as a take-main place merging into the bolt does. The send still reads as standing, the step leaves the card, and no land is ever posted. The brief's "a place on its branch is live", then "read proven again at 886b047", has that shape.

**The family.** No other tool closes or raises crew's landings cards. The runner's report and Flume's words are read as before, and no other tool changes.

**Area pages this change touches:** `core.md` (`read.1`, `read.5`, `roles.6`, `code.3`, `code.7`, `code.8`, `state.4`), `plan.md` (`plan.16`, `plan.21`), `tests.md` (`tests.4`, `tests.11`, `tests.12`) and `docs.md` (`docs.4`, `docs.7`). No rule changes, so no page is edited (`docs.7`).

## Goals / Non-Goals

**Goals:**

- An answered landings card closes as soon as each bolt it ticked has landed, been held or been stopped, and the card that follows asks for a stopped bolt again, with no act of ops's.
- The rail says what the card waits on as it is: a spent send holds nothing, and a landed bolt is not waited on.

**Non-Goals:**

- Asking ops of a stop. `unlanded_ask` stays, as role-runs "A land the runner refused" has it.
- How a stop is read from the runner's report (`runner.landing_of`, `landing_entry`).
- What `crew card read` prints.

## Decisions

### 1. The read that records a refusal or a stop raises the bolt's kit's landings card

`landing_read` hands a raise to `land_hand` once its `landing_record` recorded a refusal or a stop, when its `card` is true. The new `unheld_raise` does this. The raise goes to the drive's main machine as a landing's close does (`code.3`). The kit is the one the plan names for the bolt, else the launch's repository, as `started_land` names it. A read inside a raise (`kit_landings_read`, card false) raises none, since the raise that read it acts on what was recorded. A second read records nothing and so raises nothing. A plan that cannot be read is said, and nothing is raised (`read.1`).

A refusal raises too. The answered card's close is the same act for a held bolt (rail-cards "A ticked bolt held at the close"), and bolt-teams "A conflict recorded by a later read" already says the read raises the card. The raise is idempotent: the step leaves a card nothing changed for.

Not taken: raising only from the rail's sweep. The rail reads a drive only on its host's follower tick and only where its main level runs. Records are pulled, and the act that records the fact acts on it (`roles.6`, `plan.21`).

### 2. One decision says which bolts a stop spent a send for

`send_spent(entries, card, bolts)` gives each ticked bolt whose last landing (`stops`) was a land that card's send posted (`stopped_by`, `stop_spends`), with that land's head and what stopped it. A stop of a land on proof, or on another card's send, spends none of this card's. A stop whose posting crew cannot tell is read as spending it, so nothing is posted twice on one send (`stop_spends`, `read.1`). A later land asked of the bolt ends the stop, since the stop is no longer its last landing. It is a decision of plain facts (`code.7`), and every reader below uses it:

- `ticked_waits` gives the ticked bolts a send still waits on: none landed or dropped since the answer, and none spent. `send_waits` is it over the answer's entry, so the sweep's wait (`sweep_judged`, `sweep_cards`, `stray_cards`, `answered_cards`) ends at a stop.
- `answered_waits` names only those bolts. Once none is left it says crew's next raise closes the card.
- `record_reading` keeps `spent` on each open card's facts. `card_stand` then gives a spent bolt `follows` rather than `holds`.
- `landings_unoffered` gives `spent` to `unoffered`, which holds no spent bolt by the send and counts it unoffered. The rail's read then raises the card in the same sweep.

### 3. The raise reads a send a stop spent at any head

`landings_raised` passes the step each ticked row whose send a stop spent, at a head other than its head now, with that stop as its `stopped`. Only the step's rows get it. The card's own rows, `lands_by` and the following card's facts keep `stopped` only at the head now (`landing_rows`). A bolt not marked to stay whose head moved past its stop still lands on proof at the new head, and is no row. The step's close names the stop only for a bolt whose head did not move past the send. A bolt whose own work changed is said once, as proven since, with what changed (`work_said`). This matches `runner.lands_due`, so the raise never leaves a card waiting on a land the send will not post.

Not taken: changing `landing_rows` to keep a stop at an older head. The row's words say a stop at its head now, and rail-cards "The head moves" says a moved head says nothing of the stop.

## Risks / Trade-offs

- [A raise on every refusal or stop recorded] → It is one raise per outcome recorded, handed to the main machine as a landing's close is. A second read records nothing and raises nothing.

## After deploy

None. The logic tier proves each decision and the raise's acts on stand-ins. A host running a release that carries this fix closes the next such card at its first read.

## Task notes

**1.1** `plan.landing_read`, `plan.unheld_raise`. Cases in `tests/py/test_landing.py` `TestTheFirstReadActs`: `test_a_stop_recorded_raises_its_kits_landings_card_once` and `test_a_refusal_recorded_raises_its_kits_landings_card_and_a_landing_raises_through_its_close`. `land_hand` is stubbed in that class, in `TestALandingReadOnMainCloses` and in `tests/py/test_landings.py::test_a_landing_is_read_and_recorded_by_a_host_away_from_the_kits_with_every_ssh_refused`.

**1.2** `plan.send_spent`, `plan.ticked_waits`, `plan.send_waits`. Case `tests/py/test_rail.py::TestSweepJudged::test_an_answered_landings_card_whose_ticked_bolts_land_on_that_send_was_stopped_waits_on_it_no_more`.

**1.3** `plan.answered_waits`. Case `tests/py/test_rail.py::TestText::test_a_landings_card_the_user_sent_names_only_the_bolts_it_still_waits_on`.

**1.4** `plan.record_reading`'s `land_cards`, `plan.card_stand`. Cases `test_a_bolt_whose_land_on_the_send_was_stopped_follows_and_is_held_by_no_send` and `test_the_record_reading_keeps_each_landings_cards_rows_answer_and_the_sends_kept` in `tests/py/test_rail.py`.

**1.5** `plan.landings_unoffered`, `plan.unoffered`. Case `tests/py/test_landings.py::test_a_ticked_row_whose_land_on_the_send_was_stopped_is_unoffered`.

**1.6** `plan.landings_raised`, `plan.landings_step`. Cases in `tests/py/test_landings.py`: `test_a_stop_on_the_send_closes_the_card_and_asks_again_though_the_head_moved_since` and `test_two_of_three_ticked_landed_and_the_third_stopped_closes_the_card_asking_for_the_third_again`.
