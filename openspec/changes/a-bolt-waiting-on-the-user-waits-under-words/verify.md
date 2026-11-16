# Verify: a-bolt-waiting-on-the-user-waits-under-words

Read 2026-11-16 on `change/a-bolt-waiting-on-the-user-waits-under-words` at 2396aa4f, cut from `bolt/a-waiting-bolt-never-reads-stalled`.

## Outcome

**Archived.** The checks pass, every task is ticked, `openspec validate --strict` passes, and the code meets every requirement and scenario of the three delta specs.

## The checks

CLAUDE.md names `tests/suite --affected` as the repository's check for a finished change. It ran once, against the merge-base with `main` (b097ed4b), with uncommitted edits counted (there were none):

```
32 passed (31 replayed), 0 failed
```

- The logic tier ran fresh: `3791 passed in 31.63s`. This includes `TestRequests::test_a_request_carries_nothing_its_act_does_not_take`, which now expects the refusal to end "a preview, a confirm or a hold" (task 1.6).
- Every other task was replayed from a run that passed on this host with identical inputs: `contract`, `mod`, `t-briefs`, `t-docs`, `t-help`, `t-specs` and the end-to-end journeys among them. `tests/suite` replays only on identical inputs, so a replay is a pass of these inputs.

`openspec validate a-bolt-waiting-on-the-user-waits-under-words --strict`: valid. Each requirement's text above its first scenario is at most 448 characters. That includes the modified drive-state requirement, which `t-specs` counts once the change is archived.

## Tasks

All 13 tasks are ticked (`- [x]`), and none is open. Each task's named check is in the logic, contract or end-to-end runs above, and all of them passed.

## Specs against the work

### bolt-teams

- **A started bolt waiting on the user is held under words naming what for**: met.
  - `plan.lands_by`, `plan.user_wait` and `plan.wait_words` (`plugin/lib/plan.py`) give the scenarios' words exactly: Marked to stay, Left by the user, Its land stopped, Under a hold on its kit, Marked to stay under a hold (the send, then "; then by lifting the hold … with crew plan go"), and Waiting on a batch. `TestWaitWords` asserts them as the spec writes them.
  - A change in no batch yet: no batch keeps the bolt, so `user_wait` gives `none`.
  - Waiting on nothing of the user's: a verification that is not green gives `none`.
  - A held base place asks no role: Flume 0.26.0's status of a place under a standing hold gives no wait on its caller, so `asks.waits_on` returns nothing for `bolt-held`, and one wait on ops for `bolt-held-lapsed` (`tests/py/test_asks.py`).
  - The bound is `runner.HOLD_BOUND`, 604800.
- **A waiting bolt's hold is posted once for its words, and again as its bound nears**: met. `runner.hold_due` covers each scenario, and `TestHoldDue` proves them:
  - Read again: a standing hold with the same words and more than half its bound left posts nothing.
  - Past half its bound: posts again at four days and at exactly half.
  - Lapsed: `flume_facts` gives no standing hold, so the words are posted again.
  - Waiting on the runner's answer: a hold of the launch with no answer posts nothing.
  - A land standing: a land asked or submitted posts nothing, while a stopped land waits on the send again.
  - A base place that waits on nothing of crew's posts nothing.
  - The wait changes: new words post.
- **A wait that ends ends crew's hold**: met.
  - An end is a hold of bound 0 with `HOLD_ENDED`. It is posted only where the standing words are those of crew's newest hold of the launch with a bound above 0, so nothing follows it, and a hold whose words crew never posted is left.
  - What crew can't read: `sweep_waits` skips an `unknown` wait, posting neither words nor an end.
  - Landed on proof: the land the raise posts is at the write's tip, so `holds_change` posts no hold of the bolt.
- **The rail's read posts the holds due by one plan write in ops's name**: met.
  - `rail_read` runs `sweep_waits` after its raises, and only on the drive's main machine.
  - `holds_post` and `holds_change` make one write as `<label>-ops`.
  - At the tip, `holds_change` re-checks the bolt, its `Stays` mark, `hold_on`, and any land or hold of the launch appended since the read.
  - The rail's text names each hold asked and each write refused.
  - `TestHoldsWrite`, `TestSweepWaits` and `TestText` prove the scenarios A land posted in the same read, A hold put between the read and the write, Two bolts at once, and Another host's read.

### drive-state

- **Every request for a host's runner is a record of the drive's requests file** (modified): met.
  - The delta keeps the main spec's three scenarios and adds A hold is a request.
  - `REQUESTS` takes `hold` in the `Act` enum, `%type: Bound int`, and `Bound` after `Delivery` in `%allowed` and `FIELDS`.
  - A hold passes `recfix --check`, both new and brought in step from the older descriptor, and a `Bound` of `8h` is refused (`tests/contract/test_recfix.py`).
- **A hold names a bolt's launch, its words and a bound**: met. `ACTS["hold"]` needs `Of`, `Words` and `Bound` and takes nothing else. `request_refusal` refuses each of these, as `TestHoldRequest` proves:
  - a hold of a unit's launch, naming it;
  - a hold with no words;
  - a bound that is no whole number of seconds;
  - a hold naming a `Host`.

### run-record

- **A hold crew posts is one entry naming its request and what the bolt waits on**: met.
  - Each hold is a `bolt.hold` on `bolt/<bolt>` with `Request`, `Head` and `Form` (`send`, `hold`, `batch` or `end`), and none of its words.
  - The first hold is the write's own act, and the rest go in `Write.also`.
  - `record.py`'s descriptor notes name `bolt.hold`.
  - Proved by `test_two_holds_are_one_write_in_ops_name_each_with_its_entry` and `test_an_end_is_a_hold_of_bound_zero_recorded_as_an_end`.

### Docs and brief

- `plugin/roles/main-ops.md` says what Decision 7 asks: the words, that no stall reaches ops for such a bolt and ops runs nothing for it, and that a stall still reaches ops for a bolt that waits on nothing of the user's.
- README, `plugin/skills/crew/SKILL.md` and `plugin/bin/crew`'s usage say the rail's read holds a waiting bolt under words that are renewed, changed and ended with the wait, and that a hold is a request of `requests.rec` (`docs.2`).
- `docs/architecture/` and `docs/adr/` are untouched (`docs.7`).

## Outside this repository

Boomdrive's runner carries the hold through `the-runner-carries-a-hold-of-a-places-waiting-move`, which is on boomdrivedev/boomdrive's bolt and not yet on its main or in a release (proposal, Impact). Until a runner carries it, each hold crew posts waits unanswered, and crew posts nothing more for that bolt (design, Migration Plan). That is the design, and nothing this change owes.
