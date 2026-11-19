# Design

## Context

Read 2026-11-19 on deneb at this branch's base, `5827b6b4` (crew's main), with the host's crew at v0.67.1.

**What a restart's wait did.** `crew _renew <agent>` is handed by crew's Stop hook at the end of a due agent's turn, and by `crew update`. It looks every five seconds for up to `SETTLE`, two minutes, until herdr reads the agent idle, with no question open and no background work of its own but crew's waits (`renew_ready`). At every look it called `crew.due_of`, which reads every start record on the host (`starts`, 4,830 files, 0.56 CPU s) and builds the agent's launch and brief (`launch_now`, reading the drive's plan for its kits through `plan.kits_read`, 0.3 s). It also called `own_work`, which read the session's whole transcript three times, parsing every line as JSON: `plan.background` read `transcript.pending` and `last_at`, and `transcript.started_commands` read it again. On boomdrive-planner's 65 MB transcript that was 1.3 CPU s and 390 MB resident at each look. boomdrive-planner and boomdrive-ops each had background tasks of their own, fourteen never told over in the planner's, so neither went ready, and each wait ran its 24 looks. That is the 22 to 24 CPU seconds and 500 MB measured. The renew log shows the planner handed again at nearly every turn's end.

**What the same reading costs elsewhere in the family.** Flume reads the same two facts of the format for its places: the `own-work` row of its statement (boomdrivedev/blueprints `design/flume/requirements.md`, the agent profile's readings), built in `crates/flume/src/profiles/agent/claude/transcript.rs`'s `background_running` (flume main `ccb715e9`). A Flume start's readings read only what follows the transcript's length at its started ack (179). crew's standing agents are not Flume's runs, so Flume cannot answer for them, and crew keeps its own reading (`roles.5`: a mechanism moves to its tool when that tool runs it on the host). Once a drive runs a role on demand (record 0064), its agent leaves crew's restarts and this reading with it.

**Rules this change relies on:**

- `core.md`: `read.1` (what crew cannot read stays unread, never a guess), `read.2` (a tool's output read only by facts checked against it), `code.1` (standard library alone; `transcript.py` is piped to hosts), `code.7` (`renew_ready` and `renew_exited` stay decisions on plain facts, the reads thin around them), `code.9`.
- `teams.md`: `teams.19`, whose outcome stands: a due agent is restarted once herdr reads it idle with no question open and no background work of its own but crew's waits.
- `signals.md`: `transcript.py` is its area's module, and nothing of `check`, `end` or `received` changes.
- `tests.md`: `tests.4` (the reproducing cases in the logic tier), `tests.11`.
- `docs.md`: `docs.4`, `docs.6`, `docs.7`.

## Goals / Non-Goals

**Goals:**

- A restart's wait of two minutes on a long session costs about a second of CPU and tens of MB, not tens of seconds and hundreds of MB.
- Every outcome stands: when an agent is restarted, ended, left, or said not due.

**Non-Goals:**

- Why boomdrive-planner keeps fourteen tasks never told over, which holds its restart off. That is a separate reading of its own.
- The Stop hook's own judgment at every turn's end, beyond the cheaper start read it shares (Decision 3).

## Decisions

### Decision 1: due judged once, and again when the start's record moves

`renew` calls `crew.due_of` at its first look, then takes `crew.start_mark(started)`: the nanosecond modification times of crew's records folder and of the start's own record. A new session's record moves the first, and a start again in the same session rewrites the second (`hooks/session-start` writes it in place). A later look judges again only when the mark differs. `due_of` reads the start, the installed crew it is handed, the launch and the plan, and none of those can make the agent due or not due within a wait except a new start, which the mark sees. The teams file and the installed crew were already read once per process.

*Not taken:* comparing the session herdr names for the agent's pane with the start's session at each look. herdr's stub names its own sessions, and herdr is not crew's record of a start, so a mismatch would be read as a start that never happened. Also not taken: reading `start_of` at each look, which, even read newest first, stats every record.

### Decision 2: one follower per session, reading only what was appended

`transcript.Background(path)` keeps the byte offset of the last whole line it read, the tasks started (each with the tool_use ids its result names), the tasks told over, and each task's command once found. `look()` reads from the offset to the last complete line. It parses only lines holding `backgroundTaskId` or `task-notification`, which Claude Code writes unescaped, and the parse decides as before. A pending task whose command is unknown is looked up once, by a pass that parses only the lines holding one of its tool_use ids, JSON-encoded. A line holding a mark that is not JSON is never passed: every look answers it unread, as `pending`'s whole read did (`read.1`). A transcript now shorter than the offset is read again from its start. `hold.own_work` keeps one follower per session id in `FOLLOWED`, for the process's life. A session with no transcript yet is looked for again at the next look. Its words for what it cannot read are those `plan.background` gave.

The prefilter rests on a fact of the format, so it was read against the tool as it is now (`read.2`): on deneb on 2026-11-19, `Background(path).look()` gave the same tasks and commands as `pending` with `started_commands` on the forty largest transcripts there, 224 MB down, and a second look gave the same. Its first look at the 224 MB transcript took 0.29 CPU s. Before it, `pending` alone peaked at 1 GB.

*Not taken:* keeping `pending` and parsing every line once per look, which is still 0.6 s and the 390 MB per look; a cache keyed by the file's size and time, which would still parse the whole file whenever it grew, as an agent's transcript does each turn.

### Decision 3: a start read newest first

`crew.start_of(name)` lists the records with their times (`dated_starts`), newest first by (time, name), and reads them only until one names the agent (`start_read`). That is the same record `starts` keeps for it, the newest by (time, name). `starts` still reads them all for the board, which needs every agent's. On deneb this takes `due_of`'s start read from 0.56 s to a few hundredths. It serves the Stop hook's judgment at every turn's end too.

### Decision 4: the whole-file readers go

`plan.background`, `transcript.pending`, `last_at` and `started_commands` had no reader but `own_work`, and `last_at`'s answer was discarded there. They go, and their cases move to `Background`'s.

## Risks / Trade-offs

- [Claude Code escapes a letter or a dash in a later release] → a task's line would go unparsed and the agent read as running nothing of its own, restarted over that work. `Background`'s docstring and `transcript.py`'s module say the fact and where it was read, as for every other fact of the format.
- [A start the mark does not see: a record rewritten within the folder's and the file's timestamp granularity] → the wait restarts an agent a start already brought up on crew as it now is, once. That is an extra resume, the outcome a restart by hand has.

## Migration Plan

None: `crew _renew` and `crew hold wait` run from the crew a host has installed, so a host takes this on its next install. Rollback is reverting the commits.

## After deploy

None: every scenario is a logic case, and the cost was read on deneb's own transcripts before landing.

## Task notes

**1.1** `plugin/lib/transcript.py`: `class Background` with `MARKS`, `look`, `read`, `calls`; `import os`; the module's paragraph on background work names `Background`. Cases in `tests/py/test_transcript.py`: a task pending, a task told over, a missing transcript unread, each look reading only appended whole lines, a mark line that is not JSON staying unread, a transcript written anew. In `tests/py/test_hold.py`'s `TestTranscript`: each task's command, found once, and a task started since found at the next look.

**1.2** `plugin/lib/hold.py`: `FOLLOWED` and `own_work` on `transcript.Background`, with the words `plan.background` gave; `plugin/lib/plan.py`: `background` removed, with `transcript.pending`, `last_at` and `started_commands`. Case: `TestTranscript.test_own_work_follows_each_session_and_says_what_it_cannot_read`.

**1.3** `plugin/lib/crew.py`: `dated_starts`, `start_read`, `start_of` read newest first, `start_mark`; `starts` through the first two. Cases in `TestStarts`: the newest record read only until one names the agent, and the mark moving with a new record or its own rewritten.

**1.4** `plugin/lib/hold.py` `renew`: `due_of` at the first look and again only when `start_mark` moves. Cases in `TestRenew`: a wait on an agent that stays working judges it once over its seven looks; one whose start's record moves judges it again and ends not due.
