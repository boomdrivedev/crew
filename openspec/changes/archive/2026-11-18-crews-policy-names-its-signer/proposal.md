# crew's policy names its signer

## Why

From sluice v0.97.0, a branch whose policy has a pull request table and names no `[signers]` is refused alone (sluice record 0125, D22; sluice's clause 137): its state would be each host's own, and only the host that keeps the branch on its remote takes its pull requests in. crew's `.config/sluice.toml` gives `main` a pull request table and names no signer, so every landing on crew's main would stop on a host running that sluice, which Boomdrive's set is about to carry.

## What Changes

- **crew's policy names one signer, `sessions`, deneb's key,** as sluice's own policy names it: `[signers.sessions]` with `ssh = "deneb ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIHGx/Ip3yodP/Rg3DdMAjJXoYuBmMxTLpPrka3ei69M/ sluice deneb"`, the key deneb's sluice signs with as `sessions`.
- **Every branch the policy names trusts that signer alone:** `bolt/*`, `main` and `teamless/deneb` each read `trust = ["sessions"]`. On a branch kept on its remote under a policy with signers, sluice reads `trust` as signers and refuses an executor kind there, so `"open"` goes from every branch alike.
- Nothing else in the policy changes: its toolchain, runner, executor, required checks, timeouts, flakiness, remotes and main's pull request table stand as they are.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `merge-gate`: crew's own policy names its one signer, deneb as `sessions`, and every branch it names trusts that signer alone.

## Impact

- `.config/sluice.toml`: the `[signers.sessions]` table, and `trust` on its three branch tables.
- `tests/t-sluice.sh`: its case on crew's own policy reads the signer and every branch's trust.
- No crew code reads `trust` or `[signers]`: `kit.bolt_checks` reads a bolt table's `required`, and `gather.py` carries the policy as text. No view, command, usage or brief changes (`code.8`, `docs.2`).
- `docs/architecture/` and `docs/adr/` are not edited (`docs.7`).
