# Verify: crews-running-parts-move-to-the-installed-version

Verified at 82bae900 on `change/crews-running-parts-move-to-the-installed-version`, 2026-11-18.

**Outcome: the whole checks pass and the work meets its change. The change is archived.**

## The whole checks

`tests/suite --affected`, run once (CLAUDE.md, *Tests*): **35 passed (34 replayed), 0 failed**, exit 0.

| Task | Outcome |
|---|---|
| `tests:logic` | ok, run afresh (`tests/py/test_board.py` changed) |
| `contract`, `mod`, `nix:test`, `nix:typecheck`, and 30 end-to-end tests, `t-hold`, `t-docs` and `t-specs` among them | ok, replayed from passing runs on this host with identical inputs |

`openspec validate crews-running-parts-move-to-the-installed-version --strict`: valid. Each requirement's text above its first scenario is under 500 characters (the longest, the modified "crew reads the crew its host has installed", is 472).

## The work against the change

All 10 tasks in `tasks.md` are ticked done. No code has changed since 55a62612. 82bae900 changes only the two `TestInstalledCrew` cases of `Follower.again`, which add task 2.3, and the design's task notes.

### host-holds-and-updates

- **Each lasting process of crew's moves to the installed crew by itself**: held. The board tab (`board.follow`) and a rail tab without the lock (`board.rail_follow`) look each second through `crew.Lasting`. Each moves through `crew.move_here` as `bash <installed> _board|_rail <label>` in its own process. The flow reader looks after each round, and the follower looks at each refresh through `Follower.lagging` and `again`. A checkout's tab compares its HEAD at its start (`started_commit`) with its HEAD now (`installed_commit`, `head_here`). `ASKED` keeps one ask for each real path.
- **A lasting process moves for an install only on what it read**: held. `move_due` gives None where either commit is unread, `"stuck"` where `CREW_MOVED_TO` names the installed commit, and `"move"` once it names another. `Lasting.look` says "stuck" once. `Follower.again` carries the installed commit it moved for as `CREW_MOVED_TO`. `TestInstalledCrew` now pins that it asks the installed build `crew _release` once, where the host keeps no answer for its path, and reads a checkout's HEAD from its files with no process. A follower stuck for one install moves at the next (`TestRefresh`). `CREW_FOLLOWER_LAGGED` is gone from `plugin/`.
- **A session on an older build of crew is offered a restart at the end of its turn**: held. `plugin/hooks/stop` offers a restart only to a session that no crew agent's record names and that loaded crew from a release. It never offers one to a session loaded from a checkout (its `.git`). It prints `{"systemMessage": …}` alone, naming both versions and the session's id (`t-hold`). A standing agent is handed its restart as before.
- **A session is offered its restart once for each install**: held. The mark under `crew.OFFERS` holds the real path offered for. A later turn with that path unmoved returns before `crew.installed()` and starts no process. An installed crew that can't be read offers nothing.
- **The host keeps each installed build's answer**: held. `kept_path` is None outside `STORE`. `keep_answer` keeps only an answer that was read, writing it whole and renaming it into place. `kept_answer` reads the kept answer through `release_said` and asks again where that fails (`TestInstalled`).
- **crew reads the crew its host has installed** (modified): held. `installed` reads the kept answer before it asks, and asks at most once for each real path.

### crew-board

- **A follower starts again for its crew only on what it read** (removed): `move_due` carries its outcome, and no code still reads `CREW_FOLLOWER_LAGGED`. The requirement stands in `openspec/specs/crew-board/spec.md`, so the archive removes it there.

### run-record

- **A followed record that moves prints each entry once**: held. After printing, `record.follow` hands on `CREW_FOLLOWED` (the day and the tips printed to) through `move_here`'s env. `handed` reads it field by field. The files of a handed tip are taken as printed. A tip that can't be read is said once, and its drive starts afresh (`TestEvents`).

### Docs

README, `plugin/skills/crew/SKILL.md`, `plugin/bin/crew`'s usage header and `hooks.json`'s description say what moves and when (`t-docs` ok).
