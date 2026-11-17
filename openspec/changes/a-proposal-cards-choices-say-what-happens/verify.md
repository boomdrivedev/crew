# Verify: a-proposal-cards-choices-say-what-happens

Verified on 2026-11-17, on `change/a-proposal-cards-choices-say-what-happens` at `d99519f5`, cut from `bolt/crew-stops-flooding-the-runner-and-your-cards` at `ef7bc49f`.

**Verdict: the work falls short. The whole checks fail: the logic tier fails two cases. One is a defect in `proposal_card`, the other a case still asserting the old words. The change is not archived and goes back to its code stage.**

## The whole checks

`tests/suite --affected` ran once, from the worktree's root, as CLAUDE.md names it for a finished change. The change edits crew's command core, so every task was affected, and none replayed.

```
31 passed (0 replayed), 1 failed
```

- `logic` failed: `2 failed, 3831 passed`.
  - `tests/py/test_proposal_card.py::test_seven_new_units_are_two_lists_of_four_and_three_on_one_card`, below.
  - `tests/py/test_proposal_life.py::TestAnswers::test_drops_alone_are_a_hold_to_approve_applied_whole_or_declined_with_a_note`, below.
- `contract` and all 30 end-to-end tests passed, `t-specs`, `t-docs` and `t-cards` among them.

`openspec validate a-proposal-cards-choices-say-what-happens --strict` reports the change valid.

## What fails

### A case still asserting the old words

`tests/py/test_proposal_life.py:226` asserts a drops-alone card's summary ends "to keep a unit it drops or amends, decline with a note.", the how sentence this change replaces. The card now says, as the spec and Decision 3 have it:

```
'The case. Approved, all of it applies. Declined, none of it does, and your note tells the planner what to keep.'
```

The code is right and the case is stale. Task notes 1.4 list the cases to update in `test_proposal_card.py` and miss this one in `test_proposal_life.py`. It wants the new sentence.

### The card's subject read as the last unit's bolt

`proposal_card` in `plugin/lib/cards.py` reuses the name `to` inside its loop over the new units:

```python
to, was, now = a.bolt or None, f["before"].item(a.unit), f["after"].item(a.unit)
```

Before the loop, `to` holds the thing the card is about, the headings `title` is built from ("the switchboard-kit queue", "pages and deploys"). Two of crew's words are built from `to` after the loop, so both now name the last new unit's bolt, or `None` when it goes to a queue:

- the lists form's `about` title, `Plan change to {to}` (6 to 15 new units);
- the hold-to-approve's action, `Apply the plan change to {to}`, for a card of more than 15 new units.

Read on this branch:

| Proposal | Built | Expected |
|---|---|---|
| 7 units added to the switchboard-kit queue (lists) | `about.title`: "Plan change to None" | "Plan change to the switchboard-kit queue" |
| 16 units added to the switchboard-kit queue (approve) | `approve.action`: "Apply the plan change to None" | "Apply the plan change to the switchboard-kit queue" |

The first is `test_seven_new_units_are_two_lists_of_four_and_three_on_one_card` (`tests/py/test_proposal_card.py:229`), which fails:

```
E         Differing items:
E         {'title': 'Plan change to None'} != {'title': 'Plan change to the switchboard-kit queue'}
```

No case pins the second: `test_sixteen_new_units_are_a_hold_to_approve_that_links_its_reading_session_first` asserts no action. The spec's own words for these, the approval's action and the questions' titles ("A proposal's card names no control"), are crew's, and the design (Decision 3) keeps the action, "Apply the plan change to `<to>`", as it was. The fix is a name of the loop's own for the unit's bolt, leaving `to` as the title set it, and an assertion of the sixteen-unit card's action beside the lists case (`tests.4`).

## Tasks

All five tasks, 1.1 to 1.5, are ticked, and each case a task names exists in the file it names and passes. The ticks rest on the named cases alone. Neither failing case is among them, and the logic tier whole fails.

## Requirements and scenarios

Each scenario was read against `plugin/lib/cards.py` and the case that proves it, in `tests/py/test_proposal_card.py` unless named. Apart from what fails above, the words hold.

### Added

| Requirement / scenario | Where it holds | Proved by |
|---|---|---|
| Each new unit's choice says what happens to it: Into a started bolt | `new_row_words`, `running` read from the tip's `Path: flume` | `TestNewRowWords::test_into_a_started_bolt_it_starts_now`; `test_a_list_box_says_both_outcomes` |
| … Into a bolt the proposal starts | `starts` from the commands' `bolt start` | `TestNewRowWords::test_into_a_bolt_the_proposal_starts_it_starts_now`; `test_a_lone_unit_moved_into_a_bolt_the_proposal_starts_starts_now_or_stays_queued` |
| … After the work it needs | `after` from the plan the commands leave | `TestNewRowWords::test_after_the_work_it_needs`; on the card, read by hand on this branch: an add `--after a-first` to a started bolt is "Start e after the work it needs", "… built once a-first has landed on it.", and a `--after` on another new unit of the proposal counts too |
| … Into a bolt not started | `new_row_words` | `TestNewRowWords::test_into_a_bolt_not_started_it_is_for_later`; `test_a_move_into_a_bolt_is_a_box_to_move_it_in`; `TestBuiltDropAmendAdd` |
| … Into a queue | `new_row_words` | `TestNewRowWords::test_into_a_queue_it_is_queued_for_later`; `test_a_lone_row_is_the_choice_of_its_two_sides_since_a_list_holds_two_at_least` |
| Leaving a new unit out says where it stays: A lone unit moved from a queue | the `unticked` choice's consequence | `test_a_lone_unit_moved_into_a_bolt_the_proposal_starts_starts_now_or_stays_queued` |
| … A lone unit added | the same | `test_a_lone_row_is_the_choice_of_its_two_sides_since_a_list_holds_two_at_least` |
| … Both outcomes in a list | `option(r)` | `test_a_list_box_says_both_outcomes`; `test_chores.py::TestProposals::test_a_batch_of_chores_is_one_bolt_whose_every_chore_the_user_keeps_or_clears` |
| … Names too long for both | `option(r)`: `went` cut by words to the room `left` leaves | `test_a_box_too_long_keeps_its_left_out_whole` |
| A proposal's card names no control: Every form | the how sentences, `STAYS` | `test_no_word_of_crews_on_a_proposal_card_names_a_control`, all seven forms pass; it reads no word for "None", so it passes on the broken title and action |
| … A bolt planned to stay | the stays sentence, `STAYS` | `test_a_bolt_planned_to_stay_says_it_waits_for_the_send` |

### Modified

| Requirement / scenario | Where it holds | Proved by |
|---|---|---|
| A card asks only for its new units, in one ticked list: One dropped, three new | the `multi` form, its how sentence | `TestBuiltDropAmendAdd` |
| … A move alone | `proposal_form` | `test_a_proposals_card_form_is_read_from_its_commands_alone_as_its_card_is_built` |
| A card of one new unit is the choice of adding it: One new unit | the `choice` form, no how sentence | `test_a_lone_row_is_the_choice_of_its_two_sides_since_a_list_holds_two_at_least` |
| … One new unit beside a drop | the same | the same case's `beside` |
| A plain approval applies whole or not at all: Drops alone | the approve form's how sentences | `test_a_proposal_of_drops_alone_is_a_hold_to_approve_declined_with_a_note_to_keep_one`; `test_proposal_life.py`'s case of the same card fails on the old words, above |
| … Drops with an amendment and an order | `proposal_form` | `test_a_proposals_card_form_is_read_from_its_commands_alone_as_its_card_is_built` |
| … Keeping a dropped unit | `crew plan answer`, unchanged | its existing cases, untouched by this change |

## Rules

- `code.7`: `new_row_words` is a function of plain facts, tested in the logic tier.
- `code.8`: no view draws a proposal card's words; `board.agent_views` and the mod are untouched, as the design says.
- `docs.7`: no page under `docs/architecture/` or `docs/adr/` is edited.
- `tests.4`: the fix of what fails above carries a case for the hold-to-approve's action, which no case pins today.
