## ADDED Requirements

### Requirement: A restart's wait reads only what its readiness needs
While a restart waits for its agent to be idle, crew SHALL judge whether the agent is due once, at its first look, and again only once crew's record of the agent's start moves. Each other look SHALL read only herdr's reading of the agent, its question mark and the lines its transcript gained since the look before, building no brief and reading nothing of the plan. A task's command SHALL be found once.

#### Scenario: An agent that stays busy
- **WHEN** boomdrive-planner is due and runs background work of its own through the whole of its restart's wait
- **THEN** whether it is due is judged once, at the wait's first look, and the wait ends saying it is not restarted, its next turn's end handing it back

#### Scenario: A look reads what the session wrote since
- **WHEN** a restart's wait looks again at an agent whose transcript has gained lines since its last look
- **THEN** it reads only those lines, and a line Claude Code is still writing is read once it is whole

#### Scenario: A start since
- **WHEN** a due agent is started again while its restart waits, so crew's record of its start moves
- **THEN** the wait judges it again, and ends saying it is not due a restart where the new start runs crew as it now is

#### Scenario: A task's command
- **WHEN** an agent's restart waits while a task it started in the background goes on
- **THEN** the task's command is found once in the call that started it, and a task started since is found at the next look
