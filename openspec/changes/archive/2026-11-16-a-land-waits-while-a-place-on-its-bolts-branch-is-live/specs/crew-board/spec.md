## ADDED Requirements

### Requirement: A ledger says its landing waits on the places on its branch
While a bolt's land waits on the places on its branch (bolt-teams), the Construction lane SHALL say on its ledger that its landing at that head waits on those places, each named by its folder, nothing of the bolt's, and that crew asks the runner to land it once none is live.

#### Scenario: A landing that waits
- **WHEN** the runner answered `doctor-rows`'s land at `4e8d2c1` refused, Flume's status naming `fix--doctor-rows-1` on `bolt/doctor-rows`
- **THEN** `doctor-rows`'s head line, on the lane and in the planner's band, says its landing at `4e8d2c1` waits on `fix--doctor-rows-1` on its branch, nothing of the bolt's, and that crew asks the runner to land it once none is live

## MODIFIED Requirements

### Requirement: A ledger says its landing was refused or stopped at its head
The Construction lane SHALL show a bolt's landing on its ledger as the runner's report gives it, each state its own (record 0056 point 4): once Flume has refused it at its head, in Flume's words, that its landing was refused and the bolt is open for work, for a failed check, or that it takes main first, for a conflict; once the runner has refused its land or Flume reports its submission withdrawn or refused, that its landing was stopped at that head, in their words.

#### Scenario: A landing rejected
- **WHEN** the runner's report carries Flume's verdict on `doctor-rows`'s submission at its present head failed, waiting on its caller, its words naming `tests:logic`
- **THEN** `doctor-rows`'s head line, on the lane and in the planner's band, says its landing was refused at that head and the bolt is open for work, with Flume's words

#### Scenario: A landing refused in conflict
- **WHEN** the runner's report carries Flume's verdict on `doctor-rows`'s submission at its present head a conflict with main on `README.md`
- **THEN** `doctor-rows`'s head line says its landing was refused in conflict, with Flume's words, and that it takes main first

#### Scenario: A landing stopped
- **WHEN** the runner answered `doctor-rows`'s land refused, Flume naming no place on `bolt/doctor-rows`
- **THEN** `doctor-rows`'s head line says its landing was stopped at that head, in the runner's words
