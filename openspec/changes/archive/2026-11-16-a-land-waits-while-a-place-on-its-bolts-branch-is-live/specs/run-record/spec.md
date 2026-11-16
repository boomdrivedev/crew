## ADDED Requirements

### Requirement: A land that waits on its branch is one entry marked waiting
A land the runner answered refused while Flume's status of the bolt's base place named a place on its branch SHALL be recorded once, by the first read of it, as one `bolt.submit` on `bolt/<bolt>` carrying `Outcome: waiting`, the land's number as `Request`, the head it carried as `Head` and Flume's words as `Why`, with no `Refused` and no `Submission`.

#### Scenario: A land that waits
- **WHEN** the runner answered land 57 of `y`, posted at `abc1234`, refused, Flume's status of `y`'s base place naming `fix--y-1` on `bolt/y`
- **THEN** the run record holds one `bolt.submit` on `bolt/y` with `Outcome: waiting`, `Request: 57`, `Head` `abc1234`'s commit and Flume's words as `Why`, and no `Refused` or `Submission`, however often it is read

## MODIFIED Requirements

### Requirement: A landing's Submission is the merge queue's entry Flume names
A `bolt.submit` entry's `Submission` SHALL be only the merge queue's entry that Flume's status of the bolt's base place names, as the runner carries it. The outcome of a land, recorded as bolt-teams "A landing is recorded by the first act that reads it in the runner's report" has it, SHALL carry that entry where Flume names one, and none where it names none. crew SHALL write no `Submission` it made or read from anything but Flume's status.

#### Scenario: A landing whose entry Flume names
- **WHEN** the runner carries `y`'s base place over, landed at `9f1c2ab`, its submission entry 412, and crew records `y`'s land landed
- **THEN** that `bolt.submit` on `bolt/y` carries `Submission: 412`

#### Scenario: A land the runner refused
- **WHEN** the runner answered land 57 of `y` refused, Flume naming no place on `bolt/y` and no submission, and crew records it stopped
- **THEN** that `bolt.submit` on `bolt/y` carries no `Submission`
