## MODIFIED Requirements

### Requirement: Every request for a host's runner is a record of the drive's requests file
crew SHALL write every request for a host's runner as a record of `requests.rec` on the drive's branch: a launch of a place, or a retry, drop, priority, land or hold of one it launched, or a confirm, for a role's address, of ends of a place it launched, or a preview of a branch at a revision on the host where the work it serves runs, brought up or, marked done, put away.

#### Scenario: A land is a request
- **WHEN** `requests.rec` holds requests 1 to 7, request 1 the launch of `bolt/x`, and the user's send of `x`'s row is carried to the runner
- **THEN** request 8 is a land of request 1, and requests 1 to 7 are as they were

#### Scenario: A preview and its done
- **WHEN** `requests.rec` holds requests 1 to 7, a preview is asked from a card, and later the user is done with it
- **THEN** the preview is request 8 and its done request 9, each in a commit of its own, and requests 1 to 8 are as they were when 9 is written

#### Scenario: A confirm in a turn's end
- **WHEN** `requests.rec` holds requests 1 to 7, request 3 a launch of unit `a`, and the planner's run ends a turn that took two ends of `a`'s place
- **THEN** request 8 is a confirm of request 3 for `madswan/planner` with two `Delivery` lines, in the commit that ends the turn, and it passes `recfix --check`

#### Scenario: A hold is a request
- **WHEN** `requests.rec` holds requests 1 to 7, request 1 the launch of `bolt/x`, and the rail's read finds `x` waiting on the user's send
- **THEN** request 8 is a hold of request 1 with its `Words` and a `Bound` of `604800`, naming no `Host`, it passes `recfix --check`, and requests 1 to 7 are as they were

## ADDED Requirements

### Requirement: A hold names a bolt's launch, its words and a bound
A hold SHALL name the launch of a bolt's base place it acts on, its words and its bound in whole seconds, and no host and nothing else, for the runner that holds the launch to carry as Flume's hold of the move that place waits on (Boomdrive's core.59). crew's rules SHALL refuse a hold of any other launch, one with no words, and one whose bound is no whole number of seconds.

#### Scenario: A hold of a unit's launch
- **WHEN** a hold would name request 4, the launch of unit `a` on `bolt/x`
- **THEN** the write is refused naming request 4, since a hold names a bolt's launch

#### Scenario: A hold with no words or no whole bound
- **WHEN** a hold of request 1 would name no `Words`, or a `Bound` of `8h`
- **THEN** the write is refused by crew's rules, naming what the hold lacks, and the branch is unchanged

#### Scenario: A hold naming a host
- **WHEN** a hold of request 1 would name a `Host`
- **THEN** the write is refused naming the `Host`, which a hold does not take
