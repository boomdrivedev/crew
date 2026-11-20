# Design: crew's shell pins the family's OpenSpec

## Context

`t-stage-facts` holds gather.py's reading of a change's tasks, planning and open tasks to openspec's own on the same worktrees (`plan.12`), and `t-specs` holds crew's specs to `openspec validate --specs --strict`. Both ran the openspec on the host's path, since crew's `devenv.nix` declared none. Every other kit of the family pins it in its own shell: sluice, flume, boomdrive, timber, weir and boom each build `pkgs.openspec` over `Fission-AI/OpenSpec` at tag `v1.14.3`, read from their `devenv.nix` on main 2026-11-19.

deneb's own openspec is 2.1.0. Its `dist/utils/task-progress.js` keeps 1.14.3's `TASK_LINE_PATTERN` but reads a task's text as its whole first paragraph, joining each following line that does not end it, and a list marker of more than nine digits does not end it. 1.14.3's `parseTaskLines` reads each matching line alone, and its `openspec instructions apply` calls it line by line (`dist/commands/workflow/instructions.js`, 230).

## Decisions

### 1. The shell pins 1.14.3, as the family's kits build it

`devenv.nix` gains the `openspec` derivation the other kits carry, `overrideAttrs` of nixpkgs' `openspec` with the tag's source and `fetchPnpmDeps`, at their two hashes, and puts it in `packages`. crew's `devenv.lock` locks the same `cachix/devenv-nixpkgs` revision as boomdrive's (c2f38fe7), so the hashes hold: built on this host 2026-11-19, `devenv shell -- openspec --version` answers 1.14.3.

Not taken: matching crew's reading to deneb's 2.1.0. That reading follows one host's release, which its next upgrade moves again; the family's kits write and validate their changes with 1.14.3, and crew's reading of their tasks is held to the release they write them with.

This departs from `code.1`, which lists what devenv declares and names no openspec: the brief asks for the pin, and the rule's amendment is the design agent's after the landing (`docs.7`).

### 2. gather.py's reading is 1.14.3's already

gather.py's `TASK` is 1.14.3's `TASK_LINE_PATTERN` with JavaScript's `\s` written out, and `tasks_of` reads each line alone, as `parseTaskLines` does. With the pin, `t-stage-facts` passes every case, the ten-digit marker among them, with no change to the reading. Its comment named 1.14.1, the release it was first read from; it now names 1.14.3 and the pin, and says a bump of the pin moves the reading with it.

### 3. t-stage-facts checks the release it compares with

Before its cases, `t-stage-facts` reads `openspecVersion` from `devenv.nix` and requires `openspec --version` to answer it. A shell whose pin is lost, or a path that puts a host's openspec first, fails there and names the release it found, rather than surfacing as one case's disagreement. `devenv.nix` is already an input of every test's task (`tests.10`), so a bump reruns it.

## Risks

- A host's own openspec still answers what gather.py hands to it on that host, a change of another workflow among them, and a host on 2.x reads a wrapped task's text joined where 1.14.3 does not. That is the host's release against the family's, outside the suite; the family's next release, pinned here, moves both.
