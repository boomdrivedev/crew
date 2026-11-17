# Design

## Context

Read 2026-11-17 at this branch's base, `ef7bc49f` (`bolt/crew-stops-flooding-the-runner-and-your-cards`, cut from crew's main).

**What the card says now.** `cards.proposal_card` builds a proposal's card in one of four forms, chosen by `proposal_form` from how many units and chores the proposal makes new. For each form it adds a "how" sentence to the summary after the case's first sentence:

| Form | When | The how sentence | A new unit's words |
|---|---|---|---|
| `approve` | no new unit, or more than 15 | "Hold to apply it whole." and, with a drop or amendment, "…; to keep a unit it drops or amends, decline with a note." | none |
| `choice` | one new unit | "Its one new unit is set as proposed; pick the other side and send to leave it out." | "Add `<u>`" or "Move `<u>` in", its consequence "Cleared: not added; the rest still applies" or "Cleared: stays in …"; the second choice "Leave `<u>` out", with no consequence |
| `multi` | two to five | "Each new unit below is ticked; clear any to leave it out, and send." | the same label and consequence, on a box |
| `lists` | six to fifteen | the same as `multi` | the same, in questions of five |

Two more sentences are added after it. "What it drops or amends applies with it." is added when the form isn't `approve`. "`<bolt>` stays unlanded until your send of its landings card." is added for a bolt marked to stay. The card's text block says the same through `STAYS`, "stays unlanded until your send".

**What the user saw.** Proposal 73 in boomdrive (dropped, replaced by 75) made bolt `flume-commands-stop-freezing`, moved `a-running-settle-keeps-the-host-watched` from flume's queue into it, and started it. That made a `choice` card. Its first choice was "Move a-running-settle-keeps-the-host-watched in", with the consequence "Cleared: stays in the queue; the rest still applies", which describes the other choice. Its second was "Leave … out", with no consequence. The summary told the user to pick the other side and send. Nothing on the card said that the first choice starts the work now and the second leaves it queued. The user, on that card, relayed by boomdrive-planner: 'For fuck's sake stop saying things like "pick the other side" and "send to leave it out." It doesn't make fucking sense.'

**What decides what happens.** Approving applies the proposal's commands in one commit (`plan.3`). A new unit the user leaves out is left out along with every command that only concerns it. A cleared add is never made, and a cleared move stays where it stood (record 0018, point 7 and its answer handling). A unit or chore added to or moved into a started bolt (`Path: flume`, `plan.started`) is launched by the write itself (`op_unit_add`, `op_unit_move` through `crossed_bolt`). `bolt start` launches every unit of its bolt. A unit with `After` launches once each unit it comes after has landed on the bolt (`plan.13`). One added to a bolt that isn't started waits for the bolt's start, and one added to a queue waits for a proposal that moves it into a bolt.

**What reads the words.** Pending You shows a choice's label, detail and consequence. `crew plan answer` and the planner's brief read only the ids (`add:<unit>`, `unticked`, `rows-<k>`, `approve`, `decline`), never the labels. No view draws a proposal card's words: `board.agent_views`, `status.js` and the page have none (`code.8`). `crew plan proposed`, the proposal's page and plannotator have words of their own (`plan.describe`), and none of them is a card.

**The family.** Pending You takes the card as crew builds it (`roles.5`). Its fields are unchanged, so no other tool changes. A card's form, every word on it, is crew's (`briefs.13`).

**Area pages this change touches:**

- `core.md`: `roles.5`, `code.7`, `code.8`.
- `briefs.md`: `briefs.9`, `briefs.13`.
- `plan.md`: `plan.3`, `plan.11`, `plan.12`, `plan.13`.
- `tests.md`: `tests.4`, `tests.11`, `tests.12`.
- `docs.md`: `docs.2`, `docs.4`, `docs.6`, `docs.7`.

No rule changes. `briefs.13` already has a proposal's card offer "a choice per new unit or chore to leave it out", in prose with nothing depending on Markdown. This change only says what each choice's words are. Record 0018 point 7 quotes the old consequence, "cleared: not added; the rest still applies", as the card's words. What it decides stands: a cleared add is not made, and a cleared move stays where it was. Its quoted words are the design agent's to bring up to date after the landing (`docs.7`). This change edits no page.

## Goals / Non-Goals

**Goals:**

- Every choice on a proposal's card says what happens to its unit if picked: whether it starts now, waits for its bolt, waits on other work, or waits in a queue, and where a unit left out stays.
- None of crew's own words on a proposal's card tells the user how to work it: no pick, side, tick, clear, hold or send.
- Ids, forms, kinds, recommended ids and what an answer applies stay as they are.

**Non-Goals:**

- Changing what a choice does. A cleared add still makes nothing, and keeping it in the queue instead would change `plan.3` and record 0018.
- The landings card and the deploy card, which keep their words. Their boxes are a different decision, made by a different owner, and this change does not touch them.
- `crew plan proposed`, the proposal's page and the planner's brief, which are not cards.
- Rewording the planner's case or a unit's intent. Both are the planner's words, shown as given.

## Decisions

### 1. A new unit's words come from one function of plain facts

`cards.new_row_words(facts)` (new) words one new unit or chore from plain facts. It reads no plan and calls nothing, so it is a decision in `code.7`'s sense and is tested in the logic tier (`tests.11`). The facts are:

- `kind`: `add` or `move`. A chore's command counts as the unit's.
- `unit`.
- `bolt`: where it goes, or `None` for a queue.
- `repo`: the queue's repository, for an add to a queue or a move from one.
- `came_from`: for a move, the bolt it leaves, or `None` for its queue.
- `running`: its bolt is started at the tip.
- `starts`: the proposal holds `bolt start <bolt>`.
- `after`: the units it comes after once applied.

It returns four strings. `go` is the label for going ahead, and `went` is the sentence for what then happens. `leave` is the label for leaving it out, and `left` is the clause for what then happens, lower-case so it can follow "Left out, ".

| Where it goes | `go` | `went` |
|---|---|---|
| bolt `b`, running or started here, no `after` | Start `<u>` now | It joins bolt `b` (a move: It moves into bolt `b`), which is running (started here: which this change starts), and is built now. |
| the same, with `after` | Start `<u>` after the work it needs | …, and is built once `<after, joined>` has (have) landed on it. |
| bolt `b`, not started | Add `<u>` for later (a move: Move `<u>` in for later) | It joins (moves into) bolt `b`, which has not started, and is built once `b` starts. |
| a queue (an add) | Queue `<u>` for later | It waits in the `<repo>` queue until a bolt takes it. |

| Left out | `leave` | `left` |
|---|---|---|
| an add | Leave `<u>` out | it is not added to the plan. |
| a move from a queue | Leave `<u>` out for now | it stays in the `<repo>` queue. |
| a move from bolt `p` | Leave `<u>` out for now | it stays in bolt `p`. |

`went` never names where a move comes from, since `left` names it. That keeps a box's two outcomes inside one consequence.

"Started" here means what `plan.started` means: the bolt at the tip is marked `Path: flume`. `cards` can't import `plan`, which imports it, so `proposal_card` reads the mark from the plan at the tip (`f["before"]`). It doesn't read it from the plan the commands leave, which the drawn check builds without a runner. `starts` comes from the commands. `after` comes from the plan the commands leave (`f["after"]`), so an `--after` on the add and any `unit after` in the proposal both count. The card reads no kit (`plan.12`), so it can't tell whether a unit it comes after has already landed. Either way the sentence stays true: the unit is built once that unit has landed.

Considered: handing `proposal_card` a list of started bolts from `plan.proposal_facts`, so `plan.started` stays the only reader of the mark. Not taken: every caller of `proposal_card`, and the logic cases that build its facts by hand, would need the new key for a fact the plan at the tip already carries.

### 2. Each form uses the words

- **A box** (`multi`, `lists`): label `go`, detail the intent as before, consequence `went` + " Left out, " + `left`. The consequence holds `DETAIL` characters. `left` is never cut: `went` is cut by whole words (`by_words`) to `DETAIL` less the room "Left out, " and `left` take.
- **A lone unit** (`choice`): first choice `add:<u>`, label `go`, detail the intent, consequence `went`. Second choice `unticked`, label `leave`, consequence `left` with its first letter capitalised. "Going ahead" stays recommended.
- **A hold-to-approve** has no new unit to word.

For proposal 73 the card would offer "Start a-running-settle-keeps-the-host-watched now". Its consequence would be "It moves into bolt flume-commands-stop-freezing, which this change starts, and is built now." The second choice would be "Leave a-running-settle-keeps-the-host-watched out for now", with the consequence "It stays in the flume queue."

Labels are still cut to `LABEL` (80) by `cut`. The longest prefix and suffix, "Start " and " after the work it needs", leave 52 characters for a name, longer than any unit name the drives hold today. A longer name is cut in the label and stays whole in the paragraph on the face.

### 3. The summary says outcomes, never controls

After the case's first sentence:

| Form | Sentence |
|---|---|
| `approve` | Approved, all of it applies. With a drop or an amendment, and no reading session: Declined, none of it does, and your note tells the planner what to keep. |
| `choice` | nothing: its two choices say it |
| `multi`, `lists` | Each new unit below goes ahead as proposed unless you leave it out. |

"What it drops or amends applies with it." stays on the non-approve forms. A bolt marked to stay is said as "`<b>` stays unlanded until you say to land it." For more than one bolt it is "`<a>` and `<b>` stay unlanded until you say to land them." `STAYS`, in the card's text block, becomes "stays unlanded until you say to land it". `crew plan proposed`'s "Stays:" line is not a card's and keeps its words.

The approve block's action, "Apply the plan change to `<to>`", and a list question's title, "The change, part k of g: each row as proposed", already say what happens and stay.

### 4. A logic case holds the card to naming no control

One logic case builds the card for a proposal of each form: a hold-to-approve with drops and an amendment, one of 16 new units with a session, a lone add, a lone move into a bolt the proposal starts, one list with a drop and moves, seven new units in lists, and a bolt marked to stay. In every one it reads crew's own words: the title, the summary past the case's first sentence, each choice's label and consequence, the approve block's action and each question's title. None of them may hold "pick", "side", "tick", "ticked", "clear", "cleared", "hold" or "send" as a whole word, in any case. The case's sentence, the unit names and the intents are the planner's and are not read. This is `roles.3`'s check for `briefs.13`'s words, made at the lowest tier (`tests.4`). It reads crew's built strings, never a Markdown page.

## Risks / Trade-offs

- **A card open at the release keeps its old words** until its next change. `revision` changes or follows a card only on its event, and no sweep re-raises a card for its words alone. That is accepted: the next proposal gets the new words.
- **"Built now" means launched now.** Flume starts the work as soon as its stream has room. That is the user's own "Start this now", and Flume holds the order.
- **A bolt left empty.** Leaving out the only unit of a bolt the proposal makes and starts still makes and starts that bolt (`plan.3`). This is already the behaviour, and the card's face draws the bolt.

## Migration

None. Ids, forms and answers are unchanged, so an answer to a card raised before the release is read as before.

## After deploy

None. Every scenario is a logic case on the card crew builds, and nothing about the words depends on a host.

## Task notes

**1.1** In `plugin/lib/cards.py`, beside `new_units`, add `new_row_words(kind, unit, bolt, repo, came_from, running, starts, after)`. It returns `{"go", "went", "leave", "left"}` as Decision 1's tables word them. Use `joined` for `after` and "has" or "have" by its count. Its docstring cites this change's spec, "Each new unit's choice says what happens to it" and "Leaving a new unit out says where it stays". Add `class TestNewRowWords` to `tests/py/test_proposal_card.py`, calling the function on plain facts with no plan, with these cases:
- `test_into_a_started_bolt_it_starts_now`: an add and a move.
- `test_into_a_bolt_the_proposal_starts_it_starts_now`.
- `test_after_the_work_it_needs`: one unit and two.
- `test_into_a_bolt_not_started_it_is_for_later`: an add and a move.
- `test_into_a_queue_it_is_queued_for_later`.
- `test_left_out_says_where_it_stays`: an add, a move from a queue, a move from a bolt.

**1.2** In `proposal_card`'s loop over the commands, build each row from `new_row_words`:
- `bolt` is `a.bolt`, or `None` for a queue.
- `repo` is `a.repo` for an add to a queue. For a move from a queue it is the unit's `Repo` in `f["before"]`.
- `came_from` is `d["came_from"].get(a.unit)`.
- `running` is `f["before"].bolt(bolt).get("Path") == "flume"` when the bolt is at the tip.
- `starts` is whether any command is `bolt start <bolt>`.
- `after` is `f["after"].item(a.unit).all("After")`.

Keep the row's `id`, `unit`, `is` and `ticked`. Its `label` is `go`. Keep `went`, `leave` and `left` on the row. `option(r)` gives a box the consequence `by_words(went, DETAIL - len(" Left out, " + left)) + " Left out, " + left`. Update these cases:
- `test_proposal_card.py`: `TestBuiltDropAmendAdd::test_it_is_one_checkbox_list_of_its_new_units_ticked_with_no_box_for_the_drop_or_the_amendment` (labels "Add e-fifth for later" and the long name's) and `test_a_move_into_a_bolt_is_a_box_to_move_it_in` ("Move m-move in for later", consequence ending "Left out, it stays in bolt pages.").
- `test_chores.py`: `TestProposals::test_a_batch_of_chores_is_one_bolt_whose_every_chore_the_user_keeps_or_clears`. Each chore's consequence is "It joins bolt upkeep, which has not started, and is built once upkeep starts. Left out, it is not added to the plan."

Add to `test_proposal_card.py`:
- `test_a_list_box_says_both_outcomes`: an add to a started bolt and a move from bolt `pages` into it. Build the plan with `plan_text` and the bolt's third field set.
- `test_a_box_too_long_keeps_its_left_out_whole`: a bolt and a source bolt with names long enough that `went` is cut. The consequence ends with the whole `left` and is at most `DETAIL`.

**1.3** For `shape == "choice"`, the first choice is `option(r)` with consequence `went` only. The second is `{"id": "unticked", "label": cut(leave, LABEL), "consequence": by_words(left[0].upper() + left[1:], DETAIL)}`. The how is empty, so the summary has no stray space. Update `test_a_lone_row_is_the_choice_of_its_two_sides_since_a_list_holds_two_at_least`:
- labels "Queue g-one for later" and "Leave g-one out", and the second's consequence "It is not added to the plan.";
- the summary "One more unit, queued.";
- `beside`'s summary ending "What it drops or amends applies with it.".

Add `test_a_lone_unit_moved_into_a_bolt_the_proposal_starts_starts_now_or_stays_queued`, in proposal 73's shape. Its commands are `bolt new y "…" --repo switchboard-kit`, `unit move q-one y` for a queued unit `q-one`, and `bolt start y`. Build the plan with `plan_text`, `q-one` in the switchboard-kit queue. Assert:
- "Start q-one now", and a consequence naming bolt `y` and "which this change starts";
- "Leave q-one out for now" and "It stays in the switchboard-kit queue.";
- ids `add:q-one` and `unticked`.

If `apply` cannot run `bolt start` with no runner in the fixture, build `after` with the two other commands. `starts` is read from the commands, not from `after`.

**1.4** Set the how sentences and `STAYS` as Decision 3 has them, keeping the stays sentence's singular and plural. Update these cases in `test_proposal_card.py`:
- `TestBuiltDropAmendAdd::test_its_title_is_the_kind_and_the_thing_with_its_counts_and_no_number_or_question`: "Each new unit below goes ahead as proposed unless you leave it out."
- `test_a_proposal_with_no_new_unit_is_a_hold_to_approve_of_low_risk`: "The last goes first. Approved, all of it applies."
- `test_a_proposal_of_drops_alone_is_a_hold_to_approve_declined_with_a_note_to_keep_one`: "… Approved, all of it applies. Declined, none of it does, and your note tells the planner what to keep."
- `test_a_bolt_planned_to_stay_says_it_waits_for_the_send`: "console-pages stays unlanded until you say to land it.", and the text and `cards.drawn` counting "stays unlanded until you say to land it".

**1.5** Add `test_no_word_of_crews_on_a_proposal_card_names_a_control` to `tests/py/test_proposal_card.py`, parametrized over Decision 4's proposals, built with `built`. Its helper gathers crew's words from the card:
- `title`;
- `summary` with the case's first sentence and any "Read it all in one session: …" line removed;
- each option's `label` and `consequence`, in `options` or in each question's;
- `approve["action"]`;
- each question's `title`.

Use `re.search(r"\b(pick|side|tick|ticked|clear|cleared|hold|send)\b", words, re.I)`, and name the word and where it was found when it fails. Use cases and names that hold none of the words themselves.
