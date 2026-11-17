## ADDED Requirements

### Requirement: Each new unit's choice says what happens to it
A unit or chore a proposal makes new SHALL be offered by what happens to it: into a bolt that is started, or that the proposal starts, "Start <unit> now", or "Start <unit> after the work it needs" when it comes after other units; into a bolt not started, "Add <unit> for later" or "Move <unit> in for later"; into a queue, "Queue <unit> for later". Its consequence SHALL say where it goes and when it is built.

#### Scenario: Into a started bolt
- **WHEN** the proposal adds `e` to bolt `x`, which the plan marks started
- **THEN** `e`'s choice is "Start e now", and its consequence says it joins bolt `x`, which is running, and is built now

#### Scenario: Into a bolt the proposal starts
- **WHEN** the proposal makes bolt `y`, moves `c` from the flume queue into `y`, and starts `y`
- **THEN** `c`'s choice is "Start c now", and its consequence says it moves into bolt `y`, which this change starts, and is built now

#### Scenario: After the work it needs
- **WHEN** the proposal adds `e` to started bolt `x` after `a-first`
- **THEN** `e`'s choice is "Start e after the work it needs", and its consequence says it is built once `a-first` has landed on bolt `x`

#### Scenario: Into a bolt not started
- **WHEN** the proposal adds `e` to bolt `deploys`, which is not started, and moves `m` from bolt `pages` into `deploys`
- **THEN** `e`'s choice is "Add e for later" and `m`'s "Move m in for later", and each consequence says it goes into bolt `deploys`, which has not started, and is built once `deploys` starts

#### Scenario: Into a queue
- **WHEN** the proposal adds `g` to the switchboard-kit queue
- **THEN** `g`'s choice is "Queue g for later", and its consequence says it waits in the switchboard-kit queue until a bolt takes it

### Requirement: Leaving a new unit out says where it stays
Leaving out a unit or chore a proposal makes new SHALL say what happens to it: one the proposal adds is not added to the plan, and one it moves stays where it stood, in its queue or its bolt. A lone unit's second choice SHALL be "Leave <unit> out" for an add or "Leave <unit> out for now" for a move, its consequence saying so. A list's box SHALL say so in its consequence after "Left out,", which is never cut.

#### Scenario: A lone unit moved from a queue
- **WHEN** the proposal makes bolt `y`, moves `c` from the flume queue into `y`, and starts `y`
- **THEN** the card's second choice is "Leave c out for now", and its consequence is "It stays in the flume queue."

#### Scenario: A lone unit added
- **WHEN** the proposal adds `g` to the switchboard-kit queue and nothing else
- **THEN** the card's second choice is "Leave g out", and its consequence is "It is not added to the plan."

#### Scenario: Both outcomes in a list
- **WHEN** the proposal adds `b` to started bolt `x` and moves `m` from bolt `p` into `x`
- **THEN** `b`'s consequence ends "Left out, it is not added to the plan." and `m`'s ends "Left out, it stays in bolt p."

#### Scenario: Names too long for both
- **WHEN** a box's two outcomes run past what a consequence holds
- **THEN** the words of what happens when kept are cut, by whole words, and "Left out," with what follows it is whole

### Requirement: A proposal's card names no control
The words crew writes on a proposal's card, its title, its summary past the planner's case, its choices' labels and consequences, its approval's action and its questions' titles, SHALL say what happens. They SHALL NOT tell the user how to work the card: none of them SHALL hold "pick", "side", "tick", "ticked", "clear", "cleared", "hold" or "send".

#### Scenario: Every form
- **WHEN** crew raises the cards of a hold-to-approve, a lone new unit, one list and lists, with drops, amendments and moves among them
- **THEN** none of crew's words on any of them holds "pick", "side", "tick", "ticked", "clear", "cleared", "hold" or "send"

#### Scenario: A bolt planned to stay
- **WHEN** the planner proposes `bolt new console-pages "Console pages" --repo switchboard-kit --stays`
- **THEN** the card's summary says `console-pages` stays unlanded until the user says to land it, as its text does, and names no send

## MODIFIED Requirements

### Requirement: A card asks only for its new units, in one ticked list
When proposal n makes units or chores new to a bolt or to a kit's queue, its card SHALL ask only those: one `multi` list and nothing else to tap, a box per new unit or chore, ticked, each with its intent as its detail and, as its consequence, what happens to it kept and left out; its intent SHALL be `decide`. Its summary SHALL say each goes ahead as proposed unless the user leaves it out. No approve block SHALL sit inside the card and no question SHALL ask for words.

#### Scenario: One dropped, three new
- **WHEN** crew raises the card for a proposal that drops `a` and adds `b`, `c` and `d`
- **THEN** the card is one list of three boxes, `b`, `c` and `d`, every one ticked, with no box for `a`; its face holds a paragraph for `a`'s drop; its summary says each new unit goes ahead as proposed unless the user leaves it out; and sending it as it stands applies the proposal whole, `a` dropped

#### Scenario: A move alone
- **WHEN** the proposal moves bolt `y` first and changes no unit
- **THEN** the card is a hold-to-approve of risk low

### Requirement: A card of one new unit is the choice of adding it
A proposal of one new unit or chore SHALL be the choice of its going ahead as proposed or being left out, instead of a list, going ahead recommended, since a Pending You list holds two at least. Each of the two SHALL say what happens to the unit if it is picked, and the summary SHALL say nothing of how to pick.

#### Scenario: One new unit
- **WHEN** the proposal adds one unit `c` to the switchboard-kit queue and nothing else
- **THEN** the card is the choice of "Queue c for later" or "Leave c out", "Queue c for later" recommended, and the choice picked applies

#### Scenario: One new unit beside a drop
- **WHEN** the proposal drops `a` and adds `c`
- **THEN** the card is the choice of adding `c` or leaving it out, and `a`'s drop applies whichever is picked

### Requirement: A plain approval applies whole or not at all
Approving a proposal's hold-to-approve SHALL apply it whole; declining it SHALL apply nothing. Its summary SHALL say that approved, all of it applies. The card of a proposal that drops or amends SHALL also say that declined, none of it applies and the user's note tells the planner what to keep.

#### Scenario: Drops alone
- **WHEN** the proposal drops `a`, `b` and `c` and nothing else
- **THEN** the card is a hold-to-approve with no boxes, its face holds a paragraph for each dropped unit with its why, its summary says that approved, all of it applies, and declined, none of it does and the user's note tells the planner what to keep, and approving it drops all three

#### Scenario: Drops with an amendment and an order
- **WHEN** the proposal drops `a`, amends `x` and orders `d` first
- **THEN** the card is a hold-to-approve with no boxes, and approving it applies all three

#### Scenario: Keeping a dropped unit
- **WHEN** the user declines a drops-alone card with the note "keep b", and the planner runs `crew plan answer N plan decline --note "keep b"`
- **THEN** nothing is applied, and crew says the user's note is the planner's to act on, writing the proposal again or dropping it
