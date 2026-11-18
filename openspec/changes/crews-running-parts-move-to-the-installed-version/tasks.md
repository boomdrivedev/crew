# Tasks

Before the first task, sync the tests' venv once: `devenv shell -- moon run tests:venv`. A check below that names tests is one pytest run, `devenv shell -- tests/.venv/bin/python -m pytest -q -p no:cacheprovider <tests>`, and passes when pytest reports every test it names passed. Build the tasks in order. The verify stage runs crew's whole checks once, after the last task. Submit nothing, and never run `wt submit --help`.

## 1. One decision and one act for every lasting process

- [x] 1.1 `crew.behind` decides, for every lasting process, whether it runs another crew than the installed one, and `crew.move_due` decides whether it moves, says once that it is stuck, or runs on, from the lag, the installed commit it moved for and the installed commit now (design Decisions 2 and 4; Task notes 1.1). Passes `devenv shell -- tests/.venv/bin/python -m pytest -q -p no:cacheprovider "tests/py/test_board.py::TestMoves::test_a_process_moves_once_for_each_install" "tests/py/test_board.py::TestInstalledCrew::test_a_follower_lags_only_when_both_crews_name_a_commit_and_they_differ"`.
- [x] 1.2 `crew.installed` keeps on the host the read answer of an installed command whose real path is in the Nix store, reads it there before asking, and never keeps an unread answer or one from outside the store (design Decision 7; Task notes 1.2). Passes `devenv shell -- tests/.venv/bin/python -m pytest -q -p no:cacheprovider "tests/py/test_release.py::TestInstalled"`.
- [ ] 1.3 `crew.started_commit`, `crew.installed_commit`, `crew.lasting_look` and `crew.move_here` read the two commits with no process while the install has not moved, and start a process again through the installed command in its own process, carrying `CREW_MOVED_TO`, saying so and running on when the exec fails (design Decisions 2 and 3; Task notes 1.3). Passes `devenv shell -- tests/.venv/bin/python -m pytest -q -p no:cacheprovider "tests/py/test_board.py::TestMoves::test_a_move_runs_the_installed_command_in_its_own_process" "tests/py/test_board.py::TestMoves::test_a_move_that_cannot_start_says_so_and_runs_on" "tests/py/test_board.py::TestMoves::test_on_a_checkout_the_installed_commit_is_read_with_no_process"`.

## 2. The tabs and the follower move

- [ ] 2.1 The board tab starts again through the installed command as `crew _board <label>` once the installed crew names another commit than the one it started on, and says once and runs on when stuck (design Decision 1; Task notes 2.1). Passes `devenv shell -- tests/.venv/bin/python -m pytest -q -p no:cacheprovider "tests/py/test_board.py::TestMoves::test_a_board_tab_moves_after_its_first_draw"`.
- [ ] 2.2 A rail tab without the follower lock moves as the board tab does, and the follower's `lagging` and `again` read and carry `CREW_MOVED_TO` in place of `CREW_FOLLOWER_LAGGED`, so a follower stuck for one install moves at the next (design Decisions 3 and 4; Task notes 2.2). Passes `devenv shell -- tests/.venv/bin/python -m pytest -q -p no:cacheprovider "tests/py/test_board.py::TestMoves::test_a_rail_tab_without_the_lock_moves_and_one_holding_it_leaves_it_to_its_follower" "tests/py/test_board.py::TestInstalledCrew::test_a_follower_started_again_carries_the_installed_commit" "tests/py/test_board.py::TestRefresh"`.

## 3. The flow reader moves and prints each entry once

- [ ] 3.1 `crew events --follow` moves to the installed crew after printing what it read, handing on its day and its tips in `CREW_FOLLOWED`, and a follow handed them prints each entry after them once, saying so once where a handed tip can't be read (design Decision 5; Task notes 3.1). Passes `devenv shell -- tests/.venv/bin/python -m pytest -q -p no:cacheprovider "tests/py/test_record.py::TestEvents"`.

## 4. A session on an older build is offered its restart

- [ ] 4.1 `crew.offer_due` offers a session its restart only where it loaded a build whose release names another commit than the installed crew's and has not been offered for the installed command's real path, and `crew.offer_said` words the offer in plain English, naming both versions and the session's id (design Decision 6; Task notes 4.1). Passes `devenv shell -- tests/.venv/bin/python -m pytest -q -p no:cacheprovider "tests/py/test_hold.py::TestOffer"`.
- [ ] 4.2 crew's Stop hook shows a session that is no crew agent and runs an older build its offer once, as a `systemMessage`, marks the session for that install, and still hands a due standing agent its restart (design Decision 6; Task notes 4.2). Verify `tests/suite t-hold` ends with "0 failed".

## 5. The how-to says so

- [ ] 5.1 README, the crew skill and `plugin/bin/crew`'s usage header say that each tab and the flow reader move to the installed crew by themselves, and that a session crew did not start on an older build is offered its restart once for each install (`docs.2`; Task notes 5.1). Verify `tests/suite t-docs` ends with "0 failed".
