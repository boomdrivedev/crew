# Design

## Context

The reasoning is record 0070, boomdrive-design's, and it amends `plan.14`. The deltas, `rail-cards` and `main-level`, say what becomes true. This section records what was read on 2026-11-17, so the decisions below rest on it.

**The deployer** (swancloud `packages/swancloud-deployer/deployer.sh` at addbc878). `gather` keys every step by the first twelve hex digits of the sha256 of `<doer>\n<when>\n<words compared>`. So one step has one key on every host, whatever deploy carries it.
- `record_waited` records a step the deploy waits on through `crew ops step <env> --to <to> --key <key> --state waiting --doer user --text <file>`, with no `--when`. It does this once `crew ops offer` takes the offer (`offer_deploy`), or from `held_on_steps` for an environment with no offer, such as an `auto` one.
- `held_on_steps` holds the deploy until `crew ops steps <env> --json` gives `done` as that key's latest state on that environment.

The deployer needs nothing new. A step recorded done under its key on each host lifts each hold.

**crew as it stands** (`plugin/lib/ops.py`, `plugin/lib/cards.py`):
- A step is `(env, to, key)` (`state`). Its row and card are `op/<env>/<n>`, its n counting the environment's steps in the order first recorded (`numbered`, `rows`).
- Each environment raises its step cards one at a time (`step_due`, `step_point`, `raise_next_step`), each following the card before it on that environment (`cards.follows_of("step")`).
- A user's step that the open offer was handed marked `before` is recorded with `before` among its when words (`marked_before`). It has no row or card while that offer is open (`own_card`). The deploy's card asks it as a box (`deploy_card`, `deploy_boxes`, `deploy_form`). `crew ops approve --ticked` records it done (`ticked_refusal`).

That is how the cutover's one step became `op/mac-studio/7`, `op/macbook-pro/8` and `op/deneb/42`, for the environments with no offer open, and boxes on `deploy/chuck-herdr-alpha`, whose offer was open.

**The open change of record 0059.** `an-offer-card-shows-the-step-the-deploy-waits-on-first` is built and was never archived. Its main-level delta modifies a requirement that `crews-specs-pass-strict-validation` split, so `openspec validate` says archive would refuse it. Its rail-cards requirements, the boxes among them, never reached `openspec/specs/`. Decisions 1 and 4 of record 0059 still stand: the `before` mark, and the tie by words.

**The family.** Pending You holds the cards and is unchanged (`roles.5`). swancloud's deployer owns a step's key, and crew mints none. No other tool asks the user for a deploy's steps.

## Goals / Non-Goals

**Goals:**

- One step of the user's is one card, however many hosts wait on it. The user can read the card's title as a plain sentence of what to do and what it frees.
- One answer settles the step on every host the card named, so each deployer's hold lifts.
- A deploy card holds no boxes. A deploy waiting on a step has no card until the step is done.

**Non-Goals:**

- Any change of swancloud's.
- Rewording a step. Its words are the deployer's, and keeping them plain is the writer's (record 0070).
- One card for an agent's held step on several hosts. When the host is quiet is each host's own.
- `a-users-step-of-any-length-gets-its-card`, also unarchived. Its budgets and its face stand, and this change's title keeps its whole-word cut of the step's words.

## Decisions

### 1. One key, one step: a group is the user's steps waiting under one key

A step's group is every step whose latest entry waits on the user, the user its doer, under one key, on any environment and under any deploy. The group's members are the steps the card carries.
- An agent's step held for the user's word is a group of its own: when the host is quiet is each host's own.
- So is a gate's step (`gate_of`). It is one deploy's click on one environment.

crew reads the key as the deployer wrote it, and compares no words for the grouping. The key is the deployer's identity of a step (record 0070).

Considered: grouping by the step's words. Not taken: that makes crew a second owner of the deployer's keying, which record 0059 already declined.

### 2. The row and its card keep `op/<env>/<n>`: the carrying card's, or the first-recorded step's

A group's row key is the key of the open step card that names any of its steps (Decision 3). With none open, it is `op/<env>/<n>` of the group's step first recorded, by its first entry's `(At, Id)`.
- So the key stays put while the card is open, even when the first host's step leaves the group on its own.
- A step's number never changes (`numbered`), so the key's own step still gives the group's key.
- The card's run-record object stays `env/<env>` of its key (`plan.ROWS`). The environments it names are in its `Heads`.

Considered: a key of the step's own, `step/<deployer's key>`. Not taken, for two reasons:
- The deployer's key is no name crew accepts (`code.4`). `STEP_KEY` takes capitals, dots, colons and slashes.
- Every reader of `op/<env>/<n>` would need a second shape: `CARD_KEYS`, `ROWS`, `crews_key`, `step_since`, the brief and the views.

### 3. A step's card records the steps it names

Each post and change of a step's card records `Heads`: one word per step it carries, `<env>@<to>`, or `<env>` for a step that names no deploy, in the group's order (`plan.built_fields`, from the built card's `heads`). This keeps it as a landings card keeps its rows. The field is in the descriptor already. It holds names and commits only, no text anyone typed (`record.3`).

What reads `Heads`:
- `settle` settles exactly the steps the user was shown.
- One card at a time (Decision 5) knows each environment a card holds.
- The rail's read (Decision 7) knows when the card no longer names its row's environments as they stand.

A card from before this change records no `Heads`. It is read as naming its key's environment alone, which is all it showed (`read.1`).

### 4. The card: a plain sentence, the step's own words, no ids of crew's

A user's step's card (`cards.step_card`, the `do` as now) takes its facts from the whole group (`ops.step_facts` over the group's steps).

**The title** is `<words>, <tail>`. The words are what the step says before its first field (`step_words`), with a closing stop dropped. They are cut at whole words (`by_words`) to the room the tail leaves. The tail is one of three:
- `so <hosts> can deploy`, when any step of the group is marked `before`, or is one an open offer waits on (`waited_on`). One key is one step, so one environment's mark is the step's.
- `after <host>'s deploy`, or `after the deploys of <hosts>`, when each step names a deploy.
- `on <hosts>` otherwise.

The hosts are joined in the group's order. When the tail would take more than half of `TITLE`, it counts them instead ("so 9 hosts can deploy") and the summary names them.

**The summary** is the step's why as the deployer wrote it, when it has one, else its words. Then comes one sentence of crew's:
- for a step a deploy waits on: "It releases the deploys of <hosts>";
- for any other step: "It waits on you on <hosts>".

For more than one host it adds "; one answer settles it on each." crew writes no record or rule id: its sentence is made from host names alone.

**The face** carries the words whole as "The step" when neither the title's words, the action step nor the summary holds them whole. That rule is the one-host card's today.

**What stays as it is:** the held step's choice and the gate's card, one environment's each.

Considered: the title "After <env>'s deploy: <words>" kept, with the hosts listed after it. Not taken: the record asks for a plain sentence of what the user does and what it releases.

### 5. One step card at a time on an environment, a shared card counted on each

A step card is open on an environment when it is open and its `Heads` name that environment. A card recording no `Heads` counts on its key's environment.

The next card due (`step_due`) is the group, of those whose row key has had no card, with the earliest first-recorded step among those whose every environment has no step card open. When a card closes, crew looks for the next due on each environment the closed card named (`raise_next_step`).

Considered: each environment's first due step must be the same group. Not taken: it deadlocks. Two shared steps recorded in opposite orders on two hosts would each wait on the other's host for ever. Taking the earliest group whose hosts are all free always raises one. On one environment it is the first by number, as now.

**Which card a step card follows** (`cards.follows_of("step")`):
- the last card of the same step the user answered, when there is one, for a host that recorded the step after the answer (record 0070);
- otherwise the card before it on its first-recorded environment, its deploy's or a step's, counting a card whose `Heads` name that environment.

`cards.step_since` says, for the first case, that the user answered the earlier card and that `<hosts>` recorded the step since.

### 6. `crew ops settle`: one answer, every environment the card named

`crew ops settle <op/env/n> --state done|declined --label <label>` is the user's step row's answer, its `done` and `decline` commands. It runs where the drive's main level runs (`code.3`) and answers `-h` (`code.11`).
1. **The steps.** It reads the steps the card's last post or change named (`Heads`). With no post, it reads the steps the row carries now. It is refused, writing nothing, when no row and no card holds the key.
2. **Each step.** For each step that still waits, it records `ops.step` under that step's environment, deploy and key: `State` as given, `Doer: user`, its `When` kept, so the `before` mark stays, and `Note: answered on <key>`.
3. **The card.** It closes the card once, "Done." or "Skipped." (`CLOSED`).
4. **What follows.** For each environment the card named, it raises the next step card due. For each environment whose open offer now waits on no open step, it raises the deploy's card.

It answers once its writes are made and the raises handed on (`code.9`).

An agent's held step keeps `crew ops step`'s per-environment commands, since its answer is when to do it, and the agent records it done after.

Considered: making `crew ops step <env> --state done` settle every environment of a shared card. Not taken: the deployer records a step one host at a time, and its done on one host is that host's alone.

### 7. A card follows its group as environments come and go

When `crew ops step` records a step that joins a group whose card is open, crew changes that card in place, if the user has not answered it. The same holds for a step that leaves a group, recorded done, declined or failed on its own. The card is changed when its `Heads` differ from the group's (`ops.step_again`, extended), with a note:
- "<env> waits on it too" for a step that joined;
- "<env>'s is recorded <state>" for one that left.

A card left with no step is closed with that step's state. An answered card is left as it is (rail-cards "A card the user answered is closed, never withdrawn"). A step recorded after the answer waits for `settle`, then has its own card (Decision 5).

**The rail's read on the main level's host** does the same for a card whose `Heads` differ from its row's (`plan.sweep_cards`). That covers a raise that was missed, and the cards from before this change. When an open step card's key is no longer a row's because its step now rides another row's card, `row_gone` closes it saying "Asked on <key> with <hosts>". It does not say "its step no longer waits on you", which would be false.

### 8. A deploy waiting on a step has no card, and is raised plain once the step is done

`ops.waited_on` stands, as do the `before` mark and the tie by words (record 0059 Decisions 1 and 4). The tie compares a step's words before its first field (`ops.step_words`), each run of spaces one, so the deployer's record of a step carrying its `- why:` is tied as one recorded bare; comparing the whole text would leave the cutover's step, recorded with its why, untied. What changes:
- **No own-card exclusion.** `own_card` loses its exclusion of a step marked `before` under an open offer. Such a step has its row and card like any user's step, shared with its group.
- **The deploy's row.** While a step the open offer waits on is open, the row says it waits on that step's card by key, or that its deployer has not recorded the step yet. The rail reads the steps an offer was handed from the files kept beside it on the main level's host (`ops.offers_handed`); a host that does not keep them reads the waits from the record's `before` marks alone. Its card is raised once the step is done, and the row carries `asks: False`, so `sweep_cards` owes it no card, as a land row on proof owes none.
- **`deploy_move`.** While such a step is open it returns no move, saying why. When ops holds an unanswered card and no word stands, it returns `withdraw`. `raise_deploy` then withdraws that card with "It now waits on your step on <key>: its card is raised again once that is done." The withdrawal changes nothing of the offer.
- **`deploy_card`.** It is the hold-to-approve, always. When the deploy waited on steps, the summary says "It waited on N step(s) of yours, each done." and the face lists them first, each done. `deploy_boxes`, the multi shape and `deploy_form`'s `boxes` go.
- **Following the step's card.** `cards.follows_of("deploy")` follows the newest step card closed since the offer whose `Heads` name a step on that environment the deploy waited on. Failing that, it follows the declined deploy card, as now.
- **A card posted as boxes before.** `cards.form_asked` stays only to read such a card: a held card whose recorded form is `boxes` is withdrawn while a step is open, or followed by the hold-to-approve once none is.
- **`crew ops approve`.** It loses `--ticked` (`TICKED`, `ticks_of`), and records no step done. `ticked_refusal` becomes `waited_refusal`. Each open step is named, "the deploy of <env> to <sha7> waits on your step "<words cut>", asked on <key>", or, when the step is not recorded yet, "… which its deployer has not recorded on <env> yet". The refusal is recorded as a refused `ops.approve` (`roles.3`).
- **`crew ops step`.** For a step marked `before`, it prints that the deploy of `<env>` offered waits on it and that its card is raised once the step is done. When the last open step an offer waits on is recorded done, it raises the deploy's card. It no longer raises it again "A step it waits on is recorded done".

### 9. The views

`ops.environments` gives each waiting step the row key of its group, so every host's entry for a shared step names the one card. It gives each deploy waiting on the user's word `waits`: the row keys of the open steps it waits on, `[]` when none.

Ops's band (`board.ops_view`) changes in two places:
- A deploy line with `waits` says "waits on your step, <key>" in place of the word.
- The head line counts those deploys apart from the ones waiting on the word, and counts operations waiting once per row, so a shared step counts once.

`plugin/hooks/status.js` draws lines of `(text, style)` segments, and their shape does not change, so it is unchanged. `tests/py/test_board.py` pins that (`code.8`).

### 10. The superseded change goes, its standing parts carried

`openspec/changes/an-offer-card-shows-the-step-the-deploy-waits-on-first` is removed. The `main-level` delta here adds what of it still holds: the `before` mark read and refused on an agent's step, and the tie by words. Its boxes are what record 0070 removes. So the specs reconcile, and no later archive brings the boxes back (`docs.3`, `docs.4`). Record 0059 and the rule pages stay as the design agent wrote them (`docs.7`).

### Rules relied on

- `plan.14` as record 0070 amends it: one card however many environments wait. The deploy's card is raised only once each step is done. No ticks.
- Record 0031 §3, one thing one card, and §5, one step card at a time on an environment.
- `state.4`: every grouping, key and due card is computed from the run record. Nothing is kept beside it.
- `read.1`: a card recording no `Heads` is read as naming its key's environment. A refusal names what it could not find.
- `roles.2`: the word is the hold of the deploy's card. A step's answer is the user's, on its card.
- `roles.3`: the approval is refused by crew while a step is open. The brief's words alone do not hold it.
- `roles.5`: the cards are Pending You's, and crew builds nothing beside them.
- `briefs.11`: every card in main-level ops's name.
- `record.3`: `Heads` and `Note` are made from names.
- `code.3`, `code.4`, `code.7`, `code.8`, `code.9`, `code.11`.
- `docs.2`, `docs.3`, `docs.4`, `docs.7`.
- `tests.4`, `tests.10`, `tests.11`.

Pages whose area the change touches: `plan.md`, `briefs.md`, `record.md`, `docs.md` and `tests.md`. No rule changes, so no page is edited.

### Departures

None.

## Risks / Trade-offs

- **[A deployer that keys one step differently on two hosts]** → Two cards, as before this change. crew groups by the key alone, and swancloud keys from the step's words, doer and when.
- **[A step recorded on a new host between the user's answer and ops's settle]** → It is not settled: the card the user answered did not name it. It gets its own card, following the answered one, as the record says.
- **[A shared card's key belongs to one host]** → The key is crew's handle and not what the user reads. The title names every host. The row keeps the key while the card is open (Decision 2).
- **[One shared card holds back each of its hosts' own steps]** → That is record 0031 §5 as record 0070 keeps it. The hold ends at the one answer.
- **[A deploy row with no card]** → The row names the card it waits on, and the rail and ops's band say so, so nothing waits unseen.

## Migration Plan

None by hand. At the rail's first read with this change, on the main level's host:
- each step's open cards from before are folded: the first-recorded host's card is changed in place to name the group, and the others close naming it (Decision 7);
- each deploy card posted as boxes is withdrawn while its step is open, or followed by the hold-to-approve once the step is done (Decision 8).

A `crew ops approve --ticked` from an older brief is refused as an argument it does not take, so ops reads the new brief's words.

## After deploy

None: every behaviour here is proved by the logic tier and `t-journey-ops`. The deployer needs nothing new.

## Task notes

**1.1** Remove `openspec/changes/an-offer-card-shows-the-step-the-deploy-waits-on-first` with `git rm -r`. Check with `devenv shell -- openspec validate a-step-of-the-users-is-one-card --strict`, which must report it valid with no line saying archive would refuse it, and `test ! -e` on the removed folder.

**2.1** `ops.groups(es)`: the drive's steps waiting on the user as groups, each `{key, steps: [(n, (env, to, key), entry)], shared}`. The user's steps under one key are one group in first-recorded order. A held agent's step and a gate's step are each their own. Cases in `tests/py/test_ops.py`, a new `TestOneStepManyHosts`:
- the cutover's step on four hosts is one group;
- a held step on two hosts is two;
- a gate is one;
- a step done on one host leaves it;
- two keys are two groups.

**2.2** `ops.group_key(group, cards)`: the open step card naming any of its steps, read from `Heads` by `ops.card_steps(entries, key)`, or its key's environment alone for a card recording none. With none open, `op/<env>/<n>` of its first-recorded step. `rows` gives one row per group, with `done` and `decline` as `crew ops settle <key> --state done|declined --label <label>` for a user's group, and `crew ops step`'s for a held step. Cases in `TestOneStepManyHosts`:
- the row is `op/mac-studio/7`;
- the key is kept once mac-studio's step is done alone while the card is open;
- an old card recording no `Heads` names its key's environment.

**2.3** `ops.step_facts` over a group, and `cards.step_card`'s title, summary, `heads` and face (Decision 4). Cases in `TestStepCard`:
- the cutover's title is exactly the scenario's;
- one host after its deploy reads "…, after srv's deploy";
- nine hosts read "so 9 hosts can deploy" with the hosts in the summary;
- no sentence crew adds matches a record or rule id, `record \d|[a-z]+\.\d+`;
- `heads` is the group's `<env>@<to>`.

**2.4** `plan.built_fields` records a step card's `Heads`, and `record.py`'s descriptor comment says what a step card's `Heads` holds. Case in `tests/py/test_card_commands.py`, a new `TestAStepCardsHeads`: a shared step card's post records `Heads: mac-studio@<to> macbook-pro@<to> deneb@<to> chuck-herdr-alpha@<to>`.

**2.5** `ops.step_due` and `step_point` across environments, `raise_next_step` over every environment a closed card named, and `cards.follows_of("step")` and `step_since` for a shared step (Decision 5). Cases in `TestOneStepCardAtATime`:
- a shared card holds a host's own step back;
- two shared steps recorded in opposite orders raise one, then the other;
- a step a host records after the answer follows the answered card, saying so.

**3.1** `ops.settle` and its parser entry, `crew ops settle <key> --state done|declined`, forwarded like the other ops commands (Decision 6). `tests/py/test_help.py`'s `test_the_other_modules_parsers` asks `settle -h`. Cases in a new `TestSettle`:
- done on four hosts, each recorded under its own deploy and key with `When` kept and the note;
- the card closed once;
- the deploy raised for the host whose offer waited;
- declined raises no deploy;
- an unknown key is refused with nothing written;
- a card with no post settles the row's steps.

**3.2** `ops.step_again` and `crew ops step` change an open, unanswered shared card in place as a step joins or leaves, with the notes of Decision 7, and close a card left with no step. Cases in `TestStepRecordedAgain`.

**3.3** `plan.sweep_cards` raises a step card whose `Heads` differ from its row's, and `plan.row_gone` closes a folded card saying where it is asked (Decision 7). Cases in `tests/py/test_rail.py`, a new `TestStepCardsFold`: the three cards from before become one, and a card whose row gained a host is changed in place.

**4.1** The deploy (Decision 8):
- `own_card` without the offer exclusion;
- the deploy row's words and `asks: False`;
- `deploy_move`'s `withdraw`, and `raise_deploy` withdrawing;
- `cards.follows_of("deploy")` after the step's card;
- `crew ops step` raising the deploy once its last waited step is done.

Cases in `TestTheStepsADeployWaitsOn` and `TestAStepRecordedThatTheOfferWaitsOn`, rewritten:
- no deploy card while the step is open;
- the row names `op/mac-studio/7`;
- the sweep owes none;
- an unanswered card is withdrawn when a newer offer brings a step;
- a card from before posted as `boxes` is withdrawn, or followed once the step is done;
- the card follows the step's.

**4.2** `cards.deploy_card` as the hold-to-approve alone, its done steps listed first. `deploy_boxes` and `deploy_form`'s `boxes` are gone. Cases in `TestTheDeployCardOfAStepItWaitsOn`, rewritten: every waited step done gives the approve, its summary and face. The cases of `a-deploy-card-is-raised-whatever-its-steps` go with the boxes.

**4.3** `crew ops approve` with no `--ticked`. `waited_refusal` names each open step and its card, or that it is not recorded yet, and the refusal is recorded. Cases in `TestRefusals`. `args_refusal` no longer reads `--ticked`, and the parser refuses it.

**5.1** `ops.environments`' `row` per group and `waits` per deploy. `board.ops_view`'s deploy line and head counts (Decision 9). Cases in `tests/py/test_board.py` `TestViews`: ops's band for the cutover names one card for the four hosts, and chuck-herdr-alpha's deploy waits on it.

**6.1** `tests/t-journey-ops.sh`, its waited-on block rewritten:
- an offer to macbook-pro with a `before` step posts no deploy card;
- the deployer's record of the step on macbook-pro, and the same key on mac-studio, post one card naming both, recording `Heads`;
- `approve` is refused naming the step's card, and `--ticked` is refused;
- `settle` records done on both, closes the card and posts `deploy/macbook-pro` as an approve;
- `approve` then gives the word.

**6.2** `plugin/roles/main-ops.md` *Deploying main*:
- *An offer* loses the boxes and `--ticked`, and says a deploy waiting on a step of the user's has no card until the step is done, its row naming the step's card.
- *A step that is the user's* says one card asks a step however many hosts wait on it, and the user's answer is the row's `done` or `decline`, `crew ops settle`.

`tests/t-briefs.sh` pins "run the row's `done` or `decline` command, `crew ops settle`" and "has no card until the step is done". README, `plugin/skills/crew/SKILL.md` and `plugin/bin/crew`'s usage give `crew ops settle <key> --label L --state done|declined` and drop `[--ticked <n>[,<n>...]]`, which `tests/t-docs.sh` checks in place of its `--ticked` line.
