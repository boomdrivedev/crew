# Tasks

Submit nothing; a place's merge is Flume's.

## 1. crew's shell pins the family's OpenSpec

- [x] 1.1 `devenv.nix` builds OpenSpec 1.14.3 from its tag, at the family's hashes, and puts it in the shell's packages (design Decision 1). Verify `tests/suite t-specs t-stage-facts` ends with "0 failed".
- [x] 1.2 `t-stage-facts` requires the openspec it compares with to be the release `devenv.nix` pins, and gather.py's comment names that release (design Decisions 2 and 3). Verify `tests/suite t-stage-facts` ends with "0 failed".
- [x] 1.3 `tests/run`, `t-specs`'s opening comment and README's Needs name the shell's openspec. Verify `tests/suite t-docs` ends with "0 failed".
- [x] 1.4 The tests the change affects pass. Verify `tests/suite --affected` ends with "0 failed".
