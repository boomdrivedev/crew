## ADDED Requirements

### Requirement: A bolt whose land waits on its branch says so
While Flume names a place on the branch of a bolt that can land, its line on its kit's row under land SHALL say, after how it lands, that no land of it is asked while those places are live, each named by its folder, or, where its last land waits on them, that that land waits, nothing of the bolt's, crew asking the runner to land it once none is live.

#### Scenario: Its land on proof waits
- **WHEN** crew posted `b`'s land on proof at `4e8d2c1` as request 57, and the runner answered it refused while Flume names `fix--b-1` on `bolt/b`
- **THEN** `b`'s line says it lands on proof, and that its landing at `4e8d2c1` waits on `fix--b-1` on its branch, nothing of the bolt's, crew asking the runner to land it once none is live

#### Scenario: No land posted yet
- **WHEN** `b`, not marked to stay, reads proven, no land of it stands, and Flume names `fix--b-notes` on `bolt/b`
- **THEN** `b`'s line says it lands on proof, and that no land of it is asked while `fix--b-notes` is live on `bolt/b`, crew asking the runner once none is

## MODIFIED Requirements

### Requirement: A bolt that can land says how it lands
Once a bolt can land, its line on its kit's row under land SHALL say how it lands: on proof, with its land and request once posted; on the user's send of `land/<kit>`'s card, for a bolt marked to stay, left by the user, or whose last land at its head was stopped, saying which and, for a stop, what stopped it in the runner's or Flume's words; or once the hold on its drive or kit is lifted, naming the hold and its words. It SHALL carry no command for main-level ops.

#### Scenario: The last unit merges
- **WHEN** the last unit of crew's bolt `b`, not marked to stay, merges into `bolt/b` through sluice, every unit's change has been in a batch the user has answered, and the runner carries that unit's place landed at `bolt/b`'s head
- **THEN** crew's row under land names `b` and `swancloud-ops`, saying `b` lands on proof, crew asking the runner to land it in swancloud-ops's name, and carries no `crew tell`

#### Scenario: Its land posted
- **WHEN** crew posted `b`'s land on proof as request 57, which the runner has not answered
- **THEN** `b`'s line says its land on proof is asked, request 57

#### Scenario: Marked to stay
- **WHEN** crew's bolt `b`, marked to stay, can land
- **THEN** `b`'s line says it stays, and lands on the user's send of `land/crew`

#### Scenario: A stopped landing
- **WHEN** the runner answered `b`'s land on proof at its head refused, Flume naming no place on `bolt/b`
- **THEN** `b`'s line says it can land, that its last landing at that head was stopped, in the runner's words, nothing of the bolt's, and that it lands on the user's send of `land/crew`

#### Scenario: Under a hold
- **WHEN** the user put a hold on the drive swancloud, saying "Cutover", and `b` can land
- **THEN** `b`'s line says the hold on swancloud holds it, "Cutover", and that it lands once the hold is lifted
