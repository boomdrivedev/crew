## MODIFIED Requirements

### Requirement: crew's own policy gates its bolts and main on its whole suite
crew's `.config/sluice.toml` SHALL require the `check-full` tasks of every `bolt/*` branch and of `main`, run open on the host, and SHALL accept no replayed task for either, so every submission runs every test afresh. It SHALL name one signer, `sessions`, by deneb's key, and every branch it names SHALL trust that signer alone, so its gates count the runs deneb signs and main's pull requests are taken in. The live test SHALL be no task.

#### Scenario: crew's policy
- **WHEN** crew's `.config/sluice.toml` is read
- **THEN** `[branches."bolt/*"]` and `[branches.main]` each require `#check-full`, its executor is `open`, `[signers.sessions]` names deneb's key, and every branch it names trusts `sessions` alone
