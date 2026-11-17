# A bolt waiting on the user waits under words

## Why

A started bolt whose every unit has merged waits on the user in three ways: for their send of its row on its kit's landings card (a bolt marked to stay, one they left, one whose land was stopped), for their lift of a hold on its kit or drive, or for their answer to a review batch that holds a unit's latest change. Meanwhile its base place has no place on its branch live and its submission unasked, so it waits on its caller for a retry of the submission, under no hold's words. Flume reads such a place stalled after five minutes and delivers the stall to its recipient, main-level ops, and to the answerer behind its stream, so it reaches ops, the operator and the user as though something had failed (Flume's clause 130 and rule core.24). That is signal `2026-11-14-boomdrive-ops-f85c2fe2/01` on afterthought/crew-state's `boomdrive/main`: the weir bolt, proven and waiting on the user's send, "stalled: a retry of the submission".

Record 0067's amendment of 2026-11-14 (boomdrive-design) decides it: while a proven bolt waits on the user, its base place waits under words naming what it waits on and where the user answers it, carried to Flume as a hold of the base place's waiting move. crew posts `hold`, naming the bolt's launch and the words, and names neither Flume nor its command (record 0056 point 1). The words last as long as the wait, a `land` ends it, and a wait that changes gives the words of what the bolt waits on next, or ends them. A stall still says something: a bolt that waits on nothing of the user's still stalls.

Boomdrive's runner takes `hold` from its control plane, naming a launch, its words and a bound in whole seconds, and carries it as `flume hold <place> --waiting --for=<n>s -- <words>` (boomdrivedev/boomdrive `the-runner-carries-a-hold-of-a-places-waiting-move`, its core.59 and record 0002's amendment of 2026-11-14). Its design names this unit's side: `Act: hold` with `Of`, `Words` and `Bound`, naming no `Host`, `hold` in the `Act` enum, `%type: Bound int`, and `Bound` after `Delivery` in `%allowed` and `FIELDS`.

## What Changes

- **A hold is a request.** `requests.rec` takes `Act: hold`, naming the launch of a bolt's base place (`Of`), the words (`Words`) and a bound in whole seconds (`Bound`), and no host. crew's rules refuse a hold of any other launch, with no words, or with a bound that is no whole number of seconds.
- **crew decides what a waiting bolt waits on, and says it in words.** From the rail's land row: a bolt that can land and lands on the user's send waits on their send of its row on `land/<kit>`, saying why (marked to stay, left, its land stopped); one that can land under a hold waits on the user's lift of it, with the hold's own words; one kept from landing by batches the user has not answered, and by nothing else, waits on their answer to those batches, and on the hold too where one stands. Anything else waits on nothing of the user's.
- **The rail's read holds each such base place under those words.** On the main level's host, after the landings cards it raised, each rail read posts a `hold` of each bolt's base place whose words are due, by one plan write in main-level ops's name, with a bound of seven days: when its base place waits on crew under no standing hold with those words, or under one with less than half its bound left. Nothing is posted while a hold of the launch waits on the runner's answer, while a land of it stands, or while its base place waits on nothing of crew's.
- **A wait that changes changes its words, and one that ends ends crew's hold.** A land, on the send or on proof, ends the wait, as Flume ends the hold at the retry of the submission. A bolt whose base place still waits on crew under the words crew last posted, while it waits on nothing of the user's, gets a hold of bound 0 that Flume lets lapse at once, so its stall says something again. A hold on the waiting move that is not crew's is left.
- **crew reads the hold from Flume's status as the runner carries it.** Flume's status of a place gives the hold on its waiting move with its words, since, bound and when it lapsed; crew reads the standing one, guarded (`read.2`).
- **The run record names each hold**, as `bolt.hold` on `bolt/<bolt>` with its `Request`, the bolt's `Head` and its `Form`, what it waits on (`send`, `batch`, `hold`) or `end`, and none of its words (`record.3`).
- **The rail says what it asked**, ops's brief says why a bolt waiting on the user no longer stalls, and README, the crew skill and `crew`'s usage say the rail's read holds it (`docs.2`).

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `bolt-teams`: a started bolt waiting on the user is held under words naming what it waits on, by the rail's read, the words renewed as the bound nears, changed as the wait changes and ended when it ends.
- `drive-state`: a hold is a request of the drive's requests file, naming a bolt's launch, its words and its bound.
- `run-record`: a hold crew posts is one `bolt.hold` entry naming its request and what the bolt waits on.

## Impact

- `plugin/lib/runner.py`: `REQUESTS` (the `%doc`, `hold` in the `Act` enum, `%type: Bound int`, `Bound` in `%allowed`), `FIELDS`, `ACTS`, `request_refusal`; `flume_facts` reads the hold on the waiting move; new `holds_of`, `hold_due`, `HOLD_BOUND` and `HOLD_ENDED`.
- `plugin/lib/plan.py`: `rail_rows` gives each land row's bolt its `wait`; new `user_wait`, `wait_words`, `holds_change`, `holds_post` and `sweep_waits`; `rail_read` runs `sweep_waits` after `sweep_moved`; the rail's text; `CardActs.post_holds`.
- `plugin/lib/record.py`: the descriptor's notes on `Form` and `Request` name `bolt.hold`.
- `plugin/roles/main-ops.md`, `README.md`, `plugin/skills/crew/SKILL.md`, `plugin/bin/crew`'s usage header.
- Tests: a new `tests/py/test_waiting_holds.py`; `tests/py/test_runner.py`, `tests/py/test_rail.py`, `tests/py/test_asks.py`, `tests/contract/test_recfix.py`; new fixtures under `tests/py/flume-0.26.0/`.
- No rule or record changes: record 0067's amendment and `plan.16` already carry the decision, and `docs/architecture/` is the design agent's alone (`docs.7`).
- Outside this repository: Boomdrive's runner carries the hold. Its change `the-runner-carries-a-hold-of-a-places-waiting-move` landed on boomdrivedev/boomdrive's bolt `the-runner-needs-no-hand-on-a-host` (afba153a) and not yet on its main or in a release, read 2026-11-16; until a runner carries it, each hold crew posts waits unanswered and nothing more is posted for its bolt (design, Migration Plan).
