## ADDED Requirements

### Requirement: crew's shell pins OpenSpec at the family's release
crew's devenv shell SHALL carry OpenSpec at the family's release, the one the family's kits pin, built from its tag, and crew's tests SHALL run on it and on no host's own: `t-specs` validates crew's specs with it, and `t-stage-facts` holds gather.py's reading of a change's tasks, planning and open tasks to it, first checking that the openspec it compares with is the release `devenv.nix` pins.

#### Scenario: A host whose own openspec is another release
- **WHEN** `tests/suite t-stage-facts` runs on a host whose own openspec is not the release crew's `devenv.nix` pins
- **THEN** the openspec the test compares with answers `--version` with the pinned release, and crew's reading agrees with it in every case, a ten-digit ordered marker among them

#### Scenario: A shell that has lost the pin
- **WHEN** the openspec on the shell's path answers `--version` with a release other than `devenv.nix`'s `openspecVersion`
- **THEN** `t-stage-facts` fails before its cases, naming the release it found

## MODIFIED Requirements

### Requirement: crew's specs pass openspec's strict validation
crew's suite SHALL hold every spec under `openspec/specs/` to `openspec validate --specs --strict`, run in crew's checkout by the OpenSpec crew's devenv shell pins, as the end-to-end test `t-specs`, so a requirement past openspec's 500 characters, or one with no SHALL, MUST or scenario, fails the merge whose change brought it. `t-specs` SHALL first find, in scratch specs of its own, a requirement of 501 characters refused and one of 500 taken. Open changes SHALL be outside it.

#### Scenario: crew's specs as they stand
- **WHEN** `tests/suite t-specs` runs in crew's checkout
- **THEN** `openspec validate --specs --strict` passes every spec under `openspec/specs/`, and the test passes

#### Scenario: A requirement one character past the limit
- **WHEN** `t-specs` validates its scratch spec whose one requirement is 501 characters, and the one whose requirement is 500
- **THEN** openspec's strict validation refuses the first and takes the second
