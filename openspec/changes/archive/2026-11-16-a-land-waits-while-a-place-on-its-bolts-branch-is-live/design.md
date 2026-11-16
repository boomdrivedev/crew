# Design

## Context

This section records what was read on 2026-11-16 at this branch's base, `b097ed4b` (crew's main, which is also `bolt/a-sent-landing-waits-its-turn`), so the decisions below rest on it.

**The case, from deneb's runner branch** (`refs/crew/boomdrive/runner/deneb` of afterthought/crew-state) and `boomdrive/main`'s `requests.rec`:

| When (2026-11-15) | What |
|---|---|
| 02:35:26Z | boomdrive-ops's read posts land 332 of `bolt/flumes-settings-read-as-its-records-say` (launch 237) on the user's send of `land/flume` |
| 02:54:17Z | the runner carries 237's status: live, unsubmitted, waiting on its caller, no `fixes`, nothing on its branch |
| 03:18:02Z | Flume's settle forecasts head `26b1eca` in conflict with main `e6dc2f4` and launches `fix--flumes-settings-read-as-its-records-say-1` on the branch |
| 03:20:30Z | the runner carries land 332, and Flume refuses the retry: "the base place … is submitted once no place on its branch bolt/flumes-settings-read-as-its-records-say is live, and …-1 is (203)" |
| 03:21:57Z | the runner carries 237's status: `on_branch` naming the fix, `waits_on: places`, the fix live |

When crew posted the land, nothing was on the branch for any read of crew's to see. Flume launched its fix 43 minutes later, in the 45 minutes between crew's post and the runner carrying it. What lost the send was how crew read the refusal.

**How crew reads a refused land now.** `runner.landing_outcome` reads a newest land the runner answered refused as `stopped`, by the runner, whatever stopped it. `plan.landing_entry` records it `Outcome: stopped`, and `landing_read` asks ops (`unlanded_ask`) and raises the kit's card (`unheld_raise`). `runner.lands_due` reads the send that posted the land as spent, at that head or any. `send_spent` makes the raise close the answered card naming the stop, and the card that follows asks for the bolt again (a-stopped-landing-puts-its-bolt-back-on-a-card).

**What holds a land now.** `lands_due` posts only for a row with a box. `landing_rows` takes the box away while a fix is in flight on the bolt (`runner.fixes_in_flight`): crew's own fixes, and Flume's landing fix once Flume lists it live (`runner.landing_fix`). Nothing reads a place on the branch that crew did not launch and that is not a landing fix.

**Flume's side.** Statement 203 at `cb114fd`: a base place's retry is refused while a place whose base is its branch is live, naming those places, and the base place waits on them. Flume's status gives a base place `on_branch`, "the places being made or live whose base is a base place's branch, given for a base place alone (56, 130, 203)" (flume `crates/flume-core/src/answer.rs`), and `waits_on: places` while any is (`WaitsOn::Places`). The retry's refusal reads the same list (`crates/flume-core/src/acts.rs`, `self.on_branch`). Flume 0.19.0's status gives `on_branch` (`tests/py/flume-0.19.0/`). Flume 0.17.0's gives none (`tests/py/flume-0.17.0/`).

**The runner's side.** The runner answers a land Flume refused `Outcome: refused`, with Flume's words and no cause of its own (boomdrive `crates/boomdrive/src/carry.rs`). It carries the answer and the base place's status in one pass: deneb's commit `5f4fd5b4e7` carried both answer 332 and the status naming the fix.

**The same rule for the drop.** `runner.base_drop_due` asks a refused drop again once no piece of the bolt reads live and no landing fix is live. Flume refuses that drop on the same rule (bolt-teams "A base place's drop the runner refused is asked again once nothing on its branch is live").

**Area pages this change touches:** `core.md` (`read.1`, `read.2`, `roles.5`, `roles.6`, `code.7`, `code.8`, `state.2`, `state.4`), `plan.md` (`plan.16`, `plan.21`), `record.md` (`record.1`, `record.3`), `tests.md` (`tests.4`, `tests.11`, `tests.12`) and `docs.md` (`docs.4`, `docs.6`, `docs.7`). No rule changes, so no page is edited (`docs.7`).

## Goals / Non-Goals

**Goals:**

- crew asks no land of a bolt while Flume names a place on the bolt's branch.
- A land refused for that reason waits, and is not a stop. The send stands and its card is left. crew posts the land again once the branch is clear: on the same send at a head whose own work is unchanged, or on proof.
- crew reads "a place on the branch is live" one way, Flume's, for the land and for the drop's re-ask.

**Non-Goals:**

- How long the runner takes to carry a land. That is the runner's.
- Changing Flume, the runner or sluice. crew reads a field Flume already gives.
- What else a stop is. A refusal with no place named and Flume's submission withdrawn or refused stay stops, with their send spent.
- What `crew card read` says of a land not yet posted while places are named. It still says crew's next raise posts it.

## Decisions

### 1. crew reads Flume's `on_branch` as the one fact that a place is live on a bolt's branch

`runner.flume_facts` gives `on_branch`, the places Flume's status names on the base place's branch, each as Flume gives it. An entry that is not text is kept as a place crew can't read. It still counts, so a land is held rather than posted on a guess (`read.1`, `read.2`). A status that gives no list, as Flume 0.17.0's does not, gives `None`, read as naming no place. This follows how a status naming no fix kind reads as a base place with no landing fix (bolt-teams "A bolt's landing fix is read from its base place's status").

Flume's list is the one its retry refusal reads, so crew's guard and Flume's refusal agree by construction. crew builds no reading of its own of which places are live (`roles.5`). The family's rule is one owner: Flume owns a base place's wait (203), and crew cites it.

Not taken:

- Reading crew's own pieces and the landing fix alone, which is what holds a row today. That misses a place crew did not launch, and a place Flume is still making.
- Reading the refusal's words for "(203)". crew reads another tool's output by its facts, not its words (`read.2`).

### 2. No land is posted while Flume names a place on the branch

`runner.lands_due` skips a row whose bolt's base place names a place on its branch, on a send and on proof alike. The send stands, as it does under a hold (rail-cards "A hold on the drive or the kit posts no land"). The first raise after Flume names none posts the land.

The row itself does not change: it keeps its box and stays on its card, and only its land waits.

Not taken: taking the row's box away while a place is named. A place that only takes main in changes nothing the user approves. A box taken away and given back would change or follow the card twice for one landing (rail-cards "A landings card is followed only when its form must change").

### 3. A land refused while a place is named reads waiting, and is recorded once

In `runner.landing_outcome`, the newest land the runner answered refused reads `{outcome: waiting, by: runner, request, words, places}` while Flume's status names a place on the branch. Otherwise it reads stopped, as before.

`plan.landing_entry` records a wait once per land request: `bolt.submit`, `Outcome: waiting`, the land's `Request`, the `Head` it carried, Flume's words as `Why`, no `Refused` and no `Submission` (`record.1`). The words are a tool's, as a stop's are, so `record.3` holds.

`landing_read` records the wait, asks ops nothing and raises no card. There is nothing for ops to do and no card to close: the send stands.

`landing_phase` reads a wait as no landing in flight, so no work is held out of the bolt (`landing_hold`). Nothing is submitted, so work merged meanwhile is in the head the next land carries.

Not taken: recording nothing and reading the wait from Flume's status each time. Once the places end, the status names none, and the refusal would read as a stop and spend the send. An outcome is kept in the run record, where the first act that reads it writes it (`plan.21`).

### 4. A land that waited is no land standing once the branch is clear

`plan.lands_waited(entries)` gives the requests of the lands the run record holds recorded waiting. `runner.landing_of` and `landing_outcome` take them as `waited`. A newest land refused, in `waited`, with Flume naming no place on the branch now, reads `none`: no land stands.

`runner.lands_due` counts a land that waited as no land posted at its head, and as spending no send. `plan.lands_posted` marks each posted land whose request waited, so `lands_change` hands that through.

So the land is posted again on the send that ticked the bolt, while that send stands at the bolt's head now (`send_stands`: its own work unchanged, as when the landing fix only took main in), or on proof.

Every reader of a landing passes `waited`: `Stages.landing`, `landing_read`, `bolt_land`, `landing_phase`'s read and `lands_due`. The rail, the card and the raise then agree.

### 5. The views and the card's read say what the land waits on

`runner.landing_said` words a wait as: "landing at <head> waits on <places> on its branch, nothing of the bolt's: crew asks the runner to land it once none is live". Each place is named by its folder, the last part of Flume's path, as Flume's own line names a place.

- The ledger's head line takes those words.
- The rail's land line keeps how the bolt lands and adds those words. With no land standing while Flume names a place, it says no land of the bolt is asked while those places are live.
- `landing_lines`, for `crew card read land/<kit>`, says of a bolt whose last landing the record holds waiting that its land waits on the places on its branch, with its request and Flume's words, and that the user's send stands and lands it once none is live. It reads this from the run record alone (`waits`, beside `stops`), as it reads a stop.

No key of the views changes, so the mod is untouched (`code.8`): it draws the words it is given.

### 6. The drop's re-ask waits on the same places

`runner.base_drop_due` asks no drop again while the base place's status names a place on its branch, as well as while a piece or a landing fix is live. Flume refuses the drop on the same rule. Without this, a place crew did not launch has crew ask, Flume refuse, and crew ask again once for each refusal.

## Risks / Trade-offs

- [A refusal first read after its places ended reads stopped] → The send is spent, and the user is asked again. The runner carries the answer and the status in one pass, and a place on the branch runs for minutes, so the first read sees the place. A later read costs the user a tap, not a landing. crew infers no wait it cannot read (`read.1`).
- [A place that never ends holds the land] → Flume holds the base place the same way, and never stalls it for this (203). The views name the place, so ops and the user see what holds it.
- [`on_branch` names places being made] → A launch still being made holds the land until Flume ends it. Flume refuses the retry then too, so this is intended.

## After deploy

None. The logic tier proves each decision on Flume 0.19.0's status shapes and on the run record's entries. A host whose crew carries this change reads the next such refusal as a wait at its first read, so no step is needed on a live host.

## Task notes

**1.1** `runner.flume_facts`: `on_branch` as a tuple of the places Flume names, each as text, an entry not text kept as `a place crew can't read`; `None` where the status gives no list. Add two Flume 0.19.0 fixtures under `tests/py/flume-0.19.0/`, each with a line in its README:
- `bolt-forecast-fixed.json`: `bolt-forecast-fixing` after `y-1` landed at `5a6b7c8`, the bolt's head now, `on_branch` empty, waiting on its caller unsubmitted.
- `bolt-place-on-branch.json`: `bolt-failed-fix-due`'s shape, never submitted and with no fix, `on_branch` naming `/Users/chuck/.local/share/flume/places/f3a444f5e38a/fix--y-notes`.

Case `tests/py/test_runner.py::TestABasePlacesStatus::test_the_places_on_a_base_places_branch_are_read_as_flume_names_them`: 0.19.0's `bolt-forecast-fixing` names `fix--y-1`; `bolt-forecast-fixed` names none; 0.17.0's `bolt-submitted` gives `None`; a list holding a number keeps it as a place crew can't read.

**1.2** `runner.landing_outcome`, `runner.landing_of`: the newest land answered refused reads `waiting` with `places` while `on_branch` names any; it reads `none` where its request is in `waited` and `on_branch` names none; otherwise it reads stopped. `landing_of` adds `places` to any outcome whose status names a place. Cases in `tests/py/test_runner.py::TestLandingOf`:
- `test_a_land_refused_while_flume_names_a_place_on_the_branch_waits_on_it` (`bolt-forecast-fixing`, land refused);
- `test_a_land_that_waited_reads_none_once_flume_names_no_place` (`bolt-forecast-fixed`, `waited` holding the land);
- `test_a_land_refused_with_no_place_named_is_stopped` (`bolt-forecast-fixed`, `waited` empty).

The existing `test_the_runner_refusing_the_land_is_stopped_in_its_words` stays as it is, its 0.17.0 status naming no place.

**1.3** `runner.lands_due`: a row whose base place's status names a place on its branch is due nothing. A posted land whose request waited (`posted`'s `waited`) is left out of `here` and spends no send. Cases in `tests/py/test_landings.py::TestLandsDue`:
- `test_no_land_on_a_send_or_on_proof_while_flume_names_a_place_on_the_branch` (`bolt-place-on-branch`, a send and a proof send);
- `test_a_land_that_waited_is_due_again_on_its_send_and_head_once_no_place_is_named` (`bolt-forecast-fixed`): due at the head unmoved, and at a moved head whose own work is unchanged; nothing where its own work changed.

The class's existing cases, on 0.17.0 statuses that give no `on_branch`, stay due as they are.

**1.4** `runner.base_drop_due`: no drop asked again while `on_branch` names a place. Case `tests/py/test_runner.py::TestBaseDrop::test_no_drop_asked_again_while_flume_names_a_place_on_the_branch`.

**2.1** `plan.lands_waited`, `plan.waits` (each bolt whose last `bolt.submit` is `Outcome: waiting`, {bolt: (head, request, words)}), `plan.lands_posted`'s `waited`, and `plan.landing_entry` recording `waiting` once per request. `stops`, `send_spent`, `landing_pending` and `landing_phase` read a wait as neither a stop nor a landing in flight. Cases in `tests/py/test_landing.py::TestTheLandingsRecord`:
- `test_a_land_refused_while_a_place_is_named_is_recorded_waiting_once`;
- `test_a_wait_is_no_stop_and_no_landing_in_flight`.

**2.2** `plan.landing_read`: a wait recorded asks ops nothing (`unlanded_ask` not called) and raises no card (`unheld_raise` not called). Case `tests/py/test_landing.py::TestTheFirstReadActs::test_a_wait_recorded_asks_ops_nothing_and_raises_no_card`.

**2.3** Pass `waited` (`lands_waited` over the entries each already reads) in `Stages.landing`, `landing_read`, `bolt_land` and `landing_phase`'s read. The raise's whole path, on `raise_landings` with stand-in acts as `test_a_stop_on_the_send_closes_the_card_and_asks_again_though_the_head_moved_since` uses them. Cases in `tests/py/test_landings.py`:
- `test_a_land_that_waited_on_a_landing_fix_lands_on_the_same_send_once_it_took_main_in`: the card is left while the land waits and no card follows; once `bolt-forecast-fixed` is carried, one land is posted on the same send at `5a6b7c8`.
- `test_a_land_on_proof_that_waited_is_posted_again_on_proof`.

**3.1** The answered card is left while a ticked bolt's land waits, and the sweep names it as still waited on (`send_waits`, `answered_waits` and `landings_step` reading no stop). Case `tests/py/test_landings.py::test_an_answered_card_whose_ticked_bolts_land_waits_on_its_branch_is_left_its_send_standing`, two ticked bolts landed and the third waiting.

**3.2** `plan.landing_lines` takes `waits` and says, for a bolt the send lands whose last landing waits: "<bolt>: its land, request <n>, waits on the places on bolt/<bolt>, nothing of the bolt's: <Flume's words>; the user's send stands, and lands <bolt> once none is live". `card_read` and `landings_unopened` pass `waits(whole)` or `waits(entries)`. Case `tests/py/test_landings.py::test_crew_card_read_says_a_land_that_waits_on_its_branch_and_that_the_send_stands`.

**4.1** `runner.landing_said` and `outcome_said`: the wait's words, each place by its folder. The board's head line takes them. Case `tests/py/test_board.py::TestALandingFromTheRunnersReport::test_a_landing_that_waits_names_the_places_on_its_branch`.

**4.2** The rail's land line (`plan.rail_rows`, the land group): for outcome `waiting`, how the bolt lands followed by `landing_said`'s words at the head. With no land standing while `places` are named, and nothing else holding the bolt, how it lands followed by "no land of it is asked while <places> <is|are> live on bolt/<bolt>: crew asks the runner once none is". Cases in `tests/py/test_rail.py::TestRows`:
- `test_a_bolt_whose_land_on_proof_waits_on_its_branch_says_so`;
- `test_a_proven_bolt_with_a_place_named_on_its_branch_says_no_land_is_asked_while_it_is_live`.
