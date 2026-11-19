# Design

## Context

Read 2026-11-18 at this branch's base, `e82e9c54` (crew's main), against sluice's main at `b6c30e78` (v0.97.4) and the family's statement for sluice, boomdrivedev/blueprints `design/sluice/requirements.md`.

**What crew's policy says now.** `.config/sluice.toml` runs crew's suite open on the host (`[executor] kind = "open"`) and names three branch tables, `bolt/*`, `main` and `teamless/deneb`, each kept on `origin`, requiring `#check-full`, and trusting `["open"]`, the executor kind. `main` alone has a pull request table, `reviews = 0` and `checks = []`, since ops's landing opens a pull request that waits on nothing of GitHub's (`plan.16`). It names no `[signers]`, so each branch's records are each host's own files.

**What sluice now asks.** A branch's requests are taken in only where its records are on its remote, by the host that keeps it there (clause 137, record 0093 as amended). sluice record 0125, D22, refuses a branch whose policy gives it a pull request table and names no signer, that branch alone, with the words "name [signers] in .config/sluice.toml so its state is kept on origin (137)", from v0.97.0; its consequences name crew's peers sluice and switchboard-kit and leave the signers to ops. Naming `[signers]` keeps every branch with a `remote` on its remote (C.6). On such a branch a run counts only when a signer the branch trusts signed it (clauses 78 and 79), and `trust` lists signers: `Policy::parse` refuses an executor kind or an unnamed signer there, failing the whole policy, not the branch (`crates/sluice-core/src/policy.rs`, read at v0.97.4). A signer whose table names no `systems` may claim a run of any system, and one not marked `confined` claims no confinement, which no branch of crew's asks for.

**What sluice's own policy names.** `[signers.sessions]` with `ssh = "deneb ssh-ed25519 … sluice deneb"`, deneb's key, which deneb's sluice signs with as `sessions` (its `[signing]`), and `trust = ["sessions"]` on each of its branches.

**What reads crew's policy.** sluice, from each branch's own revision. In crew, `kit.bolt_checks` reads a bolt table's `required`, and `gather.py` carries main's policy as text; neither reads `trust` or `[signers]`. `tests/t-sluice.sh` pins the policy's shape.

**Area pages this change touches:**

- `core.md`: `state.3` (main moves only through sluice), `roles.5` (crew builds no mechanism sluice holds).
- `tests.md`: `tests.5` (every merge gated by the policy's checks), `tests.10` (the policy trusts no `cache`).
- `docs.md`: `docs.4`, `docs.6`, `docs.7`.

## Goals / Non-Goals

**Goals:**

- crew's policy reads on a sluice that carries record 0125, every branch it names gated as before, on runs deneb signs.

**Non-Goals:**

- A signer for another host. Only deneb signs runs crew's gates count, as only deneb signs sluice's; a host that comes to land crew's work adds its own signer then, ops's choice by record 0125.
- Any other key of the policy, main's pull request table among them.

## Decisions

### Decision 1: the signer sluice's own policy names

crew's policy names `[signers.sessions]` with deneb's key, the line sluice's own policy carries, byte for byte. crew's sessions run and submit on deneb, and deneb's sluice already signs as `sessions` with that key, so its runs count for crew with nothing set up on the host.

*Not taken:* a signer of crew's own name, which deneb's sluice does not sign as, so no run would count and no host would lead crew's rounds (record 0119's ruling, a branch whose trust names no signer a host signs as forms nothing); dropping main's pull request table, which `plan.16`'s landing opens.

### Decision 2: every branch trusts the signer alone

`bolt/*`, `main` and `teamless/deneb` each read `trust = ["sessions"]`. With a signer named, every branch with a remote is signed, and sluice refuses `"open"` in a signed branch's trust for the whole policy, so `teamless/deneb`, which takes no pull request, changes with the other two.

*Not taken:* `["open", "sessions"]`, which sluice refuses on a signed branch; leaving `teamless/deneb` as it is, which would refuse the policy for every branch.

## Risks / Trade-offs

- [Only a host signing as `sessions` with deneb's key leads crew's rounds or has its runs counted (clause 137)] → deneb runs crew's landings today; another host that lands crew's work names its own signer in the policy then.
- [Records a host kept in its own files before do not move to the remote] → sluice reads a signed branch's records on its remote from the next round; crew reads a bolt's verification from the runner's report and the landing commit's own trailers (`tests.5`), never from sluice's records, so nothing of crew's reads the records left behind.

## Migration Plan

None. sluice reads the policy from each branch's own revision, so the signer takes effect on a branch once this change lands on it, `main` first. Rollback is reverting the commit.

## After deploy

None: the policy is read by sluice from the branch it gates, so landing it is the whole change, and `t-sluice.sh` pins its shape.

## Task notes

**1.1** `.config/sluice.toml`: add `[signers.sessions]` after `[executor]`, `ssh = "deneb ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIHGx/Ip3yodP/Rg3DdMAjJXoYuBmMxTLpPrka3ei69M/ sluice deneb"`, with a comment naming sluice's clauses 78, 79 and 137 and record 0125, D22; set `trust = ["sessions"]` on `[branches."bolt/*"]`, `[branches.main]` and `[branches."teamless/deneb"]`. Nothing else moves.

**1.2** `tests/t-sluice.sh`, its case on crew's own policy: print the executor kind, `kit.bolt_checks`, main's `required`, the signers' names, the host that opens the `sessions` key's line, and the distinct `trust` lists of every branch table, expecting `open ['#check-full'] ['#check-full'] ['sessions'] deneb [('sessions',)]`. Its opening comment names the signer.
