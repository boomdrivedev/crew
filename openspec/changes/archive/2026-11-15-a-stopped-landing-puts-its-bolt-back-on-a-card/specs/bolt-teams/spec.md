## MODIFIED Requirements

### Requirement: A landing is recorded by the first act that reads it in the runner's report
The first act on any host to read a bolt whose landing is decided SHALL record it: its kit's card's raise, the follower's sweep, a kit's read, or `crew bolt land` (`plan.21`); `crew bolts`, a view, SHALL write nothing (`state.4`). It SHALL write one `bolt.submit`, decided at its write's tip, with the outcome, the head, Flume's entry as `Submission` where it names one, and a refusal's or stop's words; nothing while it is asked, submitted or unknown.

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
- **WHEN** the runner's branch carries `z`'s land refused, a place on `bolt/z` being live, and no read has recorded it
- **THEN** the next read records `z`'s landing stopped in those words, asks main-level ops, and raises `z`'s kit's landings card; a read inside that card's raise raises none, and a second read records and raises nothing

#### Scenario: A runner that can't be read
- **WHEN** the branch of the runner that took `z`'s launch can't be read
- **THEN** the read records nothing for `z`, and names that runner as one it could not read
