# Verify: a-bolt-waiting-on-the-user-waits-under-words

Read 2026-11-16 on `change/a-bolt-waiting-on-the-user-waits-under-words` at cf598054, cut from `bolt/a-waiting-bolt-never-reads-stalled`.

## Outcome

**Not archived.** The checks fail on one case in the logic tier. Everything else holds: every task is ticked, `openspec validate --strict` passes, and the code meets every requirement and scenario of the three delta specs. The change goes back to its code stage for the one fix below.

## The checks

`tests/suite --affected` is the repository's check for a finished change, as CLAUDE.md names it. It ran once, against the merge-base with `main`, uncommitted edits included:

```
FAIL  logic
31 passed (2 replayed), 1 failed
```

The logic tier: `1 failed, 3790 passed in 119.01s`. The failing case:

```
FAILED tests/py/test_runner.py::TestRequests::test_a_request_carries_nothing_its_act_does_not_take

>       assert runner.request_refusal([], rec(1, "reorder")) == (
            "request 1 is a reorder, and a request is a launch, a retry, a drop, a priority, a land, a preview or a confirm")
E         -  a preview or a confirm
E         +  a preview, a confirm or a hold
tests/py/test_runner.py:96: AssertionError
```

Task 1.1 (design, Task notes 1.1) asked for `request_refusal`'s unknown-act message to list a hold, and the code does. The existing case at `tests/py/test_runner.py:96` still expects the old message. The code is right; the case needs the new wording: `... a land, a preview, a confirm or a hold`. Task 1.1 names only `TestHoldRequest` as its check, so this case was never run against the change.

The other 31 tasks passed. Among them are `contract`, `mod`, `t-briefs`, `t-docs`, `t-help` and `t-specs`.

`openspec validate a-bolt-waiting-on-the-user-waits-under-words --strict`: valid.

## Tasks

All 13 tasks are ticked (`- [x]`), and none is open. Each task's named check passes within the logic and contract runs above, except for the one case above, which no task names.

## Specs against the work

### bolt-teams

- **A started bolt waiting on the user is held under words naming what for**: met.
  - `plan.user_wait` and `plan.wait_words` (`plugin/lib/plan.py`) give the scenarios' words exactly. These are Marked to stay, Left by the user, Its land stopped, Under a hold on its kit, Marked to stay under a hold, and Waiting on a batch. `TestWaitWords` asserts them as the spec writes them.
  - A change in no batch yet: `rail_rows` gives no batches while a unit's change is outside a batch, so the wait is `none` (`test_each_land_row_bolt_carries_what_it_waits_on`).
  - Waiting on nothing of the user's: a verification that is not green gives `none`.
  - A held base place asks no role: `asks.waits_on` returns nothing for `bolt-held` and one wait for `bolt-held-lapsed` (`tests/py/test_asks.py`).
  - The bound is `runner.HOLD_BOUND`, 604800.
- **A waiting bolt's hold is posted once for its words, and again as its bound nears**: met. `runner.hold_due` covers each scenario, and `TestHoldDue` proves them:
  - Read again;
  - Past half its bound, at four days and at exactly half;
  - Lapsed;
  - Waiting on the runner's answer;
  - A land standing, asked or submitted, while a refused land waits on the send again;
  - A base place that waits on nothing of crew's;
  - The wait changes.
- **A wait that ends ends crew's hold**: met.
  - An end is a hold of bound 0 with `HOLD_ENDED`. It is posted only where the standing words are those of crew's newest hold with a bound above 0, and nothing follows it (`test_after_an_end_nothing_more_is_due`).
  - What crew can't read: the `unknown` wait posts nothing (`TestSweepWaits`).
  - Landed on proof: the raise's land is at the write's tip, so no hold of the bolt is posted.
  - A hold not crew's is left.
- **The rail's read posts the holds due by one plan write in ops's name**: met.
  - `sweep_waits` runs in `rail_read` after `sweep_moved`, and only on the drive's main machine.
  - `holds_post` and `holds_change` make one write as `<label>-ops`. At the tip they re-check the bolt, its `Stays` mark, `hold_on`, and any land or hold appended since the read.
  - The rail's text names each hold asked and each write refused.
  - The scenarios A land posted in the same read, A hold put between the read and the write, Two bolts at once, and Another host's read are proved in `TestHoldsWrite`, `TestSweepWaits` and `TestText`.

### drive-state

- **Every request for a host's runner is a record of the drive's requests file** (modified): met.
  - `REQUESTS` takes `hold` in the `Act` enum, `%type: Bound int`, and `Bound` after `Delivery` in `%allowed` and `FIELDS`.
  - A hold passes `recfix --check`, both new and brought in step from the older descriptor, and a `Bound` of `8h` is refused (`tests/contract/test_recfix.py`).
- **A hold names a bolt's launch, its words and a bound**: met. `ACTS["hold"]` needs `Of`, `Words` and `Bound` and takes nothing else. `request_refusal` refuses each of these, as `TestHoldRequest` proves:
  - a hold of a unit's launch, naming it;
  - a hold with no words;
  - a bound that is no whole number of seconds;
  - a hold naming a `Host`.

### run-record

- **A hold crew posts is one entry naming its request and what the bolt waits on**: met.
  - Each hold is a `bolt.hold` on `bolt/<bolt>` with `Request`, `Head` and `Form` (`send`, `hold`, `batch` or `end`) and none of its words.
  - The first entry is the write's own act and the rest go in `Write.also`.
  - `record.py`'s descriptor notes name `bolt.hold` (`test_two_holds_are_one_write_in_ops_name_each_with_its_entry`, `test_an_end_is_a_hold_of_bound_zero_recorded_as_an_end`).

### Docs and brief

- `plugin/roles/main-ops.md` says what Decision 7 asks: the words, that ops runs nothing for such a bolt, and that a stall still reaches ops for a bolt that waits on nothing of the user's.
- README, `plugin/skills/crew/SKILL.md` and `plugin/bin/crew`'s usage say the rail's read holds a waiting bolt under words, and that a hold is a request of `requests.rec` (`docs.2`).
- `docs/architecture/` and `docs/adr/` are untouched (`docs.7`).

## What the code stage owes

At `tests/py/test_runner.py:96`, `TestRequests::test_a_request_carries_nothing_its_act_does_not_take` should expect `"request 1 is a reorder, and a request is a launch, a retry, a drop, a priority, a land, a preview, a confirm or a hold"`. Then the logic tier, and `tests/suite --affected`, should end with "0 failed".
