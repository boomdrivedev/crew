# Design

## Context

This was read on 2026-11-17 at this branch's base, `f4f8f5fb` (crew's main, which is also `bolt/crew-stops-flooding-the-runner-and-your-cards`). Record 0069, accepted 2026-11-16 by boomdrive-design, decides the outcome. This design says how crew builds it.

**How crew numbers a bolt now.** `runner.priority_of(plan, bolt)` is a bolt's place among the plan's started bolts (`Path: flume`), counted from the bottom. `runner.priorities(plan, requests)` lists every standing launch on a started bolt whose `Base` is `bolt/<bolt>` and whose number differs from the last one its requests set. `plan.reprioritise` appends a priority for each.

`reprioritise` runs from `reach_places`, so it runs on every plan write that reaches a started bolt: a start, a drop, work added, moved or amended. It also runs from `op_bolt_order`. A bolt's base place gets its number at its launch and is never re-set, since its `Base` is `main`. `runner.main_priority` gives a fix of main the count of started bolts plus one, set at its launch.

**What it cost.** These counts are from afterthought/crew-state's `boomdrive/main` and deneb's runner branch, `refs/crew/boomdrive/runner/deneb`, read 2026-11-17:

- `requests.rec` holds 1954 requests, 1675 of them priorities. 1034 of those were written on 2026-11-16, the day of the eleven starts in record 0069.
- The runner refused 775 priorities with "no place … stands on this host". Flume's status of each one's place, as the runner carried it, reads over and landed: 722 tidied, 53 over.
- So nearly half of crew's priority requests went to work that had already finished.

**What holds a land off now.** `runner.lands_due` skips a row whose `landing_of` reads `landed` or `dropped`, which comes from Flume's status of the base place or the fix of main as the runner carried it. crew also reads a bolt landed when its kit's main holds its work (`Stages.main_landing`; `plan.21`), and the first act that reads it closes it. Until then, nothing stops a land on proof for that bolt.

None of the 71 lands in `boomdrive/main`'s requests was posted after its bolt reached main. Each was posted before its landing commit. This change closes that one gap, so the unit's "never asked to land again" holds by code.

**What reads a priority.** Flume orders a stream's waiting stages by an `i64` priority (flume `crates/flume-conformance`, `priority: i64`). The runner carries `Option<i64>` (boomdrive `crates/boomdrive/src/flume.rs`). recfix's `int` takes 9007199254740991 and −5000000 (read 2026-11-17).

A role's run launches at priority 0 in the drive's own stream (`asks.py`, `roles.rec`). A kit's work runs in the stream its host maps the repository to, which can be the same stream, as `tests/py/facts.py` `ran` has it. No view and no brief reads a priority: `board.py`, `status.js` and the roles have none.

**The family.** Flume keeps one priority per place and starts waiting stages highest first (flume record 0010). The runner carries each request as given (record 0047 move 5; boomdrive c74a864, 3f7d69b). crew owns the numbers (record 0069, option 1), so the change is crew's alone, and Flume and the runner are cited, not changed.

**Area pages this change touches:**

- `core.md`: `state.1`, `state.2`, `state.4`, `read.1`, `read.2`, `roles.5`, `roles.9`, `code.7`, `code.8`.
- `plan.md`: `plan.1`, `plan.21`.
- `tests.md`: `tests.4`, `tests.11`, `tests.12`.
- `docs.md`: `docs.2`, `docs.4`, `docs.6`, `docs.7`.

No rule changes, so no page is edited (`docs.7`).

## Goals / Non-Goals

**Goals:**

- A start, a close or a drop re-sets no other bolt's places. A move re-sets only the moved bolt's places, each once.
- A new bolt's launches carry their priority from the start.
- No priority goes to work that has finished or been dropped. No land goes to a bolt or fix of main that has landed or been dropped, whatever read says so first and whether or not the plan still holds the bolt.
- The order Flume sees stays the plan's, and a fix of main stays above every bolt.

**Non-Goals:**

- Changing Flume, the runner or sluice (record 0069). The runner already carries only a launch's newest priority.
- Making work added to a bolt, an amendment or a drop cheaper beyond the priorities they no longer append.
- Changing what a view shows. No view draws a priority.

## Decisions

### 1. A bolt's priority is read from its own requests

`runner.priority_of(requests, bolt)` is the `Priority` of the newest request, by its number, among these:

- the launches of the bolt's work: `bolt/<bolt>`, and every launch whose `Base` is `bolt/<bolt>`;
- the priority requests of those launches.

It gives `None` where none is set. A launch on the bolt, a fix's or a take-main's among them, carries the bolt's priority as `priority_of` reads it: `reach`, `fix_launch` and `take_main`. A start run again for a refused launch (`restart`) keeps the number the bolt's requests already set.

Nothing new is stored. `requests.rec` already holds each number crew set, and the plan holds only intent and marks (`state.2`). A bolt started before bolts were base places has no launch of its own, so its number is read from its pieces' requests. Under the old numbering, a base place kept its launch's number while its pieces were re-set. Taking the newest request reads such a bolt at its pieces' number.

Not taken:

- A `Priority` field on the plan's `Bolt` record. It would hold a second copy of what `requests.rec` holds, written by crew on every start.
- Counting the bolt's place, which is today's way and the flood record 0069 ends.

### 2. A bolt started or moved is placed between its started neighbours

`runner.numbering(plan, requests, bolt)` gives `{bolt: its priority}` for each started bolt whose priority must change when `bolt` is started or moved. It is a decision of plain facts (`code.7`). Three numbers are named in `runner.py`:

- `SPACING`, 1000000;
- `FIRST`, 1000000000000;
- `MAIN_PRIORITY`, 2000000000000.

The neighbours are the nearest started bolt above `bolt` and below it in the plan's order that have a priority, leaving `bolt` itself out. The bolt keeps its own priority where it is in order with them: below the one above, or `MAIN_PRIORITY` where there is none, and above the one below, or 0 where there is none. Otherwise it takes:

- with none on either side: `FIRST`;
- with only one below: that one's plus `SPACING`, while that stays below `MAIN_PRIORITY`;
- with only one above: that one's less `SPACING`, while that stays above 0;
- with one on each side: the whole number halfway between theirs, rounded down, where one lies strictly between.

Where none of these gives a number, every started bolt is numbered afresh (Decision 4).

The bounds keep bolts above role runs, which launch at 0, as today. They also keep bolts below a fix of main (Decision 6). With `SPACING` at a million, two neighbours take about twenty bolts between them before a gap runs out. A million bolts can go above the top or below the bottom before a bound is reached.

Keeping its own priority makes a move that changes nothing in the order re-set nothing. It also makes a write replayed at a newer tip append nothing a second time (`plan.1`).

Not taken: no floor at 0. Negative priorities would put a kit's work below role runs where the two share a stream.

### 3. A start numbers its bolt before it launches, and only a move re-sets anything

`op_bolt_start`, for a bolt not started, works in this order:

1. It reads `numbering` once `Path: flume` is set.
2. It appends a priority for each place `priorities` gives for those numbers. That is nothing unless the bolts are numbered afresh.
3. It launches the base place at the bolt's number (`bolt_launch` takes it).
4. `reach_places` launches the pieces, which read the number from the base place's launch.

`op_bolt_order` reads `numbering` for the moved bolt after it moves it, and appends what `priorities` gives. `reach_places` no longer appends any priority. A drop, a close, work added or moved in, and an amendment append none.

`runner.priorities(requests, reads, numbers)` gives `[(launch, its priority)]`. It covers each standing launch of a bolt in `numbers` that is not finished (Decision 5) and whose last set priority differs. Its base place is among them. The base place takes no room in its stream, but it carries the bolt's number for every later launch, so a moved bolt whose pieces have all merged still has its new number read. That costs one more command per move.

`plan.reprioritise(w, numbers)` appends them. It still appends nothing when the branch holds no `requests.rec`.

`reach_places` and `runner.reach` take the bolt's priority where the caller numbered the bolt itself (`priority`), and read it from the bolt's requests otherwise. A start passes the number it gave the bolt, the same its base place's launch carries. A logic case that launches a started bolt's pieces before its base place, or with none, passes the number `numbering` gives (`tests/py/facts.py` `numbered`). Not taken: every such case launching the base place first, which would renumber the requests a hundred cases name.

### 4. Numbering afresh is rare, and each place is re-set once

Where `numbering` finds no number, it numbers every started bolt in the plan's order. The bottom takes `FIRST`, and each one above it takes `SPACING` more. Only the bolts whose priority changes are listed, so `priorities` re-sets each of their unfinished places once.

The first such numbering after this change lands is certain. Bolts numbered the old way sit 1, 2, 3 … apart, so the first start below the bottom or move between two finds no room. That numbers them afresh once, re-setting each unfinished place once. It is not the eleven re-sets each place took on 2026-11-16.

### 5. Finished or dropped work takes no priority

`runner.finished(requests, reads, launch)` is true when `piece_stage` reads the launch in any of these stages:

- `merged`, `landed` or `dropped`;
- `refused`;
- `unlaunched` with `refused`, which is a base place whose launch the runner refused.

A launch crew dropped is already left out by `standing`. This holds whether or not the plan still holds the bolt. Work gone from the plan takes no number anyway, since `numbering` lists only started bolts.

A launch whose stage reads `unknown`, because crew can't read its runner or its place, is re-set. crew takes nothing it can't read as finished (`read.1`). Leaving it out would leave a live place out of order. Re-setting a place that has ended costs one refused answer from the runner.

Not taken: reading the runner's refusals, "no place … stands on this host". crew reads another tool's facts, not its words (`read.2`). Flume's status already says the place is over.

### 6. A fix of main takes a priority above every bolt's

`runner.main_priority()` gives `MAIN_PRIORITY`. Every bolt's number stays below it (Decision 2), so a fix of main stays ahead of every bolt's work for as long as it stands, not only at its launch.

`priorities` also lists each standing fix of main that is not finished and whose last set priority is not `MAIN_PRIORITY`. That is a fix launched under the old numbering, and the next start or move re-sets it once. Two stand on `boomdrive/main` now: request 1217 at 29, live, and request 1954 at 13.

### 7. No land for work that has landed or been dropped

`runner.lands_due` already skips a row whose `landing_of` reads `landed` or `dropped`, whether or not the plan still holds the bolt. A case pins that.

It also takes `on_main`, the bolts crew reads landed on their kit's main, and posts no land for them, on a send or on proof. `plan.lands_post` reads `on_main` for its rows with a box before its write. It uses `Stages.main_landing` over the drive's plan, requests and runners, as `landing_on_main` does. `lands_change` takes `on_main` and passes it on.

A bolt read landed is closed by the first act that reads it (`plan.21`). This only keeps the raise from asking for it meanwhile. Nothing crew can't read is taken as landed (`read.1`), so a bolt whose main can't be read is posted as today.

## Risks / Trade-offs

- **Numbering afresh is still a burst.** → It costs one request for each unfinished place of the started bolts, once. It happens when two neighbours have taken about twenty bolts between them, and once after this change lands, over the old numbers.
- **Numbers are long.** A request reads `Priority: 1000001500000`. → Only the order between numbers means anything (record 0069, consequences). Nobody reads them but Flume.
- **A place crew can't read is re-set.** → If it has ended, the runner refuses one request. This is the price of not guessing a place finished (`read.1`).
- **A fix of main from before stays below the spaced bolts until the next start or move.** → Starts and moves come many times a day, and the first one re-sets it.
- **A bolt that reaches main between `lands_post`'s read and its write is posted a land.** → Flume answers it as it answers any land of a base place whose work is on main, and `plan.21`'s close follows.

## Migration

No step. The first start or move that finds no room numbers the started bolts afresh (Decision 4), and the first start or move re-sets a fix of main from before (Decision 6). Both are code in this change.

## After deploy

None. Every decision is proved in the logic tier on requests, plans and the runner's records. A host whose crew carries this change numbers bolts this way from its next start or move, with nothing to run by hand.

## Task notes

**1.1** `runner.priority_of(requests, bolt)`: the newest `Priority`, by request number, among the launches of `bolt/<bolt>` and of every launch whose `Base` is `bolt/<bolt>`, and the priority requests whose `Of` names one of those. Give it as an `int`, or `None` where none is set. Its callers drop the `plan` argument.

Case `tests/py/test_runner.py::TestPriorities::test_a_bolts_priority_is_the_newest_its_requests_set` covers:

- a bolt whose base place's launch set 7, with a piece re-set to 9 after it, reads 9;
- a bolt with no launch of its own reads its pieces' newest;
- a bolt with no requests reads `None`.

The old `test_the_first_bolt_in_the_plan_has_the_highest` goes, since it pins the count this change ends.

**1.2** `runner.numbering(plan, requests, bolt)`, with `SPACING`, `FIRST` and `MAIN_PRIORITY`, as Decision 2 gives it. Update the module docstring's "each launch's priority follows its bolt's place in the plan (priorities)" to say the bolt keeps its priority until it is moved.

Cases in `tests/py/test_runner.py::TestPriorities`:

- `test_a_placed_bolt_takes_a_number_beside_its_started_neighbours`: alone, `FIRST`; above the top, its plus `SPACING`; below the bottom, its less `SPACING`; between 1000001000000 and 1000000000000, 1000000500000. A bolt in the plan but not started is no neighbour.
- `test_a_bolt_already_in_order_keeps_its_number`: a moved bolt already between its new neighbours gets `{}`.

**1.3** `numbering` with no number left: every started bolt in the plan's order from `FIRST` up, `SPACING` apart, listing only those whose priority changes.

Case `tests/py/test_runner.py::TestPriorities::test_with_no_number_left_every_started_bolt_is_numbered_afresh`:

- 3, 2 and 1 with the bottom moved between the other two;
- a bottom at `SPACING` with a bolt started below it;
- a top at `MAIN_PRIORITY` less 1 with a bolt started above it.

**1.4** `runner.finished(requests, reads, launch)` and `runner.priorities(requests, reads, numbers)` as Decisions 3 and 5 give them.

Cases in `tests/py/test_runner.py::TestPriorities`:

- `test_finished_or_dropped_work_takes_no_priority` replaces `test_a_dropped_launch_a_fix_of_main_and_a_bolt_gone_take_no_priority`. These take no priority:
  - a launch crew dropped;
  - one the runner answered refused, through `facts.ran`'s `refused`;
  - a piece over and landed, through flume-0.3.6's `landed`;
  - a piece over and dropped, through flume-0.3.6's `dropped`;
  - a base place the runner refused.

  A piece in `code` and a base place live take the number.
- `test_a_place_crew_cant_read_is_re_set`: a launch whose runner is not in `reads` is listed.

**1.5** `runner.main_priority()` gives `MAIN_PRIORITY`, and `main_fix_launch` carries it. `priorities` lists each standing fix of main, not finished, whose last set priority is not `MAIN_PRIORITY` (Decision 6).

Cases:

- `tests/py/test_main_fix.py::TestLaunch::test_its_priority_is_above_every_started_bolt` asserts 2000000000000, and drops its `priority_of` line.
- `tests/py/test_runner.py::TestPriorities::test_a_fix_of_main_from_before_is_re_set_once`: a fix of main at 3 and live is listed once, and not after a priority of it at `MAIN_PRIORITY` stands.

**2.1** `runner.bolt_launch(plan, bolt, label, priority)`. `op_bolt_start` follows Decision 3's order for a bolt not started. `restart` relaunches at `priority_of(requests, bolt)`.

Cases in `tests/py/test_runner.py`:

- `TestPriorities::test_two_bolts_started_in_order`: `x` then `y` give `bolt/x` and its unit `FIRST`, and `bolt/y` and its unit `FIRST` less `SPACING`. Each launch's fields are as today.
- `TestPriorities::test_a_start_re_sets_no_other_bolt` replaces `test_a_third_started_raises_those_above_it`: `x`, `y` and `z` started in turn append no priority.
- `TestBoltLaunch::test_its_priority_is_the_one_it_is_given` replaces `test_its_priority_is_its_bolts_place_in_the_plan`.
- `TestBoltLaunch::test_the_launch_is_crews_kind_on_main_with_ops_its_recipient_and_no_brief_or_after` passes the priority.

**2.2** `op_bolt_order`: after the move, `reprioritise(w, runner.numbering(w.plan, requests, a.bolt))` with `w.runners()` as `reads`.

Cases in `tests/py/test_runner.py::TestPriorities`:

- `test_a_reorder_re_sets_only_the_moved_bolts_places` replaces `test_a_reorder_sends_only_what_changed`. `bolt order z --before y` over `x`, `y` and `z` appends a priority of `bolt/z` and `unit/z-unit` at the halfway number and nothing else. Applying it again appends nothing.
- `test_a_reorder_on_a_branch_with_no_requests_writes_none` stays as it is.

**2.3** `reach_places` drops its `reprioritise` call. `reach` and `fix_launch` carry `priority_of(requests, bolt)`, and `take_main` through `fix_launch`. `reach_places` refuses, naming the bolt, a launch for a started bolt whose requests set no priority (`read.1`), which no start leaves.

Cases:

- `tests/py/test_runner.py::TestPriorities::test_a_drop_a_close_or_work_added_re_sets_no_other_bolt`. Over `x`, `y` and `z` started:
  - `bolt drop y` appends no priority for `x` or `z`;
  - `y` gone from the plan, as a close leaves it, then `bolt order x --first` appends none;
  - `unit add` to `x` launches at `x`'s priority and appends no priority.
- `tests/py/test_cross.py::TestStart::test_a_third_bolt_started_has_its_launches_follow_the_requests_already_written` asserts acts `["launch", "launch", "launch"]`.

**2.4** The cases that pinned a priority counted from the plan read the bolt's number:

- `test_cross.py`'s `launch` default becomes `str(runner.FIRST)` for a lone bolt `x`;
- `test_fix.py`'s `test_a_review_note_marked_fix_is_a_launch_of_a_fix_on_the_bolts_branch`;
- `test_main_fix.py`'s `test_main_red_after_a_landing_is_a_fix_place_on_main_held_for_the_users_send_with_ops_its_recipient`.

The check runs these three files.

**3.1** `runner.lands_due(rows, sent, requests, reads, posted=(), work=None, on_main=())`: no land for a row whose bolt is in `on_main`.

Cases in `tests/py/test_landings.py::TestLandsDue`:

- `test_no_land_for_work_the_runner_reports_landed_or_dropped`. Each row is ticked and none is due:
  - `y`'s base place at flume-0.3.6's `landed`, with `y` still a row;
  - the fix of main at flume-0.3.6's `dropped`.
- `test_no_land_for_a_bolt_read_landed_on_its_kits_main`: `y` in `on_main`, its base place live with no land, is due nothing on a send or on proof, and `z` beside it stays due.

**3.2** `plan.lands_post` reads `on_main` for the bolts of its rows with a box before its write, by `Stages(fleet, plan, {}, runs={label: (requests, reads)}, label=label).main_landing`, and passes it to `lands_change`, which passes it to `lands_due`.

Case `tests/py/test_landings.py::TestTheRaisePostsTheLands::test_a_proven_bolt_already_on_main_is_posted_no_land_on_proof`. It uses `on_main` and `started_y` as `TestTheSweepClosesABoltOnMain` does. `lands_post` with `proof=True` for `y` posts nothing and writes nothing.
