# A bolt keeps its priority until it is moved

## Why

crew numbers a started bolt by where it sits among the plan's started bolts, counted from the bottom. So every start adds one to each bolt above it, and every close or drop takes one off. The order is the same, but every number has changed, and crew sends a priority request for every place whose number changed. On 2026-11-16 the planner started eleven bolts. 46 places were already launched, and each start renumbered all of them: 450 priority requests and 22 launches. The runner spent most of 89 minutes renumbering places whose order never moved, while launches and landings waited behind them (record 0069).

crew also sends a priority for a place whose work is over. Of the 1675 priority requests on afterthought/crew-state's `boomdrive/main`, deneb's runner refused 775 with "no place … stands on this host". Each was for a place Flume's status, as the runner carried it, reads over and landed. A land is held off only by the runner's report. A bolt crew reads landed on its kit's main (`plan.21`) can still be offered a land on proof before the runner reports it landed or crew closes it.

## What Changes

- **A bolt's priority is the newest one its own requests set.** Starting, closing or dropping a bolt changes no other bolt's priority, and appends no priority request for any other bolt.
- **A start places the new bolt between its started neighbours.** Its launches carry that priority from the start. A bolt alone takes 1000000000000. One above the top takes the top's plus 1000000, one below the bottom takes the bottom's less 1000000, and one between two takes the whole number halfway between theirs.
- **A move re-sets only the bolt that moved.** It appends a priority for each of that bolt's places, its base place included, at a priority between its new neighbours', and none for any other bolt. A bolt whose priority already sits between its new neighbours' keeps it.
- **Numbering afresh is rare.** It happens only when no whole number is left where a bolt goes. Then every started bolt is numbered again from 1000000000000 upward, 1000000 apart, and each place whose priority changes is re-set once. Bolts stay above 0, where role runs sit, and below a fix of main.
- **A fix of main goes above every bolt.** Its launch carries 2000000000000. A fix of main still standing from the old numbering is re-set to that once, by the next start or move.
- **No priority for finished work.** crew sends none for a place the runner reports merged, landed or dropped, or whose launch the runner refused or crew dropped, whether or not its bolt is still in the plan.
- **No land for a bolt already landed.** crew posts no land, on a send or on proof, for a bolt it reads landed on its kit's main. That adds to the bolt or fix of main the runner reports landed or dropped, whether or not the plan still holds it.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `bolt-teams`: a launch carries its bolt's priority, read from the bolt's requests. A started bolt keeps its priority until it is moved, and a move re-sets only its own places. A start, close or drop re-sets no other bolt. Finished or dropped work takes no priority, and a fix of main takes a priority above every bolt's.
- `rail-cards`: no land is posted for a bolt or fix of main that has landed or been dropped, whether read from the runner's report or from the kit's main, and whether or not the plan still holds the bolt.

## Impact

- `plugin/lib/runner.py`:
  - `priority_of` reads a bolt's priority from its requests.
  - `numbering` (new) places a started or moved bolt, or numbers every started bolt afresh. `SPACING`, `FIRST` and `MAIN_PRIORITY` hold its numbers.
  - `priorities` re-sets only the bolts `numbering` gives, and a fix of main still on an old number. `finished` (new) leaves out work that is over.
  - `bolt_launch`, `reach`, `fix_launch` and `restart` carry the bolt's priority from its requests, and `main_priority` gives `MAIN_PRIORITY`.
  - `lands_due` posts no land for a bolt read landed on main.
- `plugin/lib/plan.py`: `op_bolt_start` numbers the bolt before its launches. `op_bolt_order` re-sets only the bolt it moved. `reach_places` no longer re-sets any priority, so a drop, a close or work added re-sets none. `lands_post` reads which of its rows' bolts are landed on main, and `lands_change` passes them on.
- Tests: `tests/py/test_runner.py`, `test_cross.py`, `test_main_fix.py`, `test_fix.py`, `test_landings.py`.
- No key of the views changes, and the mod is untouched: no view draws a priority (`code.8`). No command's usage changes. README's account stays true: a start's launches carry the bolt's priority, the plan's first highest, and a reorder appends a priority for each place whose priority changed (`docs.2`).
- Flume, the runner and sluice are unchanged (record 0069).
