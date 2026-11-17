# Verify: a-bolt-keeps-its-priority-until-it-is-moved

Verified on 2026-11-17, on `change/a-bolt-keeps-its-priority-until-it-is-moved` at `0dadb34d`, cut from `bolt/crew-stops-flooding-the-runner-and-your-cards` at `f4f8f5fb`.

**Verdict: the work falls short. The whole checks fail, so the change is not archived.** It goes back to its code stage.

## The whole checks

`tests/suite --affected` ran once, from the worktree's root, as CLAUDE.md names it for a finished change. The change edits crew's command core, so every task was affected. Nothing was replayed.

```
30 passed (0 replayed), 2 failed
FAIL  contract
FAIL  logic
```

Every end-to-end test passed, `t-specs` and `t-docs` among them. `openspec validate a-bolt-keeps-its-priority-until-it-is-moved --strict` reports the change valid.

### logic: 105 failed, 3712 passed

The change causes both groups below. Every case the tasks name passes. The failures are in cases the tasks don't name.

1. **`tests/py/test_rail.py::runs` shadows its own parameter. 89 failures, all in `test_rail.py`.** The change added `numbered` to the line `from facts import FactsWrite, numbered, ran` inside `runs(p=None, at=None, before=None, numbered=None, read=True)`. That import rebinds the `numbered` parameter to the function `facts.numbered`, so line 89, `(numbered or {}).items()`, raises `AttributeError: 'function' object has no attribute 'items'` on every call. The fix is to import `facts.numbered` under another name, or to rename the parameter.

2. **Fixtures with a started bolt and no priority in its requests are now refused. 16 failures.** These are in `test_chores.py` (6), `test_unit_commands.py` (6), `test_proposals.py` (2) and `test_rail.py` (2). Task 2.3 has `reach_places` refuse a launch for a started bolt whose requests set no priority. These fixtures mark a bolt `Path: flume` with no base place launch, so each plan write that reaches the bolt (`unit add`, `chore add`, `unit split`, `unit move`, `unit drop`, `--unblocks`, a proposal's apply) now fails, for example:
   - `crew can't launch unit/a, unit/b: no request of bolt tenant-environments's sets its priority, …`
   - `launch 3 for bolt/tenant-environments names no Priority: …`, from `bolt_launch` given `priority_of` of requests with none.

   The refusal is the design's (Decision 3, Task notes 2.3). The fixtures need to give their started bolts a priority, by a base place launch or `facts.numbered` as Task notes 2.4 does for the other cases.

   Failing cases:
   - `test_chores.py::TestCommands`:
     - `test_add_writes_the_kind_where_a_unit_would_go`
     - `test_order_after_move_and_drop_act_on_a_chore`
     - `test_a_drop_takes_its_name_out_of_what_comes_after_it`
     - `test_unblocks_puts_a_chore_ahead_of_the_first_unmerged_work`
     - `test_a_signal_routes_to_the_chore_in_the_same_write`
     - `test_a_signals_short_id_routes_the_signal_it_numbers_by_its_full_id`
   - `test_unit_commands.py`:
     - `TestAdd::test_a_unit_goes_at_the_end_of_its_bolt_or_before_one_named`
     - `TestAdd::test_its_sources_and_after_are_recorded`
     - `TestSplit::test_narrows_a_unit_and_adds_the_rest_right_after_it`
     - `TestMove::test_a_unit_with_no_worktree_goes_to_the_end_of_another_bolt_and_loses_its_after`
     - `TestDrop::test_removes_the_unit`
     - `TestUnblocks::test_work_a_started_bolt_needs_goes_ahead_of_its_first_open_unit`
   - `test_proposals.py::TestRestsOnAccepted`:
     - `test_a_queued_unit_moved_into_a_bolt_is_read_from_the_plan`
     - `test_a_source_read_as_written`
   - `test_rail.py`: the cases whose bolt `held` launches `unit/n` and `unit/q`.

### contract: 1 failed, 130 passed

`tests/contract/test_remote_limit.py::TestOriginFetch::test_main_now_on_an_origin_that_never_answers[/bin/bash]` failed with `ValueError: not enough values to unpack (expected 1, got 0)` at `(pid,) = calls(pids)`: the stub origin's pid file recorded no call. The change touches neither `plan.MAIN` nor any fetch, so this looks like a timing failure on a loaded host rather than this change's. The suite was run once, as the stage asks, so it was not run again. Sluice runs it afresh on the submission.

## Tasks

All 13 tasks (1.1 to 3.2) are ticked. Each case a task names exists in the file it names. The cases the change replaces are gone: `test_the_first_bolt_in_the_plan_has_the_highest`, `test_a_third_started_raises_those_above_it`, `test_a_reorder_sends_only_what_changed`, `test_its_priority_is_its_bolts_place_in_the_plan` and `test_a_dropped_launch_a_fix_of_main_and_a_bolt_gone_take_no_priority`. The named cases pass in the logic run above. A task's check is its named cases. The whole tier, which those cases sit in, fails as above.

## Requirements and scenarios

The code matches the delta specs. Each scenario was read against `plugin/lib/runner.py` and `plugin/lib/plan.py` and the case that proves it.

### bolt-teams

| Requirement / scenario | Where it holds | Proved by |
|---|---|---|
| A launch names its repository, intent, recipient, priority and brief: Two bolts in order | `bolt_launch`, `reach` take the bolt's priority | `TestPriorities::test_two_bolts_started_in_order` |
| … Work added to a started bolt | `reach` reads `priority_of`; `reach_places` appends no priority | `test_a_drop_a_close_or_work_added_re_sets_no_other_bolt` (unit add at 1000000000000, no priority) |
| A start or a reorder appends each priority it changed: A reorder | `op_bolt_order` → `numbering` → `reprioritise` | `test_a_reorder_re_sets_only_the_moved_bolts_places` (halfway between neighbours, `bolt/z` and its unit only) |
| … A reorder that changes nothing | `numbering` keeps a bolt already in order | same case, applied twice; `test_a_bolt_already_in_order_keeps_its_number` |
| … A start below the others | `numbering`, bottom less `SPACING` | `test_a_placed_bolt_takes_a_number_beside_its_started_neighbours`; `test_a_start_re_sets_no_other_bolt` |
| … A drop and a close | `reach_places` no longer calls `reprioritise` | `test_a_drop_a_close_or_work_added_re_sets_no_other_bolt` |
| … No number left | `numbering` numbers afresh from `FIRST` | `test_with_no_number_left_every_started_bolt_is_numbered_afresh` |
| A started bolt keeps its priority until it is moved: first, between two, above the top | `numbering` | `test_a_placed_bolt_takes_a_number_beside_its_started_neighbours`; `test_a_bolts_priority_is_the_newest_its_requests_set` |
| No priority is sent for work that has finished or been dropped: A merged unit on a moved bolt | `priorities` skips `finished` | `test_finished_or_dropped_work_takes_no_priority` |
| … A landed bolt the plan still holds | `finished` reads a base place at `landed` | covered by `finished`'s stage list; no case puts a base place at `landed` (see Observations) |
| … a place crew can't read is re-set | `finished` is false on `unknown` | `test_a_place_crew_cant_read_is_re_set` |
| A fix of main goes above every bolt: launched | `main_priority()` is `MAIN_PRIORITY` | `test_main_fix.py::TestLaunch::test_its_priority_is_above_every_started_bolt` |
| … A fix of main from before | `priorities` lists a standing, unfinished fix of main below `MAIN_PRIORITY`; `op_bolt_order` always calls `reprioritise` | `test_a_fix_of_main_from_before_is_re_set_once` |

### rail-cards

| Scenario | Where it holds | Proved by |
|---|---|---|
| Landed as the runner reports it, still in the plan | `lands_due` via `landing_of` | `TestLandsDue::test_no_land_for_work_the_runner_reports_landed_or_dropped` |
| On main before the runner reports it | `lands_due(on_main)`, `landed_on_main`, `lands_post` | `TestLandsDue::test_no_land_for_a_bolt_read_landed_on_its_kits_main`; `TestTheRaisePostsTheLands::test_a_proven_bolt_already_on_main_is_posted_no_land_on_proof` |
| A fix of main dropped | `lands_due` via `landing_of` | `test_no_land_for_work_the_runner_reports_landed_or_dropped` |

## Observations

These don't block the change:

- The scenario *A landed bolt the plan still holds* has no case that puts a base place at `landed`. Run by hand against this branch, `runner.priorities` gives a base place at flume-0.3.6's `landed` or `dropped` no priority, and one at `code` or `bolt-submitted` its number. A case for it in `test_finished_or_dropped_work_takes_no_priority` would make the scenario proved by a check (`docs.6`).
- README's account of priorities ("with its bolt's priority, the plan's first bolt the highest"; "a reorder of bolts appends a priority for each place whose priority changed") still holds, as the proposal says. No view or brief reads a priority (`code.8`).

## What the code stage owes

- Fix the `numbered` shadowing in `tests/py/test_rail.py::runs`.
- Give the started bolts in the fixtures of `test_chores.py`, `test_unit_commands.py`, `test_proposals.py` and `test_rail.py` a priority their requests set, so the 2.3 refusal doesn't fire there.
- Then the logic tier has to pass whole (`tests/suite logic`), not only the cases the tasks name.
