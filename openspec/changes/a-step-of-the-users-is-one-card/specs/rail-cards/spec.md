## ADDED Requirements

### Requirement: A step of the user's is one card however many environments wait on it
The user's steps that wait under one key on several environments SHALL be one rail row and one card, keyed `op/<env>/<n>` for the environment that recorded the step first. The card SHALL name every environment it carries, and its post and each change SHALL record them. It SHALL be the open step card on each. An agent's step held for the user's word, and a gate's step, SHALL stay one environment's.

#### Scenario: One step for four hosts before the Willdan cutover
- **WHEN** afterthought's step `9c1f0e2a7b3d`, the user's, "Move the Archives disk from mac-studio to deneb.", is recorded waiting on mac-studio first, then on macbook-pro and deneb, and on chuck-herdr-alpha marked `before` under its open offer
- **THEN** one card is posted, keyed `op/mac-studio/7`, its post recording the four environments' steps, the rail shows one row for it, and no card is posted under `op/macbook-pro/8`, `op/deneb/42` or `deploy/chuck-herdr-alpha`

#### Scenario: A held step on two hosts
- **WHEN** main-ops's step "Restart crew's teams.", held for the user's word, is recorded under one key on mac-studio and on deneb
- **THEN** each has its own row and its own card, a choice of when, since when the host is quiet is each host's own

### Requirement: A shared step's card says what the user does and which hosts it releases, in the step's own words
A user's step's card SHALL be titled with a plain sentence: the step's words, cut at whole words, then the hosts. For a step a deploy waits on, it SHALL say "so <hosts> can deploy"; for another, "after <hosts>'s deploy" or "on <hosts>". Its summary SHALL be the step's why as the deployer wrote it, then which hosts it releases and that one answer settles it on each. No words of crew's on it SHALL name a record or a rule.

#### Scenario: The Archives disk's card
- **WHEN** crew raises `op/mac-studio/7` for that step, its why "The job points at deneb, which holds no repository until the disk is there."
- **THEN** its title is "Move the Archives disk from mac-studio to deneb, so mac-studio, macbook-pro, deneb and chuck-herdr-alpha can deploy", its summary opens with that why, then says the step releases those four hosts' deploys and one answer settles it on each, and no line crew adds names a record or a rule

#### Scenario: A step after one host's deploy
- **WHEN** srv's deploy of `c882cff` ends with the user's step "Rotate the kanidm admin password."
- **THEN** its card's title is "Rotate the kanidm admin password, after srv's deploy"

#### Scenario: More hosts than the title holds
- **WHEN** a step's words and the names of the nine hosts waiting on it are longer than a title holds
- **THEN** its title ends "so 9 hosts can deploy", the words before it cut at whole words, and its summary names the nine

### Requirement: A step's card changes as environments come to it or leave it
While a step's card waits on the user, crew SHALL change it in place when another environment records the step, or when one it names records the step done, declined or failed on its own, naming those it carries now. A card left naming none SHALL be closed. A card the user answered SHALL be left as it is. An environment that records the step after the answer SHALL be asked on a new card following the answered one.

#### Scenario: A fifth host records the step while the card waits
- **WHEN** `op/mac-studio/7` waits on the user naming four hosts, and swancloud-srv's deployer records step `9c1f0e2a7b3d` waiting
- **THEN** the card is changed in place, its note saying swancloud-srv waits on it too, and its change records the five environments' steps

#### Scenario: One host's deployer records the step done
- **WHEN** `op/mac-studio/7` waits on the user naming four hosts, and deneb's step `9c1f0e2a7b3d` is recorded done
- **THEN** the card is changed in place naming mac-studio, macbook-pro and chuck-herdr-alpha

#### Scenario: A host records the step after the user answered
- **WHEN** the user answered `op/mac-studio/7` done and main-level ops settled it, and swancloud-srv then records step `9c1f0e2a7b3d` waiting
- **THEN** a new card is posted for swancloud-srv's step following `op/mac-studio/7`, opening with the user's answer there and that swancloud-srv recorded the step since

### Requirement: The rail's read changes a step's card that does not name its environments as they stand
At each rail read on the main level's host, a step's card that waits on the user and does not name the environments its row carries SHALL be changed in place to name them. A step card whose row was folded into another's SHALL be closed, saying which card now asks it, and SHALL NOT be called gone.

#### Scenario: Three cards from before for one step
- **WHEN** `op/mac-studio/7`, `op/macbook-pro/8` and `op/deneb/42` are open from before this change, each for step `9c1f0e2a7b3d`, unanswered and recording no environments
- **THEN** the rail's next read changes `op/mac-studio/7` in place to name the three hosts, and closes `op/macbook-pro/8` and `op/deneb/42` saying the step is asked on `op/mac-studio/7` with the other hosts

### Requirement: A deploy that waits on a step of the user's has no card while the step is open
While a step of the user's that a deploy waits on is open, the deploy SHALL have no card, and its rail row SHALL name the step's card, or say its deployer has not recorded the step yet. The rail's sweep SHALL owe it no card. Once every such step is done, its card SHALL be the hold-to-approve, following the step's card. A card a deploy left unanswered SHALL be withdrawn when such a step opens, naming the step's card.

#### Scenario: chuck-herdr-alpha's deploy waits on the step
- **WHEN** chuck-herdr-alpha's offer of `bbbbbbb` waits on step `9c1f0e2a7b3d`, open on `op/mac-studio/7`
- **THEN** no card is posted under `deploy/chuck-herdr-alpha`, its row says it waits on the user's step on `op/mac-studio/7` and its card is raised once that is done, and the rail's sweep posts none for it

#### Scenario: The step done
- **WHEN** main-level ops settles `op/mac-studio/7` done
- **THEN** `deploy/chuck-herdr-alpha` is posted as the hold-to-approve of risk high, following `op/mac-studio/7`, its face listing the step done, with no box

#### Scenario: A newer offer brings a step while the deploy's card waits
- **WHEN** `deploy/srv`'s card waits unanswered on the offer of `abc1234`, and the deployer offers `def5678`, handing a step of the user's marked `before`, and records it waiting
- **THEN** the card is withdrawn, saying the deploy now waits on a step of the user's, no deploy card is open, and the step's card is raised as `op/srv/<n>`

#### Scenario: A deploy card of boxes from before this change
- **WHEN** `deploy/srv`'s card was posted as boxes with the form `boxes`, unanswered, and its step is open
- **THEN** it is withdrawn, naming the step's card; were the step done, it would be followed by the hold-to-approve

## MODIFIED Requirements

### Requirement: A deploy's steps for the user are carded one at a time
When steps for a card wait on an environment, crew SHALL raise one card at a time there: the first following the deploy's card, each next one following the one before, raised when crew closes it. A card naming several environments SHALL be the open step card on each. The next card SHALL be the earliest-recorded step whose environments have none open. A step recorded again while its own card is open changes that card.

#### Scenario: Two steps after one deploy
- **WHEN** srv's deploy ends with a step that is the user's and a step held for the user's word
- **THEN** one card is open, following the deploy's card, and the second is raised following the first when the first is closed

#### Scenario: A shared step's card holds a host's own step back
- **WHEN** `op/mac-studio/7` is open naming mac-studio and deneb, and deneb's deploy ends with a step of the user's of its own
- **THEN** deneb's step has no card until `op/mac-studio/7` is closed, and is then raised following it

#### Scenario: Two shared steps recorded in opposite orders
- **WHEN** steps a and b, each the user's, are recorded on mac-studio and on deneb, a before b on mac-studio and b before a on deneb, and a's record on mac-studio is the earliest of the four
- **THEN** a's card is raised, naming both hosts, and b's is raised following it once it is closed, neither waiting on the other's host for ever

### Requirement: Each rail row has a card key for its thing, not its version
Each rail row SHALL have one card key for its thing, not its version: `proposal/<n>` for a proposal chain, `n` its first proposal; `batch/<n>`; `land/<bolt>`; `deploy/<env>` for an open offer; `op/<env>/<n>` for a step that waits on the user, of the card that carries it or of its first-recorded environment; `record/<kit>/<number>`. A question's card has no row. There SHALL be no review row and no verify row.

#### Scenario: A bolt proven again on a new head
- **WHEN** bolt `y` was ready to land at head `abc1234`, a note on its landing card named a defect, and a fix landed on the bolt at `def5678` with its verification green
- **THEN** its landing row's key is still `land/y`, and crew raises a new landing card under it, following the one the fix held

#### Scenario: A unit built again
- **WHEN** unit `u` was constructed at head `abc1234`, and construct runs again and commits `def5678`
- **THEN** no review row or key exists for either head; the unit's revised change is due for the drive's next batch, whose card's key is the batch's

#### Scenario: A verify report saved
- **WHEN** unit `u`'s verify saves its report `verify-u-20261013-1200.md`
- **THEN** the rail has no row for it, and a card keyed `verify/u/20261013-1200` belongs to no row

#### Scenario: A proposal replaced
- **WHEN** proposal 4 is replaced by proposal 5
- **THEN** the rail's row for proposal 5 has the key `proposal/4`, and its card is the chain's

#### Scenario: The first host's step leaves a shared step on its own
- **WHEN** `op/mac-studio/7` is open naming mac-studio, macbook-pro and deneb, and mac-studio's step is recorded done on its own
- **THEN** the row keeps the key `op/mac-studio/7`, its card's, now naming macbook-pro and deneb

## REMOVED Requirements

### Requirement: A deploy's card waiting on steps is one list of at most five boxes
**Reason**: Record 0070: a deploy's card holds no boxes. A deploy waiting on an open step of the user's has no card. Once every step it waits on is done, its card is the hold-to-approve.
**Migration**: A deploy card still open as boxes is withdrawn while a step it waits on is open, naming the step's card. Once every step is done, it is followed by the hold-to-approve.

### Requirement: Past four open steps a deploy's fourth box holds the rest
**Reason**: Record 0070: a deploy's card holds no boxes, so no box is shared. Each step is its own card, however many hosts wait on it.
**Migration**: None beyond the boxes card's withdrawal above. `crew ops approve --ticked` is refused as an unknown argument.
