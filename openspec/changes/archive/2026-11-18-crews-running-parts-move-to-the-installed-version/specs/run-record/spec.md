## ADDED Requirements

### Requirement: A followed record that moves prints each entry once
When `crew events --follow` starts again through the installed command, it SHALL hand its new process the day its follow began and the tip of each drive's branch it last printed to. The new process SHALL take what each handed tip holds as printed, and print each entry after it once. Where a handed tip can't be read, it SHALL say so once and follow that drive from its branch as it stands.

#### Scenario: An entry arrives while the follow moves
- **WHEN** `crew events --follow --label wldn` starts again through the installed command, and an entry reaches wldn's branch after its last read and before its new process's first
- **THEN** the new process prints that entry once, and prints no entry the old process printed

#### Scenario: A handed tip crew can't read
- **WHEN** the tip the follow handed on for wldn is not in crew's cache of wldn's state repository
- **THEN** the new process says once that it can't read where the follow was, and follows wldn from its branch as it stands, printing nothing of what is there

#### Scenario: A follow with nothing handed
- **WHEN** `crew events --follow --label wldn` starts with nothing handed to it
- **THEN** its first read of wldn's branch prints nothing, as before
