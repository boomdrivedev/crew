# Verify: a-step-of-the-users-is-one-card

Verified 2026-11-17 on `change/a-step-of-the-users-is-one-card` at 9225d843, cut from `bolt/crew-stops-flooding-the-runner-and-your-cards`.

**Verdict: not ready to archive.** The suite fails four logic cases, and all four come from this change's own work. Every task is ticked, and every scenario of the deltas has a case. The change goes back to its code stage.

## The whole checks

`tests/suite --affected` was run once, as CLAUDE.md names it for a finished change before its merge. It runs every `check-full` task whose inputs differ from the merge-base with main. Nothing was replayed.

**Result: 31 passed (0 replayed), 1 failed. The failed task is `logic`: 4 failed, 3828 passed.**

- Passed: `contract`, `t-briefs`, `t-cards`, `t-docs`, `t-drive-set`, `t-flume-source`, `t-help`, `t-hold`, `t-journey-board`, `t-journey-cross`, `t-journey-land`, `t-journey-main`, `t-journey-main-fix`, `t-journey-ops`, `t-journey-plan`, `t-journey-review`, `t-journey-roles`, `t-journey-signals`, `t-journey-state`, `t-release`, `t-roles`, `t-runner`, `t-session-hook`, `t-slot`, `t-sluice`, `t-specs`, `t-stage-facts`, `t-suite`, `t-teams`, `t-waits` and `t-word`.
- Failed: `logic`, with four cases:
  1. **`tests/py/test_card_commands.py::test_a_deploy_waiting_on_seven_steps_posts_one_list_of_five_boxes_and_nothing_is_refused`**
     - Failure: `KeyError: 'highStakes'` at line 662.
     - Cause: the case still expects `deploy_card` to post a `multi` of five boxes with `highStakes`, recorded `Form: boxes`. That is the scenario "Seven steps the deploy waits on, and Pending You refuses questions carrying highStakes", and it belongs to the requirement "A deploy's card waiting on steps is one list of at most five boxes", which this change's `rail-cards` delta REMOVES.
     - `deploy_card` now builds the hold-to-approve alone, as Decision 8 asks, so the case asserts behaviour this change removes. It goes, as Task notes 4.2 says of the boxes cases. Any part of it that still stands, such as the post recording no `Form: boxes`, is restated against the hold-to-approve.
  2. **`tests/py/test_rail.py::TestSweepJudged::test_only_the_cards_posted_on_this_host_are_judged_and_a_decision_records_only_once_it_is_settled`** (line 1204)
  3. **`tests/py/test_rail.py::TestSweepJudged::test_a_card_or_row_whose_last_close_or_post_was_refused_lately_is_left_for_a_later_read`** (line 1261)
  4. **`tests/py/test_rail.py::TestSweepJudged::test_a_proposals_card_is_withdrawn_only_on_a_plan_read_at_or_past_the_commit_it_was_raised_at`** (line 1320)
     - Failure, the same in cases 2 to 4: `Left contains 1 more item: {'moved': []}`.
     - Cause: c1d7d05d (`feat(rail): the rail's read folds a step's cards into the one its row names`) added the key `moved` to the sweep's judgement in `plugin/lib/plan.py`, around line 11433. These three cases compare the whole judgement dict and were not updated, so each fails on the new key.
     - Their expected dicts need `"moved": []`.

The tasks' own checks name only the new and rewritten classes, which is why these four were missed. They run in the logic tier that every merge gate runs, so sluice would refuse this change's merge into its bolt as it stands.

## Tasks

All 13 tasks in `tasks.md` are ticked `[x]`.

- **1.1**
  - `openspec/changes/an-offer-card-shows-the-step-the-deploy-waits-on-first` is gone.
  - `devenv shell -- openspec validate a-step-of-the-users-is-one-card --strict` reports "Change 'a-step-of-the-users-is-one-card' is valid", with no line saying archive would refuse it.
- **6.1 and 6.2**: `t-journey-ops`, `t-briefs`, `t-docs` and `t-help` pass in the run above.
- **2.1 to 5.1**: their named classes pass in the run above. None of the four failures is in a class a task names.
  - `TestOneStepManyHosts`, `TestRows`, `TestStepCard`, `TestAStepCardsHeads`, `TestOneStepCardAtATime`, `TestSettle` and `TestStepRecordedAgain`.
  - `TestStepCardsFold`, `TestTheStepsADeployWaitsOn`, `TestAStepRecordedThatTheOfferWaitsOn`, `TestTheDeployCardOfAStepItWaitsOn`, `TestDeployCard`, `TestRefusals`, `TestViews` and `test_help`.

## Requirements and scenarios

Every scenario of both deltas has a case that names it or asserts its outcome.

**`rail-cards`, added requirements**

| Requirement | Scenarios | Covered by |
|---|---|---|
| A step of the user's is one card however many environments wait on it | Four hosts before the cutover; a held step on two hosts | `TestOneStepManyHosts`; `TestAStepCardsHeads`; `t-journey-ops` |
| A shared step's card says what the user does and which hosts it releases | The Archives disk's card; a step after one host's deploy; more hosts than the title holds | `TestStepCard` |
| A step's card changes as environments come to it or leave it | A fifth host; one host done; a host after the answer | `TestStepRecordedAgain`; `TestOneStepCardAtATime` |
| The rail's read changes a step's card that does not name its environments | Three cards from before | `TestStepCardsFold` |
| A deploy that waits on a step has no card while the step is open | chuck-herdr-alpha waits; the step done; a newer offer brings a step; boxes from before | `TestTheStepsADeployWaitsOn`; `TestAStepRecordedThatTheOfferWaitsOn`; `TestSettle` |

**`rail-cards`, modified requirements**

| Requirement | Scenarios | Covered by |
|---|---|---|
| A deploy's steps for the user are carded one at a time | A shared card holds a host's step back; opposite orders | `TestOneStepCardAtATime` |
| Each rail row has a card key for its thing | The first host's step leaves | `TestOneStepManyHosts` |

**`rail-cards`, removed requirements**: the boxes card and the shared fourth box. Their code is gone: `deploy_boxes` and `deploy_form` are absent, and `--ticked` is refused. One case still asserts them, failure 1 above.

**`main-level`**

| Requirement | Scenarios | Covered by |
|---|---|---|
| A step handed marked before is the user's alone | Before for an agent; one before and one after | `TestTheStepsADeployWaitsOn`; `TestTheDeployCardOfAStepItWaitsOn` |
| A user's step in the words of a waited step is recorded as one | The deployer records it | `TestTheStepsADeployWaitsOn`; `t-journey-ops` |
| One answer settles a step on every environment its card names | Done; skipped; an unknown key | `TestSettle`; `t-journey-ops` |
| The user's word holds the deploy's card (modified) | Approval while a step is open; ticks given | `TestRefusals`; `t-journey-ops` |
| A step the user is to take has a card until it is marked (modified) | A second host records the user's step | `TestStepRecordedAgain`; `t-journey-ops` |

**Spec form**
- Every requirement's text above its first scenario is at most 500 characters. The longest is 446.
- Each MODIFIED and REMOVED name matches a requirement in `openspec/specs/`.

**Docs** (`docs.2`): README, `plugin/skills/crew/SKILL.md` and `plugin/bin/crew`'s usage give `crew ops settle` and no `--ticked`. Main-level ops's brief carries the phrases `t-briefs` pins.

## What the code stage owes

1. Remove or rewrite `test_a_deploy_waiting_on_seven_steps_posts_one_list_of_five_boxes_and_nothing_is_refused` in `tests/py/test_card_commands.py`, since its requirement is removed.
2. Add `"moved": []` to the expected judgement of the three `TestSweepJudged` cases in `tests/py/test_rail.py`.
3. Run `tests/suite logic`, then `tests/suite --affected` once, to "0 failed".
