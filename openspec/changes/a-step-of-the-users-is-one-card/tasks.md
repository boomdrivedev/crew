# Tasks

Work the tasks in order, from the place's root. Before the first logic check, sync the tests' venv once: `devenv shell -- moon run tests:venv`. A logic check below is one pytest run, `devenv shell -- tests/.venv/bin/python -m pytest -q -p no:cacheprovider <test>`, and passes when pytest reports every test it names passed. An end-to-end check passes when `tests/suite` ends with "0 failed". Submit nothing, and never run `wt submit --help`.

## 1. The specs reconcile

- [x] 1.1 The change `an-offer-card-shows-the-step-the-deploy-waits-on-first` is removed, its standing requirements carried by this change's `main-level` delta (design, Decision 10; Task notes 1.1). Passes `test ! -e openspec/changes/an-offer-card-shows-the-step-the-deploy-waits-on-first && devenv shell -- openspec validate a-step-of-the-users-is-one-card --strict`, valid with no line saying archive would refuse it.

## 2. One step, one card, however many hosts

- [x] 2.1 The user's steps waiting under one key on several environments are one group in first-recorded order, and a held agent's step and a gate's step are each their own (design, Decision 1; Task notes 2.1). Passes `devenv shell -- tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_ops.py::TestOneStepManyHosts`.
- [x] 2.2 A group has one rail row, keyed by the open card that names its steps or by its first-recorded step's `op/<env>/<n>`, answered by `crew ops settle` (design, Decision 2; Task notes 2.2). Passes `devenv shell -- tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_ops.py::TestOneStepManyHosts tests/py/test_ops.py::TestRows`.
- [x] 2.3 A user's step's card is titled with a plain sentence of the step's words and the hosts it releases, its summary the step's why and the hosts, with no record or rule id of crew's, and its built card carries the group's `heads` (design, Decision 4; Task notes 2.3). Passes `devenv shell -- tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_ops.py::TestStepCard`.
- [x] 2.4 Each post and change of a step's card records `Heads`, the steps it names (design, Decision 3; Task notes 2.4). Passes `devenv shell -- tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_card_commands.py::TestAStepCardsHeads`.
- [x] 2.5 One step card is open at a time on each environment, a shared card counted on each. The next due is the earliest group whose hosts are all free, and a host's step recorded after the answer follows the answered card (design, Decision 5; Task notes 2.5). Passes `devenv shell -- tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_ops.py::TestOneStepCardAtATime`.

## 3. One answer settles it

- [x] 3.1 `crew ops settle <key> --state done|declined` records the state on every step the card named, each under its own environment, deploy and key with its `When` kept. It closes the card once and raises each host's next step card and each deploy the step released. It is refused for a key no row or card holds, and answers `-h` (design, Decision 6; Task notes 3.1). Passes `devenv shell -- tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_ops.py::TestSettle tests/py/test_help.py::TestAsked::test_the_other_modules_parsers`.
- [ ] 3.2 An open, unanswered step card is changed in place as a host's step joins or leaves its group, and closed when it names none (design, Decision 7; Task notes 3.2). Passes `devenv shell -- tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_ops.py::TestStepRecordedAgain`.
- [ ] 3.3 The rail's read changes a step card whose `Heads` differ from its row's, and closes a folded card saying which card asks it now (design, Decision 7; Task notes 3.3). Passes `devenv shell -- tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_rail.py::TestStepCardsFold`.

## 4. A deploy card holds no boxes

- [ ] 4.1 A deploy waiting on an open step of the user's has no card. Its row names the step's card and the sweep owes it none. An unanswered card, or one from before posted as boxes, is withdrawn, and the card is raised as the hold-to-approve following the step's card once each step is done (design, Decision 8; Task notes 4.1). Passes `devenv shell -- tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_ops.py::TestTheStepsADeployWaitsOn tests/py/test_ops.py::TestAStepRecordedThatTheOfferWaitsOn`.
- [ ] 4.2 A deploy's card is the hold-to-approve alone, listing the steps it waited on first, each done, and builds no boxes (design, Decision 8; Task notes 4.2). Passes `devenv shell -- tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_ops.py::TestTheDeployCardOfAStepItWaitsOn tests/py/test_ops.py::TestDeployCard`.
- [ ] 4.3 `crew ops approve` takes no `--ticked`, records no step done, and is refused while a step the deploy waits on is open, naming each step and its card or that it is not recorded yet, the refusal recorded (design, Decision 8; Task notes 4.3). Passes `devenv shell -- tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_ops.py::TestRefusals`.

## 5. The views

- [ ] 5.1 Every host's entry for a shared step names its one row, and each deploy waiting on a step names its card. Ops's band says so and counts a shared step once (design, Decision 9; Task notes 5.1). Passes `devenv shell -- tests/.venv/bin/python -m pytest -q -p no:cacheprovider tests/py/test_board.py::TestViews`.

## 6. Through the command, the brief and the docs

- [ ] 6.1 Through `crew ops` on the stubs, an offer waiting on a `before` step posts no deploy card, and two hosts' records of the step post one card. `approve` is refused naming that card, and `settle` records the step done on both, closes the card and posts the deploy's approve (Task notes 6.1). Verify `tests/suite t-journey-ops` ends with "0 failed".
- [ ] 6.2 Main-level ops's brief says a deploy waiting on the user's step has no card until it is done, and that the user's answer on a step's card is `crew ops settle`. README, the skill and the usage give `settle` and drop `--ticked` (design, Decisions 6 and 8; Task notes 6.2). Verify `tests/suite t-briefs t-docs t-help` ends with "0 failed".
