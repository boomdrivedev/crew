# A land waits while a place on its bolt's branch is live

## Why

boomdrive-ops's signal `2026-11-15-boomdrive-ops-cb087240/01` (afterthought/crew-state, `boomdrive/main`): crew asked the runner to land flume's bolt `flumes-settings-read-as-its-records-say` while Flume's own landing fix was live on its branch, so Flume refused the base place's submission and the user's send was spent.

The runner's branch shows how. crew posted land 332 at 02:35:26Z on the user's send of `land/flume`, with nothing on the bolt's branch. At 03:18:02Z Flume's settle forecast the bolt's head in conflict with main and launched `fix--flumes-settings-read-as-its-records-say-1` on the branch. At 03:20:30Z the runner carried land 332, and Flume refused the retry: "the base place … is submitted once no place on its branch bolt/flumes-settings-read-as-its-records-say is live … (203)". crew read the refusal as a stop, nothing of the bolt's, and a stop spends the send that posted it. So once the fix had taken main in, the user was asked for the bolt again.

Nothing was wrong with the bolt or the send: Flume was still working on the branch. Flume's statement says a base place waits on the places on its branch while any is live, and refuses its retry meanwhile (blueprints `design/flume/requirements.md` 203 at `cb114fd`). crew reads no place on the branch before it posts a land, and reads every refused land as a stop.

## What Changes

- **No land while Flume names a place on the bolt's branch.** crew posts no land of a bolt, on a send or on proof, while Flume's status of its base place names a place on its branch being made or live. That status field, `on_branch`, is the list Flume's own refusal reads. A send made meanwhile stands, and the first raise after Flume names none posts the land.
- **A land refused while a place is live waits.** When the runner answers a land refused and Flume names a place on the branch, the landing reads `waiting`, not stopped. The first read records it once, a `bolt.submit` with `Outcome: waiting`. It asks ops nothing, raises no card and holds no work out of the bolt. The send that ticked the bolt stands, and its card is left.
- **The land is posted again once the branch is clear.** A land that waited bars no land and spends no send. Once Flume names no place on the branch, crew posts the land again: on the same send while it stands at the bolt's head now, or on proof. A send stands at a head whose own work is unchanged, as after a landing fix that only took main in.
- **The views say it.** The ledger's head line, the rail's land line and `crew card read land/<kit>` name the places a land waits on, and say crew lands it once none is live.
- **The drop's re-ask reads the same fact.** crew asks a refused drop of a base place again only once Flume names no place on its branch, as well as no piece and no landing fix live.
- **A stop is a refusal with no place named.** A land refused while Flume names no place on the branch is still a stop. So is one read from a Flume whose status gives no `on_branch`. Specs that gave a live place as a stop's example now give a refusal with no place named.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `bolt-teams`: no land is posted while Flume names a place on the bolt's branch. A land refused while one is named reads waiting, and the land is posted again once none is. The drop's re-ask waits on the same places. A stop is a refusal with no place named.
- `rail-cards`: a send stands for a bolt whose land waits on its branch, and its card is left. A land that waited bars no land at its head. The scenarios that gave a live place as a stop's cause name a refusal with no place.
- `run-record`: a land that waits is one `bolt.submit` marked `Outcome: waiting`.
- `role-runs`: a land that waits asks ops nothing.
- `crew-board`: a ledger says its landing waits on the places on its branch.
- `crew-rail`: a bolt's land line says its land waits on the places on its branch.

## Impact

- `plugin/lib/runner.py`: `flume_facts` reads `on_branch`. `landing_outcome` and `landing_of` read `waiting`, carry the places named, and read a land that waited as none once nothing is named. `lands_due` posts no land while a place is named and counts a land that waited as none. `base_drop_due` waits on the places named. `landing_said` and `outcome_said` give the words.
- `plugin/lib/plan.py`: `lands_waited` is new. `lands_posted` marks a land that waited. `landing_entry` records `waiting`, and `landing_read` asks and raises nothing for it. `Stages.landing`, `landing_read`, `bolt_land` and `landing_phase` pass the lands that waited. The rail's land line and `landing_lines` say it.
- Tests: `tests/py/test_runner.py`, `test_landing.py`, `test_landings.py`, `test_rail.py`, `test_board.py`, and two Flume 0.19.0 status fixtures under `tests/py/flume-0.19.0/`.
- No key of the views changes, and the mod is untouched (`code.8`): only a landing's words are new. No command, usage, README or brief changes (`docs.2`).
- No change to Flume, the runner or sluice: crew reads the field Flume's status already gives.
