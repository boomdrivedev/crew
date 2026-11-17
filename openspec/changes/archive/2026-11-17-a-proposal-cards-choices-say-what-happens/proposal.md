# A proposal card's choices say what happens

## Why

A proposal's card tells the user how to work the card instead of what each choice does. A card of one new unit says "Its one new unit is set as proposed; pick the other side and send to leave it out." A card of several says "Each new unit below is ticked; clear any to leave it out, and send." Each box's consequence reads "Cleared: not added; the rest still applies", and a hold-to-approve says "Hold to apply it whole". None of it says whether the work starts now, waits for its bolt, or stays queued.

On proposal 73's card, 2026-11-17, relayed by boomdrive-planner, the user said: 'For fuck's sake stop saying things like "pick the other side" and "send to leave it out." It doesn't make fucking sense.' Proposal 73 moved `a-running-settle-keeps-the-host-watched` from flume's queue into a new bolt it started. Its card offered "Move a-running-settle-keeps-the-host-watched in" or "Leave a-running-settle-keeps-the-host-watched out", and neither said the first starts the work now and the second leaves it queued.

## What Changes

- **Each choice says what happens if it is picked.** A unit or chore going into a running bolt, or one the proposal starts, is "Start `<unit>` now". One going into a bolt not started is added or moved in "for later". One going to a queue is "Queue `<unit>` for later". Leaving one out says where it stays: "It stays in the flume queue", "It stays in bolt `<bolt>`", or "It is not added to the plan".
- **A unit that waits on other work says so.** On a running bolt, a unit that comes after other units is "Start `<unit>` after the work it needs", and its consequence names that work.
- **In a list, each box says both outcomes.** Its consequence says what happens when kept and, after "Left out,", what happens when not.
- **The card names no control.** Crew's words on a proposal's card never tell the user to pick a side, tick, clear, hold or send. The summary says outcomes: "Approved, all of it applies." "Declined, none of it does, and your note tells the planner what to keep." "Each new unit below goes ahead as proposed unless you leave it out." A bolt marked to stay "stays unlanded until you say to land it".
- **Nothing else moves.** The card's form, kind, ids (`add:<unit>`, `unticked`, `approve`), recommended ids and answers are as they were, so `crew plan answer`, the planner's brief and what an approval applies are unchanged.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `plan-proposals`: each choice on a proposal's card says what happens if it is picked, the lone unit's two choices and a list's boxes alike. The card's own words name no control. A plain approval's card says what approving and declining do.

## Impact

- `plugin/lib/cards.py`:
  - `new_row_words` (new) words a new unit's or chore's choices from plain facts.
  - `proposal_card` builds each row's label and consequence from it, and the lone unit's second choice, and says outcomes in its summary.
  - `STAYS` says "stays unlanded until you say to land it".
- Tests: `tests/py/test_proposal_card.py` (new cases and the old wording's), `tests/py/test_chores.py` (a chore's consequence).
- No view draws a proposal card's words, so `board.agent_views` and the mod are untouched (`code.8`). No command or usage changes (`docs.2`). `crew plan proposed` and the proposal's page keep their words.
- `docs/architecture/` and `docs/adr/` are not edited (`docs.7`). Record 0018's point 7 quotes the old consequence, "cleared: not added; the rest still applies". Its decision stands, since a cleared new unit is still not made and a cleared move still stays where it was. Only the words change.
