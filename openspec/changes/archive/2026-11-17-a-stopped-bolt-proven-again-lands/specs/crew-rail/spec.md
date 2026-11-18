## MODIFIED Requirements

### Requirement: Each bolt's land line says whether its card carries, holds or follows it
Each bolt line on a kit's land row SHALL end what it waits on with how the kit's card stands for it: carried, when the open card waiting on the user shows it as a row; held, when the user's send, on the open card or kept on a closed one, stands for it at its head now and no land of it that send posted was stopped; or following, when it can land and neither holds. A bolt that can't land and is no row of the card SHALL say nothing of the card.

#### Scenario: A bolt the open card carries
- **WHEN** `land/crew`'s card waits on the user and its last post shows `b` at its head now
- **THEN** `b`'s line says `land/crew` carries it, waiting on the user

#### Scenario: A bolt the card shows at an older head
- **WHEN** `land/crew`'s card waits on the user and shows `b` at `1111111`, and `b`'s head is now `2222222`
- **THEN** `b`'s line says `land/crew` carries it at `1111111`, its head now `2222222`

#### Scenario: A bolt the user's send holds
- **WHEN** the user answered `land/crew`'s card ticking `b` at its head now, and no land of `b` is posted yet
- **THEN** `b`'s line says the user's send on `land/crew` holds it and crew asks the runner to land it on that send

#### Scenario: A bolt whose land on the send was stopped
- **WHEN** the user answered `land/crew`'s card ticking `b` at its head now, and the runner stopped the land of `b` that send posted
- **THEN** `b`'s line says it follows: the card after `land/crew`'s answered one carries it, and not that the user's send holds it

#### Scenario: A send kept on a closed card
- **WHEN** `land/crew`'s answered card closed keeping the user's send for `b`, held taking main in, and `b` reads proven again at a head whose own work is the same
- **THEN** `b`'s line says the user's send holds it

#### Scenario: A send kept on a closed card whose land was stopped
- **WHEN** `land/crew`'s answered card closed keeping the user's send for `b` at its head now, the runner stopped the land of `b` that send posted, and no card is open under `land/crew`
- **THEN** `b`'s line says what stopped its last landing at that head and that it follows: the next card under `land/crew` carries it, and not that the user's send holds it

#### Scenario: A bolt proven since the send
- **WHEN** the user answered `land/crew`'s card ticking `b`, and `c` reads proven since, on no row of that card
- **THEN** `c`'s line says it follows: the card after `land/crew`'s answered one carries it

#### Scenario: A bolt no card carries yet
- **WHEN** `b` can land and no card is open under `land/crew`
- **THEN** `b`'s line says it follows: the next card under `land/crew` carries it

#### Scenario: A bolt waiting on its verification
- **WHEN** `b`'s line says it lands once its verification is green, and no card shows it
- **THEN** `b`'s line says nothing of the card
