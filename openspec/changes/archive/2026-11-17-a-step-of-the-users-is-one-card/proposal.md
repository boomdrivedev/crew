# A step of the user's is one card, however many hosts wait on it

## Why

Before swancloud's Willdan cutover deployed, it named one step of the user's for four hosts. crew asked for it four times: as a card of its own on each of three hosts (`op/mac-studio/7`, `op/macbook-pro/8`, `op/deneb/42`) and as tick boxes on chuck-herdr-alpha's deploy card. The user couldn't tell what any of them asked, or why a deploy card had Done boxes (signal `afterthought/crew-state afterthought/main signals/2026-11-16-afterthought-ops-b1d70d4c/01-one-event-gets-one-plain-card`).

Two choices of crew's made that. A step is keyed by its environment, so a step four hosts wait on is four steps. And a step the open deploy waits on is asked as boxes on that deploy's card (record 0059). Record 0070, boomdrive-design's, replaces both, and `plan.14` is amended with it. swancloud's deployer is unchanged: it already records one step on every host under one key, made from the step's words.

## What Changes

- **A step of the user's is one card, however many hosts wait on it.**
  - The user's steps that wait under one key on several environments are one rail row and one card.
  - The card's title is a plain sentence of what the user does and which hosts it releases. Its body is the step's words and why, as the deployer wrote them, and crew adds no record or rule id.
  - The card records the steps it names, so the answer settles exactly what the user was shown.
  - It counts as the open step card on each environment it names (record 0031 §5).
- **One answer settles it everywhere.** `crew ops settle <card key> --state done|declined` is the row's answer. It records the state on every step the card names, each under its own environment, deploy and key, so each deployer's hold lifts. Then it closes the card once.
  - An environment that records the step after the answer is asked on a new card that follows the answered one.
  - An environment that records it while the card is still unanswered is added to that card in place.
- **A deploy card holds no boxes.**
  - A deploy waiting on an open step of the user's has no card. Its row names the step's card, and the rail's sweep owes it none.
  - Once every step it waits on is done, its card is raised as the hold-to-approve, following the step's card.
  - A deploy card left open unanswered when a step it waits on opens is withdrawn, naming the step's card.
  - `crew ops approve` takes no `--ticked`. It is refused while a step the deploy waits on is open, naming each step and its card.
- **What still stands from record 0059** is carried into the specs:
  - crew reads the `before` mark where the deployer hands it, and refuses one on an agent's step.
  - crew ties the deployer's record of a step to the offer by its words.

  The change `an-offer-card-shows-the-step-the-deploy-waits-on-first` has no sync to `openspec/specs/`, and its main-level delta cannot be archived. It goes, since this change carries every part of it that still holds.
- **The views follow** (`code.8`). Ops's band says which card a deploy waits on, and counts a shared step once.
- **The brief and the docs follow** (`docs.2`). Main-level ops's brief, README, the skill and `crew`'s usage give `crew ops settle` and drop `--ticked`.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `rail-cards`: the user's steps under one key are one card naming each host. A deploy waiting on one has no card until it is done, and then a plain hold-to-approve. A shared card counts on each of its environments. A step's row key is its first environment's. The boxes on a deploy's card are removed.
- `main-level`: `crew ops settle` answers a step's card on every environment it names. `crew ops approve` takes no ticks and is refused while a step the deploy waits on is open. The `before` mark and the tie by words are stated.

## Impact

- `plugin/lib/ops.py`: the grouping of a step's environments, its row and its card, one card at a time across environments, `settle`, `approve` without ticks, the deploy's wait on a step's card, and `environments`' rows. The parser loses `--ticked` and gains `settle`.
- `plugin/lib/cards.py`: `step_card` for a shared step, `deploy_card` without boxes, `follows_of` and `step_since` for a shared step.
- `plugin/lib/plan.py`: `built_fields` records a step card's `Heads`. The sweep owes no card to a deploy row waiting on a step. `row_gone` names the card that now asks a folded step. The rail's read changes a step card whose environments moved.
- `plugin/lib/record.py`: the descriptor's comment on `Heads`.
- `plugin/lib/board.py`: ops's band.
- `plugin/roles/main-ops.md`, README, `plugin/skills/crew/SKILL.md` and `plugin/bin/crew`'s usage.
- Tests: `tests/py/test_ops.py`, `tests/py/test_board.py`, `tests/py/test_rail.py`, `tests/t-journey-ops.sh`, `tests/t-briefs.sh` and `tests/t-docs.sh`.
- `openspec/changes/an-offer-card-shows-the-step-the-deploy-waits-on-first` is removed.
- `plugin/hooks/status.js` is unchanged, since every line it draws keeps its shape.
- No swancloud change.
