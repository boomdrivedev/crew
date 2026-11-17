## ADDED Requirements

### Requirement: No land is posted for work that has landed or been dropped
crew SHALL post no land, on a send or on proof, for a bolt whose base place the runner's report reads landed or dropped, for a bolt crew reads landed on its kit's main, or for a fix of main the runner's report reads landed or dropped, whether or not the plan still holds the bolt.

#### Scenario: Landed as the runner reports it, still in the plan
- **WHEN** the runner carries `y`'s base place over, landed at `9f1c2ab`, the plan still holds `y`, and the user's send on `land/crew` ticked `y`
- **THEN** no land of `y` is posted

#### Scenario: On main before the runner reports it
- **WHEN** GitHub's main holds `y`'s work, the runner reads `y`'s base place live with no land standing, and `y` reads proven and is not marked to stay
- **THEN** the raise posts no land of `y` on proof, nor on a send that ticked it

#### Scenario: A fix of main dropped
- **WHEN** the runner reads `main--red`'s place over, dropped, and the user's send ticked its row
- **THEN** no land of `fix/main/crew/red` is posted
