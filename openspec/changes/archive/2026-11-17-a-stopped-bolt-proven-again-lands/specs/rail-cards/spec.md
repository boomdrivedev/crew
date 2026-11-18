## MODIFIED Requirements

### Requirement: A kit's landings card's close keeps the user's send
Every close of a kit's landings card the user answered SHALL carry as `Heads` the bolts they ticked, at the heads the card showed. This holds whichever act closes it: the raise, the sweep, `crew bolt land`, or a read that finds it ended in Pending You. The card that follows then asks for no bolt the send still lands at a head whose own work is the same. A send so kept SHALL hold no bolt once a land it posted of that bolt was stopped.

#### Scenario: The sweep closes an answered landings card
- **WHEN** the user ticked `a` at `1111111` on `land/sluice`'s card and the sweep closes it with `a` not landed
- **THEN** the close holds `Heads: a@1111111`

#### Scenario: The next card
- **WHEN** `land/sluice`'s next card is raised while `a` stands at `1111111`
- **THEN** it has no row for `a`, the send standing for it

#### Scenario: A send closed in Pending You by its owner
- **WHEN** ops's session acked `land/sluice`'s answered card in Pending You, and the next raise reads it resolved
- **THEN** crew records it closed as ended in Pending You already, with its Answer and `Heads: a@1111111`, and the card it posts has no row for `a`

#### Scenario: A kept send a stop spent
- **WHEN** `land/sluice`'s answered card closed holding `Heads: a@1111111 b@2222222`, and the runner stopped the land of `b` that send posted
- **THEN** no raise reads that send as standing for `b`, at `2222222` or at a later head whose own work is the same, while it still stands for `a`, and `crew card read land/sluice` names `a` and not `b` among what an earlier send still lands

### Requirement: A landing the runner or Flume stopped keeps its box
A bolt whose land the runner answered refused, Flume naming no place on its branch, or whose submission Flume reports withdrawn or refused and waiting on its caller, as the runner's report carries it, SHALL keep its box while its kit's main does not hold its work. Its row SHALL say what stopped its landing at that head, in the runner's or Flume's words, nothing of the bolt's. The send that ticked it SHALL be spent for good: crew SHALL post no land of it on that send again, at any head.

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

#### Scenario: A later land stopped too
- **WHEN** the land of `y` the user's send on `land/crew` posted was stopped at `abc1234`, `y`, not marked to stay, reads proven at `def5678` with its own work unchanged, and crew's land of `y` on proof at `def5678` is stopped too
- **THEN** no land of `y` is posted on that send, at `def5678` or any head, and the card asks for `y` at `def5678` with its box, saying its land on proof was stopped

## ADDED Requirements

### Requirement: A stopped bolt proven again lands on proof or is asked on its card
A bolt whose land on the user's send was stopped, held by no send that still stands, SHALL land once it reads proven again. At a new head, a bolt not marked to stay and not left SHALL land on proof, the next raise posting its land. Otherwise it SHALL be a row of its kit's landings card, at its stop's own head among them. Its land line SHALL say how it lands, never that it lands on proof or that a send holds it while no raise would post its land.

#### Scenario: Proven again at a new head
- **WHEN** `land/crew`'s answered card closed keeping the user's send for `y` at `abc1234`, the runner stopped the land of `y` that send posted, Flume naming a fix live on `bolt/y`, and that fix merged, so `y`, not marked to stay, reads proven at `def5678` with its own work unchanged
- **THEN** `y`'s line says it lands on proof, the next rail read on the main level's host raises `land/crew`, whose raise posts one land of `y` on proof at `def5678`, and the read after it posts none

#### Scenario: Marked to stay
- **WHEN** the same holds of `z`, marked to stay
- **THEN** no land of `z` is posted, and the raise of `land/crew` posts a card asking for `z` at `def5678` with its box

#### Scenario: Proven again at the stop's own head
- **WHEN** `land/crew`'s answered card closed keeping the user's send for `z` at `abc1234`, the runner stopped the land of `z` that send posted, Flume naming no place on `bolt/z`, and `z` still reads proven at `abc1234`
- **THEN** no land of `z` is posted, and the raise of `land/crew` posts a card asking for `z` at `abc1234` with its box, saying what stopped its last landing

#### Scenario: Beside a card waiting on the user
- **WHEN** the same holds of `z` at `abc1234`, and the open card under `land/crew` waits on the user showing another row and not `z`
- **THEN** the rail's read raises `land/crew`, and the card asks for `z` beside that row
