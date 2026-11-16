# crew's usage, what crew prints with no command, names the commands crew has and none it removed, a team command
# among them, and each command it removed is refused: crew send names a drive alone, runs on the sender's host, never
# over ssh, its entry pushed from the sending host (record 0068); a landing pushes nothing and levels no host (plan.18);
# a start launches the bolt's base place and makes no branch, a drop drops it last, and crew deletes no branch, a dropped
# bolt's kept by sluice while it holds work main lacks; a bolt lands on the user's send, which crew carries to the
# runner, `crew bolt submit` and `crew main fix --send` refused (Decision 11 of
# crew-lands-each-bolt-through-flumes-base-place); a piece's end is the runner's report alone, the record Flume holds
# for the runner among them, and no landing commit makes a piece merged or a bolt landed (record 0062's stopgap
# retired); a drive's runs, standing or on-demand, and its review's after_changes and after_hours name crew drive set's
# --runs and --review, and nothing names --flume or a drive's flume (record 0064 as amended 2026-11-09). A checkout
# carries the .envrc a person's direnv enters the shell with, and ignores devenv's and direnv's working files and the
# tests' .venv. No case here reads a Markdown file: what README, CLAUDE.md, the skills, the briefs and openspec's
# configuration say is kept by those who write and review them (the family's principle 16, no check reads Markdown).
# Reads: .envrc .gitignore
. "${TESTS:?run crew tests through tests/run, which puts stub herdr, ssh and claude first}/lib.sh" || exit 2
world
usage=$(crew 2>&1 || true)

# the removed crew release <team> by its command: a release is otherwise crew's own, plugin/release.json and crew _release
for gone in assign "crew release" opsx fable explorer verifier coder-; do lacks "$usage" "$gone"; done
for gone in assign release opsx list status up rebuild close restart resume clear down _tidy _status _team; do
  expect_fail "every bolt, unit and chore of the plans" crew $gone swb-1
done
team=$(grep -oE '(^|[^a-z_])crew +(list|status|up|rebuild|close|restart|resume|clear|down)([^a-z]|$)' <<<"$usage" || true)
[[ -z $team ]] || fail "the usage names a team command:"$'\n'"$team"
for gone in "<team or drive>" "(sent to <team" "SLUICE_BRANCH" "sluice_branch" "conductor fresh" "unit slot"; do
  lacks "$usage" "$gone"
done
has "$usage" 'crew send'; has "$usage" '<drive> "<text>"'
has "$usage" "pushed from the sending host"; has "$usage" "never over ssh"
lacks "$usage" "unit approve"; lacks "$usage" "review/<unit>"; has "$usage" "crew review"
for gone in "unit run" "unit wait" "unit free" "chore run" "chore wait" "chore free" "crew needs" "fix <team>"; do
  lacks "$usage" "$gone"
done
for gone in "unit run a code" "unit wait a" "chore free c"; do expect_fail "invalid choice" crew $gone; done
expect_fail "crew: each drive's plan of bolts, its main level of agents in herdr" crew needs "what it needs"
ok "the usage names none of the removed commands or roles, a team command among them, crew drives no stage and waits on none, crew send names a drive alone and runs on the sender's host and never over ssh, its entry pushed from the sending host, and it names crew review"

has "$usage" "crew ops offer <env>"; has "$usage" "[--notes <file>] [--steps <file>]"; has "$usage" "[--ticked <n>[,<n>...]]"
for gone in "crew plan card" "crew card post" "crew card change" "crew card close" "post|change" "propose|proposed|agree|card"; do
  lacks "$usage" "$gone"
done
has "$usage" "crew record"
has "$usage" "session|end <key>"; has "$usage" "read <key>"; lacks "$usage" "session|wait|end"
has "$usage" "crew card wait"; has "$usage" "refused at once, naming"; has "$usage" "beside the run record"
has "$usage" "what an earlier send still lands, with or without a card open"
has "$usage" "preview <key> <thing> [--done]"
expect_fail "invalid choice: 'post'" crew card post land/x
expect_fail "invalid choice: 'card'" crew plan card 1
ok "the usage gives crew ops offer's notes and steps and crew ops approve's ticked steps, crew record and crew card read, session, end and preview, crew card wait refused naming the read, crew card read land/<kit> with no card open, each landing as the runner reports it beside the run record, and no crew plan card or crew card post, change or close, which crew no longer has"

has "$usage" "pushes nothing and levels no host"; has "$usage" "origin/main"; lacks "$usage" "behind GitHub's"
ok "the usage says a landing pushes nothing and levels no host, and a bolt is cut from origin/main"

for want in "base place" "crew/bolt" "holds work main lacks" "lands under the crew that started it" "crew carries"; do
  has "$usage" "$want"
done
for gone in "sluice branch create" "sluice branch delete" "0.20.0" "stays local until it lands" "while main lacks its tip" \
  "have sluice delete" "standing in sluice" "landing queued as" "submitted only once crew reads them" "wt submit main"; do
  lacks "$usage" "$gone"
done
has "$usage" "start, the user's or a proposal's, makes no branch and reads no host"
has "$usage" "drop drops each"; has "$usage" "last its base place's"
has "$usage" "refused at once, before it reads anything, with any arguments"; has "$usage" "refused at once, before it reads anything, naming the way: a fix of main lands on"
ok "the usage says a start launches the bolt's base place and makes no branch, a drop drops it last, crew deletes no branch, a dropped bolt's kept while it holds work main lacks, a bolt started before lands under its crew, and a bolt and a fix of main land on the user's send, which crew carries to the runner, crew bolt submit and crew main fix --send refused"

has "$usage" '<bolt> <name> "<what is wrong>"'; has "$usage" "start"; has "$usage" "started already"; has "$usage" "waits to land"
for gone in "bolt give" "crew bolt give" "one more" "a give" "never refused for the bolts" "plan agree" "dispatch" "agreement"; do
  lacks "$usage" "$gone"
done
has "$usage" "bolt start"
expect_fail "unrecognized arguments: --merge" crew fix tenant-environments edge --merge
ok "the usage says a bolt's work is started by crew bolt start, refused for one started already, and names no give, agreement or dispatcher, a proven bolt waits to land, and crew fix names its bolt, with no --merge or --wait"

for want in "version 6, which lists no team" "version 2, 3, 4 or 5 among them" 'its drives under `drives`' "in Flume stream" "Path: flume" "no team's conductor, ops or slot" \
  "requests.rec" "<label>/runner/<host>" "crew answer" "fix <kit> <name> --send"; do has "$usage" "$want"; done
for gone in "due to cross" "due back" "however they went down" "closes what the hold left" "crossed team" "version 3 of the teams file" \
  "Version 3 of the teams file" "version-2 file" "version 4 names" "version 4 of the teams file" "at version 2 or 3" "versions 2 and 3" \
  "<team|label>" "version 5, which lists no team" "<partition>"; do lacks "$usage" "$gone"; done
lacks "$usage" "bolt teams"
has "$(head -1 <<<"$usage")" "crew: each drive's plan of bolts, its main level of agents in herdr, and its bolts' work in Flume."
ok "the usage says the teams file is version 6, its drives under drives, and lists no team, an older one refused, that crew runs no team's agents, its launches in requests.rec and its runner's branch, crew answer and crew main fix, no team due to cross or crossing, and opens on the plan and the main level"

has "$usage" "runs as its kind"
has "$usage" "role in its drive's runs' own word: standing, with its agent's status, or"
for want in "every role stands" "asks.rec" "roles.rec" "crew-<role>--<label>" "end --report <path>" \
  "open <role>" "land <repo> <name> --brief-file <file>" "delivered [--label L]" "pendingyou watch -- crew _answered" \
  "ended at its next stop" "never restarted" "turns/<role>.md"; do has "$usage" "$want"; done
ok "the usage says a drive's runs, a role that runs on demand, main status's in the file's own words, its asks in asks.rec and its record in roles.rec, crew role start, end, open and land, crew review delivered, the follower's notice of a card's change, and a standing agent of such a role ended at its stop"

has "$usage" "--runs <role> standing|on-demand"; has "$usage" "--review <after_changes> <after_hours>"
for gone in "--flume" 'its `flume`' 'names `flume` on every drive' '`every` changes' "<every> <hours>"; do lacks "$usage" "$gone"; done
ok "the usage names crew drive set's --runs and --review <after_changes> <after_hours>, and no --flume or drive's flume"

for want in "piece's end is the runner's report alone" "the record Flume holds for the runner"; do has "$usage" "$want"; done
for gone in "Sluice-From" "names its place's branch" "landed on its bolt at" "main holds its landing"; do lacks "$usage" "$gone"; done
has "$usage" "no landing commit on its kit's main read for it"
ok "the usage says a piece's end is the runner's report alone, the record Flume holds for the runner among them, names no landing commit as what makes a piece merged or a bolt landed, and reads none on main for crew bolt land"

lacks "$usage" "herdr-hosts"; lacks "$usage" "hosts file"
lacks "$usage" "below its tip"; lacks "$usage" "below the tip"
ok "the usage names no swancloud hosts file and no read below the tip"

grep -qxF 'use devenv' "$CREW/.envrc" || fail ".envrc does not enter devenv"
for line in .devenv/ .direnv/ '!.envrc' tests/.venv/; do grep -qxF -- "$line" "$CREW/.gitignore" || fail ".gitignore lacks $line"; done
ok "a checkout carries the .envrc and ignores devenv's and direnv's working files and the tests' .venv"

# A proven bolt not marked to stay lands on proof, a bolt is marked to stay by --stays and the mark lifted by crew bolt
# unstay, and a hold is put and lifted by crew plan hold and crew plan go (a-proven-bolt-lands-on-proof, Decision 8).
for want in "lands on proof" "--stays" "unstay" "plan  hold" "plan  go"; do has "$usage" "$want"; done
lacks "$usage" "bolt lands on the user's send of its row on its kit's landings card"
ok "the usage says a proven bolt not marked to stay lands on proof, and names --stays, crew bolt unstay, crew plan hold and crew plan go"
