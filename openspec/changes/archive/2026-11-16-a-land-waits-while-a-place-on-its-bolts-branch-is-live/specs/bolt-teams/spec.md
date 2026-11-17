## ADDED Requirements

### Requirement: No land is posted while Flume names a place on the bolt's branch
crew SHALL post no land of a bolt, on a send or on proof, while Flume's status of its base place, as the runner carries it, names a place on its branch being made or live (`on_branch`; Flume 203), whoever launched it. A send made meanwhile SHALL stand, and its land, or the land due on proof, SHALL be posted by the first raise after Flume names none. A status that gives no `on_branch`, as Flume 0.17.0's does not, names no place.

#### Scenario: A place on the branch at the send
- **WHEN** the user sends `land/crew` ticking `y`, proven at `4e8d2c1`, and Flume's status of `y`'s base place names `fix--y-notes` on `bolt/y`, a place no launch of crew's made
- **THEN** no land of `y` is posted, and the send stands for `y`

#### Scenario: A land due on proof
- **WHEN** `y`, not marked to stay, reads proven and Flume names `fix--y-notes` on `bolt/y`
- **THEN** no land on proof of `y` is posted

#### Scenario: Nothing on the branch any more
- **WHEN** `fix--y-notes` has ended, Flume names no place on `bolt/y`, and `y` still reads proven at `4e8d2c1`
- **THEN** the next raise posts one land of `y` on the user's send

#### Scenario: A status that names no places
- **WHEN** the runner carries Flume 0.17.0's status of `y`'s base place, which gives no `on_branch`, and the user's send ticks `y`
- **THEN** the raise posts one land of `y`

### Requirement: A land refused while a place on its bolt's branch is live waits
When the runner answers a bolt's land refused and Flume's status of its base place names a place on its branch, crew SHALL read the landing waiting on those places, in Flume's words, nothing of the bolt's, and not stopped. The first read SHALL record it once, as run-record has it, and SHALL ask main-level ops nothing, raise no card and hold no work out of the bolt.

#### Scenario: Flume's landing fix launched after the land was posted
- **WHEN** crew posted `y`'s land on the user's send at `4e8d2c1`, Flume then forecast `y` in conflict with main and launched `fix--y-1` on `bolt/y`, and the runner answers the land refused in Flume's words
- **THEN** `y`'s landing reads waiting on `fix--y-1`, and the next read records it waiting in those words, asks ops nothing and raises no card

#### Scenario: Read again
- **WHEN** a later read finds the same land refused and `fix--y-1` still live
- **THEN** it records nothing

#### Scenario: Work joins the bolt meanwhile
- **WHEN** `y`'s land waits on `fix--y-1`, and a fix of `y`'s is started on `bolt/y`
- **THEN** the fix is not refused for a landing in flight, `y`'s landing holding no work

### Requirement: A land that waited is posted again once no place on its branch is live
Once Flume names no place on a bolt's branch, a land of it that waited SHALL bar no land and spend no send: crew SHALL post the bolt's land again, on the send that ticked it while that send stands at the bolt's head now, or on proof, once the bolt reads proven there.

#### Scenario: The landing fix took main in
- **WHEN** `y`'s land on the user's send of `land/crew` at `4e8d2c1` waited on `fix--y-1`, which took main in and landed on `bolt/y`, and `y` reads proven at `5a6b7c8` with its own work unchanged
- **THEN** the next raise posts one land of `y` at `5a6b7c8` on that send, and no card asks for `y` again

#### Scenario: The place ended with the head unmoved
- **WHEN** `y`'s land at `4e8d2c1` on the user's send waited on `fix--y-notes`, which was dropped, and `y` still reads proven at `4e8d2c1`
- **THEN** the next raise posts one land of `y` at `4e8d2c1` on that send

#### Scenario: A land on proof that waited
- **WHEN** crew's land on proof of `y`, not marked to stay, at `4e8d2c1` waited on `fix--y-1`, which landed on `bolt/y`, and `y` reads proven at `5a6b7c8`
- **THEN** the next raise posts one land of `y` on proof at `5a6b7c8`

#### Scenario: Its own work changed
- **WHEN** `y`'s land on the user's send waited on a fix that committed `fix: keep the lease` to `bolt/y`, and `y` reads proven at its new head
- **THEN** no land of `y` is posted on that send, and `y` is a row of the next landings card, its note naming `fix: keep the lease`

## MODIFIED Requirements

### Requirement: A landing's outcome is read from the runner's report
crew SHALL read a started bolt's landing from its launch, the lands of it in `requests.rec`, and Flume's status of its base place as the runner that took the launch carries it, as one outcome: unlaunched, none, asked, submitted, landed, refused for a failed check or a conflict, waiting on its branch, stopped, dropped, or unknown, naming why. Each fact SHALL be guarded (`read.2`). An outcome not landed is read against main ("A bolt whose work is on its kit's main reads landed").

#### Scenario: Unlaunched
- **WHEN** the runner has not answered `z`'s launch, or answered it held or refused
- **THEN** `z`'s landing reads unlaunched, in the runner's words where it gave any

#### Scenario: None
- **WHEN** `z`'s base place is launched and no land of it stands
- **THEN** `z`'s landing reads none

#### Scenario: Asked
- **WHEN** a land of `z`'s launch is posted as request 57 and the runner has not answered it
- **THEN** `z`'s landing reads asked, with request 57

#### Scenario: Under test
- **WHEN** the runner carries Flume 0.17.0's status of `z`'s base place with its submission `#412` under test
- **THEN** `z`'s landing reads submitted, with entry 412 under test

#### Scenario: Landed
- **WHEN** the runner carries `z`'s base place over, landed at `5d1a9e0`
- **THEN** `z`'s landing reads landed, with `5d1a9e0`

#### Scenario: A failed check
- **WHEN** the runner carries `z`'s base place waiting on its caller with the verdict failed and Flume's words
- **THEN** `z`'s landing reads refused, the bolt's, in those words

#### Scenario: A conflict
- **WHEN** the runner carries `z`'s base place with the verdict conflict on `README.md` against main at `4d3d9be`
- **THEN** `z`'s landing reads refused for a conflict, naming `README.md` and `4d3d9be`

#### Scenario: Withdrawn
- **WHEN** the runner carries `z`'s base place waiting on its caller with the verdict withdrawn
- **THEN** `z`'s landing reads stopped, in Flume's words

#### Scenario: A land the runner refused
- **WHEN** the runner answers `z`'s land refused, and Flume's status of `z`'s base place names no place on `bolt/z`
- **THEN** `z`'s landing reads stopped, in the runner's words

#### Scenario: A land refused while a place on the branch is live
- **WHEN** the runner answers `z`'s land refused, and Flume's status of `z`'s base place names `fix--z-1` on `bolt/z`
- **THEN** `z`'s landing reads waiting on `fix--z-1`, in Flume's words

#### Scenario: A land that waited, nothing on the branch now
- **WHEN** the run record holds `z`'s land 57 waiting, the runner's answer to it refused, and Flume's status of `z`'s base place now names no place on `bolt/z`
- **THEN** `z`'s landing reads none

#### Scenario: Dropped
- **WHEN** the runner carries `z`'s base place over, dropped
- **THEN** `z`'s landing reads dropped

#### Scenario: Flume could not read the submission
- **WHEN** the runner carries `z`'s base place with Flume's words that it could not read the submission
- **THEN** `z`'s landing reads unknown, in those words, and is read as no other outcome

#### Scenario: A runner that can't be read
- **WHEN** the branch of the runner that took `z`'s launch can't be read
- **THEN** `z`'s landing reads unknown, naming that runner, and is read as no other outcome

### Requirement: A landing is recorded by the first act that reads it in the runner's report
The first act on any host to read a bolt whose landing is decided SHALL record it: its kit's card's raise, the follower's sweep, a kit's read, or `crew bolt land` (`plan.21`); `crew bolts`, a view, SHALL write nothing (`state.4`). It SHALL write one `bolt.submit`, decided at its write's tip, with the outcome, the head, Flume's entry as `Submission` where it names one, and a refusal's, stop's or wait's words; nothing while it is asked, submitted or unknown.

#### Scenario: Nobody runs anything
- **WHEN** a land of `z` is posted, no agent of the drive runs a command, and the runner's branch then carries `z`'s base place landed at `5d1a9e0`
- **THEN** the next raise of `z`'s kit's landings card records `z`'s `bolt.submit` landed and its `bolt.land` at `5d1a9e0`, and closes `z`

#### Scenario: Two reads at once
- **WHEN** two reads of `z` find its base place landed, and the second's write is applied to a tip that holds the first's
- **THEN** the run record holds one `bolt.submit` outcome and one `bolt.land` for `z`, the second read writing nothing and recording no refused close

#### Scenario: crew bolts reads it
- **WHEN** `crew bolts` runs while the runner's report has `z`'s base place landed and no read has recorded it
- **THEN** `crew bolts` says `z` landed at Flume's commit and writes nothing, and the next raise of its kit's card or the follower's sweep records it

#### Scenario: Still under test
- **WHEN** a read finds `z`'s base place with its submission `#412` under test
- **THEN** nothing is recorded, and `z`'s last `bolt.submit` stays asked

#### Scenario: A conflict recorded by a later read
- **WHEN** the runner's report has `z`'s submission `#412` with the verdict conflict
- **THEN** the next read records `z`'s landing refused at its head in Flume's words, appends its take-main fix, and raises its kit's landings card with `z`'s row saying it takes main first

#### Scenario: A stop recorded by a later read
- **WHEN** the runner's branch carries `z`'s land refused, Flume naming no place on `bolt/z`, and no read has recorded it
- **THEN** the next read records `z`'s landing stopped in the runner's words, asks main-level ops, and raises `z`'s kit's landings card; a read inside that card's raise raises none, and a second read records and raises nothing

#### Scenario: A runner that can't be read
- **WHEN** the branch of the runner that took `z`'s launch can't be read
- **THEN** the read records nothing for `z`, and names that runner as one it could not read

### Requirement: A landing stopped by nothing of the bolt's is recorded stopped, and its send is spent
When the runner answers a bolt's land refused, Flume naming no place on its branch, or Flume's verdict on its submission is withdrawn or refused, crew SHALL record the landing stopped at the bolt's head, in the runner's or Flume's words, with no refusal, and SHALL hold nothing of the bolt for it. The send that ticked the bolt SHALL be spent: a land of it SHALL be posted again only on a new send of the user's. Its row keeps its box, as rail-cards has it.

#### Scenario: A place on the branch is live
- **WHEN** the runner answers `z`'s land refused, Flume's status of `z`'s base place naming `fix--z-1` on `bolt/z`
- **THEN** `z`'s landing is not recorded stopped and its send is not spent: it waits on `fix--z-1`, as "A land refused while a place on its bolt's branch is live waits" has it

#### Scenario: The runner refuses the land
- **WHEN** the runner answers `z`'s land refused, Flume's status of `z`'s base place naming no place on `bolt/z`
- **THEN** the run record's `bolt.submit` for `z` carries no `Refused`, its `Outcome` stopped, its `Why` the runner's words and its `Head`, and `crew bolts` says `z`'s landing stopped in those words

#### Scenario: No land again on the same send
- **WHEN** `z`'s landing is recorded stopped and its kit's landings card is raised again on the send that ticked it
- **THEN** no land of `z` is posted, and once the user sends the card again with `z` ticked, one land of `z` is posted

### Requirement: A base place's drop the runner refused is asked again once nothing on its branch is live
Where the runner answered a bolt's drop refused, as Flume refuses it while a place on the bolt's branch is live, the next plan write that finds the bolt gone from the plan, its launch standing, no piece of it live, no landing fix of its base place live and no place Flume names on its branch SHALL ask the drop again, once for each refusal (`runner.base_drop_due`).

#### Scenario: A refused drop asked again
- **WHEN** the runner answered `x`'s drop refused while `a`'s place was live, and a later plan write finds `x` gone from the plan, its launch standing and no place of its pieces live
- **THEN** that write appends one drop of `x`'s launch, and a write after it, while that drop is unanswered, appends none

#### Scenario: Not while a piece is live
- **WHEN** the runner answered `x`'s drop refused and `a`'s place is still live
- **THEN** no plan write asks the drop again

#### Scenario: Not while a landing fix is live
- **WHEN** the runner answered `x`'s drop refused and `x`'s base place lists its landing fix `x-1` live
- **THEN** no plan write asks the drop again, and the first write after `x-1` has ended appends one

#### Scenario: Not while Flume names a place on the branch
- **WHEN** the runner answered `x`'s drop refused, no piece of `x` is live, and Flume's status of `x`'s base place names `fix--x-notes` on `bolt/x`
- **THEN** no plan write asks the drop again, and the first write after Flume names none appends one
