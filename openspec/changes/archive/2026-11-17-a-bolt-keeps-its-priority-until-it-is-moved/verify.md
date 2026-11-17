# Verify: a-bolt-keeps-its-priority-until-it-is-moved

Verified on 2026-11-17, on `change/a-bolt-keeps-its-priority-until-it-is-moved` at `a400ddc2`, cut from `bolt/crew-stops-flooding-the-runner-and-your-cards` at `f4f8f5fb`.

**Verdict: the work holds. The whole checks pass, every task is ticked, and every requirement and scenario of the delta specs is met. The change is archived with this report.**

## The whole checks

`tests/suite --affected` ran once, from the worktree's root, as CLAUDE.md names it for a finished change. The change edits crew's command core, so every task was affected.

```
32 passed (30 replayed), 0 failed
```

- `logic` and `contract` ran afresh and passed.
- The 30 end-to-end tests replayed: `tests/suite` replays a test whose inputs are identical to a run that passed on this host. Every end-to-end test passed afresh on this branch at `0dadb34d`. Since then only `tests/py/` and this change's own design, tasks and report have moved, and the end-to-end tests read none of them. `t-specs` and `t-docs` are among them.
- `openspec validate a-bolt-keeps-its-priority-until-it-is-moved --strict` reports the change valid. Each requirement's text above its first scenario is at most 476 characters, under the 500 `t-specs` holds the archived specs to.

## Tasks

All 12 tasks, 1.1 to 3.2, are ticked. Each case a task names exists in the file it names and passes in the logic run above; task 2.5's check is the logic tier whole, which passes. The cases the change replaces are gone: `test_the_first_bolt_in_the_plan_has_the_highest`, `test_a_third_started_raises_those_above_it`, `test_a_reorder_sends_only_what_changed`, `test_its_priority_is_its_bolts_place_in_the_plan` and `test_a_dropped_launch_a_fix_of_main_and_a_bolt_gone_take_no_priority`.

## Requirements and scenarios

Each scenario was read against `plugin/lib/runner.py` and `plugin/lib/plan.py` and the case that proves it. Unless a file is named, the cases are in `tests/py/test_runner.py::TestPriorities`.

### bolt-teams

| Requirement / scenario | Where it holds | Proved by |
|---|---|---|
| A launch names its repository, intent, recipient, priority and brief: Two bolts in order | `op_bolt_start` numbers the bolt, `bolt_launch` and `reach` take its priority | `test_two_bolts_started_in_order` |
| … Work added to a started bolt | `reach` reads `priority_of`; `reach_places` appends no priority | `test_a_drop_a_close_or_work_added_re_sets_no_other_bolt` |
| A start or a reorder appends each priority it changed: A reorder | `op_bolt_order` → `numbering` → `reprioritise` | `test_a_reorder_re_sets_only_the_moved_bolts_places` |
| … A reorder that changes nothing | `numbering` keeps a bolt already in order | the same case, applied twice; `test_a_bolt_already_in_order_keeps_its_number` |
| … A start below the others | `numbering`: the bottom's less `SPACING` | `test_a_placed_bolt_takes_a_number_beside_its_started_neighbours`; `test_a_start_re_sets_no_other_bolt` |
| … A drop and a close | `reach_places` no longer calls `reprioritise` | `test_a_drop_a_close_or_work_added_re_sets_no_other_bolt` |
| … No number left | `numbering` numbers afresh from `FIRST` | `test_with_no_number_left_every_started_bolt_is_numbered_afresh` |
| A started bolt keeps its priority until it is moved: the first, between two, above the top | `numbering`, `priority_of` | `test_a_placed_bolt_takes_a_number_beside_its_started_neighbours`; `test_a_bolts_priority_is_the_newest_its_requests_set` |
| No priority is sent for work that has finished or been dropped: A merged unit on a moved bolt | `priorities` leaves out what `finished` reads over | `test_finished_or_dropped_work_takes_no_priority` |
| … A landed bolt the plan still holds | `finished` reads a launch on `main` over and landed as `landed` | see below |
| … a place crew can't read is re-set | `finished` is false on `unknown` | `test_a_place_crew_cant_read_is_re_set` |
| A fix of main goes above every bolt: launched | `main_priority()` is `MAIN_PRIORITY` | `test_main_fix.py::TestLaunch::test_its_priority_is_above_every_started_bolt` |
| … A fix of main from before | `priorities` lists a standing, unfinished fix of main below `MAIN_PRIORITY`; `op_bolt_order` always calls `reprioritise` | `test_a_fix_of_main_from_before_is_re_set_once` |

*A landed bolt the plan still holds* is proved by two cases that share its one path. `stage_of` reads any launch whose `Base` is `main`, over and landed, as `landed`. `test_a_fix_of_main_from_before_is_re_set_once` pins that `priorities` leaves such a launch out. `test_stages.py` pins a base place over and landed reading `landed`. Run by hand on this branch, `runner.priorities` over a base place `bolt/y` at flume-0.3.6's `landed` or `dropped`, with `y` renumbered, lists only `bolt/x`; at `code` or `bolt-submitted` it lists both.

### rail-cards

| Scenario | Where it holds | Proved by |
|---|---|---|
| Landed as the runner reports it, still in the plan | `lands_due` via `landing_of` | `test_landings.py::TestLandsDue::test_no_land_for_work_the_runner_reports_landed_or_dropped` |
| On main before the runner reports it | `lands_due(on_main)`, `landed_on_main`, `lands_post` | `TestLandsDue::test_no_land_for_a_bolt_read_landed_on_its_kits_main`; `TestTheRaisePostsTheLands::test_a_proven_bolt_already_on_main_is_posted_no_land_on_proof` |
| A fix of main dropped | `lands_due` via `landing_of` | `TestLandsDue::test_no_land_for_work_the_runner_reports_landed_or_dropped` |

## Rules

- `code.7`: `priority_of`, `numbering`, `priorities`, `finished` and `lands_due` are functions of plain facts. `landed_on_main` is the read around `lands_due`.
- `read.1`: a place crew can't read is re-set, not taken as finished. A started bolt whose requests set no priority is refused a launch, naming the bolt. A bolt whose main crew can't read is posted a land as before.
- `state.2`: nothing new is stored. A bolt's number is read from `requests.rec`.
- `code.8`: no view or brief reads a priority, so `board.agent_views` and the mod are untouched.
- `docs.2`: README's account still holds: "with its bolt's priority, the plan's first bolt the highest" and "a reorder of bolts appends a priority for each place whose priority changed". So does the usage header's "a drop and an order of bolts are launches, retries, drops and priorities". No command's usage changes.
- `docs.7`: no page under `docs/architecture/` or `docs/adr/` is edited.
