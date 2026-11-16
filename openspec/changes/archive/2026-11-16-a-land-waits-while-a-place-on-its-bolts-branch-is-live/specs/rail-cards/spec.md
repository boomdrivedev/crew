## ADDED Requirements

### Requirement: A send stands for a bolt whose land waits on its branch, its card left
While a land of a bolt the user's send ticked waits on the places on its branch, or none is posted while Flume names one (bolt-teams), crew SHALL keep the send standing: the card SHALL be left, and SHALL NOT be closed counting the bolt stopped or held. `crew card read land/<kit>` SHALL say of a land that waits that the send stands and lands the bolt once no place on its branch is live.

#### Scenario: Ticked beside two that land
- **WHEN** the user sent `land/flume` ticking `x`, `y` and `z`, `x` and `y` land, and `z`'s land on that send waits on `fix--z-1`
- **THEN** `land/flume` is left as it is, not closed saying `z` was stopped, and the sweep says it waits on the runner to land `z`

#### Scenario: The card's read
- **WHEN** `z`'s land on the user's send of `land/flume`, request 332, waits on `fix--z-1`
- **THEN** `crew card read land/flume` says `z`'s land, request 332, waits on the places on `bolt/z`, nothing of the bolt's, in Flume's words, and that the user's send stands and lands `z` once none is live

#### Scenario: The send carried
- **WHEN** `fix--z-1` takes main in and lands on `bolt/z`, and `z` reads proven at `6c693a0` with its own work unchanged
- **THEN** the next raise posts `z`'s land at `6c693a0` on that send, and once `z` lands, `land/flume` closes saying `x`, `y` and `z` landed

## MODIFIED Requirements

### Requirement: A landings row is due one land for each send and head
A row of a landings card SHALL be due a land when its box was ticked on a send that stands for it at its head now, it can land, and no land of it stands undecided or was posted at that head, but one that waited on its branch or was stopped there on proof or on another send, which bars no send. A send read twice SHALL post once, and one standing through a take-main fix SHALL post again once the bolt is proven at its new head. A write replayed on a tip holding them SHALL write nothing.

#### Scenario: The send read again
- **WHEN** a later raise reads the user's send on `land/crew` with `y` and `z` still at the heads they were ticked at, their lands posted
- **THEN** it posts no land

#### Scenario: A ticked bolt taking main in
- **WHEN** the user ticked `z` at `abc1234`, Flume refused `z`'s landing in conflict with main, and `z`'s take-main fix merged, so `z` reads proven at `def5678` with its own work unchanged
- **THEN** no land of `z` is posted while it takes main in, and the first raise after it reads proven at `def5678` posts one land of `z` on that send

#### Scenario: A stopped row on the same send
- **WHEN** the runner answered `z`'s land on the user's send refused
- **THEN** no raise posts another land of `z` on that send

#### Scenario: A send at the head of a stopped land on proof
- **WHEN** crew's land on proof of `y` at `abc1234` was stopped by the runner, and the user sends `land/crew` ticking `y`, still at `abc1234`
- **THEN** the next raise posts one land of `y` at `abc1234` on that send

#### Scenario: A later card at the head of a stopped land
- **WHEN** `z`'s land on the user's send of one card was stopped at `abc1234`, and they send the card that follows it ticking `z`, still at `abc1234`
- **THEN** the next raise posts one land of `z` at `abc1234` on that later send
- **AND** that later card is left as answered, its send not read as spent, and no card follows it asking for `z` again
- **AND** `crew card read` of it says the earlier card's send is the one spent and the user's send of this card lands `z`

#### Scenario: A write replayed
- **WHEN** the plan write posting `y`'s land is applied again to a tip that already holds that land
- **THEN** it writes nothing

### Requirement: A landing the runner or Flume stopped keeps its box
A bolt whose land the runner answered refused, Flume naming no place on its branch, or whose submission Flume reports withdrawn or refused and waiting on its caller, as the runner's report carries it, SHALL keep its box while its kit's main does not hold its work. Its row SHALL say what stopped its landing at that head, in the runner's or Flume's words, nothing of the bolt's. The send that ticked it SHALL be spent: crew SHALL post no land of it again on that send.

#### Scenario: The runner refuses the land
- **WHEN** the user sent `land/crew` with `z` ticked, crew posted `z`'s land, and the runner answered it refused, Flume naming no place on `bolt/z`
- **THEN** `z` keeps its box, its row says its landing at that head was stopped, in the runner's words, nothing of the bolt's, and no raise posts another land of `z` on that send

#### Scenario: Flume's submission withdrawn
- **WHEN** the runner's report carries `z`'s base place with its submission withdrawn, waiting on its caller
- **THEN** `z` keeps its box, and its row says its landing was stopped, in Flume's words, nothing of the bolt's

#### Scenario: A new card while it is stopped
- **WHEN** `z`'s landing was stopped and a card of crew's landings follows the one the user answered
- **THEN** the closed card's outcome names `z` as stopped, with what stopped it, and the card that follows has `z` as a row with its box, ticked as crew proposes, saying what stopped its last landing

#### Scenario: The head moves
- **WHEN** `z`'s landing was stopped at `abc1234` and `z`'s head moves to a new head that reads proven
- **THEN** `z`'s row says nothing of the stop

#### Scenario: A stopped landing that landed
- **WHEN** `z`'s landing was stopped at `abc1234`, and GitHub's main holds `abc1234` and the commit each of `z`'s units landed at on `bolt/z`
- **THEN** `land/crew` has no row for `z`, and no word of the stop is said on the card

### Requirement: A landings card asks only about the rows a send must land
A kit's landings card SHALL ask only about bolts marked to stay, bolts the user left, bolts whose land on proof at their head was stopped, and fixes of main, each with the rows taking main first beside them as this spec has it. Each requirement of this spec on a landings card's row SHALL hold of those rows alone, and a bolt that lands on proof SHALL be no row of it.

#### Scenario: A bolt not marked beside one marked
- **WHEN** bolts `y` and `z` of crew read proven, `z` marked to stay
- **THEN** `land/crew` is an approve naming `z` alone, and `y` is no row of it

#### Scenario: A land on proof stopped
- **WHEN** crew posted `y`'s land on proof at `abc1234` and the runner answered it refused, Flume naming no place on `bolt/y`
- **THEN** `land/crew` asks for `y` with its box, its row saying its land on proof at `abc1234` was stopped, in the runner's words, nothing of the bolt's, no raise posts another land of `y` at that head, and the user's send lands it, a stop of crew's land on proof spending no send of theirs

#### Scenario: A bolt the user left
- **WHEN** the user left `y`, not marked to stay, on their send of an earlier card, and `y` reads proven
- **THEN** `land/crew` shows `y` unticked, and no land on proof is posted for `y` while it is left

#### Scenario: Taking main first
- **WHEN** `y`, not marked to stay, is forecast to conflict with main, and `z`, marked, can land
- **THEN** `land/crew` asks for `z` alone, and `y` is no row of it

### Requirement: A stop closes the answered landings card with no read of ops's
The read that records a ticked bolt's landing stopped or refused SHALL raise its kit's landings card, and the rail's read SHALL raise an answered card a stop spent the send of, so the card closes as each bolt it ticked lands, is held or is stopped, with no act of main-level ops's. A stop of a land the send posted SHALL spend that send at that head or any, the bolt's head moved since among them.

#### Scenario: Two landed and one stopped
- **WHEN** the user sent `land/flume` ticking `x`, `y` and `z`, `x` and `y` land, and a read records `z`'s land on that send stopped, nothing of the bolt's
- **THEN** that read raises `land/flume`, which is closed saying `x` and `y` landed and `z` was stopped and in whose words, and a card following it asks for `z`, with no `crew card read` run

#### Scenario: A stopped land whose head moved
- **WHEN** `z`, marked to stay, was ticked on `land/crew`'s send at `abc1234`, the land that send posted was stopped there, Flume naming no place on `bolt/z`, and a take-main fix later merged into `bolt/z`, so `z` reads proven at `def5678` with its own work unchanged
- **THEN** no land of `z` is posted on that send, and the next raise closes `land/crew` naming `z`'s stop, its send spent, and posts a card following it that asks for `z` at `def5678`
