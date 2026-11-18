# A stopped bolt proven again lands

## Why

boomdrive-ops's signal `2026-11-18-boomdrive-ops-9c91dc07/01` names four bolts on deneb that waited one to three days after their checks passed again: flume's `flumes-settings-read-as-its-records-say` (stopped at 26b1eca, green at 340bcb5), and boomdrive's `a-drives-machine-and-state-are-named-once` (b586cd6, green at 39c3a31), `the-runner-needs-no-hand-on-a-host` (5332f1c, green at a50bb36) and `boomdrives-checks-read-no-markdown` (ac7caa9, green at 0322639). The rail said each "lands on proof: crew asks the runner to land it in boomdrive-ops's name at the next read of the rail on the main level's host", and no land was ever posted. Their last lands were boomdrive's 332, 1378, 1379 and 1383.

Each of those lands was posted on the user's send of a landings card. That card then closed keeping the send for the bolt in its `Heads`, as rail-cards "A kit's landings card's close keeps the user's send" has it. The runner stopped the land, Flume naming a fix live on the bolt's branch. The fix merged, so the bolt read proven at a new head with its own work unchanged.

From then on, crew read the kept send as standing for the bolt, since its own work was unchanged, though the stop had spent that send. The raise handed the bolt to that send, which posts nothing once spent. It was neither a land on proof nor a row of the card, and the rail went on saying it lands at the next read. At the stop's own head the same send made the rail say "held by your send", with nothing sent either. The fix `a-stopped-landing-puts-its-bolt-back-on-a-card` read a stop as spending the send of the card still open. It left the send kept on a closed card, and read a send as spent only while its stopped land is the bolt's last landing.

## What Changes

- **A stop spends the send that posted the land for good.** A send is spent for a bolt once any land it posted of that bolt was stopped, as rail-cards "A landing the runner or Flume stopped keeps its box" says. A later land of the bolt, on proof or on another send, does not make the send stand again. `send_spent` and the runner's `lands_due` both hold to it.
- **A send kept on a closed card holds no bolt a stop spent.** The kept sends crew reads leave such a bolt out. So the raise, the rail's line, the rail's read and `crew card read` read no send holding it.
- **A stopped bolt proven again lands.** It lands on proof at a new head when it is not marked to stay and the user has not left it. Otherwise it is a row of its kit's landings card, the card asking for it with its box, at the stop's own head too. Its land line says which, and never that it lands on proof or that a send holds it while no raise would post its land.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `rail-cards`: a kept send holds no bolt a stop spent. A stop spends its send for good, though a land was asked since. A new requirement says a stopped bolt proven again lands on proof or is asked on its card.
- `crew-rail`: a bolt's land line counts it held by a send kept on a closed card only while no land that send posted of it was stopped.

## Impact

- `plugin/lib/plan.py`:
  - `send_spent` reads every stop of a land the send posted.
  - `landings_sent` leaves out a bolt whose kept send a stop spent. Its readers follow: `landings_raised` and `rows_unsent`, `record_reading`'s `sends` and `card_stand`, `landings_unoffered` and `unoffered`, and `landings_earlier` and `sent_left`.
  - `lands_posted` marks each land the run record holds stopped, from a new decision, `lands_stopped`.
- `plugin/lib/runner.py`: `lands_due` posts no land on a send any land of which a row was stopped.
- Tests: `tests/py/test_landings.py`, `tests/py/test_rail.py`.
- No change to the views' shape or crew's mod (`code.8`). No bolt, unit, stage, card key or rail row changes shape, only which bolts a kept send holds and the words of their lines.
- No command, usage, brief or README changes (`docs.2`), and no rule or record changes.
