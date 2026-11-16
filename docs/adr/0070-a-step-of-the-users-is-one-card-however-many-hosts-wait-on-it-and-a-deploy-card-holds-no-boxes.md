---
status: accepted
date: 2026-11-16
decision-makers: boomdrive-design (the record and every choice in it)
---

# 0070. A step of the user's is one card, however many hosts wait on it, and a deploy card holds no boxes

Status: accepted, boomdrive-design's. What swancloud record 0038 makes true still holds: a deploy waits on the steps of the user's it names, and the user's word for it counts only once each is done. This record changes only how crew asks for them.

Deciders: boomdrive-design, on afterthought's signal `2026-11-16-afterthought-ops-b1d70d4c/01-one-event-gets-one-plain-card` (afterthought/crew-state, afterthought/main), relayed by boomdrive-operator and boomdrive-planner, and on the user's reaction to the deploy card it quotes.

Amends: record 0059, decisions 2, 3, 5 and 6 and its amendment of 2026-11-14, which this record replaces. Decisions 1 and 4 stand: crew reads the `before` mark where the deployer hands it, and ties the step to the deployer's record of it by its words. Amends `plan.14`. Relies on record 0031 §3 (one thing, one card) and §5 (one step card at a time on an environment). Sources: `plugin/lib/ops.py` `handed_steps`, `waited_on`, `own_card`, `step_due`, `step_facts` and `plugin/lib/cards.py` `deploy_card` and the step card on crew's main at b097ed4b; swancloud's deployer, which records a step it hands as waited on once per environment, under a key made from the step's words, so every host records one step under one key.

## Context and problem statement

One step of the user's, given before swancloud's Willdan cutover deploys, was named for four hosts. crew asked it four times: as a card of its own on each of three hosts (`op/mac-studio/7`, `op/macbook-pro/8`, `op/deneb/42`) and as tick boxes on chuck-herdr-alpha's deploy card, next to ops's own card about the same cutover. Each showed the step's raw text, record and rule ids and all. The user couldn't tell what any of them asked, or why a deploy card had Done boxes.

Two choices of crew's made that. A step is keyed by its environment, so a step four hosts wait on is four steps. And a step the open deploy waits on is asked as boxes on that deploy's card (record 0059), so one go-ahead becomes a list of checkboxes.

## Considered options

1. **One card per step, and the deploy's card after it (chosen).** A step of the user's is asked once, on a card of its own that names every host waiting on it. A deploy that waits on it raises its card only once the step is done, as the plain hold-to-approve.
2. **Keep the boxes on the deploy card and drop the separate step cards.** A step shared by four hosts would still be asked on up to four deploy cards, and the boxes are what the user couldn't make sense of.
3. **One card per step, with the deploy cards raised beside it saying they wait.** Two cards at once for one go-ahead, one of which the user can't act on yet.

## Decision outcome

Option 1.

- **A step is one card, however many hosts wait on it.** A step of the user's that several environments record under one key is one card. Its title says in a plain sentence what the user does and which hosts it releases. One answer, done or skipped, settles it on every environment waiting on it when it is answered. An environment that records the same step later is asked on a new card that follows the answered one.
- **A deploy card holds no boxes.** A deploy that waits on a step of the user's has no card while the step is open. Its rail row says which card it waits on. Once every step it waits on is done, its card is raised as the hold-to-approve, and holding it is the word. The word is refused while a step the deploy waits on is open.
- **The step's card shows the step's words and nothing of crew's.** The card's body is the step's words and its why, as the deployer wrote them. crew adds no record or rule id of its own. Keeping a step's own words plain is up to whoever writes the step.
- **One step card at a time on an environment still holds.** A shared step's card counts as the open step card on each environment it names (record 0031 §5).

### Consequences

- One go-ahead the user owes is one card. It is followed by the deploy cards it releases, each a plain hold-to-approve.
- `crew ops approve` takes no ticked steps. A deploy approved while a step it waits on is open is refused, naming that step, as before.
- swancloud's deployer is unchanged. It still hands the step with its offer and records it on each host, and its hold still lifts once crew records the step done under its key on that host.
