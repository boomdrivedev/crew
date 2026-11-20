# crew's shell pins the family's OpenSpec

## Why

`tests:t-stage-facts` failed on crew's main at 5827b6b4 under a docs-only submission (boomdrive-design's #2, 195ddd70, which touches no code): `FAIL: markers: crew reads {"tasks":[2,5],"planning":true,"open":["star","numbered","nine digits"]} where openspec reads {"tasks":[2,5],"planning":true,"open":["star","numbered","nine digits 1234567890. [ ] ten digits"]}`. crew's `devenv.nix` took openspec from the machine, so the test compared crew's reading with whatever release the host carried. deneb's is now 2.1.0, whose task parser joins a line that is no task onto the task above it (its `parseLocatedTaskLines`, OpenSpec #2227), so `1234567890. [ ] ten digits`, ten digits being no list marker, became part of the nine-digit task's text. A host's upgrade turned main red with nothing of crew's moved.

## What Changes

- **crew's devenv shell pins OpenSpec at the family's release, 1.14.3,** built from its tag as sluice, flume, boomdrive, timber, weir and boom build it, with their hashes, since crew's `devenv.lock` holds the same nixpkgs. A host's own openspec no longer decides `t-specs` or `t-stage-facts`.
- **`t-stage-facts` first checks that the openspec it compares with is the release `devenv.nix` pins,** so a shell that loses the pin fails there by name rather than in a case's reading.
- **gather.py's reading of a change's tasks follows 1.14.3's rules,** which it already matches: 1.14.3's `TASK_LINE_PATTERN` is the one gather.py's `TASK` writes out, and 1.14.3 reads each task from its own line, joining nothing. Only the comment that names the release moves.
- `tests/run`, `t-specs`'s opening comment and README's Needs name the shell's openspec in place of the machine's.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `test-suite`: crew's shell pins OpenSpec at the family's release, and `t-specs` and `t-stage-facts` run on it, never on a host's own.

## Impact

- `devenv.nix`: the `openspec` derivation at 1.14.3, in the shell's packages. This departs from `code.1`, whose list of what devenv declares names no openspec; its amendment is the design agent's (`docs.7`).
- `tests/t-stage-facts.sh`: the check of the pinned release before its cases.
- `plugin/lib/gather.py`: a comment alone; no decision moves (`code.7`), and no view, command, usage or brief changes (`code.8`, `docs.2`).
- `tests/run`, `tests/t-specs.sh`, `README.md`: words naming where openspec comes from.
- A host's own openspec still answers what gather.py hands to openspec on that host; the flake's package keeps openspec the host's (README, Flake).
- `docs/architecture/` and `docs/adr/` are not edited (`docs.7`).
