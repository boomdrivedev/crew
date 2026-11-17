## ADDED Requirements

### Requirement: A step handed marked before is one the deploy waits on, and the user's alone
A line of `crew ops offer`'s steps file with `before` among its when words SHALL be a step of the user's that the deploy waits on (swancloud record 0038). The offer SHALL be refused, with nothing offered, when such a line's doer is not the user, or when two such lines for one environment share a number. The step SHALL be listed first on the deploy's card, done, once the card is raised, and left out of the after-deploy list.

#### Scenario: A step marked before for an agent
- **WHEN** the deployer hands a step marked `before` whose doer is main-ops
- **THEN** the offer is refused naming the line, a step the deploy waits on being the user's alone, and nothing is offered

#### Scenario: A step the deploy waits on and one after it
- **WHEN** the deployer offers swancloud-srv `bbbbbbb` handing "Move the Archives disk from mac-studio to deneb.", the user's, marked `before`, and "rotate the kanidm admin password", the user's, and the first is done
- **THEN** the deploy's card lists the move first, done, then the notes, then the rotation as the one step after the deploy

### Requirement: A user's step in the words of a step the open offer waits on is recorded as one
`crew ops step` SHALL record a user's step whose words, each run of spaces one, are those of a step the environment's open offer waits on with `before` among its when words. It SHALL say the deploy waits on it. The step SHALL have its own row and card as any user's step, shared with every environment that records it under its key. The deploy's row SHALL name that card.

#### Scenario: The deployer records the step it waits on
- **WHEN** chuck-herdr-alpha's offer of `bbbbbbb` was handed "Move the Archives disk from mac-studio to deneb." marked `before`, and the deployer records step `9c1f0e2a7b3d` waiting with doer user and the text "Move the Archives disk\nfrom mac-studio to deneb."
- **THEN** the run record holds it with `before` among its when words, the command says the deploy of chuck-herdr-alpha waits on it, and its card is raised as any user's step's

### Requirement: One answer settles a step on every environment its card names
`crew ops settle <op/env/n> --state done|declined` SHALL record the state on each step the card's last post or change named that still waits, each under its environment, deploy and key, noting the card. With no post, it SHALL use the steps the row carries. It SHALL close the card once, then raise each environment's next step card and the deploy card each step released. It SHALL be refused, writing nothing, for a key no step row or card holds.

#### Scenario: The user answers the Archives disk's card done
- **WHEN** the user answered `op/mac-studio/7` done, its post naming the step on mac-studio, macbook-pro, deneb and chuck-herdr-alpha, and main-level ops runs `crew ops settle op/mac-studio/7 --state done --label afterthought`
- **THEN** step `9c1f0e2a7b3d` is recorded done on each of the four, under each one's deploy and the key, `crew ops steps deneb --json` gives it done, the card closes "Done.", and `deploy/chuck-herdr-alpha` is raised as the hold-to-approve

#### Scenario: The user skips it
- **WHEN** main-level ops runs `crew ops settle op/mac-studio/7 --state declined --label afterthought` on the user's skip
- **THEN** the step is recorded declined on each of the four, the card closes "Skipped.", and no deploy card is raised for chuck-herdr-alpha

#### Scenario: A key no step holds
- **WHEN** main-level ops runs `crew ops settle op/deneb/99 --state done --label afterthought` and no row or card holds `op/deneb/99`
- **THEN** it is refused, naming the key, and nothing is recorded

## MODIFIED Requirements

### Requirement: The user's word holds the deploy's card, and the deploy's end closes it
The user's word SHALL be holding the deploy's card, recorded with `crew ops approve`, which takes no ticked steps and SHALL be refused, recorded refused, while a step of the user's the deploy waits on is open, naming each step and its card. `crew ops record --act end` SHALL close the card with the deploy's outcome when that end spends the user's word, naming the deploy and the commit the user approved when the deploy is a newer one.

#### Scenario: A deploy offered and approved
- **WHEN** the deployer offers mac-studio a deploy of main's head and the user holds its card
- **THEN** main-level ops runs `crew ops approve`, the row leaves the rail, `crew ops word mac-studio` prints the commit until the deploy's end is recorded, and `crew ops record mac-studio --act end` closes the card with each step's outcome

#### Scenario: An approval for another commit
- **WHEN** `crew ops approve` names a commit other than the open offer's
- **THEN** it is refused, recorded as refused, and no word is given

#### Scenario: An approval while a step it waits on is open
- **WHEN** chuck-herdr-alpha's offer of `bbbbbbb` waits on step `9c1f0e2a7b3d`, open on `op/mac-studio/7`, and `crew ops approve chuck-herdr-alpha --to bbbbbbb` is run
- **THEN** it is refused naming the step's words and `op/mac-studio/7`, the refusal is recorded, and no word is given

#### Scenario: Ticks given
- **WHEN** `crew ops approve chuck-herdr-alpha --to bbbbbbb --ticked 1` is run
- **THEN** it is refused as an argument `crew ops approve` does not take, and nothing is recorded

### Requirement: A step the user is to take, or held for their word, has a card until it is marked
`crew ops step` SHALL raise a step's card when the step's doer is the user or it is held for the user's word, one card for the user's steps under one key on several environments. It SHALL change the card when the step is recorded again while it is open with other words, doer or hold, or comes to or leaves an environment, printing the line that adopts it. It SHALL close the card when no step it names still waits.

#### Scenario: An operation the user is to take
- **WHEN** the deployer records a step whose doer is the user as waiting, after a deploy or on its own
- **THEN** the rail shows it under operations with its `do` card until it is recorded done or declined, and `crew ops steps` gives its latest state

#### Scenario: A held step
- **WHEN** the deployer records a step whose doer is main-ops and marked held, after mac-studio's deploy
- **THEN** the rail shows it under operations with a card asking now, when quiet or skip, and the step runs when the user answers

#### Scenario: A second host records the user's step
- **WHEN** `op/mac-studio/7` is open for step `9c1f0e2a7b3d` on mac-studio, and deneb's deployer records the step waiting under the same key
- **THEN** no second card is posted, `op/mac-studio/7` is changed in place to name both hosts, and the command prints its id and the line that adopts it
