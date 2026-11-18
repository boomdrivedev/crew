# Design

## Context

This section records what was read on 2026-11-18 from boomdrive's drive branch (`afterthought/crew-state`, `boomdrive/main` as crew's cache held it at 2026-11-17 20:43 -0500) and at this branch's base, `616c17df`. The decisions below rest on it.

**The case.** The signal `2026-11-18-boomdrive-ops-9c91dc07/01` names four bolts on deneb. The run record holds each the same way:

| Bolt | Land, send it was posted on | Close that kept the send | Stopped | Proven again |
|---|---|---|---|---|
| `flumes-settings-read-as-its-records-say` | 332, `req_d2c7ae4c54e24fcebf2d`, at 26b1eca | `req_d2c7…`, `Heads: flumes-settings-read-as-its-records-say@26b1eca` | 2026-11-15 03:23Z | 340bcb5 |
| `a-drives-machine-and-state-are-named-once` | 1378, `req_cc0ab9d4abaa4f378cba`, at b586cd6 | `req_cc0a…`, its `Heads` | 2026-11-16 15:47Z | 39c3a31 |
| `the-runner-needs-no-hand-on-a-host` | 1379, `req_cc0ab9d4abaa4f378cba`, at 5332f1c | `req_cc0a…`, its `Heads` | 2026-11-16 15:47Z | a50bb36 |
| `boomdrives-checks-read-no-markdown` | 1383, `req_03d6e942ee0b423ba19f`, at ac7caa9 | `req_03d6…`, its `Heads` | 2026-11-16 16:11Z | 0322639 |

Each card closed once its send's lands were posted, a card following it for other rows. As rail-cards "A kit's landings card's close keeps the user's send" has it, the close kept the send for the ticked bolts in its `Heads`. Each land was then refused, and crew recorded it `Outcome: stopped` in Flume's words: "the base place … is submitted once no place on its branch … is live, and …/fix--<bolt>-1 is (203)". These stops were recorded before crew read Flume's 203 refusal as a wait (`a-land-waits-while-a-place-on-its-bolts-branch-is-live`, archived 2026-11-16 21:56Z). The fix then merged into each bolt, moving its head with its own work unchanged, and the bolt read proven there. None is marked to stay.

**Why nothing was posted.** At the new head:
- `rail_rows` reads no stop at the head now (`stopped_at`), so `lands_by` reads `"proof"`. The line says the bolt lands on proof at the next read.
- `landings_proven` finds no land posted at the new head, so `proof_due` holds and `sweep_moved` raises the kit on every read.
- `landings_raised` reads the kept send from `landings_sent`, the bolt at its old head. `rows_unsent` finds the send standing, since the bolt's own work is unchanged (`send_stands`). So the bolt goes to `landing`, the bolts an earlier send lands. It is then neither in `proven` nor a row of the card.
- `post_lands` hands that send to `runner.lands_due`. The bolt's last land was stopped and was posted on that card's send, so the send is spent and nothing is due.

So every read raised the kit, posted nothing and asked nothing, and the rail went on saying the bolt lands at the next read.

**At the stop's own head** the same kept send holds the bolt. `lands_by` reads `"send"`. `card_stand` gives `holds` for a bolt in the kept sends that the open card does not show, so the line says "held by your send on land/<kit>: crew asks the runner to land it on that send". `unoffered` counts the bolt held, so the rail's read raises nothing for it. `rows_unsent` hands it to the spent send as above.

**What the fix of 2026-11-15 covered.** `a-stopped-landing-puts-its-bolt-back-on-a-card` added `send_spent` for the send of the card still open: `card_stand`'s answered branch, `unoffered`'s ticked, `ticked_waits` and the raise's step read it. It left two gaps:
- No reader of the sends kept on closed cards (`landings_sent`) asks whether a stop spent them.
- `send_spent` and `runner.lands_due` read a send as spent only while its stopped land is the bolt's last landing (`stops`, and `lands_due`'s match of the last land's request). rail-cards "A landing the runner or Flume stopped keeps its box" says the send is spent: "crew SHALL post no land of it again on that send". Once a later land of the bolt is asked, on proof at a new head, the spent send reads as standing again. If that later land is stopped in turn, `lands_due` would post a land on the spent send.

**The family.** No other tool keeps, reads or spends crew's sends. The runner carries the lands crew posts, Flume answers them, and crew reads both from the runner's branch as before. Flume's 203 refusal is a wait since `a-land-waits-while-a-place-on-its-bolts-branch-is-live`. This change leaves that reading alone, and no other tool changes.

**Area pages this change touches:** `core.md` (`read.1`, `roles.3`, `code.7`, `code.8`, `state.2`, `state.4`), `plan.md` (`plan.16`, `plan.21`), `tests.md` (`tests.4`, `tests.11`, `tests.12`) and `docs.md` (`docs.4`, `docs.6`, `docs.7`). No rule changes, so no page is edited (`docs.7`).

## Goals / Non-Goals

**Goals:**

- A bolt whose land on a send was stopped lands once it reads proven again:
  - on proof at a new head, when it is not marked to stay and the user has not left it;
  - otherwise as a row of its kit's landings card, its stop's own head among them.
- A send a stop spent is spent for good, for every reader and for the act that posts lands.
- The rail's line and the raise agree: no line says a bolt lands on proof, or is held by a send, while no raise would post its land.

**Non-Goals:**

- Re-reading the stops recorded before crew read Flume's 203 refusal as a wait. The run record is append-only (`state.4`), and those four bolts land on proof by this change.
- How a stop is read from the runner's report (`runner.landing_of`, `landing_entry`).
- What `lands_by` says of a bolt whose earlier send still stands. The raise lands such a bolt on that send, as today.

## Decisions

### 1. A stop spends the send that posted the land for good

`send_spent(entries, card, bolts)` keeps its signature and its result, `{bolt: (head, words)}`. It gives each bolt of which a land that card's send posted was stopped, whatever was asked of the bolt since. The head and words are those of the newest such stop.
- A stop is matched to the land it stopped by its `Request`. A stop naming none, as an older crew recorded it, is matched to the newest land crew posted of the bolt at the stop's head (`stopped_by`).
- A stop counts as `stops` counts one: `Outcome: stopped`, naming its head, not refused, and not one `sent_back` reads as landing nothing.
- A stop whose posting crew can't tell still spends the send only where it is the bolt's last landing (`stop_spends(None, card)`, `read.1`), as now. An old stop crew can't place spends nothing, so no send is barred by a guess.

`lands_stopped(entries)` is the new decision that matches stops to lands: the requests of the lands crew posted that the run record holds stopped, as text. `lands_posted` marks each such land `stopped: True`, as it marks one that waited, and `send_spent` reads it. A land that waited is no stop and spends nothing, as before (`lands_waited`).

Not taken: the last landing alone, as `send_spent` read it. A land on proof asked at a new head made the spent send read as standing again. Every kept-send reader of Decision 2 would then hand the bolt back to that send while its land on proof was in flight, and to the spent send once that land was stopped too.

### 2. A send kept on a closed card holds no bolt a stop spent

`landings_sent(entries, key, owner)` keeps its result, `{bolt: the head they ticked}`, from the `Heads` of each close of the key in the owner's name, the last for each bolt. It now leaves out each bolt that `send_spent` spends for the card whose close kept it. A later close keeping the bolt again, from a later card's send, is read on its own card.

Every reader of the kept sends follows, with no change of its own:
- **The raise.** `landings_raised` reads `sent` from it. `rows_unsent` then finds no send for the bolt and keeps it a row, and `bolt_work` is asked of none. The bolt lands as `lands_by` reads it (Decision 4).
- **The rail's line.** `record_reading`'s `sends` reads it, and `card_stand` gives the bolt `carries` or `follows`, never `holds`.
- **The rail's read.** `landings_unoffered` hands it to `unoffered`, which counts a bolt that lands on the send and can land, held by no send and shown on no row, so the read raises the card.
- **`crew card read land/<kit>`.** `landings_earlier` and `sent_left` no longer name the bolt among what an earlier send still lands.

`lands_sent`, the sends the raise posts on, keeps reading each close's `Heads` as it is. The act that posts holds the spent rule itself (Decision 3), so a reader that misses it posts nothing on a spent send (`roles.3`).

Not taken: dropping the bolt from the close's `Heads` when the stop is read. The close is written before the stop, a run-record entry is never rewritten (`state.4`), and the reading of a send is a decision on the record as it stands (`code.7`).

### 3. The runner's `lands_due` posts nothing on a spent send

`runner.lands_due` skips a row whose send's card posted a land of the row that the run record holds stopped, read from `posted` (`lands_posted`'s `stopped`), at the row's head now or any. This is besides its present checks: a land that card's send posted at the head now, and the runner's stop of the last land, not yet recorded, that card's send posted. A send at the head of a land stopped on proof or on another card's send is still due its land there, so rail-cards "A send at the head of a stopped land on proof" and "A later card at the head of a stopped land" hold as they are.

### 4. A stopped bolt proven again lands on proof or is asked on its card

With Decisions 1 to 3, no send holds such a bolt, and `lands_by` decides how it lands, as for any bolt:
- **At a new head**, its stop no longer at its head now, a bolt not marked to stay and not left reads `"proof"`. `landings_proven` raises its kit at the next rail read on the main level's host. The raise keeps it a row and posts its land on proof (`Form: proof`, no `Card`), since `lands_due` reads no land at the new head. The read after it finds the land posted and raises none. Once that land lands, the bolt is told on its card (`told_on`).
- **Marked to stay or left**, it reads `"send"`. It is a row of the card at its new head, posted, changed or followed by `landings_step` as any row.
- **At its stop's own head**, it reads `"send"`, its row saying what stopped its last landing. Its land line says the card carries or follows it. `unoffered`, or `sweep_judged` with no card open, raises the card, which asks for it with its box.
- **A later land on proof stopped too.** If that land, at the new head, is stopped in turn, the bolt reads `"send"` there. Its row says its land on proof was stopped (`stopped_on_proof`), and only a new send of the user's lands it. The spent send posts nothing (Decision 3).

Not taken:
- **A land posted on the spent send at the new head**, as a wait's standing send would have been. The stop spent it, as the run record holds, and rail-cards says crew posts no land of it again on that send.
- **The rail's line naming the kept send for a bolt the raise hands to it.** A send that still stands posts its land, so that line is right in what follows. Only a spent send left a bolt with nothing sent, and Decision 2 ends that.

## Risks / Trade-offs

- [A stop recorded of a land that was really a wait, as the four bolts' were] → The send is read as spent, and the bolt lands on proof in ops's name, or is asked on its card if it stays. That is what the user would see of any bolt proven at a new head, and nothing is posted twice.
- [A land on proof posted for a bolt whose stopped send the user meant to stand] → A bolt not marked to stay lands on proof once proven, the user's word since record 0067. A bolt the user means to keep is marked to stay or held.

## Migration Plan

- Nothing is written: the run record and the plan stand as they are.
- On deneb, the first rail read on boomdrive's main level whose crew carries this change raises `land/flume` and `land/boomdrive`. Their raises post the four bolts' lands on proof at their heads now, and each is told on its kit's card once it lands.

## After deploy

None. The logic tier proves each decision, the raise's acts on stand-ins, and the rail's read through `sweep_moved`.

## Task notes

The cases use `tests/py/test_landings.py`'s helpers: `proof_acts` (y not marked to stay, z marked), `proof_read`, `SweepActs`, `TestLandsDue`, `row`, `work`, `H1` (abc1234) and `H2` (def5678).

**1.1** `plan.lands_stopped`, `plan.lands_posted`'s `stopped`, `plan.send_spent`, as Decision 1 has it. Case `tests/py/test_landings.py::test_a_send_is_spent_for_good_once_a_land_it_posted_was_stopped`, covering:
- a land on req_k1's send stopped, the last landing: spent;
- a land on proof asked since at a new head, and that land stopped too: req_k1's send still spent, with the head and words of its own stop;
- a stop of a land on proof, or on req_k2's send, spends none of req_k1's;
- a stop naming no request, matched at its head;
- a stop crew can't place, the last landing, spends it; the same stop followed by a later land spends nothing;
- a land recorded waiting is not marked stopped.

In `tests/py/test_rail.py::TestSweepJudged::test_an_answered_landings_card_whose_ticked_bolts_land_on_that_send_was_stopped_waits_on_it_no_more`, the case of a later land asked again becomes a land of `b` asked on proof at a new head, `Form: proof` and no `Card`. With it, `send_waits` is `[]`: the send waits on `b` no more.

**1.2** `runner.lands_due`, as Decision 3 has it. Case `tests/py/test_landings.py::TestLandsDue::test_a_spent_send_posts_no_land_at_any_head_after_a_later_land`, covering:
- y's land 5 on req_1's send, stopped at H1, then a land on proof at H2, stopped too;
- the row ticked on req_1's send at H1, standing at H2 by its own work unchanged: nothing due;
- req_2's send at H2: due.

`TestLandsDue::test_a_stopped_row_posts_nothing_on_the_same_send_and_once_on_a_new_one` passes unchanged.

**2.1** `plan.landings_sent`, as Decision 2 has it. Case `tests/py/test_landings.py::test_a_send_kept_on_a_closed_card_holds_no_bolt_a_stop_spent`, covering:
- req_k1's close keeping y and z at H1, and z's land on that send stopped: `landings_sent` gives y alone;
- z's stop of a land on proof, or on req_k2's send: z kept;
- a later close of req_k2 keeping z at H2: z kept at H2;
- `rows_unsent` over y and z at H2, their own work unchanged: y lands on the earlier send, and z is a row with no words of a send;
- `sent_left` names y alone.

**2.2** The raise, as Decision 4 has it, through `plan.raise_landings` on `proof_acts`. Each case's entries hold req_k1 posted, answered and closed keeping the bolt at H1, and its land 5 on req_k1's send asked and then stopped at H1, Flume's 203 words as `Why`.

Case `tests/py/test_landings.py::test_a_bolt_a_spent_kept_send_held_lands_on_proof_once_proven_at_a_new_head`, covering:
- y read proven at H2 with its own work unchanged: one land posted on proof at H2, `Form: proof` and no `Card`, no card posted, and the next raise posting none;
- z, marked to stay, the same: no land, and a card posted asking for z at H2 with its box;
- y's land on proof at H2 stopped too: no land on req_k1's send, and a card asking for y at H2, saying its land on proof was stopped.

Case `tests/py/test_landings.py::test_a_bolt_a_spent_kept_send_held_at_its_stops_head_is_asked_on_the_card`: z still at H1, its row stopped there. No land is posted, and the card posted asks for z at H1 with its box, saying what stopped it.

**2.3** The rail's line and read. Case `tests/py/test_rail.py::TestRows::test_a_bolt_a_spent_kept_send_held_is_held_by_no_send`, through `rail_rows` on a record reading holding req_k1's close keeping `b` and `b`'s land on that send stopped, covering:
- `b` at the stop's head, no card open: its line says what stopped its last landing and that the next card under `land/crew` carries it, and not "held by your send";
- the same with that land recorded waiting rather than stopped: `b`'s line says the user's send on `land/crew` holds it;
- `b`, not marked to stay, proven at a new head with its own work unchanged after the stop: its line says it lands on proof, and nothing of the send.

Case `tests/py/test_landings.py::test_the_rail_read_raises_a_kit_whose_bolt_a_spent_kept_send_held`, through `plan.sweep_moved` on `SweepActs` over `proof_read`, covering:
- y at H2, the signal's case: the read raises crew for y on proof, the raise posts its land on proof, and the read after it raises none;
- z at H1 beside an open card waiting on the user that shows another row: `landings_unoffered` names z, and the raise changes the card to ask for z.

## Rules relied on

- `plan.16` as record 0067 amends it: a proven bolt not marked to stay lands on proof, and a send lands one marked to stay.
- `plan.21`: what the runner reports is read by the first act that reads it. No agent and no user is needed for these bolts to land.
- `read.1`: a stop crew can't place spends a send only at the bolt's last landing, and nothing is posted twice on one send.
- `roles.3`: the act that posts lands holds the spent rule itself.
- `state.2`, `state.4`: nothing is written to undo a close's `Heads`. Each reading is computed from the record.
- `code.7`: `lands_stopped`, `send_spent`, `landings_sent`, `rows_unsent`, `card_stand`, `unoffered` and `runner.lands_due` start no process.
- `code.8`: no shape the views or the mod read changes.
- `tests.4`, `tests.11`, `tests.12`: every case is in the logic tier.
- `docs.4`, `docs.6`, `docs.7`: the specs change only by this change's deltas, every scenario has its case, and no rule page or record is edited.
