## REMOVED Requirements

### Requirement: A follower starts again for its crew only on what it read
**Reason**: Every lasting process of crew's now moves to the installed crew, the follower among them, and one rule governs when any of them starts again for an install. That rule is host-holds-and-updates "A lasting process moves for an install only on what it read". It keeps this requirement's outcome, and moves a process once stuck for one install again once the host installs another, where this requirement never started the follower again for it.
**Migration**: None. The follower's mark `CREW_FOLLOWER_LAGGED` gives way to `CREW_MOVED_TO`, the installed commit it moved for, which every lasting process carries. A follower already running carries neither and reads as never moved.
