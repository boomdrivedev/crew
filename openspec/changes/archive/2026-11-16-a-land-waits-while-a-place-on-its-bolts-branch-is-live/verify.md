# Verify: a-land-waits-while-a-place-on-its-bolts-branch-is-live

Verified 2026-11-16 on `change/a-land-waits-while-a-place-on-its-bolts-branch-is-live` at `c0c6a9de`, cut from `bolt/a-sent-landing-waits-its-turn` (`b097ed4b`).

**Verdict: the work holds.** The whole checks pass, every task is ticked done, and every requirement and scenario of the six delta specs is met by the code and proved by a case.

## The whole checks

`tests/suite` was run once, from the place's root, as the branch stands. It ran every project's `check-full` tasks, the ones sluice requires of `bolt/*` and `main`.

```
37 passed (5 replayed), 0 failed
exit 0
```

Every task passed: `contract`, `logic`, `mod`, `nix:format`, `nix:lint`, `nix:test`, `nix:typecheck`, and all 30 end-to-end tests (`t-briefs` to `t-word`, `t-specs` and `t-suite` among them). The five replayed were `mod` and the four `nix:*` tasks. This change touches none of their inputs. The rest ran fresh.

Also run:

- `openspec validate a-land-waits-while-a-place-on-its-bolts-branch-is-live --strict`: valid.
- Each requirement's text above its first scenario, added or modified, is at most 500 characters. The longest is 488 (rail-cards "A landings row is due one land for each send and head"). So `t-specs` holds once the change is archived.
- No MODIFIED requirement drops a scenario its main spec holds. Each one keeps every scenario and adds the waiting cases.

## Tasks

All 13 tasks are `[x]`. Every case a task names exists once, at the path and class it gives, and passed in the logic tier above:

| Task | Cases |
|---|---|
| 1.1 | `test_runner.py::TestABasePlacesStatus::test_the_places_on_a_base_places_branch_are_read_as_flume_names_them` |
| 1.2 | `test_runner.py::TestLandingOf::` `…waits_on_it`, `…reads_none_once_flume_names_no_place`, `…with_no_place_named_is_stopped` |
| 1.3 | `test_landings.py::TestLandsDue::` `test_no_land_on_a_send_or_on_proof_while_flume_names_a_place_on_the_branch`, `test_a_land_that_waited_is_due_again_on_its_send_and_head_once_no_place_is_named` |
| 1.4 | `test_runner.py::TestBaseDrop::test_no_drop_asked_again_while_flume_names_a_place_on_the_branch` |
| 2.1 | `test_landing.py::TestTheLandingsRecord::` `…recorded_waiting_once`, `test_a_wait_is_no_stop_and_no_landing_in_flight` |
| 2.2 | `test_landing.py::TestTheFirstReadActs::test_a_wait_recorded_asks_ops_nothing_and_raises_no_card` |
| 2.3 | `test_landings.py::` `test_a_land_that_waited_on_a_landing_fix_lands_on_the_same_send_once_it_took_main_in`, `test_a_land_on_proof_that_waited_is_posted_again_on_proof` |
| 3.1 | `test_landings.py::test_an_answered_card_whose_ticked_bolts_land_waits_on_its_branch_is_left_its_send_standing` |
| 3.2 | `test_landings.py::test_crew_card_read_says_a_land_that_waits_on_its_branch_and_that_the_send_stands` |
| 4.1 | `test_board.py::TestALandingFromTheRunnersReport::test_a_landing_that_waits_names_the_places_on_its_branch` |
| 4.2 | `test_rail.py::TestRows::` `test_a_bolt_whose_land_on_proof_waits_on_its_branch_says_so`, `…says_no_land_is_asked_while_it_is_live` |

Both Flume 0.19.0 fixtures the Task notes name, `bolt-forecast-fixed.json` and `bolt-place-on-branch.json`, are under `tests/py/flume-0.19.0/`, each with its line in that folder's README.

## Requirements and scenarios

### bolt-teams

- **No land is posted while Flume names a place on the bolt's branch.** `runner.flume_facts` reads `on_branch`: a tuple of places, an entry that is not text kept as `UNREAD_PLACE`, and `None` where the status gives no list. `runner.landing_of` carries it as `places`. `runner.lands_due` skips any row whose landing names `places`, on a send and on proof alike. Scenarios: "A place on the branch at the send", "A land due on proof" and "Nothing on the branch any more" are `test_no_land_on_a_send_or_on_proof…`, which covers both a send and proof, and the same send due once the place is gone. "A status that names no places" is the class's existing 0.17.0 cases, which stay due.
- **A land refused while a place on its bolt's branch is live waits.** `runner.landing_outcome` reads a land the runner refused as `waiting`, with Flume's words and `places`, while `on_branch` names any. `plan.landing_entry` records it once per request. `plan.landing_read` returns before `unlanded_ask` and `unheld_raise`. Scenarios: "Flume's landing fix launched after the land was posted" and "Read again" are `test_a_wait_recorded_asks_ops_nothing…`, which records once, asks nothing and raises nothing. "Work joins the bolt meanwhile" is `test_a_wait_is_no_stop_and_no_landing_in_flight`: `landing_phase` is `None`, so `landing_hold` holds nothing.
- **A land that waited is posted again once no place on its branch is live.** `plan.lands_waited` and `lands_posted`'s `waited` mark feed `landing_of`/`landing_outcome`, which read such a land as `none` once no place is named. `lands_due` leaves it out of `here` and spends no send. `plan.landing_waited` passes it through `Stages.landing`, `landing_read`, `started_land` (`crew bolt land`) and `phase_at`. Scenarios:
  - "The landing fix took main in" is `test_a_land_that_waited_on_a_landing_fix_lands_on_the_same_send…`: one land at `5a6b7c8` on `req_k1`, and no card follows.
  - "The place ended with the head unmoved" and "Its own work changed" are `test_a_land_that_waited_is_due_again…`: due at the unmoved head and at a moved head with the bolt's own work unchanged, and nothing where its own work changed. Once the send does not stand, the following card asks for the bolt as before.
  - "A land on proof that waited" is `test_a_land_on_proof_that_waited…`.
- **MODIFIED "A landing's outcome is read from the runner's report".** It now names the outcomes waiting and none-after-a-wait, proved by the three `TestLandingOf` cases. The existing 0.17.0 stop case is unchanged.
- **MODIFIED "A landing is recorded by the first act that reads it".** A wait's words are recorded as `Why`. `landings_judged` counts `waiting` as decided, so the sweep's read records it.
- **MODIFIED "A landing stopped by nothing of the bolt's…".** A refusal with no place named is still a stop that spends the send. `test_an_answered_card…` checks the stopped variant too: the card closes naming the stop.
- **MODIFIED "A base place's drop … asked again once nothing on its branch is live".** `runner.base_drop_due` skips while `on_branch` names a place. `TestBaseDrop` proves it.

### rail-cards

- **A send stands for a bolt whose land waits on its branch, its card left.** `stops`, `send_spent` and `ticked_waits` read a wait as no stop, so `landings_step` leaves the card and `answered_waits` says "waits on the runner to land z". `landing_lines` takes `waits` and says the send stands, from both `card_read` and `landings_unopened`. Scenarios: "Ticked beside two that land" is case 3.1, "The card's read" is case 3.2, and "The send carried" is case 2.3's raise. Its close once z lands is the existing close path, which reads `bolt.land`.
- **MODIFIED** "due one land for each send and head", "keeps its box", "asks only about the rows a send must land" and "A stop closes the answered landings card…" now name a refusal with no place. The stop paths are unchanged, and the existing cases still pass.

### run-record

- **A land that waits on its branch is one entry marked waiting.** `landing_entry` gives `Outcome: waiting`, `Request`, `Head`, Flume's words as `Why`, and no `Refused` or `Submission`. A second read writes nothing (case 2.1). The run record's descriptor comment in `record.py` names the new use of `Request`. No field is new.
- **MODIFIED "A landing's Submission is the merge queue's entry Flume names".** A wait carries no `Submission`.

### role-runs

- **MODIFIED "A landing refused or stopped is an ask of ops".** A wait asks ops nothing: `landing_read` returns before `unlanded_ask` (case 2.2).

### crew-board

- **A ledger says its landing waits on the places on its branch.** `runner.outcome_said` words a wait at its head, and `places_said` names each place by its folder. `landing_line` passes `waiting` with its head (case 4.1).
- **MODIFIED "refused or stopped at its head".** The stop's words are unchanged, and the existing cases pass.

### crew-rail

- **A bolt whose land waits on its branch says so.** `rail_rows` adds the wait's words after how the bolt lands. Where no land stands while places are named, it says no land is asked while they are live (case 4.2, both scenarios).
- **MODIFIED "A bolt that can land says how it lands".** It is unchanged for a stop, and the existing `TestRows` cases pass.

## Rules

- `code.7`: `lands_waited`, `waits` and `landing_waited` are decisions on facts. `landing_waited` reads the run record only through the function it is handed, and only where a stop by the runner might be a wait.
- `code.8`: no key of the views changes, `plugin/hooks/status.js` is untouched, and `mod` and `t-journey-board` pass.
- `read.1` and `read.2`: an unreadable `on_branch` entry holds the land. A status with no list names no place. A run record that can't be read makes `Stages.landing` say unknown, not a guess.
- `roles.5`: crew reads Flume's own list, the one Flume's refusal reads. It builds no reading of its own of what is live.

## Findings

None. Nothing falls short of the change.
