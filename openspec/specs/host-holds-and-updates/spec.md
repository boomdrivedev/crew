# host-holds-and-updates Specification

## Purpose
How crew is put on the brakes, a host at a time, before herdr is upgraded or a host rebooted, and how an update of crew, or of an agent's brief, reaches every standing agent at its next stop, each agent's band saying the crew it runs (`teams.19`).

## Requirements

### Requirement: A host can be held
`crew hold <host>|--all "<why>"` SHALL hold each host named, or every host crew runs agents on, the hosts of its drives' main levels: crew SHALL start no agent there until `crew go`, refusing with the hold's words every command that would, and SHALL tell every standing agent up there to finish the step it is in and start nothing new. With `--now` crew SHALL end every crew agent there at once. The run record SHALL name the host and never the why.

#### Scenario: Held
- **WHEN** the user runs `crew hold deneb "herdr 0.9.6"`
- **THEN** each main-level agent up on deneb is told the hold, and `crew main up swancloud` on deneb is refused naming who held it and why

#### Scenario: Held at once
- **WHEN** the user runs `crew hold --all "reboot" --now`
- **THEN** every crew agent on every host crew runs agents on is ended, and each is brought back by `crew go`

### Requirement: A held host says when it is quiet
`crew hold status` SHALL say what still works on each held host: an agent working, one waiting on a question to the user, one running background work of its own other than crew's waits, a stage not yet ended, and crew's tests running. `crew hold wait` SHALL wait until each host is quiet and then end every crew agent there, its panes kept, and SHALL stop at its timeout saying what still works.

#### Scenario: Waiting on a submission
- **WHEN** swancloud-ops runs `wt submit main` in the background on a held host
- **THEN** `crew hold status` names it, and `crew hold wait` ends nothing until the submission is over

### Requirement: Go lifts a hold
`crew go <host>|--all` SHALL lift the hold, bring each standing agent whose pane is empty back with its conversation, greeted as `crew revive` greets it, tell each one still up that the hold is lifted, run each console's tabs again, and restart every agent an update made due.

#### Scenario: After herdr's restart
- **WHEN** the user restarts herdr on a host whose agents `crew hold wait` ended, then runs `crew go` there
- **THEN** each main-level agent is back with its conversation, its effort, mode and folders, and greeted

### Requirement: A band shows the crew its agent runs
Each standing agent's band SHALL show the crew version it started on, and once it is due the version of the crew the host has installed, which it takes at its next stop. Every band on a held host SHALL open with the hold: who held it, since when and why.

#### Scenario: Due
- **WHEN** the planner started on crew v0.12.1 and v0.13.0 changed its brief
- **THEN** its band's first line ends with "crew v0.12.1 → v0.13.0 at its next stop"

#### Scenario: Due for a release
- **WHEN** the planner started on a build whose release names the version `0.44.1`, and the host's installed crew is a build whose release names `0.44.2`
- **THEN** its band's first line ends with "crew v0.44.1 → v0.44.2 at its next stop"

### Requirement: A standing agent of a role that now runs as its kind is ended at its next stop
A standing agent whose drive's `runs` now names its role `on-demand`, so that it runs as its kind, SHALL be ended at its next stop, once herdr reads it idle with no question open and no background work of its own but crew's waits, told that its role now runs as its kind, and started again by nothing: no restart, no `crew revive`, no `crew update`. Nothing SHALL be ended on a held host.

#### Scenario: The planner moves
- **WHEN** madswan's teams entry's `runs` comes to name its planner `on-demand` while `madswan-planner` stands, and it ends its turn
- **THEN** `madswan-planner` is ended, its pane is left with no agent started in it, and its log says its role now runs as its kind

#### Scenario: An update after the move
- **WHEN** `crew update` runs on deneb after madswan's planner has moved
- **THEN** no planner of madswan is restarted or started

### Requirement: crew knows the release it runs from
crew SHALL read the crew it runs as from where it runs: in a checkout, HEAD's commit and the version git gives it; with no git, the version `plugin/release.json` names, and its commit where named; and nothing where it finds neither, or a release file naming neither a full commit nor a release's version, saying what it could not read wherever a decision rests on it. A session's start SHALL record the commit and version of the crew whose plugin it loaded.

#### Scenario: A build's release
- **WHEN** crew runs from a folder with no git whose `plugin/release.json` names the commit `fcedc22e6df6380f1f640efac5f796416b1fb4c9` and the version `0-unstable-2026-11-08`, and a crew agent's session that loaded that folder's plugin starts
- **THEN** the start records that commit and the version `0-unstable-2026-11-08+fcedc22`

#### Scenario: A release tag's plugin copied whole
- **WHEN** crew runs from a folder with no git whose `plugin/release.json` names the version `0.56.0` and no commit
- **THEN** crew reads the version `v0.56.0` and no commit, from the release, and says nothing is unread

#### Scenario: A copy of main's plugin
- **WHEN** crew runs from a folder with no git whose `plugin/release.json` names the version `0.0.0` and no commit
- **THEN** crew reads no release there and says the file names no commit

#### Scenario: A build with no release
- **WHEN** crew runs from a folder with no git and no release file
- **THEN** a start that loads its plugin records no commit and no version

#### Scenario: A release file crew can't read
- **WHEN** a build's release file names a commit that is not forty hexadecimal characters
- **THEN** crew reads no release there and says the file names no commit

#### Scenario: A start records the crew it loaded
- **WHEN** a crew agent's session starts on a crew checkout
- **THEN** its start records the commit and version `crew _release` prints for that checkout

### Requirement: A build's version is shown as a checkout's is
crew SHALL show a build's version as `v<x.y.z>` where its release file names a release's version, `x.y.z` other than main's `0.0.0`, and otherwise as the version the file names followed by `+` and the commit's first seven characters, so two builds of one day read apart.

#### Scenario: A release version
- **WHEN** a build's release file names the version `0.44.1`
- **THEN** crew's version there is `v0.44.1`

#### Scenario: An untagged version
- **WHEN** a build's release file names the version `0-unstable-2026-11-08` and the commit `fcedc22e6df6380f1f640efac5f796416b1fb4c9`
- **THEN** crew's version there is `0-unstable-2026-11-08+fcedc22`

#### Scenario: Main's version
- **WHEN** a build's release file names the version `0.0.0` and the commit `fcedc22e6df6380f1f640efac5f796416b1fb4c9`
- **THEN** crew's version there is `0.0.0+fcedc22`

### Requirement: crew _release prints what a crew is
`crew _release` SHALL print, as one line of JSON, the crew's root, commit and version, the commit null where a release names none, and whether they came from a checkout or a release, reading nothing else and starting nothing; `-h` and `--help` SHALL print its usage.

#### Scenario: From a build
- **WHEN** `crew _release` runs from a build whose release file names a commit and a version
- **THEN** it prints them with `from` `release`

#### Scenario: From a build of a tag that names no commit
- **WHEN** `crew _release` runs from a build whose release file names the version `0.56.0` and no commit
- **THEN** it prints the version `v0.56.0`, a null commit and `from` `release`

#### Scenario: From a checkout
- **WHEN** `crew _release` runs from a checkout
- **THEN** it prints the checkout's commit and version with `from` `checkout`

#### Scenario: From a build with no release
- **WHEN** `crew _release` runs from a folder with no git and no release file
- **THEN** it prints no commit and no version, with `from` null

### Requirement: crew names its command by the crew its host has installed
crew's own command SHALL be the crew the host has installed: its checkout's `plugin/bin/crew` where crew runs from a checkout; else the first `crew` on its path in a folder outside the Nix store, a profile's link that each install moves; and its own build's `plugin/bin/crew` only where it finds neither.

#### Scenario: A build with a profile's crew
- **WHEN** crew runs from `/nix/store/abc-crew-0.44.1`, with no git, and its path holds `/nix/store/def-claude-code/bin`, which has a `crew`, then `/etc/profiles/per-user/chuck/bin`, which has a `crew`, then `/run/current-system/sw/bin`
- **THEN** crew's command is `/etc/profiles/per-user/chuck/bin/crew`

#### Scenario: A checkout
- **WHEN** crew runs from `/workspace/crew/main`, a checkout
- **THEN** crew's command is `/workspace/crew/main/plugin/bin/crew`, whatever its path holds

#### Scenario: A build with nothing installed
- **WHEN** crew runs from a build and no folder of its path outside the Nix store has a `crew`
- **THEN** crew's command is the build's own `plugin/bin/crew`

### Requirement: A standing agent's crew commands run the crew its host has installed
Wherever crew names its own command for a later run, in a role's brief, a command forwarded to this host, the hand of a restart to `crew _renew`, the follower's Pending You notice, its `_update` and its start again, and the console's tabs, crew SHALL name it by crew's command as the requirement above gives it, and never by a build's store path while the host has a crew installed.

#### Scenario: A brief built by a build
- **WHEN** crew runs from `/nix/store/abc-crew-0.44.1` and its command is `/etc/profiles/per-user/chuck/bin/crew`
- **THEN** the planner's brief names `/etc/profiles/per-user/chuck/bin/crew` for every crew command it gives, and nothing of `/nix/store/abc-crew-0.44.1`

#### Scenario: A restart is handed to the installed crew
- **WHEN** the Stop hook of a session that loaded `/nix/store/abc-crew-0.44.1/plugin` finds wldn-ops due, and the host's installed crew is `/etc/profiles/per-user/chuck/bin/crew`
- **THEN** it runs `crew _renew wldn-ops` through `/etc/profiles/per-user/chuck/bin/crew`

### Requirement: crew reads the crew its host has installed
crew SHALL read what the installed crew is from its own files where the installed command is its own, and otherwise by asking it, `crew _release`, within five seconds. An answer that does not come in time, fails, or lacks a field SHALL read as unread, saying which; a null commit is no lack where the answer is from a release naming a release's version. A process SHALL ask at most once for each real path of the installed command, and not where the host keeps its answer.

#### Scenario: Its own crew
- **WHEN** the installed command is crew's own checkout's `plugin/bin/crew`
- **THEN** crew reads the checkout with no process

#### Scenario: The installed crew does not answer
- **WHEN** the installed command does not answer `crew _release` within five seconds
- **THEN** crew reads the installed crew as unread, saying it did not answer

#### Scenario: An answer with a field missing
- **WHEN** the installed command's `crew _release` prints JSON from a checkout with no `commit`
- **THEN** crew reads the installed crew as unread, saying the answer names no commit

#### Scenario: An installed release that names no commit
- **WHEN** the installed command's `crew _release` prints the version `v0.56.0`, a null commit and `from` `release`
- **THEN** crew reads the installed crew as `v0.56.0` with no commit, from a release

### Requirement: The launch digest reads crew's command as one word
A role's launch digest SHALL read every path a brief may name crew's command by as one word, so that two crews of one host digest one start alike.

#### Scenario: Two crews of a host
- **WHEN** a start's brief named crew by `/etc/profiles/per-user/chuck/bin/crew`, and a checkout of crew on the same host builds the same brief naming its own `plugin/bin/crew`
- **THEN** both digest the start alike, and neither reads the other's start as due

#### Scenario: A start made before this release
- **WHEN** wldn-ops's start recorded the launch digest an older crew made, its brief naming crew by that build's own path
- **THEN** wldn-ops is due a restart, its brief having changed

### Requirement: A standing agent whose brief, model, effort or folders changed is due a restart
crew SHALL record at each agent's start the crew it loaded and what it was started with, and SHALL judge whether a standing agent is due against the crew the host has installed now, which its commands run. A standing agent whose brief, model, effort or folders changed since its start SHALL be due a restart.

#### Scenario: A brief changed
- **WHEN** a landing changes the planner's brief
- **THEN** the planner is due a restart

### Requirement: A standing agent is due when the plugin it loaded is no longer the installed crew's
Where the installed crew is a checkout, an agent whose loaded part of crew's plugin changed between its start's commit and the checkout's SHALL be due, and a change to crew's code alone SHALL make none due, since every command runs crew's checkout as it is. Where the installed crew is a build, an agent whose start recorded another commit SHALL be due, since its session loaded that build's plugin folder whole and its hooks run from that folder.

#### Scenario: Code alone changed
- **WHEN** a landing changes only `plugin/lib/plan.py`, and the host's installed crew is a checkout
- **THEN** no agent is due

#### Scenario: A release is installed
- **WHEN** wldn-ops started on a build whose release names commit `1111111111111111111111111111111111111111`, and the host's installed crew is a build whose release names `2222222222222222222222222222222222222222`
- **THEN** wldn-ops is due a restart, crew's release having changed

#### Scenario: The same release
- **WHEN** wldn-ops started on the release the host's installed crew is now, its brief, model, effort and folders unchanged
- **THEN** wldn-ops is not due

### Requirement: crew makes no agent due for its plugin where it can't tell, and says why
Where the start recorded no commit, or crew can't read the installed crew, crew SHALL make no agent due for crew's plugin and SHALL say it can't tell, and why.

#### Scenario: A start that recorded no release
- **WHEN** wldn-ops's start recorded its launch and no crew commit, and its brief, model, effort and folders are unchanged
- **THEN** wldn-ops is not due, and crew says it can't tell whether its plugin changed since that start, which recorded no release of crew's

#### Scenario: The installed crew can't be read
- **WHEN** wldn-ops's start recorded a commit and crew can't read the crew the host has installed
- **THEN** wldn-ops is not due, and crew says it can't read the crew this host has installed, and why

### Requirement: A due agent is restarted once herdr reads it idle, resumed and told what changed
crew SHALL restart a due agent once herdr reads it idle with no question open and no background work of its own but crew's waits: at the end of its turn, and for one sitting idle when crew's checkout, the crew the host has installed or the teams file moves, or on `crew update`. Every standing role SHALL resume its conversation and be told what changed. Nothing SHALL be restarted on a held host.

#### Scenario: At the end of its turn
- **WHEN** the planner is due and ends its turn
- **THEN** the planner is resumed with its new brief and told the crew it now runs and what changed

#### Scenario: Running a submission
- **WHEN** swancloud-ops is due and is waiting in the background on a landing it submitted
- **THEN** it is restarted only once the submission is over and its turn ends

#### Scenario: An install moves while an agent sits idle
- **WHEN** crew's follower runs from a build, and the host's installed command's real path moves from one build to another
- **THEN** the follower's next refresh hands out the restarts the install made due, running `crew _update` through the installed command, and starts again through the installed command's `crew _follow`

### Requirement: A restart ends with its agent running, on crew as it now is or as it was
A restart SHALL end with its agent running: on crew as it now is once the agent has exited, or as it was when it could not be ended. A restart whose agent has not exited when its stop gives up SHALL watch it for ten minutes and start it the moment it exits; one whose agent still runs after that SHALL leave it running, still due, and say so.

#### Scenario: Slow to exit
- **WHEN** swancloud-ops is due and is restarted, and it is still up when the stop's `/exit` and Ctrl+C have had their time, then exits a few seconds later
- **THEN** it is resumed on crew as it now is and told what changed, and its restart's log ends "swancloud-ops is restarted on crew"

#### Scenario: Never exits
- **WHEN** swancloud-ops is due and is restarted, and it is still up ten minutes after its stop gave up
- **THEN** it is left running as it was, nothing is started in its pane, and its restart's log says it did not exit and runs on, its next turn's end handing it back

### Requirement: A later restart starts an agent an earlier restart's keys exited
A later restart that finds the agent exited by an earlier restart's keys, its pane kept and no start of it since, SHALL start it without a stop. No restart SHALL leave its agent's pane a shell with no agent in it.

#### Scenario: Exits after the restart gave up
- **WHEN** a restart of swancloud-ops gave up and left it running, and it later exits with its pane kept and nothing has started it since, and its restart is handed again
- **THEN** that restart starts it in its pane without a stop, resumed and told what changed

#### Scenario: Exited by something else
- **WHEN** swancloud-ops is due and not up, and no restart of its session gave up on it, or its main level was taken down with `crew main down`
- **THEN** the restart starts nothing and says it is not up

### Requirement: A checkout reads each release tag at the commit it was cut from
In a checkout, crew's version SHALL be the newest release tag, `v<x.y.z>` by version, whose source is HEAD or an ancestor of it, with `+<n>` for the n commits from the source to HEAD, and the tag alone where HEAD is the tag's own commit. A tag's source SHALL be the parent of the commit it names where that commit is a release commit, its subject `chore(release): <tag>`, and otherwise that commit.

#### Scenario: Main past a release
- **WHEN** a checkout's HEAD on main is two commits past P, and `v0.56.0` names a commit off main, `chore(release): v0.56.0`, whose parent is P
- **THEN** crew's version there is `v0.56.0+2` and its commit HEAD's

#### Scenario: Main at the commit a release was cut from
- **WHEN** a checkout's HEAD is P, from which `v0.56.0`'s release commit was cut
- **THEN** crew's version there is `v0.56.0`

#### Scenario: A checkout of the tag
- **WHEN** a checkout's HEAD is the release commit `v0.56.0` names
- **THEN** crew's version there is `v0.56.0`

#### Scenario: A release tagged on main's own commit
- **WHEN** a checkout's HEAD on main is three commits past the commit `v0.55.0` names, a commit of main that is no release commit, and no newer tag's source is HEAD or before it
- **THEN** crew's version there is `v0.55.0+3`

#### Scenario: No release tag before HEAD
- **WHEN** no release tag's source is HEAD or an ancestor of it
- **THEN** crew reads HEAD's commit and no version

### Requirement: Each lasting process of crew's moves to the installed crew by itself
The rail tab, the board tab, the flow reader and the follower SHALL each start again through the installed command, with their own arguments and in their own process, once the installed crew names another commit than the one they started on: a build's release commit, or a checkout's HEAD at their start. A tab and the flow reader SHALL look each second, and the follower at each refresh.

#### Scenario: A board tab older than the install
- **WHEN** wldn's board tab runs a build whose release names commit `1111111111111111111111111111111111111111`, and the host's installed crew answers `crew _release` naming `2222222222222222222222222222222222222222`
- **THEN** within a second the tab starts again through the installed command as `crew _board wldn`, in the same process, and draws the board again

#### Scenario: A rail tab without the follower lock
- **WHEN** wldn's rail tab draws the frames of swancloud's job, which holds the follower lock, and runs a build older than the installed crew
- **THEN** within a second the tab starts again through the installed command as `crew _rail wldn`, holding no lock

#### Scenario: A checkout moves under a tab
- **WHEN** the board tab of a host that runs crew from its checkout started at HEAD `aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa`, and the checkout moves to `bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb`
- **THEN** within a second the tab starts again through the checkout's `plugin/bin/crew` as `crew _board wldn`

#### Scenario: The installed crew's own tab
- **WHEN** a tab runs the build whose release names the commit the installed crew names
- **THEN** it starts nothing again, and asks the installed crew `crew _release` at most once while the installed command's real path stays

### Requirement: A lasting process moves for an install only on what it read
A lasting process that cannot read the commit it started on or the installed crew's SHALL run on as it is, starting nothing again on a guess. One started again through the installed command SHALL carry the installed commit it moved for; while the installed crew still names that commit and it still runs another, it SHALL say so once and run on, and it SHALL move again once the installed crew names another.

#### Scenario: The installed crew can't be read
- **WHEN** a tab runs a build and the installed command does not answer `crew _release` within five seconds
- **THEN** the tab runs on as it is and starts nothing again

#### Scenario: Started again and still another
- **WHEN** a board tab started again for the installed commit `2222222222222222222222222222222222222222` still reads its own release as `1111111111111111111111111111111111111111`
- **THEN** it says once that it runs on as it is, and starts nothing again while the installed crew names `2222222222222222222222222222222222222222`

#### Scenario: A later install
- **WHEN** that tab's host then installs a build whose release names `3333333333333333333333333333333333333333`
- **THEN** the tab starts again through the installed command

#### Scenario: A follower stuck for one install
- **WHEN** the follower was started again for the installed commit `2222222222222222222222222222222222222222`, still runs another, and the host then installs a build naming `3333333333333333333333333333333333333333`
- **THEN** at its next refresh it hands out the restarts due and starts again through the installed command, keeping its lock

### Requirement: A session on an older build of crew is offered a restart at the end of its turn
At the end of a turn of a session that is no crew agent and loaded crew's plugin from a build, crew's Stop hook SHALL, when the installed crew names another commit than that build's release, show the person one message. It SHALL name the version the session runs, the version installed and the session's id, and say that exiting and resuming the conversation moves it. It SHALL give the model nothing and hold up no turn.

#### Scenario: The user's own session
- **WHEN** a session started with the plugin folder of a build of crew v0.59.0, which no crew agent's record names, ends a turn, and the host's installed crew is v0.67.1
- **THEN** its Stop hook prints a `systemMessage` naming v0.59.0, v0.67.1 and the session's id, saying that exiting and resuming the conversation runs v0.67.1 there, and gives the model nothing

#### Scenario: A standing agent
- **WHEN** wldn-ops runs a build older than the installed crew and ends its turn
- **THEN** it is handed its restart as before, and offered nothing

#### Scenario: A session on the installed build
- **WHEN** a session that loaded the build the installed crew is ends a turn
- **THEN** nothing is shown

#### Scenario: A session loaded from a checkout
- **WHEN** a session that loaded crew's plugin from a checkout ends a turn after the checkout moved
- **THEN** nothing is shown

### Requirement: A session is offered its restart once for each install
crew SHALL offer a session its restart once for each real path of the installed command, and SHALL offer it again once an install moves that path while the session still runs an older build. Where it cannot read the installed crew, or the build's release names no commit, it SHALL offer nothing.

#### Scenario: The next turn
- **WHEN** a session was offered its restart, and ends another turn while the installed command's real path is unmoved
- **THEN** nothing is shown, and the Stop hook starts no process

#### Scenario: A later install
- **WHEN** the host then installs another build, and the session still runs v0.59.0
- **THEN** the end of its next turn offers it again, naming the new version

#### Scenario: The installed crew can't be read
- **WHEN** the installed command does not answer `crew _release` within five seconds
- **THEN** nothing is shown

### Requirement: The host keeps each installed build's answer
crew SHALL keep on the host, by the command's real path, the read and complete answer to `crew _release` of an installed command whose real path is in the Nix store, and SHALL read it there before asking, since a path there names one build for ever. An answer unread SHALL never be kept, and a command whose real path is outside the store SHALL be asked as before.

#### Scenario: Two processes of a host
- **WHEN** two processes on a host read the installed crew, whose command's real path is `/nix/store/def-crew/bin/crew`
- **THEN** the first asks it `crew _release` and keeps its answer, and the second reads the kept answer and starts no process

#### Scenario: An unread answer
- **WHEN** the installed command does not answer `crew _release` within five seconds
- **THEN** nothing is kept, and the next process asks again

#### Scenario: A kept answer crew can't read
- **WHEN** the kept answer for the installed command's real path is not JSON
- **THEN** crew asks the command again and keeps its new answer

#### Scenario: A command outside the store
- **WHEN** the installed command's real path is a checkout's `plugin/bin/crew`, outside the Nix store
- **THEN** each process asks it, and nothing is kept
