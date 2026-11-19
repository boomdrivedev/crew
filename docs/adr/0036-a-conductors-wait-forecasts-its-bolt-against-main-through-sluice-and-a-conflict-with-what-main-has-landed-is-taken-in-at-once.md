---
number: 36
title: A conductor's wait forecasts its bolt against main through sluice, and a conflict with what main has landed is taken in at once
status: accepted
date: 2026-10-20
decision-makers:
- Chuck Swanberg
---

# A conductor's wait forecasts its bolt against main through sluice, and a conflict with what main has landed is taken in at once

Status: accepted by the user on 2026-10-21 in the sluice design session that wrote sluice's early-conflicts change and proposed this record on 2026-10-20 ("yes: mark crew record 0036 accepted, push the blueprints C.5 row, and land crew with wt submit main"); their card req_8d4eaee655104222a6cd asked the same.

Status: accepted by the user on 2026-10-26, on their card (req_f15d7f51dfbc45b0b557, "Approved"). Amended 2026-11-19, below: main is taken into a bolt with no agent, and only a conflict goes to one. Amended 2026-10-24: a bolt the user left takes main in only once they tick it. The user, 2026-10-24, through the operator: "I've noticed that we've been rebuilding the bolt with the about:phone even though it's parked. We keep rebuilding it probably because the main branch is changing" (signal 2026-10-24-swancloud-design-f4cdfd2a/01). Their words settle what is asked: a bolt they parked is rebuilt as main moves; what follows is the design agent's reading of why and what changes, put to them on this record's card. Read 2026-10-24: builds-reach-the-phone (swc-3) has waited to land since 2026-10-23 at the user's word, and its conductor's waits forecast it against main at each move of main and started a take-main fix on each conflict, fix/builds-reach-the-phone/take-main-0306be7 at 01:24Z after `packages/swancloud-doctor/*` changed on main, each fix a slot's work and a sluice run on a loaded host for a bolt nothing lands until they tick it; and crew shows a bolt left unticked on the card that follows only while its head stands (`plan.py` landings_step), so each such fix also made the parked bolt a fresh row, asked again. What changes: a bolt the user left, unticked on their send of the landings card or stopped in their words to ops, is still forecast against main as main moves, its row saying whether it lands clean or would take main first, and no take-main fix is started for it while it is left; when they tick it, a conflict starts the fix then, the row saying it takes main first and their approval standing through it (record 0031 as amended 2026-10-24); and a left bolt stays left on the card that follows, its head moving by no hand of crew's meanwhile. What stays: the forecast on every move of main and on every conductor's wait (`teams.21`), and the fix at once for a bolt not yet asked or ticked, so no bolt is carded as landable while it conflicts. Considered: keep taking main into a left bolt at every move, the churn the user named, a slot and a run each time for work nobody wants yet; stop forecasting a left bolt too, which leaves its row stale and the user ticking a bolt that then surprises them with a fix. The unit `a-waiting-bolt-takes-main-in-when-main-moves`, approved and in code, stands as written for bolts not yet asked or ticked; the left bolt's exception is a crew unit on the yes, `a-left-bolt-takes-main-in-only-when-ticked`.

Deciders: the user, approving the design ("Finding a worktree's conflicts before it is submitted", 2026-10-20); written by that session.
Amends: `plan.8`; adds `teams.21`.
Sources: switchboard-kit's main records on chuck-herdr-alpha, `log.jsonl`'s conflict events of 2026-10-19 to 10-21; sluice's ADR 0039 and its `sluice submit --check --head`; the sluice statement's clauses 64, 65, 47a and its C.5 crew row, amended on blueprints branch `crew-forecast` (eaef7e9), not yet ratified; `plan.py` `reach`, `forecasts_due`; `conductor.md` *Forecasts and settling* and *Fixes*.

## Context and problem statement

Main's records on chuck-herdr-alpha hold twelve conflicts from 2026-10-19 to 10-21. Nine were bolts conflicting with what main had landed since they took it: #183, #215, #216, #246, #267, #281, #288, #292 and #293, each knowable from 7 minutes to 18 hours before main-level ops submitted it, #215 and #216 after twenty more commits each. Each was found only at ops's submission, went back to the team by ops's word, and was settled by a take-main fix in minutes. A tenth, #231, and two design submissions conflicted with a submission queued on main ahead of them, each of which later failed.

On each conductor's wait crew already dry-runs each unmerged unit against the bolt and the units ahead of it (`teams.12`), and the bolts' own queues held no conflict in those days. Nothing forecasts the bolt against main: `plan.8` has a bolt meet main only at its landing, and the bolt has no worktree a forecast could read (record 0032). sluice can now forecast a branch no worktree holds against another branch and everything queued on it, in the order it will form them (ADR 0039).

## Decision outcome

On each conductor's wait, after the units' forecasts, crew runs `sluice submit main --check --head bolt/<bolt> --json` in the kit's main checkout for each bolt the team holds. The wait says what it finds once for the same bolt head, revision of main and submissions queued on main it meets, recorded as a `forecast` on the bolt (`Reached: wait`):

- **A conflict with what main has landed** (sluice names no submission): the conductor starts the take-main fix at once, as when main-ops says a landing conflicts. The wait gives the command and the files, so the conflict is taken in while it is small.
- **A conflict with a submission queued on main**: nothing is taken in, since that submission may yet fail and leave the queue. The next forecast follows main and its queue.
- **A forecast sluice can't give**, as on a host whose sluice has no `--head`: named once for the bolt's head, not on every wait.

`plan.8` is amended to let a bolt meet main before its landing on such a forecast; `teams.21` holds the rest.

## Considered options

- **crew dry-runs the bolt against main with `git merge-tree`**, as it does units against the bolt: it can't see main's queue as sluice orders it, which three of the twelve conflicts were with.
- **sluice forecasts every bolt after each landing and keeps the result**: sluice keeps no forecast and sends sessions no word (its ADRs 0024 and 0039), and does not know which branch a bolt lands on.
- **Take main into each bolt after every landing on main**: fifty-three landings on main in those two days, each a fix through the bolt's gate for every open bolt.
- **Forecast on the conductor's wait through sluice** (chosen): the reader that can act, at the moment it already reads the kit, forming exactly what ops's submission will meet.

## Consequences

- A take-main fix can now come before a bolt is proven, not only after a landing failed; it is the same fix, with the same words, and merges into the bolt like any other.
- Every conductor's wait runs one more sluice command on the team's host, a forecast of one merge behind main's formed combinations and a fetch of the bolt where it is on GitHub.
- Until a host's sluice has `--head`, its conductors are told once per bolt head that it can't forecast, and tell ops as for any forecast crew could not make.

## Amendment, 2026-11-19: main is taken into a bolt with no agent, and only a conflict goes to one

Status: the user's decision of 2026-11-19, in boomdrive-design's pane: taking main into a bolt is the merge queue's work, and an agent is started only when that merge conflicts. boomdrive-design for how, each choice cheap to change.

Deciders: the user, for the decision; boomdrive-design for the rest.

Sources: record 0056, point 1 (crew talks only to the runner, by messages named for what they do); `plan.8`; flume's statement, clauses 111, 112, 117, 203 and 212, and flume record 0056 as amended on 2026-11-19; sluice's `sluice submit <branch> --head <branch>` and its record 0039; Boomdrive's core.1, core.16, core.53 and core.62. The fix `sluice-merges-as-the-boomdrive-app--take-main`, request 2213 on afterthought/crew-state's `boomdrive/main`, an agent's run whose one commit was a clean merge of main.

Since a bolt became a Flume base place (record 0056), Flume forecasts it against main at its settles and launches its fix itself when it conflicts (flume 203). The conductor's forecast above no longer runs. What was left was the take-main fix crew launches when a unit needs work main holds: a place with an agent whose only work, when nothing conflicts, is a merge the merge queue can make itself.

- **crew asks for main, and no agent takes it in.** When a bolt needs main's work, because a unit on it needs work main holds or the planner or the user says so, crew posts one act, `take base`, naming the bolt's launch. Flume submits main's current revision to the bolt's branch through the merge queue, and a merge that passes the bolt's checks lands with no agent (flume 212).
- **Only a conflict or a failure goes to an agent.** Where the merge conflicts, or main with the bolt fails the bolt's checks, Flume launches the bolt's fix, with the merge queue's words and files as its brief, as it does for a conflict its forecast finds (flume 203). crew launches no take-main fix of its own.
- **When is crew's.** Flume takes nothing in on its own. crew asks when a unit needs main's work, and not at every landing on main, for the reason this record gave against taking main in after each one.
- **crew reads the outcome from the runner alone** (record 0056, point 4): landed, refused or a fix launched, as Flume gave it.

### Not taken

- **crew's take-main fix for every take, as before.** It spends an agent's run, and a slot, on a merge with nothing to decide.
- **The runner submitting main to the bolt through sluice itself.** Two tools would then drive one bolt's branch, Flume and the runner, as record 0056 rejected for a landing. The runner would also have to follow the submission's outcome, which Flume already collects at its settles and turns into the bolt's fix.
- **Flume taking main in whenever main moves ahead.** Each landing on main would run every open bolt's checks again, the cost this record gave against it.

### Consequences

- `plan.8` says a bolt takes main in by asking, and that only a conflict or a failure starts a fix.
- A crew unit gives the planner a way to ask for main in a bolt and posts `take base`, and launches no take-main fix.
- A Boomdrive unit carries `take base` as Flume's taking in (core.62), and a Flume unit builds clause 212.
