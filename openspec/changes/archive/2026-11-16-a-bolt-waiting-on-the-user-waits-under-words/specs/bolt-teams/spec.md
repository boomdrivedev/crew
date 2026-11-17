## ADDED Requirements

### Requirement: A started bolt waiting on the user is held under words naming what for
While a started bolt waits on the user, for their send of its row on its kit's landings card, for their lift of a hold on its kit or drive, or for their answer to the batches that alone keep it from landing, and its base place waits on crew, the rail's read SHALL post a `hold` of its base place's launch whose words name what it waits on and where the user answers it, bounded by seven days (record 0067 as amended 2026-11-14; Flume's clause 130).

#### Scenario: Marked to stay
- **WHEN** bolt `z` of crew, marked to stay, can land at `abc1234`, and its base place, launched by request 41, waits on crew for a retry of its submission under no hold
- **THEN** the rail's read on the main level's host appends a hold of request 41 whose `Words` are `the user, by their send of its row on crew's landings card, land/crew: it is marked to stay` and whose `Bound` is `604800`

#### Scenario: Left by the user
- **WHEN** the user left `y`, not marked to stay, unticked on an earlier send, and `y` can land, its base place waiting on crew under no hold
- **THEN** the hold's words are `the user, by their send of its row on crew's landings card, land/crew: they left it unticked on an earlier send`

#### Scenario: Its land stopped
- **WHEN** crew's land of `y` at `abc1234` was stopped, and its base place waits on crew under no hold
- **THEN** the hold's words are `the user, by their send of its row on crew's landings card, land/crew: its land at abc1234 was stopped`

#### Scenario: Under a hold on its kit
- **WHEN** the user put a hold on crew saying `Cutover`, and `y`, not marked to stay, can land, its base place waiting on crew under no hold
- **THEN** the hold's words are `the user, by lifting the hold on crew's landings ("Cutover") with crew plan go: it then lands on proof`

#### Scenario: Marked to stay under a hold
- **WHEN** `z`, marked to stay, can land while the hold on crew saying `Cutover` stands
- **THEN** the hold's words name the user's send of its row on `land/crew`, then their lift of the hold on crew's landings, `Cutover`, with `crew plan go`

#### Scenario: Waiting on a batch
- **WHEN** `y`'s verification is green, its unit `a`'s latest change is in batch 5, whose card the user has not answered, and nothing else keeps `y` from landing
- **THEN** the hold's words are `the user, by answering review batch 5 on its card, batch/5`

#### Scenario: A change in no batch yet
- **WHEN** `y`'s verification is green and its unit `a`'s latest change has been in no batch
- **THEN** no hold of `y` is posted, since the batch is crew's to make and nothing waits on the user

#### Scenario: Waiting on nothing of the user's
- **WHEN** `y`'s every unit has merged and its verification is not green, its base place waiting on crew under no hold
- **THEN** no hold of `y` is posted, and Flume's stall of its base place reaches whom it reaches today

#### Scenario: A held base place asks no role
- **WHEN** the runner carries Flume's status of `z`'s base place waiting for a retry of its submission under the hold crew posted, not lapsed
- **THEN** it is no place that waits on main-level ops, and once Flume reads it stalled after the hold lapsed, it waits on ops again

### Requirement: A waiting bolt's hold is posted once for its words, and again as its bound nears
The rail's read SHALL post no hold of a launch while a hold of it waits on the runner's answer, while a land of it stands, or while its base place waits on nothing of crew's, and none while the hold standing on its waiting move has the words due and more than half its bound left. It SHALL post those words again once half its bound or more has passed or it lapsed, and new words once the wait changes.

#### Scenario: Read again
- **WHEN** a later rail read finds `z` waiting on the same send, the hold crew posted standing on its base place's waiting move with the same words, posted a day before
- **THEN** it posts no hold

#### Scenario: Past half its bound
- **WHEN** the hold standing on `z`'s base place's waiting move has the words due and was taken four days before
- **THEN** the rail's read posts a hold of `z`'s launch with the same words and a bound of seven days

#### Scenario: Lapsed
- **WHEN** the hold crew posted of `z`'s base place lapsed at its bound, and `z` still waits on the user's send
- **THEN** the rail's read posts its hold again

#### Scenario: Waiting on the runner's answer
- **WHEN** crew posted hold 52 of `z`'s launch and the runner has not answered it
- **THEN** the rail's read posts no hold of `z`'s launch, whatever `z` waits on

#### Scenario: A land standing
- **WHEN** crew's land of `y` is asked or submitted
- **THEN** the rail's read posts no hold of `y`'s launch

#### Scenario: A base place that waits on nothing of crew's
- **WHEN** `z` can land and its base place waits on a fix live on its branch, Flume's status giving it no move waiting on crew
- **THEN** the rail's read posts no hold of `z`'s launch

#### Scenario: The wait changes
- **WHEN** `z`, marked to stay, waits on the user's send under crew's hold, and the user puts a hold on crew saying `Cutover`
- **THEN** the next rail read posts a hold of `z`'s launch whose words name the send and then the hold on crew's landings

### Requirement: A wait that ends ends crew's hold
Where a bolt's base place waits on crew under the words of the hold crew last posted of its launch, and the bolt waits on nothing of the user's, the rail's read SHALL post a hold of its launch with a bound of 0, which Flume lets lapse at once, so the place's stall says something. A land ends the wait by itself, and crew SHALL leave a hold on the waiting move whose words are not its own.

#### Scenario: The bolt no longer waits on the user
- **WHEN** `y` waited on the user's answer to batch 5 under crew's hold, their answer amended unit `a`, and `a`'s new change has merged and been in no batch since, `y`'s base place waiting on crew under that hold
- **THEN** the rail's read posts a hold of `y`'s launch with bound 0, recorded as an end, and the next read posts nothing more for it

#### Scenario: What crew can't read
- **WHEN** `y`'s base place waits on crew under crew's hold and `y`'s verification can't be read
- **THEN** the rail's read posts nothing of `y`'s launch, neither words nor an end

#### Scenario: Landed on proof
- **WHEN** the hold on crew is lifted and the raise posts `y`'s land on proof
- **THEN** no hold of `y`'s launch is posted, the land ending the wait

#### Scenario: A hold not crew's
- **WHEN** `y` waits on nothing of the user's and the hold standing on its base place's waiting move has words crew never posted of its launch
- **THEN** crew posts nothing of `y`'s launch

### Requirement: The rail's read posts the holds due by one plan write in ops's name
On the main level's host, each rail read SHALL post every hold due, after the landings cards it raised, by one plan write in main-level ops's name, re-checked at the tip it is applied to: a hold or land of the launch appended since the read, or a hold on its kit or drive put, changed or lifted since, posts nothing for that bolt. The rail's text SHALL name each hold posted, and a read on any other host SHALL post none.

#### Scenario: A land posted in the same read
- **WHEN** the rail read's raise of `land/crew` posts `z`'s land on the user's send, the read having found `z` waiting on that send
- **THEN** the holds' write, applied to a tip holding the land, posts no hold of `z`'s launch

#### Scenario: A hold put between the read and the write
- **WHEN** the user puts a hold on crew after the read found `y` waiting on its send and before the holds' write
- **THEN** the write posts nothing for `y`, and the next read posts the words that name the hold

#### Scenario: Two bolts at once
- **WHEN** one rail read finds `y` and `z` of crew each due a hold
- **THEN** one plan write in `swancloud-ops`'s name appends both holds, and the rail's text names each with its request

#### Scenario: Another host's read
- **WHEN** the rail is read on a host that is not the drive's main level's
- **THEN** it posts no hold
