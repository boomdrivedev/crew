## MODIFIED Requirements

### Requirement: A landing refused or stopped is an ask of ops
A landing crew's read records refused or stopped SHALL be an ask of a main-level ops that runs as its kind, with Flume's or the runner's words, keyed by the land's request, so an outcome read twice asks once (record 0056 point 4). A land that waits on the places on its bolt's branch SHALL ask ops nothing (bolt-teams).

#### Scenario: A landing that conflicts
- **WHEN** ops runs as its kind, the user's send of bolt `y` was carried to the runner as land request 57, and the runner reports `y`'s base place refused for a conflict with main
- **THEN** crew's read writes one ask of ops naming `bolt/y` with Flume's words, keyed by request 57, however often the outcome is read, and ops's next run takes it

#### Scenario: A land the runner refused
- **WHEN** ops runs as its kind, and the runner answers `y`'s land request 57 refused, Flume naming no place on `bolt/y`
- **THEN** crew's read records `y`'s landing stopped and writes one ask of ops naming `bolt/y` with the runner's words, keyed by request 57

#### Scenario: A land that waits
- **WHEN** ops runs as its kind, and the runner answers `y`'s land request 57 refused while Flume names `fix--y-1` on `bolt/y`
- **THEN** crew's read records `y`'s landing waiting and writes no ask of ops
