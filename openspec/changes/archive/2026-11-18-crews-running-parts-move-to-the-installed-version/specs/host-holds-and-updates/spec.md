## ADDED Requirements

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

## MODIFIED Requirements

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
