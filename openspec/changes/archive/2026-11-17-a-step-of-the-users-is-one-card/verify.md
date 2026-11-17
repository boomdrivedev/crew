# Verify: a-step-of-the-users-is-one-card

Verified 2026-11-17 on `change/a-step-of-the-users-is-one-card` at eb989441, cut from `bolt/crew-stops-flooding-the-runner-and-your-cards`.

**Verdict: ready to archive.** The whole checks pass. All 17 tasks are ticked, and every requirement and scenario of both deltas is met, each with a case.

## The whole checks

`tests/suite --affected` was run once, as CLAUDE.md names it for a finished change before its merge. It runs every `check-full` task whose inputs differ from the merge-base with main.

**Result: 32 passed (31 replayed), 0 failed.**

- `logic` ran fresh and passed.
- The other 31 replayed a pass on this host with identical inputs, which `tests/suite` allows: `contract`, `t-briefs`, `t-cards`, `t-docs`, `t-drive-set`, `t-flume-source`, `t-help`, `t-hold`, `t-journey-board`, `t-journey-cross`, `t-journey-land`, `t-journey-main`, `t-journey-main-fix`, `t-journey-ops`, `t-journey-plan`, `t-journey-review`, `t-journey-roles`, `t-journey-signals`, `t-journey-state`, `t-release`, `t-roles`, `t-runner`, `t-session-hook`, `t-slot`, `t-sluice`, `t-specs`, `t-stage-facts`, `t-suite`, `t-teams`, `t-waits` and `t-word`.
  - The only files changed since 9225d843 are `tests/py/test_card_commands.py`, `tests/py/test_rail.py` and this change's `tasks.md`, which are inputs of `logic` alone.
- The two cases of this change's own that pin the whole sweep judgement and the deploy card now hold:
  - `test_a_deploy_that_waited_on_seven_steps_posts_the_hold_to_approve_and_nothing_is_refused` asserts rail-cards "The step done". It posts the hold-to-approve of risk high with the seven steps listed done first. It has no box, question or `highStakes`, and records no form.
  - The three `TestSweepJudged` cases expect the `moved` key the sweep's judgement carries (task 3.4).

## Tasks

All 17 tasks in `tasks.md` are ticked `[x]`, and none is open.

- **1.1**
  - `openspec/changes/an-offer-card-shows-the-step-the-deploy-waits-on-first` is gone.
  - `devenv shell -- openspec validate a-step-of-the-users-is-one-card --strict` reports "Change 'a-step-of-the-users-is-one-card' is valid".
- **2.1 to 5.1**: their named classes and files run in `logic`, which passed above.
  - `tests/py/test_ops.py`: `TestOneStepManyHosts`, `TestRows`, `TestStepCard`, `TestOneStepCardAtATime`, `TestSettle`, `TestStepRecordedAgain`, `TestTheStepsADeployWaitsOn`, `TestAStepRecordedThatTheOfferWaitsOn`, `TestTheDeployCardOfAStepItWaitsOn`, `TestDeployCard` and `TestRefusals`.
  - `tests/py/test_card_commands.py`, `TestAStepCardsHeads` among it.
  - `tests/py/test_rail.py`: `TestStepCardsFold` and `TestSweepJudged`.
  - `TestViews` in `tests/py/test_board.py`, and `test_help`.
- **6.1 and 6.2**: `t-journey-ops`, `t-briefs`, `t-docs` and `t-help` pass above.

## Requirements and scenarios

Every scenario of both deltas has a case that names it or asserts its outcome.

**`rail-cards`, added requirements**

| Requirement | Scenarios | Covered by |
|---|---|---|
| A step of the user's is one card however many environments wait on it | Four hosts before the cutover; a held step on two hosts | `TestOneStepManyHosts`; `TestAStepCardsHeads`; `t-journey-ops` |
| A shared step's card says what the user does and which hosts it releases | The Archives disk's card; a step after one host's deploy; more hosts than the title holds | `TestStepCard` |
| A step's card changes as environments come to it or leave it | A fifth host; one host done; a host after the answer | `TestStepRecordedAgain`; `TestOneStepCardAtATime` |
| The rail's read changes a step's card that does not name its environments | Three cards from before | `TestStepCardsFold`; `TestSweepJudged` (`moved`) |
| A deploy that waits on a step has no card while the step is open | chuck-herdr-alpha waits; the step done; a newer offer brings a step; boxes from before | `TestTheStepsADeployWaitsOn`; `TestAStepRecordedThatTheOfferWaitsOn`; `TestSettle`; `test_a_deploy_that_waited_on_seven_steps_posts_the_hold_to_approve_and_nothing_is_refused` |

**`rail-cards`, modified requirements**

| Requirement | Scenarios | Covered by |
|---|---|---|
| A deploy's steps for the user are carded one at a time | Two steps after one deploy; a shared card holds a host's step back; opposite orders | `TestOneStepCardAtATime` |
| Each rail row has a card key for its thing | The standing scenarios; the first host's step leaves | `TestOneStepManyHosts`; the existing rail cases |

**`rail-cards`, removed requirements**: the boxes card and the shared fourth box.
- Their code is gone: `deploy_boxes` and `deploy_form` are absent, and `--ticked` is refused.
- No case pins them any more. Every `boxes` left in `plugin/` and `tests/py/` is one of two kinds:
  - the landings or proposal cards, which are other requirements;
  - the migration's read of a deploy card posted as boxes before this change (`cards.form_asked`, `ops.py`).

**`main-level`**

| Requirement | Scenarios | Covered by |
|---|---|---|
| A step handed marked before is the user's alone | Before for an agent; one before and one after | `TestTheStepsADeployWaitsOn`; `TestTheDeployCardOfAStepItWaitsOn` |
| A user's step in the words of a waited step is recorded as one | The deployer records it | `TestTheStepsADeployWaitsOn`; `t-journey-ops` |
| One answer settles a step on every environment its card names | Done; skipped; an unknown key | `TestSettle`; `t-journey-ops` |
| The user's word holds the deploy's card (modified) | Offered and approved; another commit; approval while a step is open; ticks given | `TestRefusals`; `TestDeployCard`; `t-journey-ops` |
| A step the user is to take has a card until it is marked (modified) | An operation; a held step; a second host records the user's step | `TestStepRecordedAgain`; `t-journey-ops` |

**Spec form**
- Every requirement's text above its first scenario is at most 500 characters.
- Each MODIFIED and REMOVED name matches a requirement in `openspec/specs/`.
- `t-specs` passes.

**Docs** (`docs.2`)
- README, `plugin/skills/crew/SKILL.md` and `plugin/bin/crew`'s usage give `crew ops settle` and no `--ticked`.
- Main-level ops's brief carries the phrases `t-briefs` pins.
