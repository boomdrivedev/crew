## MODIFIED Requirements

### Requirement: The sweep leaves an answered landings card while a bolt it ticked waits to land
The rail's sweep SHALL NOT close a kit's landings card the user answered while a bolt they ticked on it has neither landed, been dropped nor had the land that send posted stopped, even when the kit's row is gone from the read. It SHALL leave the card, saying it waits on the runner to land what was ticked. The event that ends the send closes it.

#### Scenario: The row is gone for a moment
- **WHEN** the user approved `land/sluice`'s card ticking `a`, `a` has no `bolt.land` or `bolt.drop` since, and the rail's read finds no `land/sluice` row
- **THEN** the sweep leaves the card open and says it waits on the runner to land `a`; nothing is withdrawn

#### Scenario: The ticked bolt landed
- **WHEN** `a` has landed and no other ticked bolt waits, and the read finds no `land/sluice` row
- **THEN** the sweep closes the card as answered, saying `a` landed

#### Scenario: The ticked bolt's land was stopped
- **WHEN** the user approved `land/sluice`'s card ticking `a` and `b`, `a` has landed, the runner stopped the land of `b` that send posted, and the read finds no `land/sluice` row
- **THEN** the sweep closes the card as answered; a stop of a land of `b` posted on proof or on another card's send would have left it waiting on `b`

### Requirement: The rail's read raises a landings card that does not show a row as it stands
On the main level's host, the rail's read SHALL raise each kit's landings card open in main-level ops's name whose land row holds a row that can land, held by no send at its head now, a send a stop spent holding none, that the card shows on no row, at another head, taking main first, or, once answered, with no box or ticked by a send whose land of it was stopped. It SHALL raise none for a card that shows every such row as it stands.

#### Scenario: A bolt proven between a send and its landing
- **WHEN** the user sent `land/crew` ticking `y`, whose land the runner has not answered, main has not moved, and `z` reads proven, on no row of that card
- **THEN** the rail's read raises `land/crew` in the same sweep: the card they sent is closed keeping their send for `y`, and a card following it asks for `z`

#### Scenario: A bolt proven while the card waits
- **WHEN** `land/crew` waits on the user with `y`, main has not moved, and `z` reads proven
- **THEN** the rail's read raises `land/crew` for `z`, and the read after it, the card showing `z` at its head, raises none

#### Scenario: A ticked bolt proven at a new head
- **WHEN** the user ticked `z` at `abc1234`, Flume refused its landing in conflict with main, and `z`'s take-main fix merged, so `z` reads proven at `def5678`, main not having moved since
- **THEN** the rail's read raises `land/crew`, whose raise posts `z`'s land on that send while it stands for `z`'s work

#### Scenario: A ticked bolt whose land on the send was stopped
- **WHEN** the user sent `land/flume` ticking `x`, `y` and `z`, `x` and `y` have landed, and the runner stopped the land of `z` that send posted, `z` still reading proven
- **THEN** the rail's read raises `land/flume` in the same sweep: the card they sent is closed naming what landed and `z`'s stop, in the runner's words, and a card following it asks for `z`

#### Scenario: A bolt the user left beside a send still landing
- **WHEN** the user sent `land/crew` ticking `y` and leaving `z`, `y` has not landed, and `z` stands at the head the card showed
- **THEN** the rail's read raises no landings card

#### Scenario: The rail names the card it raised
- **WHEN** the rail's read raised `land/switchboard-kit` for `apex-zones`
- **THEN** `crew rail` says so under the landings cards raised for rows they did not offer as they stand, naming `apex-zones` and the card, or the raise's refusal in its words

## ADDED Requirements

### Requirement: A stop closes the answered landings card with no read of ops's
The read that records a ticked bolt's landing stopped or refused SHALL raise its kit's landings card, and the rail's read SHALL raise an answered card a stop spent the send of, so the card closes as each bolt it ticked lands, is held or is stopped, with no act of main-level ops's. A stop of a land the send posted SHALL spend that send at that head or any, the bolt's head moved since among them.

#### Scenario: Two landed and one stopped
- **WHEN** the user sent `land/flume` ticking `x`, `y` and `z`, `x` and `y` land, and a read records `z`'s land on that send stopped, nothing of the bolt's
- **THEN** that read raises `land/flume`, which is closed saying `x` and `y` landed and `z` was stopped and in whose words, and a card following it asks for `z`, with no `crew card read` run

#### Scenario: A stopped land whose head moved
- **WHEN** `z`, marked to stay, was ticked on `land/crew`'s send at `abc1234`, the land that send posted was stopped there, a place on `bolt/z` being live, and that place merged, so `z` reads proven at `def5678` with its own work unchanged
- **THEN** no land of `z` is posted on that send, and the next raise closes `land/crew` naming `z`'s stop, its send spent, and posts a card following it that asks for `z` at `def5678`
