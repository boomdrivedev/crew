# Design: crew's running parts move to the installed version

## Context

The proposal gives deneb's reading of 2026-11-18. Rules this change relies on:

- `state.4`: crew runs no service; a derived cache is kept only as a read of what it is keyed by.
- `read.1`: refuse, or act on nothing, rather than guess.
- `read.2`: another tool's output, and a file crew did not just write, is read field by field.
- `read.4`: crew never takes over something it did not make.
- `code.2`: a refusal is a `Refusal`, never a traceback.
- `code.7`: a decision is a function of facts.
- `teams.19`: a standing agent is restarted for an update at its next stop.
- `roles.3`: a fix adds a check in crew, not firmer words.

The family's principles (boomdrivedev/blueprints `design/principles.md`) it relies on:

- 5: a process a tool starts holds nothing its records do not hold.
- 3: a design never rests on one host's layout.
- 12: no code carries a transition.
- 19: what the person reads is plain English.

It touches the areas of these pages:

- `teams.md`: `plugin/lib/crew.py`.
- `record.md`: `plugin/lib/record.py`.
- `briefs.md`: `plugin/skills/`.
- `tests.md`: `tests/`.
- `docs.md`: `README.md`, `openspec/`.

`plugin/lib/board.py` and `plugin/hooks/stop` belong to no page's area. The change departs from no rule. It changes nothing crew models, so the views and the mod are not reached (`code.8`).

The tasks name no run of the tests the change affects (`tests/suite --affected`). This stage's brief asks for the narrowest check on each task, and the verify stage runs crew's whole checks once, after the last task. That departs from `openspec/config.yaml`'s rule that the last task runs `--affected`.

### What runs crew, and what moves today

A host runs crew in three kinds of place:

- **Commands** start, act and end. Each runs the crew the host has installed (host-holds-and-updates "A standing agent's crew commands run the crew its host has installed"), so a command is never old.
- **Lasting processes** run until something ends them. These are the host's follower (`crew _follow`, or a rail tab holding the follower lock) and the console's tabs: rail, board and flow. The flow tab runs `crew events --follow`, which a person can also run by hand. A tab's process runs the code it was started with. A waiting command, such as `crew unit wait` or `crew review --wait`, ends within its own timeout (`code.9`), so it is a command here.
- **Claude sessions** load crew's plugin folder when they start: its hooks, its mod and its skills. On a build, the folder is a path in the Nix store, and the session keeps running that build's hooks and mod for as long as it lives.

Only two of these move when a newer crew is installed. The follower starts itself again through the installed command (crew-board "A follower follows on the crew its host has installed"). A standing agent of a main level is restarted at its next stop (`teams.19`). Everything else keeps its crew until a person ends it.

### The family

sluice holds that no sluice reader outlives the sluice its host installs. A newer watch takes the reader's lease and the older reader follows it, and a newer command has an older host process hand over and end (sluice 134, 135). Flume reports at a start's ack a plugin version other than its binary's (flume, the `started` row). Read in blueprints' statements on 2026-11-18, no tool of the family offers a session a restart for its plugin.

This design gives crew's own processes sluice's outcome: no process outlives the crew its host installs. It does this without a lease, since every lasting process of crew's but the follower reads only. Each tool moves its own processes, and no tool calls another (principle 7).

A session's plugins come from several tools at once, built from one flake (principle 17). Should another tool come to offer a session a restart for its plugin, the offers should be one, owned by whatever installs a session's plugins together. Until then crew offers for its own.

## Decisions

### Decision 1: each lasting process moves itself

Each lasting process of crew's looks, on its own clock, at whether the host's installed crew is still the one it started on. When it is not, the process starts itself again through the installed command. The board tab, the rail tab and the flow reader look once a second, the clock they already draw or read on. The follower looks at each refresh, as it does now.

This is principle 5's shape. A tab holds nothing its files and the branch do not hold: the rail and board frames, and the run record. So it loses nothing by starting again. A process that starts itself again needs no service, no timer and no host job, so the move works on any host and for a flow reader run by hand (principle 3, `state.4`).

Considered and not taken:

- `crew console up` ending each tab whose process runs an older crew. swancloud's timer runs it every five minutes on deneb. That is one host's layout, it would not reach a flow reader run by hand, and it would be a second mover beside the process itself.
- A job that ends crew's old processes on an install. crew runs no service (`state.4`), and ending a process from outside cuts a draw or a read midway, where the process can choose its point.

### Decision 2: what the process compares

Two facts are compared by commit:

- **The crew the process started on.** On a build, its release's commit (`crew.crew_read`, a file read, read once since a build never changes). On a checkout, the checkout's HEAD when the process started (`crew.head_here`, read from the checkout's files with no process).
- **The installed crew.** Where the installed command is the process's own checkout, the checkout's HEAD now (`crew.head_here`). Otherwise the installed crew's answer to `crew _release` (`crew.installed`), asked once for each real path of the installed command, and kept on the host for a build (Decision 7).

`behind(mine, theirs)` decides, as it decides for the follower now. It is True when both name a commit and the commits differ, False when they name the same one, and None when either names none. It moves from `board.py` to `crew.py`, so that `record.py` and the Stop hook share it.

Comparing a checkout's HEAD at the start with its HEAD now is new for the tabs. It is what the follower already does, through its stamp (`board.crew_stamp`). On a host in the live mode, `crew/live` moves under a running tab, and the tab then runs the code of the commit it started at.

A look costs file reads alone while the install has not moved: the path walk of `crew.installed_here`, the real path of the installed command, and on a checkout three small files. It starts a process only when the installed command's real path moved and the host keeps no answer for the new path.

### Decision 3: a move starts the process again in its own process

`crew.move_here(argv, moved_to)` is the act. It runs `os.execvpe` on `bash <installed command> <argv>`, where `argv` is the process's own arguments after its module: `_board wldn`, `_rail wldn`, or `events --follow --label wldn`. The environment carries `CREW_MOVED_TO`, the installed commit it moved for, and whatever the process hands on (Decision 5). This is the follower's own way of starting again (`Follower.again`), made one act for every lasting process.

The process keeps its id through the exec. So the console still reads the tab's pane as running crew's command (`crew.tab_holds`), and a SIGUSR1 sent to it still reaches it. Where the exec fails, the process says so once on its standard error and runs on as it is.

The rail tab that holds the follower lock moves at the follower's refresh, through `Follower.again`, which hands the lock on and hands out the restarts due. A rail tab without the lock moves through `move_here`, with no lock to hand.

### Decision 4: a move happens only on what was read, and once for each install

`move_due(lag, moved_to, installed)` decides, from `behind`'s answer, the commit the process was started again for (`CREW_MOVED_TO`, or None), and the installed commit now:

- **None, run on as it is.** The lag is not True. Either commit is unread, so nothing starts again on a guess (`read.1`).
- **"stuck", say once and run on.** The lag is True, and the process was already started again for this installed commit. This happens when a build's release disagrees with its own `crew _release`, or when an install moves between the ask and the exec.
- **"move".** The lag is True, and the process was not started again for this commit.

So a stuck process moves again once the installed crew names another commit. The follower's mark, `CREW_FOLLOWER_LAGGED`, said only whether the follower had ever started again for a lag. A follower once stuck that way never followed a later install. `CREW_MOVED_TO` replaces it: `Follower.lagging` reads `move_due`, and `Follower.again` sets `CREW_MOVED_TO` to the installed commit it read, for an update as for a lag. crew-board's "A follower starts again for its crew only on what it read" gives way to host-holds-and-updates' rule for every lasting process.

### Decision 5: the flow reader hands on where it was

`crew events --follow` prints what reaches the branch after it starts, and its first read of a branch prints nothing. A move that started it afresh would skip every entry that arrived between the old process's last read and the new one's first. So before it moves, the follow sets `CREW_FOLLOWED` to JSON naming the day its follow began and, for each drive, the tip it last read.

`record.handed(text)` reads that value field by field (`read.2`). It returns the day and the tips, or None for a value that is missing or not that shape. The new process takes a handed tip as its first read of that drive: it reads the run-record files at that tip as already printed, and then goes on from the branch's tip as it stands. A tip that crew's cache cannot read is said once, and the drive starts as a new follow would, from the branch as it stands. A drive the handed value does not name starts the same way.

The follow moves only after it has printed everything it read, so the tips it hands on are the tips it printed to.

### Decision 6: a session crew did not start is offered its restart

crew's Stop hook today acts only for a standing crew agent. Every other session is left alone. Now, at the end of a turn of any session that is not a crew agent, the hook offers a restart where the session runs an older build of crew. That covers the user's own sessions, a Flume place's agent and a role's run that the user opened.

The hook runs from the plugin folder the session loaded. On a build, that folder is the session's crew for as long as it lives, so the hook reads what the session loaded from its own root (`crew.crew_read`), with no record of the session's start.

`offer_due(loaded, installed, offered_for, real)` decides. Its facts are what the session loaded, the installed crew, the real path of the installed command the session was last offered for (its mark), and that real path now. It is True only when all of these hold:

- the session loaded a build, read from a release;
- the session has not already been offered for this real path;
- `behind(loaded, installed)` is True.

Unread facts give False (`read.1`).

The offer is one message shown to the person, the Stop hook's JSON `systemMessage`, which Claude Code shows in the session and gives the model nothing. `offer_said` words it in plain English (principle 19), as in "This session runs crew v0.59.0, and v0.67.1 is installed. To run v0.67.1 here, exit and resume this conversation (session `<id>`)." The hook then writes the session's mark, `~/.local/state/crew/offers/<session id>`, holding the real path it offered for. A later turn reads the mark first, and while the install has not moved it starts no process and shows nothing. An install that moves the path while the session still runs an older build is offered again.

A standing agent is handled as now: handed its restart when due (`teams.19`), never offered. The reviewer, started fresh for each batch, is left alone as now.

Considered and not taken:

- **crew restarting these sessions itself, as it restarts a standing agent.** crew did not start them (`read.4`). It does not know their launch: the account's settings, the MCP configuration, the other tools' plugin folders, the folders added. A resume crew made would lose them, and the person may be mid-thought. The person's own resume brings them back whole.
- **The offer in crew's band, above the prompt.** The mod draws a view only for a crew agent, from the follower's frames. The end of a turn is the pause the brief names, and the Stop hook is the part of crew that runs there for every session.
- **Offering a session loaded from a checkout.** On a host in the live mode, a session's hooks run from the checkout as it stands at every call, so what is old is only what it loaded once: the mod and the hooks list. Telling what it loaded would need a record of every session's start on the host. A standing agent is already restarted for it (`teams.19`).

### Decision 7: the host keeps each installed build's answer

A path in the Nix store names one build forever, so its answer to `crew _release` never changes. `crew.installed` keeps a read, complete answer from a command whose real path is in the store at `~/.cache/crew/installed/<first 32 hex of the path's SHA-256>.json`. It writes the file whole and renames it into place. Before asking, it reads the kept file through `release_said`, as it reads an answer (`read.2`), and asks again where that read fails.

These are never kept:

- an unread answer: late, failed or missing a field;
- the answer of a command outside the store, such as a checkout, a profile's own script or a host's link, whose answer can change under the same path.

This is a derived cache under `state.4`: a read of an immutable thing, keyed by it, thrown away with no loss. It lets each turn's end of every session on a build start no process. Without it, a session on an older build would ask the installed crew once for each turn until it is offered. A session on the installed build reads its own release and the kept answer, and asks nothing.

### Decision 8: what already runs is moved by hand

Every process and session started before a host installs this change runs code that cannot move it (principle 12). No guard, fallback or keeper is written for them. The design's *After deploy* names the hand step.

## Risks

- A tab or the flow reader whose host installs a build may wait up to five seconds once, while the first process on the host asks the new build `crew _release`.
- A session's turn on a host whose installed command does not answer asks again at each turn's end, up to five seconds within the hook's ten, as a standing agent's turn already does (`crew.due_of`). An unread answer is not kept, so that it is read once it answers.
- A message from the Stop hook may show in a Flume place's session where no person reads it. It is shown once for each install and costs nothing else.

## After deploy

One step, for every host whose crew was installed before this change, deneb among them, once that host's installed crew carries this change:

- **The host's main-level ops** ends each console tab process and each `crew events --follow` that runs an older build than the installed crew, read with `ps` and named by its store path. The next `crew console up`, which the host's timer runs, starts each tab again on the installed crew. ops tells the user which of their sessions still run an older build.
- **The user** restarts each of their sessions that still runs an older build, by exiting and resuming it.

No check can do this, since the processes run the code of a crew older than any check. Principle 12 keeps it out of code.

## Task notes

**1.1** `plugin/lib/crew.py`:

- `behind(mine, theirs)` moves here from `board.py`, unchanged. `board.behind_here` calls `crew.behind`.
- New `move_due(lag, moved_to, installed)` returns None, `"stuck"` or `"move"` as in Decision 4.
- New `MOVED_TO = "CREW_MOVED_TO"`.

Cases in `tests/py/test_board.py`, class `TestInstalledCrew`: the existing `behind` table, `test_a_follower_lags_only_when_both_crews_name_a_commit_and_they_differ`, now calls `crew.behind`. New class `TestMoves`, its first case `test_a_process_moves_once_for_each_install`, a table of `move_due`:

- a lag of None or False, with or without a mark, gives None;
- a lag with no mark gives `"move"`;
- a lag marked for the installed commit gives `"stuck"`;
- a lag marked for another commit gives `"move"`.

**1.2** `plugin/lib/crew.py` `installed`: for a real path starting with `STORE`, read `~/.cache/crew/installed/<digest>.json` through `release_said` before `ask_release`. Write a read answer there (temporary file in the same folder, then `os.replace`). Never write an unread one, or one for a path outside `STORE`. The folder is `KEPT = pathlib.Path.home() / ".cache/crew/installed"`, a module name the tests can set. `ASKED` still holds what this process read.

Cases in `tests/py/test_release.py`, class `TestInstalled`, with `KEPT` set to a scratch folder for every case of the class:

- `test_a_store_builds_answer_is_kept_on_the_host_and_read_before_asking`: the second process, `ASKED` emptied, reads the kept answer and `ask_release` is not called;
- `test_an_unread_answer_and_one_from_outside_the_store_are_never_kept`: an unread answer is not kept and is asked again, and a command whose real path is outside the store is asked each process and never kept;
- `test_a_kept_answer_crew_cannot_read_is_asked_again`: a kept file that is not JSON is asked again and replaced.

**1.3** `plugin/lib/crew.py`:

- New `started_commit()`: on a checkout `head_here()`, else `crew_read()["commit"]`. A lasting process reads it once, at its start.
- New `installed_commit()`: where the installed command is this crew's own checkout, `head_here()`; else `installed()["commit"]`; None where the host has none.
- New `move_here(argv, moved_to, env=None)`: `os.execvpe("bash", ["bash", installed_here() or crew_command(), *argv], os.environ | {MOVED_TO: moved_to} | (env or {}))`. On `OSError` it prints once on standard error, "crew could not start <argv> again as the installed crew (<why>); it runs on as it is", and returns.
- New `lasting_look(started)`: returns `(what, installed)`, what the process does this second, `"move"`, `"stuck"` or None, and the installed commit it read. `installed` is `installed_commit()`, read once per call, and `what` is `move_due(behind({"commit": started}, {"commit": installed}), os.environ.get(MOVED_TO), installed)`.

Cases in `tests/py/test_board.py`, class `TestMoves`, with `os.execvpe` monkeypatched as `TestInstalledCrew` does:

- `test_a_move_runs_the_installed_command_in_its_own_process`: `move_here` runs the installed command with the given words and `CREW_MOVED_TO`;
- `test_a_move_that_cannot_start_says_so_and_runs_on`: a failing exec says so and returns;
- `test_on_a_checkout_the_installed_commit_is_read_with_no_process`: on a checkout, `installed_commit` and `started_commit` read HEAD from files, with `subprocess` made to raise.

**2.1** `plugin/lib/board.py` `follow` (the board tab): read `started = crew.started_commit()` once before the loop. After each draw, `what, installed = crew.lasting_look(started)`: on `"move"` call `crew.move_here(sys.argv[1:], installed)`; on `"stuck"` print once that the tab runs on as it is. Leave `--once` alone: it draws once and moves nothing.

Case in `tests/py/test_board.py`, `TestMoves::test_a_board_tab_moves_after_its_first_draw`: a board tab whose started commit differs from the installed one starts again as `["bash", <installed>, "_board", "wldn"]` after its first draw, and one stuck for the installed commit says so once and draws on. Use `time.sleep` patched to raise after the first second, as `TestEvents` does for the flow.

**2.2** `plugin/lib/board.py`:

- `rail_follow`: while `follower is None`, the same look as **2.1** after each draw. A rail tab holding the lock leaves the move to its `Follower`.
- `Follower.__init__`: drop `started_lagging` and `CREW_FOLLOWER_LAGGED`. Keep `said_lag`.
- `Follower.lagging`: `move_due(behind_here(), os.environ.get(crew.MOVED_TO), crew.installed()["commit"])`. True on `"move"`; on `"stuck"`, say once as now and answer False.
- `Follower.again`: set `CREW_MOVED_TO` to the installed commit it read (`crew.installed_commit()`, empty where unread), for an update as for a lag. Drop the `lag` parameter's mark.

Cases in `tests/py/test_board.py`:

- `TestInstalledCrew::test_a_follower_started_again_for_its_lag_says_so_as_it_starts` becomes `test_a_follower_started_again_carries_the_installed_commit`;
- `TestRefresh`'s started-for-lag cases read `CREW_MOVED_TO`, and a follower stuck for one install moves once the installed commit changes;
- new `TestMoves::test_a_rail_tab_without_the_lock_moves_and_one_holding_it_leaves_it_to_its_follower`.

**3.1** `plugin/lib/record.py`:

- New `handed(text)`: `CREW_FOLLOWED`'s JSON read field by field, `{"day": "YYYY-MM-DD", "tips": {label: 40-hex}}`, else None.
- `follow`: read `started = crew.started_commit()` and `handed(os.environ.pop("CREW_FOLLOWED", None))` before the loop. The day is the handed day where given. For each label with a handed tip, the first read lists `plan.blobs_at(repo, handed_tip, "runs/")`, takes its entries as seen and prints nothing, then sets `tips[l]` to the handed tip, so the loop's next read at the branch's tip prints what came after. A handed tip that raises `Refusal` is said once ("<label>/main: crew can't read where the follow was before it moved (<why>); it follows from the branch as it stands") and the label starts afresh.
- At the end of each round, after printing, the look of **2.1**: on `"move"`, `crew.move_here(sys.argv[1:], installed, {"CREW_FOLLOWED": json.dumps({"day": day, "tips": tips})})`.

Cases in `tests/py/test_record.py`, class `TestEvents`, with `plan` patched as `test_a_follows_start_fetches_nothing_the_hosts_follower_fetches` does:

- `handed` reads a good value and gives None for each bad shape;
- a follow handed wldn's tip T prints, at the branch's tip U, the entries U holds that T does not, and nothing T holds;
- a follow handed an unreadable tip says so once and prints nothing at its first read;
- a follow that moves hands on its day and the tips it printed to, in `move_here`'s env.

**4.1** `plugin/lib/crew.py`:

- New `offer_due(loaded, installed, offered_for, real)` as in Decision 6.
- New `offer_said(mine, theirs, session)`: one sentence pair in plain words. It names the version the session runs (`loaded["version"]`), the version installed, and the session's id, and says that exiting and resuming the conversation runs the installed crew there. Where a version is None it names the commit's first seven characters.
- New `OFFERS = pathlib.Path.home() / ".local/state/crew/offers"`.

Cases in `tests/py/test_hold.py`, new class `TestOffer`, `test_an_offer_is_due_once_for_each_install`, a table of `offer_due`:

- a build behind with no mark gives True;
- the same with a mark for this real path gives False;
- a mark for another real path gives True;
- a checkout loaded gives False;
- an unread loaded or installed crew gives False;
- the same commit gives False.

Plus `test_the_offer_names_both_versions_and_the_session`, `offer_said`'s words for a release and for an untagged build.

**4.2** `plugin/hooks/stop`. After the hook reads its input and before it looks up the session's record: a session whose record names a crew agent goes on as now. For any other session:

1. Read `loaded = crew.crew_read()`. Return unless it is from a release.
2. Read `cmd = crew.installed_here()`. Return when it is None.
3. Read `real = os.path.realpath(cmd)` and the mark `OFFERS/<sid>`. Return when the mark holds `real`.
4. Read `installed = crew.installed()`. When `offer_due`, write the mark (whole, renamed into place) and print `json.dumps({"systemMessage": offer_said(...)})`.

The hook's docstring says so, and still never fails a turn. `hooks.json`'s description names the offer.

Case in `tests/t-hold.sh`. Build a folder with no git holding a copy of `plugin/` whose `plugin/release.json` names commit `1111…` and version `0.59.0`. Put a profile folder on the path whose `crew` answers `crew _release` for commit `2222…` and version `0.67.1`. Then:

- its `hooks/stop`, given a session id with no record, prints a `systemMessage` naming `v0.59.0`, `v0.67.1` and the id;
- a second run prints nothing;
- the case's `# Reads:` line, and `tests/moon.yml` through `tests/moon-tasks`, follow what the test reads.

**5.1** `README.md`:

- the console's paragraph says each tab moves to the installed crew by itself, the flow tab printing every entry once;
- the update paragraph, where crew's Stop hook is named, says a session crew did not start that runs an older build is offered its restart once for each install, and that the host keeps each installed build's answer.

`plugin/skills/crew/SKILL.md`: the console's row and "A brief, the teams file or the installed crew changed" say the same in a line each. `plugin/bin/crew`'s usage header for `crew events --follow` says it moves to the installed crew.
