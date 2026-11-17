## MODIFIED Requirements

### Requirement: A launch names its repository, intent, recipient, priority and brief
Each launch of a started bolt's work SHALL name the kit's repository as the plan names it and no host or stream, a runner whose configuration names the repository taking it, in the stream its host's Flume configuration maps the repository to, the intent `<label>/<bolt>`, the recipient `<label>/planner`, its bolt's priority, the plan's first bolt the highest, and its brief, the work's own words as crew's prompts give them.

#### Scenario: Two bolts in order
- **WHEN** `x` and then `y` are started, `x` above `y` in the plan
- **THEN** `x`'s launches carry a higher priority than `y`'s, each names crew's repository and no host or stream, intent `madswan/<bolt>` and recipient `madswan/planner`

#### Scenario: Work added to a started bolt
- **WHEN** started bolt `x`'s requests set its priority at 1000000000000, and unit `c` is added to `x`
- **THEN** `c`'s launch carries priority 1000000000000, and `requests.rec` gains no priority

### Requirement: A start or a reorder appends each priority it changed
A move of a started bolt in the plan's order SHALL append a priority for each of that bolt's places, its base place among them, and none for another bolt's. A start SHALL append none, its launches carrying its priority from the start. A close, a drop or work added SHALL append none. Where crew numbers the started bolts afresh, the write SHALL append a priority once for each place whose priority changed.

#### Scenario: A reorder
- **WHEN** `x`, `y` and `z` are started in that order, at 1000002000000, 1000001000000 and 1000000000000, and `crew bolt order z --before y` runs
- **THEN** `requests.rec` gains a priority at 1000001500000 for each launched place of `z`, its base place among them, and none for `x`'s or `y`'s

#### Scenario: A reorder that changes nothing
- **WHEN** `crew bolt order z --before y` runs again
- **THEN** `requests.rec` gains no priority

#### Scenario: A start below the others
- **WHEN** `x` and `y` are started, `y` at 1000000000000, and `z` below them is started
- **THEN** `z`'s launches carry 999999000000, and `requests.rec` gains no priority for `x`'s or `y`'s places

#### Scenario: A drop and a close
- **WHEN** started bolt `y`, between started `x` and `z`, is dropped, or lands and is closed
- **THEN** `requests.rec` gains no priority for any place of `x` or `z`

#### Scenario: No number left
- **WHEN** `x`, `y` and `z` are started at 3, 2 and 1, numbered before bolts kept their priority, and `crew bolt order z --before y` runs
- **THEN** `x`, `z` and `y` take 1000002000000, 1000001000000 and 1000000000000, and `requests.rec` gains one priority for each of their places that is not finished

## ADDED Requirements

### Requirement: A started bolt keeps its priority until it is moved
A started bolt's priority SHALL be the newest its requests set, changed only when it is moved or numbered afresh. A bolt started or moved SHALL keep its own where it is in order with its started neighbours', else take the whole number halfway between theirs, rounded down, the top's plus 1000000, the bottom's less 1000000, or 1000000000000 alone. Where none is left above 0 and below a fix of main's, every started bolt SHALL be numbered from 1000000000000 up, 1000000 apart.

#### Scenario: The first bolt started
- **WHEN** `x` is started in madswan, and no other bolt of madswan is started
- **THEN** `x`'s launches carry 1000000000000

#### Scenario: Started between two
- **WHEN** `x` at 1000001000000 and `z` at 1000000000000 are started, and `y`, between them in the plan, is started
- **THEN** `y`'s launches carry 1000000500000

#### Scenario: Started above the top
- **WHEN** `y` at 1000000000000 is started, and `x`, above it in the plan, is started
- **THEN** `x`'s launches carry 1000001000000

### Requirement: No priority is sent for work that has finished or been dropped
crew SHALL append no priority for a launch crew dropped, one the runner answered refused, or one whose place the runner's records read merged, landed or dropped, whether or not the plan still holds its bolt. A launch whose place crew can't read SHALL be re-set, since crew takes nothing it can't read as finished.

#### Scenario: A merged unit on a moved bolt
- **WHEN** started bolt `x`'s unit `a` has merged on `bolt/x` as the runner reports it, its unit `b` is in code, and `x` is moved
- **THEN** `requests.rec` gains a priority for `x`'s base place and for `b`, and none for `a`

#### Scenario: A landed bolt the plan still holds
- **WHEN** the runner reports `y`'s base place over, landed, the plan still holds `y`, and crew numbers the started bolts afresh
- **THEN** `requests.rec` gains no priority for any place of `y`

### Requirement: A fix of main goes above every bolt
A fix of main's launch SHALL carry priority 2000000000000, above any a started bolt takes. A fix of main standing, its place not finished, with a priority launched before bolts kept theirs SHALL be re-set to 2000000000000 once, by the next start or move.

#### Scenario: A fix of main launched
- **WHEN** `x` and `y` are started, and ops runs `crew main fix crew red "<the failure's words>"`
- **THEN** the fix's launch carries priority 2000000000000

#### Scenario: A fix of main from before
- **WHEN** a launch of `fix/main/crew/red` at priority 3 stands, its place live, and `crew bolt order y --first` runs
- **THEN** `requests.rec` gains one priority of `fix/main/crew/red` at 2000000000000, and the next move gains none for it
