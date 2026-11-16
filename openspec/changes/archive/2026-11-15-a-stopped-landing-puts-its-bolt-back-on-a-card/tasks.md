# Tasks

Before the first task, sync the tests' venv once: `devenv shell -- moon run tests:venv`. A logic-tier check below is one pytest run, `devenv shell -- tests/.venv/bin/python -m pytest -q -p no:cacheprovider <test>`, and passes when pytest reports every test it names passed. Submit nothing, and never run `wt submit --help`.

## 1. A stop closes the answered card with no read of ops's

- [x] 1.1 The read that records a bolt's landing refused or stopped raises its kit's landings card once, a read inside a raise raising none (design Decision 1; Task notes 1.1). Passes `devenv shell -- tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_landing.py::TestTheFirstReadActs tests/py/test_landing.py::TestALandingReadOnMainCloses "tests/py/test_landings.py::test_a_landing_is_read_and_recorded_by_a_host_away_from_the_kits_with_every_ssh_refused"`.
- [x] 1.2 An answered landings card's send waits on no bolt whose land on that send was stopped, so the sweep closes the card its row is gone for (design Decision 2; Task notes 1.2). Passes `devenv shell -- tests/.venv/bin/python -m pytest -q -p no:cacheprovider "tests/py/test_rail.py::TestSweepJudged::test_an_answered_landings_card_whose_ticked_bolts_land_on_that_send_was_stopped_waits_on_it_no_more"`.
- [x] 1.3 An answered landings card's line names only the bolts its send still waits on, or that crew's next raise closes it (design Decision 2; Task notes 1.3). Passes `devenv shell -- tests/.venv/bin/python -m pytest -q -p no:cacheprovider "tests/py/test_rail.py::TestText::test_a_landings_card_the_user_sent_names_only_the_bolts_it_still_waits_on"`.
- [x] 1.4 A bolt whose land on the send was stopped follows, the card after the answered one carrying it, and no send holds it (design Decision 2; Task notes 1.4). Passes `devenv shell -- tests/.venv/bin/python -m pytest -q -p no:cacheprovider "tests/py/test_rail.py::TestRows::test_a_bolt_whose_land_on_the_send_was_stopped_follows_and_is_held_by_no_send" "tests/py/test_rail.py::TestRows::test_the_record_reading_keeps_each_landings_cards_rows_answer_and_the_sends_kept"`.
- [x] 1.5 The rail's read raises an answered landings card whose send a stop spent for a ticked bolt (design Decision 2; Task notes 1.5). Passes `devenv shell -- tests/.venv/bin/python -m pytest -q -p no:cacheprovider "tests/py/test_landings.py::test_a_ticked_row_whose_land_on_the_send_was_stopped_is_unoffered"`.
- [x] 1.6 The raise closes an answered card at a stop of the land its send posted, at the bolt's head or after it moved, and the card that follows asks for the bolt again (design Decision 3; Task notes 1.6). Passes `devenv shell -- tests/.venv/bin/python -m pytest -q -p no:cacheprovider "tests/py/test_landings.py::test_a_stop_on_the_send_closes_the_card_and_asks_again_though_the_head_moved_since" "tests/py/test_landings.py::test_two_of_three_ticked_landed_and_the_third_stopped_closes_the_card_asking_for_the_third_again"`.

## 2. The whole

- [x] 2.1 The tests the change affects pass. Verify `tests/suite --affected` ends with "0 failed".
