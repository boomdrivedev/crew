# Tasks

Submit nothing, and never run `wt submit --help`.

## 1. crew's policy names its signer

- [x] 1.1 crew's `.config/sluice.toml` names `[signers.sessions]` by deneb's key, and its `bolt/*`, `main` and `teamless/deneb` tables each trust `sessions` alone, nothing else moving (design Decisions 1 and 2; Task notes 1.1). Verify `tests/suite t-sluice` ends with "0 failed".
- [x] 1.2 `tests/t-sluice.sh`'s case on crew's own policy reads its one signer, deneb's, and every branch's trust of it alone (design Decision 2; Task notes 1.2). Verify `tests/suite t-sluice` ends with "0 failed".
- [x] 1.3 The tests the change affects pass. Verify `tests/suite --affected` ends with "0 failed".
