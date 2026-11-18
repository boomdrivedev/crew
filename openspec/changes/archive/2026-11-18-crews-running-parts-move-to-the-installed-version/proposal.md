# crew's running parts move to the installed version

## Why

A host installs a newer crew, and every crew process already running keeps the crew it started on. Read on deneb on 2026-11-18, with crew 0.67.1 installed:

- the board tab of wldn's console ran crew 0.50.2, opened on 2026-11-11;
- wldn's flow tab, `crew events --follow`, ran 0.50.2, and a second flow reader for wldn ran 0.61.0, started 2026-11-14;
- 27 Claude sessions had loaded crew's plugin from builds of 0.50.2 (9), 0.59.0 (9), 0.61.0 (7) and 0.64.1 (2), and one from 0.67.1. Their hooks and their band still run that crew's code.

The user saw crew 0.61 and 0.59 still running while 0.67.1 was installed (proposal 90 on boomdrive's plan, approved 2026-11-18).

Two parts of crew already move. The host's follower starts again through the installed crew when it runs another (crew-board "A follower follows on the crew its host has installed"). A standing agent of a main level is restarted at its next stop when the plugin it loaded is no longer the installed crew's (teams.19). Nothing else moves:

- a rail tab that does not hold the follower lock, the board tab and the flow reader run the code they started with until someone ends them;
- a session crew did not start, such as the user's own, a Flume place's, or a role's run the user opened to talk, is never told that its crew is old. Its Stop hook leaves it alone.

The family's principle 5 (boomdrivedev/blueprints `design/principles.md`) asks that a process a tool starts holds nothing its records do not hold, so the next command can start it again and nothing is lost. sluice's statement already says no sluice reader outlives the sluice its host installs (sluice 134). crew's own processes should do the same.

## What Changes

- **Every lasting process of crew's moves to the installed crew by itself.** These are the rail tab, the board tab, the flow reader (`crew events --follow`, in a tab or run by hand) and the follower. Each looks once a second, or at each of the follower's refreshes. When the installed crew names another commit than the one the process started on, the process starts again through the installed command with its own arguments. It keeps its process id, so its tab still reads as crew's. Where crew runs from a checkout, the commit it started on is the checkout's HEAD at its start, so a tab follows the checkout as the follower already does.
- **The flow reader loses and repeats no entry when it moves.** It hands its new self the day its follow began and the tip it last read of each drive's branch. The new process reads from there.
- **A process moves only on what it read, and once for each install.** Where either commit can't be read, it runs on as it is. A process started again for an install that still runs another crew says so once and runs on. The next install moves it again. This replaces the follower's one-time mark, `CREW_FOLLOWER_LAGGED`, with one mark for every lasting process, `CREW_MOVED_TO`, the installed commit it moved for.
- **A session that loaded an older crew is offered a restart at its next pause.** At the end of a turn of any session that is not a standing crew agent, crew's Stop hook checks the build of crew the session loaded. If it names another commit than the installed crew, the hook shows the person one message: the version the session runs, the version installed, and that exiting and resuming the conversation moves it. The message names the session's id. It is shown once for each install, never told to the model, and holds up no turn. A standing agent is still restarted as before.
- **The host keeps each installed build's answer.** A build in the Nix store never changes. So the answer to `crew _release` from an installed command whose real path is in the store is kept on the host by that path, and read there before crew asks again. A session's Stop hook then starts no process at a turn's end until the install moves. An answer crew could not read is never kept.
- README and the crew skill say what moves and when.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `host-holds-and-updates`: a lasting process moves to the installed crew only on what it read, once for each install; a session that loaded an older build is offered a restart at the end of its turn, once for each install; the host keeps each installed build's answer, so a process asks at most once for a real path.
- `crew-board`: the rail and board tabs move to the installed crew by themselves. The follower's own once-only rule gives way to the rule every lasting process holds.
- `run-record`: a followed record moves to the installed crew and prints every entry once.

## Impact

- `plugin/lib/crew.py`: `behind` and `behind_here` move here from `board.py`, so `record.py` and the Stop hook share them; the new decisions `move_due` and `offer_due`; the act `move_here`; the host's kept answers in `installed`.
- `plugin/lib/board.py`: `rail_follow` and `follow` look and move; `Follower.lagging` and `Follower.again` take `CREW_MOVED_TO`.
- `plugin/lib/record.py`: `follow` looks, moves and hands on its place; `handed`, which reads what it was handed.
- `plugin/hooks/stop`: the offer for a session that is no standing agent.
- `tests/py/test_board.py`, `tests/py/test_record.py`, `tests/py/test_release.py`, `tests/py/test_hold.py`, `tests/t-hold.sh`.
- `README.md`, `plugin/skills/crew/SKILL.md`.
- Unchanged: what crew models and the agents' views (`code.8` not reached); a standing agent's restart (teams.19).
- The processes and sessions already running an older crew when this lands carry the old code, which cannot move them. The design's *After deploy* names the hand step for them.
