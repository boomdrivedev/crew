# Tasks

Submit nothing, and never run `wt submit --help`.

## 1. A restart's wait reads only what its readiness needs

- [x] 1.1 `transcript.Background` follows a session's transcript as it grows. It reads only the whole lines written since its last look, parses only those naming a background task or its end, and finds each task's command once (design Decision 2; Task notes 1.1). Verify `tests/suite logic` ends with "0 failed".
- [x] 1.2 `hold.own_work` reads each session's background work through one follower kept for the process, and `plan.background`, `transcript.pending`, `last_at` and `started_commands` are gone (design Decisions 2 and 4; Task notes 1.2). Verify `tests/suite logic` ends with "0 failed".
- [x] 1.3 `crew.start_of` reads the records newest first, only until one names the agent, and `crew.start_mark` gives what a new start moves (design Decisions 1 and 3; Task notes 1.3). Verify `tests/suite logic` ends with "0 failed".
- [x] 1.4 `crew _renew` judges whether its agent is due at its first look, and again only once its start's mark moves (design Decision 1; Task notes 1.4). Verify `tests/suite logic` ends with "0 failed".
- [ ] 1.5 The tests the change affects pass. Verify `tests/suite --affected` ends with "0 failed".
