# Design

## Context

**Why a waiting bolt reads stalled.** A started bolt's base place, of crew's kind `crew/bolt@1`, has no stages and lands (`plugin/flume/kinds/bolt@1/kind.toml`). Once no place on its branch is live and its submission has not been asked for, Flume reads it waiting on its caller for a retry of its submission, `waiting_on` `{act retry, stage null, why unsubmitted}` (Flume `crates/flume-core/src/status.rs` `base_waiting_on`, clause 203). That is the moment its last unit merges. crew asks for the submission only by a `land`, on proof or on the user's send (record 0056, record 0067). So a bolt that waits on the user waits on its caller under no hold's words, and after five minutes Flume reads it stalled and delivers that once to its recipient, `<label>/ops`, and to the answerer behind its stream (clause 130, core.24). crew's own `asks.waits_on` then reads it pending for ops, so ops's run is woken for it too. That is signal `2026-11-14-boomdrive-ops-f85c2fe2/01`.

**What crew holds today of what a bolt waits on.** The rail's land row (`rail_rows`, the group `land`) holds each started bolt of a kit whose every unit has merged, with:
- whether it can land (`can`): verification green at its head, every unit's latest change in a batch the user answered, no fix in flight, no refusal, conflict or landing in flight at its head;
- how it lands once it can (`lands_by`): `proof`; `send` for a bolt marked to stay, one the user left and one whose land at its head was stopped; `hold` for any other while a hold stands on its kit or drive (`hold_on`);
- its line, saying what keeps it from landing, the batches the user has not answered among them (`unread`).

The raise of a kit's landings card posts the lands (`landings_raised`, `lands_post`), and the rail's read on the main level's host raises the kits that need it (`sweep_moved`). The rail's read is the host's follower, which reads again whenever a kit's refs, the state branch, a runner's branch or the run record move (`plan.12`).

**What the family holds.**
- **Flume** lets a caller hold the move a place waits on it for, `flume hold <place> --waiting [--for <time>] <words>`, with words saying who makes it and how and a bound after which the hold lapses. While it stands the place is not stalled. A later hold on that move replaces it, a retry naming the stage or the submission ends it as the move made, and Flume watches no event and ends no hold itself (clause 130, core.24, from `v0.17.0`). A place that waits on no move of its caller's is refused a hold. Its status lists every hold, the one on the waiting move as `{on: waiting, words, since, bound, lapsed}` (`crates/flume-seams/src/held.rs` `Hold`, read at `v0.26.0`). A hold is not tied to the move it was put on: one put while the place waited stays until its bound, a retry or a drop, and covers the place's next wait.
- **Boomdrive's runner** carries a control plane's `hold` as Flume's hold of the launch's place's waiting move, with exactly the words and bound given, once, under the launch's lease. It refuses a hold with no words and one of a launch not launched, and Flume's refusal is the hold's answer. It judges nothing of the wait and renews and ends no hold of its own (boomdrivedev/boomdrive `the-runner-carries-a-hold-of-a-places-waiting-move`, its core.59 and record 0002's amendment of 2026-11-14). crew's side is named there (its design, Decision 6): `Act: hold` with `Of`, `Words` and `Bound` in whole seconds, naming no `Host`; `hold` in the `Act` enum, `%type: Bound int`, `Bound` after `Delivery` in `%allowed` and in `FIELDS`. That change landed on Boomdrive's bolt `the-runner-needs-no-hand-on-a-host` (afba153a) and, read 2026-11-16, is not yet on its main or in a release.
- **crew** decides what a bolt waits on and the words (record 0067 as amended 2026-11-14; Boomdrive core.1, the control plane decides what a place waits on).

So each piece has one owner: the hold and its lapse are Flume's, carrying it is the runner's, the words and when to post them are crew's. No other tool changes for this unit.

**Area pages this change touches:**
- `core.md`: `state.1`, `state.4`, `state.5`, `roles.5`, `roles.6`, `read.1`, `read.2`, `code.1`, `code.2`, `code.7`, `code.8`, `code.9`.
- `plan.md`: `plan.1`, `plan.2`, `plan.12`, `plan.16`.
- `record.md`: `record.1`, `record.3`.
- `briefs.md`: `briefs.11`, `briefs.12`.
- `docs.md`: `docs.2`, `docs.6`, `docs.7`.
- `tests.md`: `tests.4`, `tests.11`.

No rule changes, so no page is edited (`docs.7`): record 0067's amendment and `plan.16` already carry the decision.

## Goals / Non-Goals

**Goals:**

- A started bolt that waits on the user, for their send, their lift of a hold or their answer to a batch, has its base place held under words saying what it waits on and where the user answers it, so Flume reads it waiting and delivers no stall, and no role is woken for it.
- The words last as long as the wait, follow it when it changes, and end when it ends, so a bolt that waits on nothing of the user's stalls as today.

**Non-Goals:**

- **A fix of main waiting on the user's send.** Its place waits under the submission hold its launch puts (`Hold: submission`). Whether that stalls, and its words, are a unit of their own.
- **A base place that waits on crew before the bolt is proven, for anything but the user.** It still stalls, and the stall reaches whom it reaches today (record 0067's amendment, "a stall still says something"), a batch crew has yet to make among it.
- **New drawing in the views.** The rail's land line already says what such a bolt waits on (`lands once you have answered batch 5`, `stays: can land on your send of land/crew`, `held by the hold on crew's landings`), and the board's time says who holds it (`plan.20`). Flume's own status and list show the place waiting under the words.
- **A hold of a hosted control plane.** No version of the hosted protocol carries one (Boomdrive core.42); that is Boomdrive's and the cloud's.

## Decisions

### 1. A hold is a request of the drive's requests file

`runner.REQUESTS` takes a hold as the runner's design names it:
- the `%doc` and the file's comment name a hold of a bolt's base place under `Words`, for `Bound` seconds;
- `%type: Act enum launch retry drop priority land preview confirm hold`;
- `%type: Bound int`;
- `%allowed` gains `Bound` after `Delivery`, and `FIELDS` likewise.

`ACTS["hold"] = (("Of", "Words", "Bound"), ())`: a hold carries its launch, its words and its bound, and takes nothing else, `Host` among it. `request_refusal`:
- names a hold among the acts in its message for an act it does not know;
- checks a hold's `Of` as it checks a land's: a launch of the same work, and that work a bolt's, `bolt/<bolt>`;
- refuses a `Bound` that is not decimal digits, naming it as no whole number of seconds.

A hold with no `Words`, or empty ones, is refused as missing a field, as every act's needs are. The descriptor reaches each branch's `requests.rec` by `in_step` at its next write, as `land`, `preview` and `confirm` did.

Not taken:
- **`Bound` in Flume's span form, `7d`.** The runner reads a whole number of seconds, and recutils checks an `int`.
- **A hold naming the runner's host.** A request acting on a launch names no host; the runner holding the launch takes it (drive-state).

### 2. What a bolt waits on is read from its land row, and said from crew's own records

`plan.user_wait(f)` decides it from the land row's facts of one bolt (`code.7`): `can`, `how` (`lands_by`), `stays`, `left`, `stop`, `hold` (`hold_on`), `batches` and `known`. It answers one of:
- `{on: send, why: stays | left | stopped, hold}`: it can land and lands on the user's send; `hold` is the hold standing on its kit or drive, or None. A bolt marked to stay, left or stopped reads `send` even under a hold (`lands_by`), and its words name both.
- `{on: hold, hold}`: it can land and would land on proof, but a hold stands.
- `{on: batch, batches, hold}`: it cannot land, and what alone keeps it is the batches the user has not answered: its verification is green, no unit's latest change is outside a batch, and nothing after the batch line replaced its line in `rail_rows` (no landing in flight, refused, unknown or carried from before bolts were base places).
- `{on: none}`: every fact read, it waits on nothing of the user's: it lands on proof, its verification is not green (`none`), a unit's change waits for a batch, a fix is in flight, it takes main first, it carries another bolt's work, or its landing is in flight.
- `{on: unknown, why}`: a fact it rests on can't be read: its verification `unknown`, whether its units have been in a batch, or its landing (`read.1`).

`rail_rows` gives each bolt of a land row its `wait`, beside `bolt`, `host`, `can`, `head` and `stays`.

`plan.wait_words(label, kit, wait, head)` says it in crew's own words, made from names and the hold's own `Why`, saying who makes the move and how and where they answer it (clause 130):
- send: `the user, by their send of its row on <kit>'s landings card, land/<kit>: ` and then `it is marked to stay`, `they left it unticked on an earlier send`, or `its land at <head7> was stopped`;
- hold: `the user, by lifting the hold on <held_named> ("<why>") with crew plan go: it then lands on proof`;
- batch: `the user, by answering review batch 5 on its card, batch/5`, or `review batches 4 and 5 on their cards, batch/4 and batch/5`;
- a send or a batch under a hold adds `; then by lifting the hold on <held_named> ("<why>") with crew plan go`;
- none and unknown have no words.

`held_named` is the raise's own (`crew's landings`, `the landings of swancloud's every kit`).

Not taken:
- **Reading the wait at the raise of the kit's landings card.** The raise reads only what a card shows: a bolt kept by a batch is no row, and a bolt under a hold is raised by no read. The land row holds every bolt whose units have merged, and is read on every follower read.
- **One generic sentence, `waits on the user`.** Clause 130 asks who makes the move and how, and the user answers each wait in a different place.

### 3. Whether a hold is due is read from crew's requests and Flume's status

`runner.flume_facts` gains `waiting_hold`: the hold Flume's status lists `on: waiting`, not lapsed, as `{words, since, bound}`, `since` in seconds, `bound` None where it gives none; None where there is none, or its words or since are absent or of another shape (`read.2`).

`runner.hold_requests(requests, launch)` gives each hold of a launch in `requests.rec`'s order. `runner.hold_due(launch, words, requests, reads, now)` decides (`code.7`), `now` in seconds since the epoch, as Flume's `since` is:
1. None for no launch (a bolt from before bolts were base places), a launch no runner crew read has taken, or one it can't tell (`taken`).
2. None while a hold of the launch has no answer from the runner that holds it: one at a time, so a runner that does not carry holds yet is asked once.
3. None unless its landing reads `none` or `stopped` (`landing_outcome`): a land asked or submitted is the move made, and Flume ends the hold at its retry.
4. None unless Flume's status of the base place, as the runner carried it, gives a move it waits on (`waiting`): Flume refuses a hold of a place that waits on none.
5. With words: `("hold", words)` unless the standing `waiting_hold` has those words, a bound, and more than half of it left (`since + bound - now > bound // 2`).
6. With none: `("end", HOLD_ENDED)` where the standing hold's words are the `Words` of the newest hold crew posted of the launch, with a bound above 0. Otherwise None.

`HOLD_BOUND` is 604,800 seconds, seven days. A hold is posted again at the first read past half its bound, so the bound holds while any read falls between three and a half and seven days after the last post. A drive's branch, its runners' branches or a kit's refs move far more often than that, a weekend's quiet among them. A hold that lapses unrenewed makes Flume stall the place once, which wakes ops's run, whose turn moves the branch, and the read that follows posts the words again.

Not taken:
- **Eight hours, the runner's example.** A quiet night holds no read for four hours, so the place would stall overnight, the case the amendment names.
- **Reading only crew's own requests, with no status.** Flume keeps a hold until its bound, a retry or a drop, not until the wait it was put for ends. Only its status tells whether crew's words still stand on the place, so a refused or lapsed hold is posted again and a stale one ended.
- **A timer of crew's to renew.** crew runs no service (`state.4`) and the follower reads on moves (`plan.12`); the long bound makes the reads that come enough.

### 4. A wait that ends ends crew's hold; a hold not crew's is left

A land ends the wait itself: Flume ends the hold at the retry of the submission (clause 130), and step 3 posts nothing while it stands. Any other end leaves Flume's hold standing, and it covers the place's next wait. So where the base place waits on crew under the words of the hold crew last posted, and the bolt waits on nothing of the user's, crew posts a hold of its launch with a bound of 0 and the words `HOLD_ENDED`, `crew ends its hold: the bolt waits on nothing of the user's`. Flume lets it lapse at once, and the place stalls as it would have, its stall saying something. That end is then the newest hold crew posted, so nothing more is posted for it.

A hold whose words crew never posted of the launch, a role's or a person's, is left: crew replaces it only with words of its own when the bolt waits on the user, as Flume lets a later hold replace an earlier one.

Nothing is posted when crew can't tell what the bolt waits on (`{on: unknown}`, `read.1`).

Not taken:
- **Leaving a stale hold to its bound.** For up to seven days the place would read waiting on the user under words no longer true, which is the stall hidden.
- **A request to end a hold.** The runner's interface has none, and a hold of bound 0 is one it carries as given (Boomdrive's design, Decision 2).

### 5. The rail's read posts the holds due, after its raises, by one plan write in ops's name

`plan.sweep_waits(fleet, read, acts)` runs in `rail_read` after `sweep_moved`, on the main level's host alone, as `sweep_moved` does. For each drive whose main machine is this host, it reads each land row's bolts:
- skips a bolt whose `wait` is absent or `unknown`;
- finds its base place's launch (`runner.launch_of(requests, "bolt/<bolt>")`);
- makes its words (`wait_words`), none for `{on: none}`;
- asks `runner.hold_due` with the read's requests and runners and the clock (`acts.now()`).

The holds due, if any, go to `acts.post_holds(label, owner, due, requests)`, `owner` being `<label>-ops`, which is `holds_post`. Each due item carries the bolt, its kit, its launch, its head, its `Form` (`send`, `hold`, `batch` or `end`), its words, its bound (`HOLD_BOUND`, or 0 for an end), and the facts its words were made under: its `Stays` mark and `hold_on`.

`holds_post` makes one plan write in ops's name (`state.1`), whose change `holds_change` re-checks each item at the tip it is applied to (`plan.1`). It skips one whose bolt the plan no longer holds, whose `Stays` mark or `hold_on` differs at the tip, or whose launch has a land or a hold at the tip that the read's requests lacked. Each one left is a `request(w, "hold", "bolt/<bolt>", Of=…, Words=…, Bound=…)`. The write raises `Unposted` where none is left, writing nothing. A write refused is said on the rail's text and the read goes on.

The read's raises run first, so a land they post is at the write's tip, and its bolt is skipped.

The rail's text names each hold posted, under `holds asked of the runner for bolts waiting on you:`, each `<bolt> (<label>): hold <n>, ` and then `waits on your send`, `waits on the hold's lift`, `waits on your answer to a batch`, or `crew's hold ended: it waits on nothing of yours`.

Not taken:
- **Posting holds from the raise of the kit's landings card.** See Decision 2. The raise still posts the lands first, and `sweep_waits` reads its result at the tip.
- **One write per bolt.** One per drive per read keeps the branch's commits few (`plan.12`) and needs one push.

### 6. The run record names each hold

Each hold posted is one entry, `bolt.hold` on `bolt/<bolt>`, carrying:
- `Request`, the hold's number;
- `Head`, the bolt's head the read found;
- `Form`, `send`, `hold`, `batch` or `end`.

It carries none of the hold's words, which may hold the user's own (`record.3`). The first is the write's own act and the rest are written with it (`Write.also`), as `lands_change` does. `Request` and `Form` are fields the descriptor already allows, so only `record.py`'s notes on them name `bolt.hold`.

### 7. The briefs and the docs

Main-level ops's brief says that while a proven bolt waits on the user, crew holds its base place under words naming what it waits on, so Flume reads it waiting and no stall reaches ops for it, and ops runs nothing for it. A stall of a base place still reaches ops when the bolt waits on nothing of the user's, as before.

README's State section names a hold among `requests.rec`'s requests, and its Landing section says the rail's read holds a waiting bolt's base place under words. `plugin/skills/crew/SKILL.md`'s `crew rail` line and `plugin/bin/crew`'s usage line for `crew rail` say so too (`docs.2`).

### Rules relied on

- `roles.5`, `roles.6`: crew decides the words and posts a request on its branch; the runner carries it and Flume holds it. crew builds no wait or timer of Flume's or the runner's, and messages no one.
- `state.1`, `state.5`, `plan.1`, `plan.2`: one plan write in ops's name, each request checked by recfix and crew's rules, re-checked at the tip, each act with its entry, pushed without force.
- `state.4`, `plan.12`: the rail's read is the host's follower, reading on moves; `sweep_waits` decides from the read alone and writes only when a hold is due.
- `read.1`: a bolt whose wait can't be told, a runner crew can't read, or a status with no move read gets nothing posted, neither words nor an end.
- `read.2`: Flume's hold is read from its status by guarded facts.
- `code.1`: standard library only.
- `code.2`: a refusal from `request_refusal` reaches the write as a `Refusal`.
- `code.7`: `user_wait`, `wait_words`, `hold_requests`, `hold_due` and the item checks of `holds_change` start no process.
- `code.8`: nothing the views draw changes. The land row's bolts gain `wait`, which `sweep_waits` alone reads; `board.agent_views` and `plugin/hooks/status.js` read no new key.
- `code.9`: the rail's read answers once its write is made; the runner carries the hold in its own pass.
- `plan.16` as record 0067 amends it, `briefs.11`, `briefs.12`: what lands a bolt and what the landings card asks are unchanged; a batch is still the one place the user reviews the work.
- `record.1`, `record.3`: one entry per hold, with none of its words.
- `docs.2`, `docs.6`, `docs.7`.
- `tests.4`, `tests.11`: every case is in the logic tier but recfix's reading of the descriptor, in the contract tier, and the briefs' and usage's wiring, in their end-to-end tests.

### Departures

None.

## Risks / Trade-offs

- **The hold reaches Flume after the place stalled.** Between the last unit's merge and the runner carrying the hold are the runner's pass, the follower's fetch, crew's write and the runner's next pass, a few minutes. Where that passes five, Flume delivers the stall once, and the hold then takes the place out of stalling (clause 130). A hold cannot be put sooner: Flume refuses one before the place waits.
- **The runner does not carry holds yet.** Boomdrive's change is on a bolt, not in a release. A runner before it gives an unhosted hold nothing, so each launch's first hold waits unanswered, and crew posts nothing more for it: the place stalls as today. Once the runner carries it, it carries that one hold. If its words are stale, the read after its answer posts the current words or an end.
- **No read falls in a hold's renewal window.** The place stalls once, which wakes ops's run, and its turn's commit brings a read that posts the words again.
- **The rail's land row and the raise disagree.** The row may read a bolt able to land that the raise then finds in conflict with main. Its hold is posted with send words, and the base place soon waits on a fix, not on crew. Once the fix merges, the same words stand, or an end follows.
- **A hold's words hold the user's own,** the `Why` of a hold on the drive or kit, in `requests.rec`, as a retry's `Words` and a launch's `Brief` hold theirs. The run record holds none (`record.3`).
- **Mixed releases.** An older crew that writes `requests.rec` after the first hold brings its descriptor to its own `Act` enum, and recfix refuses the hold's `Act`, so that host's write is refused naming it until it takes this release. Holds are posted only on the drive's main level's host, whose crew writes the drive's requests.

## Migration Plan

- Nothing held changes shape but `requests.rec`'s descriptor, which `in_step` brings each branch to at its next write, and the run record's `bolt.hold` entries, whose fields the descriptor already allows.
- A bolt waiting on the user when this lands is held at the first rail read on its main level's host running this crew, once its base place waits on crew. One already stalled is taken out of stalling by the hold.
- Until a host's runner carries holds, each launch's first hold waits unanswered and the place stalls as today (Risks).

## After deploy

None. Every outcome here is a logic-tier or contract case, or the briefs' and the usage's end-to-end tests. Flume's reading of a hold is Flume's, proven in its own repository, and the runner's carrying of it is Boomdrive's, proven in its own.

## Task notes

**1.1** `plugin/lib/runner.py`:
- `REQUESTS`: the comment and `%doc` name a hold of a bolt's base place under its words for its bound; `%type: Act enum launch retry drop priority land preview confirm hold`; a line `%type: Bound int` after `%type: Request,Of,After,Priority int`; `%allowed` with `Bound` after `Delivery`.
- `FIELDS` with `"Bound"` after `"Delivery"`.
- `ACTS["hold"] = (("Of", "Words", "Bound"), ())`.
- `request_refusal`:
  - its unknown-act message lists `a hold`;
  - `hold` joins the acts whose `Of` must be a launch of the same work;
  - a hold of work not `bolt/` is refused, `hold <n> for <work> names launch <of>, which is no bolt's: a hold is of a bolt's base place`;
  - a `Bound` that is not decimal digits is refused, `hold <n> for <work> names Bound <v>, which is no whole number of seconds`.

Cases, a new `TestHoldRequest` in `tests/py/test_runner.py`, built as `TestConfirmRequest`'s are:
- `test_a_hold_of_a_bolts_launch_with_words_and_a_bound_is_taken`
- `test_a_hold_of_a_units_launch_is_refused_naming_it`
- `test_a_hold_with_no_words_or_no_whole_bound_is_refused`
- `test_a_hold_naming_a_host_is_refused`
- `test_request_fields_writes_bound_after_delivery`

**1.2** `tests/contract/test_recfix.py`, `test_a_hold_with_words_and_a_bound_passes_recfix_and_a_bound_of_no_number_is_refused`, beside the confirm's:
- a launch of `bolt/x` and a hold of it with `Words` and `Bound: 604800` pass `plan.checked` with `runner.REQUESTS`;
- a hold whose `Bound` is `8h` is refused by recfix;
- a `requests.rec` written under the descriptor before this change, brought in step by `in_step`, takes the hold and passes.

**1.3** Fixtures in a new `tests/py/flume-0.26.0/`, with a `README` and `version.txt` (`0.26.0`), written from Flume v0.26.0's own types: `crates/flume-seams/src/held.rs` (`Hold`, `HoldOn::Waiting`, `Waits::Unsubmitted`), `crates/flume-core/src/status.rs` (`base_waiting_on`) and `crates/flume-core/src/answer.rs` (`PlaceStatus`). Each starts from `tests/py/flume-0.17.0/bolt-submitted.json`'s keys and is trimmed as those are. The README says each was written, not recorded, since no host had held a base place's waiting move when they were made.
- `bolt-unsubmitted.json`: a base place live with no place on its branch, its submission unasked, `waiting_on {act retry, stage null, why unsubmitted, since 1794700000, words null}`, `holds []`, `stalled true`.
- `bolt-held.json`: the same, `holds [{on waiting, words "the user, by their send of its row on crew's landings card, land/crew: it is marked to stay", since 1794700300, bound 604800}]`, `stalled false`.
- `bolt-held-lapsed.json`: `bolt-held.json` with the hold's `lapsed 1795305100` and `stalled true`.

`runner.flume_facts` gains `"waiting_hold"`, read from `p["holds"]` when it is a list: the first entry that is a dict with `on == "waiting"`, no `lapsed` (absent or null), `words` a non-empty string and `since` an int that is not a bool, as `{"words", "since", "bound"}`, `bound` an int or None; else None. Its docstring names it.

Cases, a new `TestABasePlacesHold` in `tests/py/test_runner.py`, reading the fixtures as `TestABasePlacesStatus` reads flume-0.17.0's:
- `test_a_hold_on_the_waiting_move_is_read_with_its_words_since_and_bound`: `bolt-held` gives `waiting` `unsubmitted` and that hold.
- `test_a_lapsed_hold_is_no_hold`: `bolt-held-lapsed` gives `waiting_hold` None and `stalled` True.
- `test_a_hold_of_another_move_or_missing_its_words_is_none`: a stage's or the submission's hold, and a waiting hold with no words or a string `since`, each built in the test from `bolt-held`, give None.

**1.4** `plugin/lib/runner.py`:
- `HOLD_BOUND = 604800` and `HOLD_ENDED = "crew ends its hold: the bolt waits on nothing of the user's"`, each with a comment naming design Decisions 3 and 4.
- `hold_requests(requests, launch)`: the `Act: hold` records whose `Of` is the launch's number, in order.
- `hold_due(launch, words, requests, reads, now)` as Decision 3 has it, returning `("hold", words)`, `("end", HOLD_ENDED)` or None. `now` is an int of seconds since the epoch. It reads the runner's answers by `taken(reads, n)` as `landing_outcome` does, the landing by `landing_outcome(launch, lands_of(requests, launch), reads)`, and the base place by `base_facts(launch, reads)`.

Cases, a new `tests/py/test_waiting_holds.py`, its module docstring naming bolt-teams' requirements "A started bolt waiting on the user is held under words naming what for", "A waiting bolt's hold is posted once for its words, and again as its bound nears" and "A wait that ends ends crew's hold". Its runners' reads are built as `tests/py/test_runner.py`'s `TestLandingOf` builds them, carrying the 0.26.0 fixtures. Class `TestHoldDue`:
- `test_a_base_place_waiting_under_no_hold_is_due_the_words`
- `test_the_same_words_standing_with_more_than_half_their_bound_left_are_due_nothing`
- `test_the_same_words_past_half_their_bound_are_due_again`
- `test_a_lapsed_hold_is_due_the_words_again`
- `test_new_words_replace_the_standing_ones`
- `test_a_hold_the_runner_has_not_answered_holds_back_any_other`
- `test_a_land_asked_or_submitted_is_due_no_hold`
- `test_a_base_place_waiting_on_no_move_is_due_no_hold`
- `test_crews_standing_words_with_no_wait_are_due_an_end`
- `test_after_an_end_nothing_more_is_due`
- `test_a_hold_crew_never_posted_is_left`
- `test_no_launch_or_an_unread_runner_is_due_nothing`

**1.5** No code changes: `asks.waiting` already reads a base place `unsubmitted` under no hold and not stalled as no wait. Cases in `tests/py/test_asks.py`'s `TestWaitsOn`, reading the 0.26.0 fixtures as places the runner carried for a launch whose `Recipient` is `swancloud/ops`:
- `test_a_base_place_held_under_crews_words_waits_on_no_role`: `bolt-held` gives `waits_on("swancloud/ops", …)` nothing.
- `test_a_base_place_stalled_after_its_hold_lapsed_waits_on_ops`: `bolt-held-lapsed` gives one wait.

**2.1** `plugin/lib/plan.py` `user_wait(f)` as Decision 2 has it, `f` a dict with `can`, `how`, `stays`, `left`, `stop`, `hold`, `batches` and `known` (True, or the why crew can't tell). Cases in `tests/py/test_waiting_holds.py`, class `TestUserWait`:
- `test_a_bolt_marked_to_stay_waits_on_the_send`
- `test_a_left_bolt_and_a_stopped_one_wait_on_the_send_saying_why`
- `test_a_bolt_marked_to_stay_under_a_hold_waits_on_both`
- `test_a_bolt_due_a_land_on_proof_under_a_hold_waits_on_its_lift`
- `test_a_bolt_kept_only_by_unanswered_batches_waits_on_them`
- `test_a_bolt_landing_on_proof_or_waiting_on_crew_waits_on_nothing_of_the_users`
- `test_a_fact_crew_cant_read_is_unknown`

**2.2** `plan.wait_words(label, kit, wait, head)` as Decision 2 has it. Cases, class `TestWaitWords`, each asserting the words bolt-teams' scenarios give, word for word:
- `test_the_send_words_say_why`
- `test_the_hold_words_name_the_hold_and_its_why`
- `test_the_batch_words_name_each_batch_and_its_card`
- `test_a_send_or_batch_under_a_hold_names_the_hold_after`
- `test_no_words_for_none_or_unknown`

**2.3** `plan.rail_rows`: each bolt of a land row carries `wait`, `user_wait` of its facts:
- `batches` is `unread` where its verification is `green`, `outside` is empty, and no later branch replaced `lands`; else `[]`;
- `known` is False with the why where its verification is `unknown`, `due` is None for a drive whose plan was read (`can't be told`), or its landing reads `unknown`;
- the row's `bolts` list gains `"wait"` beside `bolt`, `host`, `can`, `head` and `stays`.

Cases in `tests/py/test_rail.py`'s `TestRows`:
- `test_each_land_row_bolt_carries_what_it_waits_on`: a bolt marked to stay that can land, one kept by batch 5 alone, one under a hold, and one whose verification is not green, built as that class's other land-row cases are.
- `test_a_land_row_bolt_whose_verification_cant_be_read_waits_on_what_crew_cant_tell`.

Existing cases that compare a land row's `bolts` whole take the new key.

**2.4** `plugin/lib/plan.py`:
- `holds_change(w, label, due, requests)` and `holds_post(fleet, label, owner, due, requests)`, as Decisions 5 and 6 have them, mirroring `lands_change` and `lands_post`.
- `CardActs.post_holds(label, owner, due, requests)`.
- The write's subject is `plan(<label>): hold <bolts> while waiting on the user`, or `plan(<label>): end crew's hold of <bolts>` where every item is an end, or both joined by `; ` where both are.
- `plugin/lib/record.py`'s notes on `Request` and `Form` name `bolt.hold` and its forms.

Cases in `tests/py/test_waiting_holds.py`, class `TestHoldsWrite`, applying the change to a tip as `tests/py/test_landings.py`'s `-k writes_tip` cases do:
- `test_two_holds_are_one_write_in_ops_name_each_with_its_entry`: two items give requests `hold` with `Of`, `Words` and `Bound`, and two `bolt.hold` entries with `Request`, `Head` and `Form`, no words, the first the write's own act.
- `test_an_end_is_a_hold_of_bound_zero_recorded_as_an_end`.
- `test_a_land_or_hold_appended_since_the_read_posts_nothing_for_its_bolt`.
- `test_a_hold_on_the_kit_put_or_lifted_since_the_read_posts_nothing_for_its_bolts`.
- `test_a_bolt_gone_from_the_plan_or_whose_mark_changed_is_skipped`.
- `test_nothing_left_writes_nothing`.

**2.5** `plugin/lib/plan.py`:
- `sweep_waits(fleet, read, acts=None)` as Decision 5 has it. It returns `{"held": [{label, bolt, request, form}], "unheld": [{label, why}]}`, `unheld` naming a write refused.
- `rail_read` sets `read["waits"] = sweep_waits(fleet, read)` right after `read["moved"]`.
- The rail's text (`rail_text`, beside the landings cards' sections) gives Decision 5's section, and `holds not asked:` with each `unheld`.
- `SweepActs` gains nothing new beyond `CardActs.post_holds` and its `now`.

Cases in `tests/py/test_waiting_holds.py`, class `TestSweepWaits`, with a read built as `tests/py/test_landings.py`'s `proof_read` builds one, carrying the 0.26.0 fixtures as its runners' places, and a stand-in acts recording `post_holds`:
- `test_the_main_level_hosts_read_posts_each_hold_due_in_one_write`: `y` and `z` due, one call naming both.
- `test_a_read_on_another_host_posts_none`.
- `test_a_bolt_waiting_on_crew_or_unknown_posts_nothing`.
- `test_a_bolt_no_longer_waiting_under_crews_words_is_ended`.
- `test_a_refused_write_is_said_and_the_read_goes_on`.

And in `tests/py/test_rail.py`'s `TestText`, `test_the_rail_names_each_hold_it_asked`.

**3.1** `plugin/roles/main-ops.md`, after the paragraph on landing on proof: while a proven bolt waits on the user, for their send, their answer to a batch or their lift of a hold, crew holds its base place under words naming what it waits on, so Flume reads it waiting and no stall reaches you for it, and you run nothing for it; a stall of a base place still reaches you when the bolt waits on nothing of the user's.

**3.2**
- `README.md`: the State section's `requests.rec` line names a hold of a bolt's base place, with its words and a bound in seconds; the Landing section, after landing on proof, says the rail's read on the main level's host holds a waiting bolt's base place under words naming what it waits on, renews them as their seven-day bound nears, changes them as the wait changes, ends them when it waits on nothing of the user's, records each as `bolt.hold`, and that a land ends it.
- `plugin/skills/crew/SKILL.md`'s `crew rail` row says the same in a clause.
- `plugin/bin/crew`'s usage line for `crew rail` says the read holds a bolt waiting on the user under words.
