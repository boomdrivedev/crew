# Verify: crews-running-parts-move-to-the-installed-version

Verified at 55a62612 on `change/crews-running-parts-move-to-the-installed-version`, 2026-11-18.

**Outcome: the whole checks fail. The change is not archived and goes back to its code stage.**

## The whole checks

`tests/suite --affected`, run once (CLAUDE.md, *Tests*): **34 passed (1 replayed), 1 failed**, exit 1.

| Task | Outcome |
|---|---|
| `tests:logic` | **FAIL**: 2 failed, 3906 passed |
| `contract`, `mod`, `nix:test`, `nix:typecheck`, and 30 end-to-end tests, `t-hold`, `t-docs` (replayed) and `t-specs` among them | ok |

`openspec validate crews-running-parts-move-to-the-installed-version --strict`: valid. Each requirement's text above its first scenario is under 500 characters (the longest, the modified "crew reads the crew its host has installed", is 472).

### What fails

Both are existing cases of `tests/py/test_board.py::TestInstalledCrew`, which pin that `Follower.again` runs `crew _update` for each drive and no other process:

- `test_an_install_hands_out_the_restarts_and_starts_the_follower_again_through_the_installed_crew` (line 525): `again` also ran `bash <profile>/crew _release`.
- `test_on_a_checkout_the_follower_starts_again_as_its_own_board` (line 607): `again` also ran `git -C <checkout> rev-parse HEAD`.

The cause is in c62f653a: `Follower.again` now builds its environment with `crew.MOVED_TO: crew.installed_commit()`. On a build where the process has not asked for this real path and the host keeps no answer, `installed_commit` asks the installed command `crew _release`. On a checkout whose files can't say its HEAD, `head_here` falls back to `git rev-parse`. Both go through `subprocess.run`, which these cases record. Task 2.2's check names `TestRefresh` and two single cases of `TestInstalledCrew`, so it passed while these two cases of the same class failed.

Either `again` hands on the installed commit it has already read (its `lagging`, or an update's own read) without starting a process, or these two cases change to say what `again` now runs. The design (Decision 2) says a look costs file reads alone while the install has not moved; that is the code stage's call.

## The work against the change

Every task in `tasks.md` is ticked done. Read against the delta specs at 55a62612:

### host-holds-and-updates

- **Each lasting process moves to the installed crew by itself**: held. The board tab (`board.follow`) and a rail tab without the lock (`board.rail_follow`) look each second through `crew.Lasting`, and move through `crew.move_here` as `bash <installed> _board|_rail <label>` in their own process. The flow reader looks after each round. The follower moves at its refresh through `Follower.lagging` and `again`. A checkout's tab compares its HEAD at its start with its HEAD now (`started_commit`, `installed_commit`). `ASKED` keeps one ask for each real path.
- **A lasting process moves for an install only on what it read**: held. `move_due` gives None where either commit is unread, `"stuck"` where `CREW_MOVED_TO` names the installed commit, and `"move"` once it names another. `Lasting.look` says "stuck" once. A follower stuck for one install moves at the next (`TestRefresh`). `CREW_FOLLOWER_LAGGED` is gone from `plugin/`.
- **A session on an older build is offered a restart at the end of its turn**: held. `plugin/hooks/stop` offers only a session whose record names no crew agent, loaded from a release, and never one loaded from a checkout (its `.git`). It prints `{"systemMessage": …}` alone, with both versions and the session's id (`t-hold`). A standing agent goes on to its restart as before.
- **A session is offered its restart once for each install**: held. The mark under `crew.OFFERS` holds the real path offered for. A later turn with the path unmoved returns before `crew.installed()` and starts no process. An unread installed crew offers nothing.
- **The host keeps each installed build's answer**: held. `kept_path` is None outside `STORE`. `keep_answer` keeps only a read answer, written whole and renamed into place, and `kept_answer` reads through `release_said` and asks again where that fails (`TestInstalled`).
- **crew reads the crew its host has installed** (modified): held, `installed` reading the kept answer before it asks.

### crew-board

- **A follower starts again for its crew only on what it read** (removed): its outcome is carried by `move_due`, and no code still reads `CREW_FOLLOWER_LAGGED`.

### run-record

- **A followed record that moves prints each entry once**: held. `record.follow` hands on `CREW_FOLLOWED` (day and tips printed to) through `move_here`'s env after printing. `handed` reads it field by field. A handed tip's files are taken as printed. An unreadable tip is said once, and its drive starts afresh (`TestEvents`).

### Docs

README, `plugin/skills/crew/SKILL.md`, `plugin/bin/crew`'s usage header and `hooks.json`'s description say what moves and when (`t-docs` ok).

Apart from the two failing cases, the work meets its specs.
