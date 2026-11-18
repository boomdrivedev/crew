# Verify: a-stopped-bolt-proven-again-lands

Verified on 2026-11-17, on `change/a-stopped-bolt-proven-again-lands` at `82ea2df1`, cut from `bolt/crew-lands-bolts-it-stopped` at `616c17df`.

**Verdict: the whole checks pass and the work holds. Every requirement and scenario of the change's two delta specs is met, and every task is ticked done. The change is archived.**

## The whole checks

`tests/suite --affected` ran once, from the worktree's root, as CLAUDE.md names it for a finished change. The change edits crew's command core (`plugin/lib/plan.py`, `plugin/lib/runner.py`), so every test task was affected. None was replayed.

```
32 passed (0 replayed), 0 failed
```

`logic`, `contract` and all 30 end-to-end tests passed, `t-specs`, `t-docs`, `t-cards`, `t-runner` and `t-journey-land` among them. `mod` and the `nix` project's tasks were not affected: no view shape or flake file changed.

`openspec validate a-stopped-bolt-proven-again-lands --strict` reports the change valid. Each requirement's text above its first scenario is under 500 characters (445, 437, 490 and 449), so `t-specs` holds the archived specs too.

## Tasks

All five tasks, 1.1 to 2.3, are ticked. Each case a task names exists in the file it names and passed in the logic tier above.

## What the code does

- **Decision 1.** `plan.stopped_lands` reads each stop, as `stops` counts one. It skips a refused stop, one naming no head, and one that landed nothing at the head of a refusal that still stands (`sent_back`). It matches each stop to its land by `Request`, or to the newest land of the bolt at the stop's head when it names none.
  - `plan.lands_stopped` gives those lands' requests, and `lands_posted` marks each such land `stopped`.
  - `send_spent` spends a card's send for each bolt of which a land that send posted was stopped, whatever was asked since. A stop crew can't place still spends only as the bolt's last landing (`read.1`).
- **Decision 2.** `plan.landings_sent` reads each kept bolt on the card whose close kept it last. It leaves out the bolts `send_spent` spends for that card. Every reader goes through it: `landings_raised` (the raise and `rows_unsent`), `record_reading`'s `sends` (`card_stand`), `landings_unoffered` (`unoffered`) and `landings_earlier` (`sent_left`, `crew card read`).
- **Decision 3.** `runner.lands_due` skips a row whose send's card posted a land of it marked `stopped`, at any head. It adds this to its existing checks.
- **Decision 4** needs no code of its own. Once no send holds the bolt, `lands_by` decides how it lands, as the cases below show.

The rules the design cites hold. Every new function is a decision on facts alone (`code.7`). No view shape changes (`code.8`), and every case is in the logic tier (`tests.4`, `tests.11`). Nothing is written to undo a close (`state.4`).

## Requirements and scenarios

### crew-rail, modified

| Requirement / scenario | Proved by |
|---|---|
| Each bolt's land line says whether its card carries, holds or follows it: its text now counts a send kept on a closed card | `tests/py/test_rail.py::TestRows::test_a_bolt_a_spent_kept_send_held_is_held_by_no_send` |
| … the eight scenarios carried unchanged | `test_rail.py::TestRows`'s `card_stand` table (lines 450–460) and `test_rail.py:484`, unchanged and passing |
| … A send kept on a closed card whose land was stopped (added) | `TestRows::test_a_bolt_a_spent_kept_send_held_is_held_by_no_send`: no card open, the line says what stopped the last landing and that the next card carries it, never "held by your send". The same land recorded waiting still reads held. |

### rail-cards, modified

| Requirement / scenario | Proved by |
|---|---|
| A kit's landings card's close keeps the user's send: a kept send holds no bolt a stop spent | `tests/py/test_landings.py::test_a_send_kept_on_a_closed_card_holds_no_bolt_a_stop_spent` |
| … The sweep closes, The next card, A send closed in Pending You (unchanged) | `test_landings.py` lines 1790 and 1808, passing |
| … A kept send a stop spent (added) | the same case. `landings_sent` gives `y` alone, `rows_unsent` keeps `z` a row at a later head with its own work unchanged, and `sent_left` names `y` alone. A stop on proof or on another card's send keeps `z`. |
| A landing the runner or Flume stopped keeps its box: spent for good, at any head | `test_landings.py::test_a_send_is_spent_for_good_once_a_land_it_posted_was_stopped`; `TestLandsDue::test_a_spent_send_posts_no_land_at_any_head_after_a_later_land` |
| … the five scenarios carried unchanged | `test_landings.py` lines 160, 996 and 2926, `test_runner.py`'s withdrawn cases, and `TestLandsDue::test_a_stopped_row_posts_nothing_on_the_same_send_and_once_on_a_new_one`, unchanged and passing |
| … A later land stopped too (added) | `TestLandsDue::test_a_spent_send_posts_no_land_at_any_head_after_a_later_land`: nothing due on req_1's send, while req_2's is due. The third part of `test_a_bolt_a_spent_kept_send_held_lands_on_proof_once_proven_at_a_new_head`: no land on the spent send, and the card asks for `y` at def5678, saying its land on proof was stopped. |

`test_rail.py::TestSweepJudged::test_an_answered_landings_card_whose_ticked_bolts_land_on_that_send_was_stopped_waits_on_it_no_more` changed as Task notes 1.1 says. A later land on proof at a new head leaves the stopped send waiting on `b` no more.

### rail-cards, added: A stopped bolt proven again lands on proof or is asked on its card

| Scenario | Proved by |
|---|---|
| Proven again at a new head | `test_landings.py::test_a_bolt_a_spent_kept_send_held_lands_on_proof_once_proven_at_a_new_head`: one land on proof at def5678, no card, and the next raise posts none. `test_the_rail_read_raises_a_kit_whose_bolt_a_spent_kept_send_held`: the read raises crew for `y` on proof, and the read after it raises none. `TestRows::test_a_bolt_a_spent_kept_send_held_is_held_by_no_send`: the line says it lands on proof. |
| Marked to stay | the second part of `test_a_bolt_a_spent_kept_send_held_lands_on_proof_once_proven_at_a_new_head`: no land, and a card asks for `z` at def5678 |
| Proven again at the stop's own head | `test_landings.py::test_a_bolt_a_spent_kept_send_held_at_its_stops_head_is_asked_on_the_card`: no land, and the card asks for `z` at abc1234, saying what stopped its last landing |
| Beside a card waiting on the user | the second part of `test_the_rail_read_raises_a_kit_whose_bolt_a_spent_kept_send_held`: `landings_unoffered` names `z`, and the raise changes req_k2 to ask for `z` beside `y` |

## An observation, not a blocker

`landings_sent` now calls `send_spent` once for each card whose close last kept a bolt. Each call reads the whole record again (`stopped_lands`, `last_submits`, `stops`). On a real record I measured `landings_sent` over every landings key, all time, from deneb's `afterthought/crew-state` cache, with the suite running beside it:

| Drive | Before | After |
|---|---|---|
| madswan, 50,802 entries | 0.05 s | 6.0 s |
| afterthought, 30,639 entries | 0.9 s | 2.9 s |

`record_reading` reads only some of those keys, and over the rail's 60-day window it differed by under a second. The cost grows with closes times entries, so a busy drive will feel it. Reading `stopped_lands` once per call of `landings_sent` would remove it. That is a chore for later, and no requirement of this change rests on it.

On the same records, the change drops the bolts it should from the kept sends: boomdrive 26 to 20, agentplot 36 to 29, afterthought 25 to 22.
