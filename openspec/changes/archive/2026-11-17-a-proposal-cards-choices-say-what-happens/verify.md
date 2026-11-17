# Verify: a-proposal-cards-choices-say-what-happens

Verified on 2026-11-17, on `change/a-proposal-cards-choices-say-what-happens` at `b9e4fc0a`, cut from `bolt/crew-stops-flooding-the-runner-and-your-cards` at `ef7bc49f`.

**Verdict: the whole checks pass and the work holds. Every requirement and scenario of the change's spec is met, and every task is ticked done. The change is archived.**

## The whole checks

`tests/suite --affected` ran once, from the worktree's root, as CLAUDE.md names it for a finished change. The change edits crew's command core, so every task was affected, and none replayed.

```
32 passed (0 replayed), 0 failed
```

`logic`, `contract` and all 30 end-to-end tests passed, `t-specs`, `t-docs` and `t-cards` among them.

`openspec validate a-proposal-cards-choices-say-what-happens --strict` reports the change valid.

## The card's subject

`proposal_card` in `plugin/lib/cards.py` names a new unit's bolt `into` inside its loop over the new units. `to` keeps what the title set it to, the headings the card is about. So the two words built from `to` after the loop name the title's bolts or queue:

- the lists form's `about` title, "Plan change to the switchboard-kit queue", which `test_seven_new_units_are_two_lists_of_four_and_three_on_one_card` asserts;
- a card of more than 15 new units, whose hold-to-approve action is "Apply the plan change to the switchboard-kit queue", which `test_sixteen_new_units_are_a_hold_to_approve_that_links_its_reading_session_first` asserts (`tests.4`).

A drops-alone card's summary ends "Declined, none of it does, and your note tells the planner what to keep.", which `tests/py/test_proposal_life.py`'s `TestAnswers::test_drops_alone_are_a_hold_to_approve_applied_whole_or_declined_with_a_note` asserts.

## Tasks

All six tasks, 1.1 to 1.6, are ticked. Each case a task names exists in the file it names and passes in the logic tier.

## Requirements and scenarios

Each scenario was read against `plugin/lib/cards.py` and the case that proves it. Cases are in `tests/py/test_proposal_card.py` unless named.

### Added

| Requirement / scenario | Where it holds | Proved by |
|---|---|---|
| Each new unit's choice says what happens to it: Into a started bolt | `new_row_words`, `running` read from the tip's `Path: flume` | `TestNewRowWords::test_into_a_started_bolt_it_starts_now`; `test_a_list_box_says_both_outcomes` |
| … Into a bolt the proposal starts | `starts` from the commands' `bolt start` | `TestNewRowWords::test_into_a_bolt_the_proposal_starts_it_starts_now`; `test_a_lone_unit_moved_into_a_bolt_the_proposal_starts_starts_now_or_stays_queued` |
| … After the work it needs | `after` from the plan the commands leave | `TestNewRowWords::test_after_the_work_it_needs` |
| … Into a bolt not started | `new_row_words` | `TestNewRowWords::test_into_a_bolt_not_started_it_is_for_later`; `test_a_move_into_a_bolt_is_a_box_to_move_it_in`; `TestBuiltDropAmendAdd` |
| … Into a queue | `new_row_words` | `TestNewRowWords::test_into_a_queue_it_is_queued_for_later`; `test_a_lone_row_is_the_choice_of_its_two_sides_since_a_list_holds_two_at_least` |
| Leaving a new unit out says where it stays: A lone unit moved from a queue | the `unticked` choice's consequence | `test_a_lone_unit_moved_into_a_bolt_the_proposal_starts_starts_now_or_stays_queued` |
| … A lone unit added | the same | `test_a_lone_row_is_the_choice_of_its_two_sides_since_a_list_holds_two_at_least` |
| … Both outcomes in a list | `option(r)` | `test_a_list_box_says_both_outcomes`; `test_chores.py::TestProposals::test_a_batch_of_chores_is_one_bolt_whose_every_chore_the_user_keeps_or_clears` |
| … Names too long for both | `option(r)`: `went` cut by words to the room `left` leaves | `test_a_box_too_long_keeps_its_left_out_whole` |
| A proposal's card names no control: Every form | the how sentences, `STAYS`, the action and the questions' titles built from `to` | `test_no_word_of_crews_on_a_proposal_card_names_a_control`, all seven forms |
| … A bolt planned to stay | the stays sentence, `STAYS` | `test_a_bolt_planned_to_stay_says_it_waits_for_the_send` |

### Modified

| Requirement / scenario | Where it holds | Proved by |
|---|---|---|
| A card asks only for its new units, in one ticked list: One dropped, three new | the `multi` form, its how sentence | `TestBuiltDropAmendAdd` |
| … A move alone | `proposal_form` | `test_a_proposals_card_form_is_read_from_its_commands_alone_as_its_card_is_built` |
| A card of one new unit is the choice of adding it: One new unit | the `choice` form, no how sentence | `test_a_lone_row_is_the_choice_of_its_two_sides_since_a_list_holds_two_at_least` |
| … One new unit beside a drop | the same | the same case's `beside` |
| A plain approval applies whole or not at all: Drops alone | the approve form's how sentences | `test_a_proposal_of_drops_alone_is_a_hold_to_approve_declined_with_a_note_to_keep_one`; `test_proposal_life.py::TestAnswers::test_drops_alone_are_a_hold_to_approve_applied_whole_or_declined_with_a_note` |
| … Drops with an amendment and an order | `proposal_form` | `test_a_proposals_card_form_is_read_from_its_commands_alone_as_its_card_is_built` |
| … Keeping a dropped unit | `crew plan answer`, unchanged | its existing cases, untouched by this change |

## Rules

- `code.7`: `new_row_words` is a function of plain facts, tested in the logic tier.
- `code.8`: no view draws a proposal card's words, so `board.agent_views` and the mod are untouched, as the design says.
- `docs.7`: no page under `docs/architecture/` or `docs/adr/` is edited.
- `tests.4`: the hold-to-approve's action for more than 15 new units is pinned by a logic case.
