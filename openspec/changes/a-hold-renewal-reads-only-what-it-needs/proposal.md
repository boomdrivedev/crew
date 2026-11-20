# A hold renewal reads only what it needs

## Why

On deneb, crew 0.67.1's restart of a due agent, `crew _renew`, took about 500 MB and over 20 CPU seconds in the two minutes it waits for the agent to be idle: boomdrive-ops 24 s, boomdrive-planner 22 s, at up to 83% of a core. Both agents ran background work of their own, so neither went ready and each wait ran its 24 looks. At every look, five seconds apart, the wait judged again whether the agent was due, rebuilding its brief and reading the drive's plan for its kits (`crew.due_of`, `launch_now`), and read the agent's whole transcript three times, parsing every line (`plan.background`, `transcript.pending`, `last_at`, `started_commands`). Read on deneb on 2026-11-19 against boomdrive-planner's 65 MB transcript: 1.3 CPU s for the transcript and 0.4 s for the due at each look, at 390 MB resident. A Stop hook hands such a wait at the end of every turn of an agent that stays busy. `hold.py` is unchanged since 0.67.1, so 0.68.0 does not mend it.

## What Changes

- **A restart's wait judges whether its agent is due once, at its first look,** and again only once crew's record of the agent's start moves (`crew.start_mark`: two stats, the records folder and the start's own record). Its other looks build no brief and read nothing of the plan.
- **Each look reads only the agent's readiness:** herdr's reading of it, its question mark, and the lines its transcript gained since the look before. `transcript.Background` follows one session's transcript as it grows. It parses only the lines naming a background task or its end, and finds each task's command once. `hold.own_work` keeps one follower per session for the life of the process, which `crew hold wait`'s looks share.
- **An agent's start is read from the newest records, only until one names it** (`crew.start_of`), never from all of them. deneb holds 4,830, which every due judgment read whole, the Stop hook's at every turn among them.
- `plan.background`, `transcript.pending`, `last_at` and `started_commands` go, since nothing else reads them.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `host-holds-and-updates`: a restart's wait reads only what its readiness needs.

## Impact

- `plugin/lib/hold.py`: `renew`'s loop and `own_work`.
- `plugin/lib/transcript.py`: `Background` in place of `pending`, `last_at` and `started_commands`. It is still standard library alone, since it is piped to hosts (`code.1`).
- `plugin/lib/crew.py`: `start_of` read newest first, `dated_starts`, `start_read` and `start_mark`.
- `plugin/lib/plan.py`: `background` removed.
- `tests/py/test_hold.py`, `tests/py/test_transcript.py`: the logic cases.
- No command's words, usage, view or brief changes (`docs.2`, `code.8`). `docs/architecture/` and `docs/adr/` are not edited (`docs.7`).
