---
status: accepted
date: 2026-11-16
decision-makers: boomdrive-design (the record and every choice in it)
---

# 0069. A bolt keeps its priority until it is moved

Status: accepted, boomdrive-design's.

Deciders: boomdrive-design, on the user's question of 2026-11-16, relayed by boomdrive-ops: what is the root of a reorder producing hundreds of acts, and which of crew, the runner and flume should change so a start or reorder doesn't flood the runner at all.

Sources: `plugin/lib/runner.py` `priority_of`, `priorities` and `main_priority`, and `plugin/lib/plan.py` `reprioritise` and `op_bolt_order`, on crew's main at b097ed4b; `openspec/specs/bolt-teams/spec.md`, "A launch names its repository, intent, recipient, priority and brief" and "A start or a reorder appends each priority it changed"; record 0047 move 5 (the rail's order reaches Flume as each place's priority, set at the launch and changed after); flume record 0010 (Flume starts waiting stages by the caller's priority); afterthought/crew-state `requests.rec` on `boomdrive/main`, requests 1394 on; boomdrivedev/boomdrive c74a864 and 3f7d69b.

## Context and problem statement

A started bolt's places carry its priority, and Flume starts waiting stages highest first. crew numbers each bolt by its place among the plan's started bolts, counted from the bottom: the bottom bolt is 1, the one above it 2, and so on. So any start, even of a bolt at the bottom, adds one to every other started bolt's number, and closing a bolt takes one off every bolt above it. Their order hasn't changed, but every number has, and crew writes a priority for every place whose number changed.

On 2026-11-16 the planner started eleven bolts. 46 places were already launched, and each was renumbered at every start: request 977's place went 4, 5, 6 … 14. That came to 450 priority requests and 22 launches. The runner turns each request into its own `flume priority` command, so it spent most of 89 minutes renumbering places whose order never moved, while launches and landings waited behind it.

## Considered options

1. **A bolt keeps its number until it is moved (chosen).** Numbers are spaced apart. A started or moved bolt takes a number between its neighbours', and no other bolt's number changes.
2. **Flume takes one priority per bolt.** Flume would order waiting stages by a priority set on the intent, which all of a bolt's places share, so a reorder becomes one command per moved bolt. That adds a second ordering key to Flume's queue, beside the stream's and the place's, which every caller of Flume would then have to set. It only saves anything when a large bolt is moved, and the renumbering that floods the runner would still happen.
3. **The runner gathers or drops acts.** The runner already passes on only a launch's newest priority (boomdrive c74a864), and its acts take turns with its launches (3f7d69b). But each start really does change every number, so the runner still has one command to run per place per start. That treats the symptom and leaves crew writing hundreds of needless requests.

## Decision outcome

Option 1.

- **A started bolt keeps its number until it is moved.** Starting a bolt, closing one or dropping one changes no other bolt's number, so it adds no priority request. A new bolt's launches carry its number from the start.
- **A move re-sets only the bolt that moved.** Moving a bolt in the plan's order adds a priority request for each of that bolt's places and none for any other bolt.
- **Numbers leave room.** A bolt started or moved between two others takes a number between theirs, one above the top or below the bottom takes one past it, and the numbers are spaced widely enough that this rarely runs out. Only when two neighbours have no number left between them are all the started bolts numbered afresh, each re-set once.
- **The highest goes first, as before.** The order Flume sees is the plan's order, and a fix of main still goes above every bolt.
- **Flume and the runner are unchanged.** Flume keeps one priority per place (record 0047 move 5; flume record 0010), and the runner carries each request as it does now.

### Consequences

- A start costs the runner its launches and nothing else. A reorder costs one command for each place of the bolt that moved.
- The number a bolt carries no longer says how many bolts sit below it. Only the order between numbers means anything.
