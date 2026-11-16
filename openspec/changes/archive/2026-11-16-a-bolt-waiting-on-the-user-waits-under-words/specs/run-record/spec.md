## ADDED Requirements

### Requirement: A hold crew posts is one entry naming its request and what the bolt waits on
Each `hold` crew posts SHALL be recorded as one `bolt.hold` on `bolt/<bolt>` carrying the hold's number in `requests.rec` as `Request`, the bolt's head as `Head`, and as `Form` what it waits on, `send`, `hold` or `batch`, or `end` for a hold that ends crew's own, and none of the hold's words, which may hold the user's (`record.3`).

#### Scenario: A hold of a bolt marked to stay
- **WHEN** the rail's read posts hold 52 of `z`'s launch at `abc1234`, `z` waiting on the user's send
- **THEN** the run record holds a `bolt.hold` on `bolt/z` with `Request: 52`, `Head` `abc1234`'s commit and `Form: send`, and no word of the hold's

#### Scenario: An end
- **WHEN** the rail's read posts hold 60 of `y`'s launch with bound 0, ending crew's hold
- **THEN** the run record holds a `bolt.hold` on `bolt/y` with `Request: 60` and `Form: end`

#### Scenario: Two holds in one write
- **WHEN** one rail read posts holds of `y` and `z`
- **THEN** the run record holds one `bolt.hold` for each, both written by that one plan write
