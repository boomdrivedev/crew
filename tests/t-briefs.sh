# Every brief prints for its drive's main level with no token left unfilled, standing or on-demand, and none for a team,
# a dispatcher or a retired role (Decision 2 of the-team-machinery-leaves); what the teams file gives a drive reaches
# its briefs: each role's session and account, its main level's host's checkouts and folders, a runner host's kept
# repositories, whether the host is a Mac, and how the drive runs each role. What a brief says is kept by those who
# write and review it, and no case here pins its words (the family's principle 16, no check reads Markdown).
# Reads: plugin/roles/
. "${TESTS:?run crew tests through tests/run, which puts stub herdr, ssh and claude first}/lib.sh" || exit 2
world
# wldn's plan names three kits, which its main level's host, the box, keeps (Decision 3 of the-team-machinery-leaves).
blueprints WilldanGroup/willdan-blueprints >/dev/null; crew state init wldn >/dev/null
for k in atlas breadboard switchboard; do crew bolt new "$k-work" "Work in $k-kit." --repo "$k-kit" --label wldn >/dev/null; done
for role in conductor ops construct coder verify dispatcher fable; do
  expect_fail "no definition '$role' for a main level. definitions: design planner main-ops operator reviewer" crewpy brief wldn $role
done
expect_fail "no drive 'swb-1'. drives: wldn madswan swancloud" crewpy brief swb-1 planner
for gone in fable explorer verifier conductor ops dispatcher construct coder verify; do
  [[ ! -e $CREW/plugin/roles/$gone.md ]] || fail "the retired role $gone is still there"
done
ok "no brief prints for a team, a dispatcher or a retired role"

unfilled() { [[ $out =~ \{\{[A-Z_]+\}\} ]] && fail "roles/$1.md left ${BASH_REMATCH[0]} unfilled${2:+ $2}"; return 0; }
for role in design planner main-ops operator reviewer; do
  expect_ok crewpy brief wldn $role; unfilled $role
  echo "$role: $(wc -c <<<"$out" | tr -d ' ') characters"
done
ok "every main-level brief prints for wldn with no unfilled token"

# Each role's session is named with the account the drive's `accounts` gives the role (record 0064), read from the
# teams file alone: wldn's every role in wldn-3 on credits; with its planner and reviewer on ia in wldn-1, those two
# there on ia.
for r in design planner ops operator reviewer; do has "$out" "\`wldn-$r\` in session wldn-3 (account credits)"; done
edit teams "$(part wldn)['roles'] = {'planner': {'session': 'wldn-1'}}; $(part wldn)['accounts'].update(planner='ia', reviewer='ia')"
expect_ok crewpy brief wldn design
for r in planner reviewer; do has "$out" "\`wldn-$r\` in session wldn-1 (account ia)"; done
for r in design ops operator; do has "$out" "\`wldn-$r\` in session wldn-3 (account credits)"; done
fixtures
ok "a brief names each role's session with the account the drive's accounts gives it"

# A brief names the checkouts its main level's host keeps, with their folders (Decision 7 of
# a-kept-repositorys-folder-is-the-runners-container), and in words one the host keeps none of (teams.10).
w=$(space chuck-herdr-alpha willdan)
expect_ok crewpy brief wldn design
for at in "$w/willdan-blueprints/main" "$w/willdan-blueprints" "$w/atlas-kit/main" "$w/atlas-kit"; do has "$out" "\`$at\`"; done
sc=$(space mac-studio madswan)/swancloud
expect_ok crewpy brief madswan operator
has "$out" "\`$sc/main\`"; has "$out" "\`$sc\`"
HOST=chuck-herdr-alpha expect_ok crewpy brief wldn operator
has "$out" "swancloud's checkout, which chuck-herdr-alpha does not keep"; lacks "$out" "$sc"
ok "a brief names its main level's host's checkouts and folders, and in words one the host keeps none of"

# Whether the host the brief is built on is a Mac is read from the teams file's hosts (teams.10): a Mac opens a site in
# terminal-browser, a box does not.
expect_ok crewpy brief wldn operator; has "$out" "terminal-browser open <url> --split right"
HOST=chuck-herdr-alpha expect_ok crewpy brief wldn operator; lacks "$out" "terminal-browser open"
ok "a brief built on a Mac opens sites in terminal-browser and one built on a box does not"

# How a main-level role's work reaches it follows its drive's `runs` (design Decision 9): an on-demand role's brief names
# crew role start and end, a standing one's neither, and every brief fills for a drive running all five on-demand.
for role in design planner reviewer main-ops operator; do
  expect_ok crewpy brief wldn $role; lacks "$out" "$CREW/plugin/bin/crew role start"
done
for r in design planner reviewer ops operator; do role_runs wldn $r on-demand; done
for role in design planner reviewer main-ops operator; do
  expect_ok crewpy brief wldn $role; unfilled $role "for a drive running all five on-demand"
  has "$out" "$CREW/plugin/bin/crew role start"; has "$out" "$CREW/plugin/bin/crew role end"
done
for r in design planner reviewer ops operator; do role_runs wldn $r standing; done
ok "a brief names crew role start and end where its drive runs the role on-demand, and not where it stands, every brief filled for a drive running all five on-demand"

# A runner host's teams file names its kept repositories (record 0061; Decision 7 of
# a-kept-repositorys-folder-is-the-runners-container): built there, the design agent's brief names its blueprints
# checkout and each kit's at the runner's view with the runner's container as its folder, and the operator's names
# swancloud's, and neither names the drive's own folder for them.
blueprints afterthought/blueprints >/dev/null; blueprints agentplot/blueprints >/dev/null; crew state init madswan >/dev/null
crew bolt new crew-work "Work in crew." --repo crew --label madswan >/dev/null
r=/Users/chuck/.local/share/flywheel/repositories; v=/Users/chuck/Code/boomdrive
tf=$(home_of mac-studio)/.config/crew/teams.json
jq --arg r "$r" --arg v "$v" '.repositories = ({} | reduce ("afterthought/blueprints", "agentplot/crew", "afterthought/swancloud") as $a
  (.; .[$a] = {dir: "\($r)/\($a)", checkout: "\($v)/\($a)"}))' "$tf" > "$tf.new" && mv "$tf.new" "$tf"
expect_ok crewpy brief madswan design; unfilled design "on a runner host"
for at in "$v/afterthought/blueprints" "$r/afterthought/blueprints" "$v/agentplot/crew" "$r/agentplot/crew"; do has "$out" "\`$at\`"; done
lacks "$out" "$(space mac-studio madswan)"
expect_ok crewpy brief madswan operator; unfilled operator "on a runner host"
for at in "$v/afterthought/swancloud" "$r/afterthought/swancloud"; do has "$out" "\`$at\`"; done
lacks "$out" "$(space mac-studio madswan)/swancloud"
teams_json mac-studio > "$tf"
ok "on a runner host the design agent's and the operator's briefs name the teams file's checkouts with the folders it gives"
