#!/usr/bin/env python3
"""crew ops: the operations on a drive's environments, a deploy being one kind (plan.14, ADR 0012).

A deploy is the act of a kit's deployer, or of a hosted CI/CD standing in for it, under each environment's policy; crew
gates a `manual` one on the user's word and records it. Every other operation, a command after a deploy, a restart, a
check, is a step: done by an agent it is handed to or by the user, recorded with its state, and tied to a deploy only
when it names one.

  crew ops offer <env> --label L --to <sha> --from <sha|none> [--notes <file>] [--steps <file>]
      a deploy of a commit, offered for a `manual` environment: a row under *operations* on the rail, deploy/<env>,
      and its card, which crew raises in main-level ops's name and tells it the line that adopts. On its face the
      kit's release notes for the range, --notes, as its changelog tool wrote them, and the range's steps, --steps,
      one a line as the deployer gathers them (step <n> <doer> <when> <environments> <why> <text>, tab-separated,
      held among the when words for an agent's step held for the user's word, before for a step of the user's the
      deploy waits on, which the card lists first, done, every other step after the deploy); handed no notes, the landings it carries: the first-parent commits
      of the kit's main from --from to --to, read with git, a landing of sluice's by the branch it merged. Run away
      from the main level's host, it carries the files' text there. The same `to` again records no second offer: it
      posts the card again when main-level ops holds none open, as when Pending You refused its post, changes the card
      in place when it is handed other notes or steps, and otherwise changes nothing; a newer one replaces it and
      changes its card. A deploy that waits on a step of the user's has no card while that step is open: its row
      names the step's card, a card left unanswered is withdrawn, and its card is raised once each step is done
  crew ops approve <env> --label L --to <sha>
      the user's word for that deploy, given by holding its card, recorded by whoever the user's yes reached; the row
      leaves the rail. Refused, nothing recorded but the refusal, while a step of the user's the deploy waits on is
      open, naming each step and its card
  crew ops word <env> --label L
      the commit the user's word was given for, exit 0; exit 1 when there is none. A word is for one deploy: once that
      deploy's end is recorded, or the end of a newer deploy of the environment, one started after the word was given,
      there is none until the user approves a new offer
  crew ops record <env> --label L --to <sha> --act start|step|end [--from <sha|none>] [--step machine|guests|suite]
                  [--outcome ok|failed|done] [--log <path>] [--rows <json file>] [--does <words>]
      a deploy's start, one of its steps, or its end, in the run record as it runs; its end, when it ends the word,
      closes the deploy's card with each step's outcome, or the step that failed and its log, naming the deploy when
      it is a newer one than the word's, then, where the end was handed --does, the deployer's words of what the user
      does
  crew ops step <env> --label L --key <key> --state waiting|handed|done|failed|declined [--to <sha>]
                [--doer main-ops|user] [--agent <name>] [--when deployed|quiet] [--held] [--text <file>]
                [--changes <a,b>] [--note <text>]
      an operation of its own and its state, after the deploy it names with --to or on its own; one the user is to
      take, or an agent's held for the user's word, that waits is a rail row with a card, which crew raises one at a
      time on an environment, each following the one before, and closes when no step it names still waits. The
      user's steps under one key on several environments are one row and one card, naming each host and counted as
      the open step card on each; a host's step joining or leaving changes it in place while the user has not
      answered it. A user's step in the words of a step the environment's open offer waits on is recorded as one
      (before among its when words), and the deploy's card is raised once it is done. Recorded again while its card
      is open, the card is changed in place when its words, doer or hold differ, and the line that adopts it is
      printed either way. The text's field lines, `- why:`, `- where:`, `- command:`
      (one a command) and `- done:`, are the card's. Run away from the main level's host, it carries the text there
  crew ops settle <op/env/n> --label L --state done|declined
      the user's answer on a step's card, its row's done or decline: the state recorded on every step the card named
      at its last post or change that still waits, or the row's with no card, each under its own environment, deploy
      and key, its when words kept; the card closed once; then each environment's next step card raised, and each
      deploy the step released. Refused, nothing recorded, for a key no step's row or card holds
  crew ops steps <env> --label L --json
      the latest state of every step on the environment: [{to, key, state, by, at, note}], to empty for a step that
      names no deploy
  crew ops quiet <env> --label L
      exit 0 when no Flume place of the drive's has a stage working on the environment's host, as its runner there
      carries Flume's status, and no test of crew's runs there; exit 1 saying what is

Every command acts on the drive's operations where its main level runs, on that host's run record, as ops.*
entries on env/<env>: run anywhere else, it is run there, as the one asking. An environment is a machine of the fleet,
named as the deployer names it.
"""
import argparse, datetime, json, pathlib, re, subprocess, sys

LIB = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(LIB))
import crew  # noqa: E402
import record  # noqa: E402
import runner  # noqa: E402
from crew import Refusal, fail  # noqa: E402

NAME = re.compile(r"^[a-z0-9][a-z0-9-]*$")
SHA = re.compile(r"^[0-9a-f]{7,40}$")
STEP_KEY = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/#-]*$")
STEP_CARD = re.compile(r"^op/[a-z0-9][a-z0-9-]*/[0-9]+$")  # a step's row and card key, which crew ops settle answers
ACTS = ("start", "step", "end")
STATES = ("waiting", "handed", "done", "failed", "declined")
DOERS = ("main-ops", "user")
DAYS = 60  # how far back the operations are read: an offer, a word or a step older than this has no row


def entries(label, days=DAYS):
    """The ops entries of the drive's run record on this host, oldest first."""
    since = (datetime.datetime.now(datetime.timezone.utc).date() - datetime.timedelta(days=days)).isoformat()
    d = record.ROOT / label / "runs" / crew.this_host()
    out = []
    for f in sorted(d.glob("*.rec")) if d.is_dir() else []:
        if f.stem >= since:
            out += [e for e in record.parse(f.read_text()) if (e.get("Act") or "").startswith("ops.")]
    return sorted(out, key=lambda e: (e["At"], e["Id"]))


def env_of(e):
    return next((o[4:] for o in e.get("On", []) if o.startswith("env/")), None)


def spends(word, to, started):
    """Whether a deploy's end of to spends the word, the user's approve entry or None (plan.14): the end of a deploy of
    the word's own head, or of a newer one, a deploy whose start is recorded after the word was given (started, the
    heads whose deploys started since). A deploy that was running when the word was given, or whose start the record
    lacks, is no newer one, and the word stands (read.1)."""
    return bool(word) and (word.get("Head") == to or to in started)


def state(es):
    """Each environment's operations as the record holds them: its deploy offer still open (unanswered, no deploy of
    it ended), {env: entry}; the word the user gave that no deploy's end has spent since (spends), {env: entry}; and
    each step's latest entry, {(env, to or "", key): entry}, in the order of each step's first entry."""
    offers, words, steps, started = {}, {}, {}, {}
    for e in es:
        env, act, to = env_of(e), e["Act"], e.get("Head")
        if not env:
            continue
        if act == "ops.offer":
            offers[env] = e
        elif act == "ops.approve" and not e.get("Refused"):
            words[env], started[env] = e, set()
            if offers.get(env, {}).get("Head") == to:
                offers.pop(env)
        elif act == "ops.deploy" and e.get("Phase") == "start":
            started.setdefault(env, set()).add(to)
        elif act == "ops.deploy" and e.get("Phase") == "end":
            if spends(words.get(env), to, started.get(env, ())):
                words.pop(env)
            if offers.get(env, {}).get("Head") == to:
                offers.pop(env)
        elif act == "ops.step":
            steps[(env, to or "", e.get("Key"))] = e
    return offers, words, steps


def ordered(steps):
    return sorted(steps.items(), key=lambda kv: (kv[1]["At"], kv[1]["Id"]))


def numbered(steps):
    """Each step with its number among its environment's steps, counted in the order each was first recorded, so a
    step's number never changes when another's state does: [(n, (env, to, key), latest entry)]."""
    n, out = {}, []
    for k, e in steps.items():
        n[k[0]] = n.get(k[0], 0) + 1
        out.append((n[k[0]], k, e))
    return out


def held(e):
    """Whether a step is held for the user's word: held among its when words, as the deployer marks it."""
    return "held" in (e.get("When") or "").split()


def waits_on_user(e):
    """Whether a step's latest entry waits on the user: theirs to take, or an agent's held for their word."""
    return e.get("State") == "waiting" and (e.get("Doer") == "user" or held(e))


BEFORE = "before"  # a step the deploy waits on, among the when words as the deployer marks it (swancloud record 0038)


def waits_before(e):
    """Whether a recorded step is one the deploy of its environment waits on: before among its when words, as crew
    records a user's step in the words of a step the open offer was handed marked so (marked_before)."""
    return BEFORE in (e.get("When") or "").split()


def groups(es):
    """The drive's steps that wait on the user, as the rail's rows and their cards carry them (record 0070), from its
    ops entries (es, oldest first), in the order each group's first step was first recorded: each {key, steps:
    [(n, (env, to, key), latest entry)], shared}. The user's steps waiting under one key, the deployer's identity of a
    step, on any environment and under any deploy, are one group, shared; an agent's step held for the user's word and
    a gate's step (gate_of) are each a group of their own, since when a host is quiet, and a deploy's click at its
    gate, are each one environment's. crew compares no words for it (Decision 1)."""
    out, by_key = [], {}
    for n, k, x in numbered(state(es)[2]):
        if not waits_on_user(x):
            continue
        if x.get("Doer") == "user" and not gate_of(x):
            if k[2] in by_key:
                by_key[k[2]]["steps"].append((n, k, x))
                continue
            by_key[k[2]] = g = dict(key=k[2], steps=[(n, k, x)], shared=True)
        else:
            g = dict(key=k[2], steps=[(n, k, x)], shared=False)
        out.append(g)
    return out


def head_word(k):
    """A step as a step card's Heads names it: <env>@<to>, or <env> for a step that names no deploy."""
    return f"{k[0]}@{k[1]}" if k[1] else k[0]


def shown_heads(entries, card):
    """The Heads of a card's last post or change the run record holds done, as words; None when it records none, as a
    card posted before crew recorded a step card's heads."""
    heads = None
    for e in entries:
        if e.get("Act") in ("card.post", "card.update") and e.get("Card") == card and not e.get("Refused"):
            heads = e.get("Heads")
    return heads.split() if heads else None


def key_step(nsteps, key):
    """The step a step card's key, op/<env>/<n>, numbers, (env, to, key), from the numbered steps; None for none."""
    _, env, n = key.split("/")
    return next((k for m, k, _ in nsteps if k[0] == env and str(m) == n), None)


def card_steps(es, entries, key, card):
    """The steps the step card under key names, {(env, to, key)}, from the drive's ops entries and the card entries
    (entries): each word of the Heads its last post or change recorded, under the deployer's key of the step its own key
    numbers; that step alone for a card recording no Heads, which is all it showed (read.1); none when its key numbers no
    step."""
    mine = key_step(numbered(state(es)[2]), key)
    if not mine:
        return set()
    words = shown_heads(entries, card)
    return {(w.partition("@")[0], w.partition("@")[2], mine[2]) for w in words} if words else {mine}


def step_cards(es, entries):
    """Each step card the run record shows open, oldest first, from the drive's ops entries and the card entries
    (entries): {key, card, by, named, envs}, named the steps it names (card_steps), envs the environments its Heads
    name, its key's alone when it records none, on each of which it is the open step card (record 0031 §5)."""
    import cards  # its decisions only: what the run record shows posted and closed
    out = []
    for c in cards.posted_cards(entries):
        if c["state"] is None and re.fullmatch(r"op/[a-z0-9][a-z0-9-]*/\d+", c["key"]):
            words = shown_heads(entries, c["card"])
            envs = list(dict.fromkeys(w.partition("@")[0] for w in words)) if words else [c["key"].split("/")[1]]
            out.append(dict(c, named=card_steps(es, entries, c["key"], c["card"]), envs=envs))
    return out


def group_key(group, opened):
    """A group's rail row key (Decision 2): the key of the open step card (opened, step_cards') that names any of its
    steps, the one naming its earliest-recorded step when several do, as the cards from before record 0070 each named
    one host's; with none open, op/<env>/<n> of its first-recorded step."""
    order = [k for _, k, _ in group["steps"]]
    hits = [(min(order.index(s) for s in o["named"] if s in order), o["key"]) for o in opened if any(s in order for s in o["named"])]
    if hits:
        return min(hits)[1]
    n, k, _ = group["steps"][0]
    return f"op/{k[0]}/{n}"


def keyed(es, entries=()):
    """Each step that waits on the user to the key of the row that carries it, {(env, to, key): row key}, from the
    drive's ops entries and the card entries (group_key)."""
    opened = step_cards(es, entries)
    return {k: key for g in groups(es) for key in [group_key(g, opened)] for _, k, _ in g["steps"]}


def words_of(text):
    """A step's words as crew compares them: all its text says before its first field (step_words), each run of
    spaces, line breaks among them, one space, so a step recorded with its why or its commands is tied by its words
    alone."""
    return step_words(text)[0]


def waited_on(handed, es, env):
    """The steps the open offer's deploy of env waits on (swancloud record 0038, record 0059), from the steps it was
    handed (handed_steps') and the drive's ops entries (es, oldest first): each handed step marked before, in the
    order handed, with the user's step the record holds on env in the same words (words_of), the one whose latest
    entry is newest when several are: each {n, text, why, to, key, state}, its to, key and state None while its
    deployer has not recorded it, and done once its state is done."""
    steps, worded = state(es)[2], {}
    for e in es:
        if e.get("Act") == "ops.step" and env_of(e) == env and e.get("Text") and e.get("Doer") == "user":
            worded[(env, e.get("Head") or "", e.get("Key"))] = words_of(e["Text"])
    out = []
    for s in handed or []:
        if not s.get("before"):
            continue
        mine = [(k, steps[k]) for k, w in worded.items() if w == words_of(s["text"]) and k in steps]
        k, latest = max(mine, key=lambda kv: (kv[1]["At"], kv[1]["Id"])) if mine else (None, None)
        out.append(dict(n=s["n"], text=s["text"], why=s.get("why"), to=(k[1] or None) if k else None, key=k[2] if k else None,
                        state=latest.get("State") if latest else None))
    return out


def marked_before(doer, text, handed):
    """Whether a step recorded now is one the open offer's deploy waits on (record 0059): the user's, in the words of a
    step the offer was handed marked before (handed_steps'). The deployer records such a step as it records any
    user's step, with no mark (swancloud's record_waited), so crew carries the offer's mark onto the record by the
    step's words."""
    return doer == "user" and bool(words_of(text)) and any(s.get("before") and words_of(s["text"]) == words_of(text) for s in handed or [])


def deploy_waits(es, env, handed=None):
    """The steps of the user's that env's open offer waits on and that are not done (swancloud record 0038, record
    0070), from the drive's ops entries: from the steps the offer was handed (handed, handed_steps'), each it waits on
    as waited_on reads it; handed None, where the offer's files are not kept on this host, each user's step recorded on
    env marked before that still waits. Each {text, k, state}, k its (env, to, key), None while its deployer has not
    recorded it."""
    if handed is not None:
        return [dict(text=w["text"], k=(env, w["to"] or "", w["key"]) if w["key"] else None, state=w["state"])
                for w in waited_on(handed, es, env) if w["state"] != "done"]
    return [dict(text=step_words(x.get("Text"))[0] or k[2], k=k, state=x.get("State")) for k, x in state(es)[2].items()
            if k[0] == env and x.get("Doer") == "user" and waits_before(x) and x.get("State") in WAITING]


def waits_said(env, waits, rowed):
    """The steps a deploy waits on as its row, its refusal and its withdrawal name them (deploy_waits'): each by its
    words and the card it is asked on (rowed, keyed's), or that its deployer has not recorded it on env yet, or the
    state it is recorded in."""
    import cards  # its words only
    said = []
    for w in waits:
        words = f'your step "{cards.by_words(w["text"], 60)}"'
        said.append(f"{words}, asked on {rowed[w['k']]}" if w["k"] in rowed else
                    f"{words}, which its deployer has not recorded on {env} yet" if not w["k"] else
                    f"{words}, recorded {w['state']}")
    return cards.joined(list(dict.fromkeys(said)))


def offers_handed(label, es):
    """The steps each open offer was handed, {env: steps}, read from the files kept beside it where this host keeps
    them, the drive's main level's alone (kept); an environment whose offer's files are not on this host is left out,
    its waits read from the record's marks (deploy_waits). A file crew can't read is left out the same way. No offer
    open, nothing is read."""
    out = {}
    for env, offer in state(es)[0].items():
        d = kept(label, env, offer["Head"])
        steps, why = handed_steps(kept_text(d / "steps.txt"), env, label) if d.is_dir() else (None, "not kept here")
        if why is None:
            out[env] = steps
    return out


def rows(fleet, label, es, entries=(), handed=None):
    """The rail's rows for the drive's operations, from its ops entries (es) and its card entries on the main level's
    host (entries): each open deploy offer, deploy/<env>, answered by crew ops approve, but one waiting on a step of the
    user's, which names that step's card, or that its deployer has not recorded it yet, and owes no card while it is
    open (asks false), its card raised once each is done (deploy_waits, from the steps each offer was handed, handed,
    {env: steps}, where known); and each group of steps that waits on the user (groups), keyed by the card that carries
    it or by its first-recorded step's op/<env>/<n> (group_key), the user's answered by crew ops settle on every
    environment its card names, an agent's held for their word by marking it done or declined, a gate's step
    (gate_of) said as the deploy waiting at its gate for the user. Each row's card is raised by crew in main-level ops's
    name (briefs.11); a step's row carries the heads its card names (head_word) and the deployer's key of its step."""
    import cards  # its words only
    offers, _, _ = state(es)
    rowed = keyed(es, entries)
    out = []
    for env, e in sorted(offers.items()):
        to, base = e["Head"], e.get("Base") or "none"
        waits = deploy_waits(es, env, (handed or {}).get(env) if env in (handed or {}) else None)
        head = f"deploy {env} ({label}) to {to[:7]}, from {base[:7] if base != 'none' else 'nothing deployed'}: "
        what = [head + (f"it waits on {waits_said(env, waits, rowed)}, and crew raises its card in {label}-ops's name once "
                        f"{'that is' if len(waits) == 1 else 'each is'} done" if waits else
                        f"crew raises its card in {label}-ops's name, and holding it is the word to deploy")]
        out.append(dict(group="operations", label=label, key=f"deploy/{env}", at=e["At"], what=what,
                        cmds=[("answer", f"crew ops approve {env} --to {to} --label {label}")], **({"asks": False} if waits else {})))
    opened = step_cards(es, entries)
    for g in groups(es):
        key = group_key(g, opened)
        n, (env, to, k), e = g["steps"][0]
        link = gate_of(e)
        if link:
            deploy = f"the deploy of {env} to {to[:7]}" if to else f"a deploy of {env}"
            what = [f"{deploy} waits at its gate ({label}), yours to approve there: {link}"]
        else:
            hosts = list(dict.fromkeys(s[0] for _, s, _ in g["steps"]))
            after = (f"on {cards.joined(hosts)}" if len(hosts) > 1 else f"after the deploy of {env} to {to[:7]}" if to else f"on {env}")
            whose = ("yours to do" + (", one answer settling it on each" if len(hosts) > 1 else "") if e.get("Doer") == "user"
                     else f"{e.get('Agent') or e.get('Doer')}'s, held for your word")
            what = [f"an operation {after} ({label}), {whose}: {e.get('Text') or k}"]
        if g["shared"]:
            cmds = [(s, f"crew ops settle {key} --state {'done' if s == 'done' else 'declined'} --label {label}") for s in ("done", "decline")]
        else:
            to_arg = f" --to {to}" if to else ""
            cmds = [(s, f"crew ops step {env}{to_arg} --key {k} --state {'done' if s == 'done' else 'declined'} --label {label}")
                    for s in ("done", "decline")]
        out.append(dict(group="operations", label=label, key=key, at=e["At"], what=what, cmds=cmds,
                        heads=[head_word(s) for _, s, _ in g["steps"]], step=k))
    return out


WAITING = ("waiting", "handed", "failed")  # a step in one of these states is an operation still waiting


def landings(es):
    """The drive's landings, from its bolt.land entries not refused, oldest first: each {bolt, units, at, by, repo,
    head}, the kit it landed on, its Repo as written, and the commit that kit's main held afterwards, None where the
    entry has none."""
    out = []
    for e in es:
        bolt = next((o[5:] for o in e["On"] if o.startswith("bolt/")), None) if e.get("Act") == "bolt.land" and not e.get("Refused") else None
        if bolt:
            out.append(dict(bolt=bolt, units=[o[5:] for o in e["On"] if o.startswith("unit/")], at=e["At"], by=e.get("By"),
                            repo=e.get("Repo"), head=e.get("Head")))
    return out


def carried(to, frm, lands):
    """The bolts a deploy from frm to to carried, from the landings (oldest first): the landings on the kit whose main
    one of them left at to, after the one that left it at frm, up to that one; every one up to it when frm is none,
    nothing having been deployed. ([bolts], None), or (None, why) when the record holds no landing at to or at frm, so
    which landings the deploy carried can't be read from it (read.1)."""
    at = next((i for i, l in enumerate(lands) if l["head"] and l["head"] == to), None)
    if at is None:
        return None, f"{to[:7]} is no landing's commit in the record"
    mine = [l for l in lands[:at + 1] if l["repo"] == lands[at]["repo"]]
    if frm in (None, "", "none"):
        return [l["bolt"] for l in mine], None
    start = next((i for i, l in enumerate(mine) if l["head"] == frm), None)
    if start is None:
        return None, f"{frm[:7]} is no landing's commit in the record"
    return [l["bolt"] for l in mine[start + 1:]], None


# How crew reads a deploy's range on its kit's main: each first-parent commit, its parents, its subject, and the
# trailers sluice writes on a landing's merge commit, its submission and the branch and pull request it merged.
RANGE = "%H%x1f%P%x1f%s%x1f%(trailers:key=Sluice-Submission,valueonly,separator=%x20)%x1f%(trailers:key=Sluice-From,valueonly,separator=%x20)"
PULL = re.compile(r"\(pull/(\d+)\)")


def first_parents(text):
    """The commits git log --first-parent prints in RANGE's form, newest first: each {sha, parents, subject, landed
    (sluice's submission, or None for a commit sluice did not land), pr (the pull request it merged, or None)}; None
    when a line is not in that form (read.2)."""
    out = []
    for line in (text or "").splitlines():
        f = line.split("\x1f")
        if len(f) != 5 or not SHA.match(f[0]):
            return None
        pr = PULL.search(f[4])
        out.append(dict(sha=f[0], parents=f[1].split(), subject=f[2], landed=f[3].strip() or None, pr=int(pr.group(1)) if pr else None))
    return out


def range_landings(commits, merged, lands):
    """The landings a deploy's range carries, oldest first, as its card names them ({pr, subject}): each first-parent
    commit of the kit's main in the range (commits, newest first, as first_parents reads them), by the bolt where the
    record holds a landing at it (lands), which git does not name; else, for a landing of sluice's, by the subject of
    the branch it merged (merged: {sha: subject} of each landing's second parent); else by its own subject."""
    out = []
    for c in reversed(commits):
        bolt = next((l["bolt"] for l in lands if l["head"] == c["sha"]), None)
        branch = merged.get(c["parents"][1]) if c["landed"] and len(c["parents"]) > 1 else None
        out.append({"pr": c["pr"], "subject": bolt or branch or c["subject"]})
    return out


def kit_range(fleet, label, frm, to):
    """What a deploy from frm to to carries on its kit's main, read with git on this host, the drive's main level's,
    in the main checkouts the teams file keeps on that host (crew.kept: the file's checkout where it names the repo for
    this host, else the one in the folder of a drive there that lists it): the kit is the one that holds to. (commits, merged)
    as range_landings takes them, and None; or (None, None, why) naming what git could not read (read.1)."""
    import plan
    p = crew.drive_of(fleet, label)

    def git(where, *args):
        return subprocess.run(["git", "-C", where, *args], capture_output=True, text=True, env=plan.gitenv())
    held = [m for m in (k["main"] for k in crew.kept(fleet, p["machine"]))
            if pathlib.Path(m).is_dir() and git(m, "cat-file", "-e", f"{to}^{{commit}}").returncode == 0]
    if len(held) != 1:
        return None, None, (f"{to[:7]} is a commit of {len(held)} kits {label}'s main level keeps on {p['machine']}" if held
                            else f"{to[:7]} is a commit of no kit {label}'s main level keeps on {p['machine']}")
    r = git(held[0], "log", "--first-parent", f"--format={RANGE}", f"{frm}..{to}")
    if r.returncode:
        return None, None, f"git can't read {frm[:7]}..{to[:7]} in {held[0]}: " + ((r.stderr or "").strip() or f"exit {r.returncode}")
    commits = first_parents(r.stdout)
    if commits is None:
        return None, None, f"git's log of {frm[:7]}..{to[:7]} in {held[0]} is not in the form crew reads"
    seconds = [c["parents"][1] for c in commits if c["landed"] and len(c["parents"]) > 1]
    merged = {}
    if seconds:
        r = git(held[0], "log", "--no-walk=unsorted", "--format=%H%x1f%s", *seconds)
        if r.returncode:
            return None, None, f"git can't read the branches landed in {frm[:7]}..{to[:7]} in {held[0]}: " + (
                (r.stderr or "").strip() or f"exit {r.returncode}")
        merged = dict(line.split("\x1f", 1) for line in r.stdout.splitlines() if "\x1f" in line)
    return commits, merged, None


def environments(es, since=None, entries=()):
    """Each environment's deploys and the operations waiting on it, from the drive's entries (es, oldest first) and the
    card entries of its main level's host (entries),
    as the board's Operation lane and the page's deploys view show them (plan.14, state.4): {env: {"deploys": [...],
    "waiting": [...]}}, by environment.

    A deploy is one commit offered or deployed until its deploy ends: its to and from, when it was offered, the user's
    word (who held its card, and when), its answer (approved; waiting on the word; replaced, an unanswered offer a newer
    one replaced, or an approved one not started when the user's word went to another commit or a newer deploy's end
    spent it, as state reads the word, spent naming that newer deploy's commit; or unasked, a deploy started with no
    offer in the record, an auto environment's), when it started
    and ended and its outcome, each of its steps with its outcome, the suite's checks (the rows of its last step that
    has them), the bolts it carried or why the record can't tell, every after-deploy step recorded against its commit
    with its doer and latest state, its rail row while it waits on the word, the rows of the steps of the user's it waits
    on that are open (waits, deploy_waits from the record's marks; [] when none), and when it last moved; newest first,
    those that last moved before since left out unless still open. Waiting are the operations whose latest state is
    waiting, handed or failed, each with whether it is held for the user's word, the link of the gate it waits at
    (gate_of) or None, and the rail row that carries it while it waits on the user (keyed), one for every host's
    entry of a shared step."""
    lands = landings(es)
    offers, _, steps = state(es)
    rowed = keyed(es, entries)
    envs = {}
    for e in es:
        env, act, to = env_of(e), e.get("Act") or "", e.get("Head")
        if not env or not act.startswith("ops.") or act == "ops.step" or not to:
            continue
        E = envs.setdefault(env, {"deploys": [], "open": {}, "word": None, "started": set()})

        def new(frm, offered, answer):
            d = {"to": to, "from": frm, "offered": offered, "word": None, "answer": answer, "spent": None, "started": None, "ended": None,
                 "outcome": None, "steps": [], "checks": None, "at": e["At"]}
            E["deploys"].append(d)
            E["open"][to] = d
            return d
        d = E["open"].get(to)
        if act == "ops.offer":
            for o in [o for o in E["open"].values() if o["to"] != to and o["answer"] == "waiting" and not o["started"]]:
                o.update(answer="replaced", at=e["At"])
                del E["open"][o["to"]]
            d or new(e.get("Base"), e["At"], "waiting")
        elif act == "ops.approve" and not e.get("Refused"):
            E["word"], E["started"] = e, set()
            if not d:
                continue
            for o in [o for o in E["open"].values() if o["to"] != to and o["answer"] == "approved" and not o["started"]]:
                o.update(answer="replaced", at=e["At"])
                del E["open"][o["to"]]
            d.update(word={"at": e["At"], "by": e.get("By")}, answer="approved", at=e["At"])
        elif act == "ops.deploy":
            phase = e.get("Phase")
            if phase == "start":
                d = d or new(e.get("Base"), None, "unasked")
                d.update({"started": e["At"], "from": e.get("Base") or d["from"], "at": e["At"]})
                E["started"].add(to)
            elif d and phase == "step":
                d["steps"].append({"step": e.get("Step"), "outcome": e.get("Outcome"), "at": e["At"]})
                try:
                    d["checks"] = json.loads(e["Rows"]) if e.get("Rows") else d["checks"]
                except ValueError:
                    pass
                d["at"] = e["At"]
            elif d and phase == "end":
                d.update(ended=e["At"], outcome=e.get("Outcome"), at=e["At"])
                del E["open"][to]
                if spends(E["word"], to, E["started"]):
                    for o in [o for o in E["open"].values() if o["answer"] == "approved" and not o["started"]]:
                        o.update(answer="replaced", spent=to, at=e["At"])
                        del E["open"][o["to"]]
                    E["word"] = None
    out = {}
    for env in sorted(set(envs) | {k[0] for k in steps}):
        E = envs.get(env, {"deploys": [], "open": {}})
        deploys = []
        for d in reversed(E["deploys"]):
            if since and d["at"] < since and not any(d is o for o in E["open"].values()):
                continue
            bolts, why = carried(d["to"], d["from"], lands)
            after = [{"key": key, "state": x.get("State"), "doer": x.get("Doer"), "agent": x.get("Agent"), "at": x["At"], "note": x.get("Note")}
                     for (en, t, key), x in steps.items() if en == env and t == d["to"]]
            row = f"deploy/{env}" if d["answer"] == "waiting" else None
            waits = list(dict.fromkeys(rowed[w["k"]] for w in deploy_waits(es, env) if w["k"] in rowed)) if row and env in offers else []
            deploys.append(dict(d, bolts=bolts, bolts_why=why, after=after, row=row, waits=waits))
        waiting = [{"key": key, "to": t or None, "state": x.get("State"), "doer": x.get("Doer"), "agent": x.get("Agent"), "at": x["At"],
                    "text": next((l.strip() for l in (x.get("Text") or "").splitlines() if l.strip()), None), "note": x.get("Note"),
                    "held": held(x), "gate": gate_of(x), "row": rowed.get((en, t, key))}
                   for n, (en, t, key), x in numbered(steps) if en == env and x.get("State") in WAITING]
        out[env] = {"deploys": deploys, "waiting": waiting}
    return out


# ----------------------------------------------------------------- the deploy's and the step's cards (record 0031)

RELEASE = re.compile(r"^##\s+\[?([^\]\s(]+)", re.M)  # a release's heading in git-cliff's Markdown: ## v0.3.0 (date)
FIELD = re.compile(r"(?:^|\s)[-*]\s+(why|where|command|done):\s*", re.I)  # a field of a step's text, on a line or flattened
CARRIED = ("ok", "done")  # a deploy's end that left its environment running its commit


def doer_of(doer, agent, label, env):
    """Who does a step, as a card names them: the user, the agent it is handed to, or its doer's crew name."""
    return agent or {"main-ops": f"{label}-ops"}.get(doer, doer)


def handed_steps(text, env, label):
    """The steps a deployer hands crew ops offer --steps, one a line, tab-separated, as its after-deploy.awk prints
    them: step <n> <doer> <when> <environments> <why> <text>, held among the when words for an agent's step held for
    the user's word, and before for a step the deploy waits on, the user's alone (swancloud record 0038). Those for
    env, or for every environment when they name none, in the order handed, each {n, text, doer, held, before, why},
    its doer as a card names it: ([steps], None), or (None, why) naming the first line crew can't read, a step the
    deploy waits on whose doer is not the user among them (read.1)."""
    out = []
    for i, line in enumerate((text or "").splitlines(), 1):
        if not line.strip():
            continue
        f = line.split("\t", 6)
        if len(f) != 7 or f[0] != "step" or f[2] not in DOERS or not f[6].strip():
            return None, (f"line {i} is no step crew reads: step <n> <doer> <when> <environments> <why> <text>, "
                          f"tab-separated, the doer {', '.join(DOERS[:-1])} or {DOERS[-1]}")
        when = f[3].split()
        if BEFORE in when and f[2] != "user":
            return None, f"line {i} is a step the deploy waits on, which is the user's alone, with the doer {f[2]}"
        envs = [x.strip() for x in f[4].split(",") if x.strip()]
        if envs and env not in envs:
            continue
        if BEFORE in when and any(s["before"] and s["n"] == f[1].strip() for s in out):
            return None, f"line {i} numbers a step the deploy waits on {f[1].strip()}, as an earlier line does, so the two can't be told apart"
        out.append(dict(n=f[1].strip(), text=f[6].strip(), doer=doer_of(f[2], None, label, env), held="held" in when,
                        before=BEFORE in when, why=f[5].strip() or None))
    return out, None


def release_of(notes):
    """The release the notes are for, from git-cliff's heading of it; None when they hold none, or several."""
    names = RELEASE.findall(notes or "")
    return names[0] if len(names) == 1 else None


def deploy_facts(env, offer, es, ranged, notes=None, steps=None, waited=None):
    """The facts of the deploy's card for env's open offer (cards.deploy_card, plan.14), from the drive's entries
    (es, oldest first: the main level's ops entries and every landing) and its range as git read it on the kit's main
    (ranged, kit_range's (commits, merged, why)): the environment, the head and the commit it runs, None when nothing is
    deployed, whose range is then not read; the landings it carries, each first-parent commit of the range named as
    range_landings names it, the record adding only the bolt it holds a landing of, or why git could not read them; the
    notes as handed, their release, and the steps as handed for after the deploy; the steps the deploy waits on, as
    waited_on reads them (waited); the environments whose deploy of the head has ended done, which it comes after. The
    deployer hands no order of its environments, so none comes after."""
    to, base = offer["Head"], offer.get("Base")
    base = None if base in (None, "", "none") else base
    commits, merged, why = ranged if base else (None, None, None)
    lands = range_landings(commits, merged or {}, landings(es)) if commits is not None else []
    before = sorted({env_of(e) for e in es if e.get("Act") == "ops.deploy" and e.get("Phase") == "end" and e.get("Head") == to
                     and e.get("Outcome") in CARRIED and env_of(e) not in (None, env)})
    return dict(env=env, head=to, base=base, landings=lands, landings_why=why,
                notes=notes or None, release=release_of(notes), steps=[s for s in steps or [] if not s.get("before")],
                waited=list(waited or []), before=before, after=[])


def deploy_move(es, env, held_card, waits=(), rowed=None, answered=False):
    """What the deploy's card of env does now (record 0031 §3, record 0070), from the drive's ops entries, whether
    main-level ops holds a card under deploy/<env>, the steps of the user's its open offer waits on that are not done
    (waits, deploy_waits'), the rows that ask them (rowed, keyed's) and whether the user answered the card held:
    ("post", None) when it holds none; ("change", the change note) when the card asks for an older offer still
    unanswered, the note naming the head offered now and the one it replaces; ("withdraw", why) while a step it waits
    on is open and ops holds a card the user has not answered and no word stands, naming the step's card; (None, why)
    when nothing is offered, while a step it waits on is open, its card raised once each is done, or when the card asks
    for a deploy the user approved, which closes at the end of that deploy or of a newer one (spends), the open
    offer's card raised then."""
    offers, words, _ = state(es)
    offer = offers.get(env)
    if not offer:
        return None, f"no deploy of {env} is offered"
    if waits and held_card and not answered and env not in words:
        return "withdraw", f"It now waits on {waits_said(env, waits, rowed or {})}: its card is raised again once that is done."
    if waits:
        return None, f"it waits on {waits_said(env, waits, rowed or {})}: its card is raised once {'that is' if len(waits) == 1 else 'each is'} done"
    if not held_card:
        return "post", None
    if env in words:
        return None, (f"its card asks for the deploy of {words[env]['Head'][:7]}, approved, and the offer of "
                      f"{offer['Head'][:7]} is raised once that deploy ends")
    was = [e["Head"] for e in es if e.get("Act") == "ops.offer" and env_of(e) == env and e is not offer and e["Head"] != offer["Head"]
           and (e["At"], e["Id"]) < (offer["At"], offer["Id"])]
    return "change", f"Now offering {offer['Head'][:7]}" + (f", which includes {was[-1][:7]}" if was else "")


def deploy_outcome(es, env, to, outcome, log=None, does=None, word=None):
    """What the deploy's card closes with at the deploy's end (record 0031 §1): each step of its run with its outcome,
    or the step that failed and its log, from the drive's ops entries since its start, and after them, when the
    end was handed them, the deployer's words of what the user does, as it wrote them (swancloud deploy.6); and, when
    the card asked for another commit, word, the head the user approved, that this newer deploy ended before it
    (plan.14)."""
    mine = [e for e in es if e.get("Act") == "ops.deploy" and env_of(e) == env and e.get("Head") == to]
    starts = [i for i, e in enumerate(mine) if e.get("Phase") == "start"]
    ran = [e for e in mine[starts[-1] if starts else 0:] if e.get("Phase") == "step" and e.get("Step")]
    failed = next((e for e in ran if e.get("Outcome") == "failed"), None)
    newer = f", newer than the {word[:7]} you approved," if word and word != to else ""
    if failed or outcome == "failed":
        at = f" at {failed['Step']}" if failed else ""
        where = (failed or {}).get("Log") or log
        said = f"The deploy of {to[:7]} to {env}{newer} failed{at}" + (f"; its log: {where}" if where else "") + "."
        does = " ".join((does or "").split())
        if not does:
            return said
        return f"{said} What you do: {does}" + ("" if does.endswith((".", "!", "?")) else ".")
    return (f"Deployed {to[:7]} to {env}{newer[:-1]}" + (": " + ", ".join(f"{e['Step']} {e.get('Outcome') or 'done'}" for e in ran) if ran else "")
            + ".")


def step_words(text):
    """A step's text as the deployer hands it, read as its card's: its words, all it says before its first field, each
    run of spaces one; and its fields, `- why:`, `- where:`, `- command:` (one a command, in order) and `- done:`, each
    running to the next. Read alike from the file's lines and from the run record's one line of it."""
    parts = FIELD.split(" ".join((text or "").split()))
    fields = {"commands": []}
    for name, value in zip(parts[1::2], parts[2::2]):
        if name.lower() == "command":
            fields["commands"].append(value.strip())
        else:
            fields[name.lower()] = value.strip()
    return parts[0].strip(), fields


GATE = re.compile(r"^https?://\S+$")  # a gate's step: its words one link alone (plan.14)


def gate_of(e):
    """The link of the gate a step's latest entry waits at, or None: a step that is the user's whose words, all its
    text says before its first field (step_words), are one link alone is a deploy a hosted deployer holds at a gate
    whose reviewer is the user (plan.14). An agent's step is never one, since a gate's reviewer is the user."""
    words = step_words(e.get("Text"))[0]
    return words if e.get("Doer") == "user" and GATE.match(words) else None


def step_facts(env, n, e, label, working=None, group=None, waited=()):
    """The facts of a step's card (cards.step_card) from its latest entry: its environment and number, its words and
    fields as its text gives them (step_words), its doer as a card names it, whether it is held, the gate it waits at
    (gate_of) and the deploy it names, and for a held step what doing it now cuts: working, the Flume places whose stage
    works on its host as the card is raised (places_working), or why crew could not tell (a string). Over the group
    that carries it (group, groups' steps; the step alone when none is given, Decision 4): the hosts it names, in the
    group's order; its heads (head_word), which each post and change of its card records; whether a deploy waits on
    it, any of its steps marked before or one an open offer waits on (waited, the (env, to, key) of each); and whether
    each names a deploy."""
    words, fields = step_words(e.get("Text"))
    doer = "user" if e.get("Doer") == "user" else doer_of(e.get("Doer"), e.get("Agent"), label, env)
    steps = [s for _, s, _ in group] if group else [(env, e.get("Head") or "", e.get("Key"))]
    latest = [x for _, _, x in group] if group else [e]
    f = dict(env=env, n=n, text=words or e.get("Key"), doer=doer, held=held(e), why=fields.get("why"), where=fields.get("where"),
             commands=fields["commands"], done=fields.get("done"), gate=gate_of(e), to=e.get("Head") or None,
             hosts=list(dict.fromkeys(s[0] for s in steps)), heads=[head_word(s) for s in steps],
             before=any(waits_before(x) for x in latest) or any(s in set(waited) for s in steps), deployed=all(s[1] for s in steps))
    if f["held"]:
        if isinstance(working, str):
            now = f"It runs at once, whatever is working on {env}: crew could not tell what is ({working})"
        elif working:
            now = f"It runs at once, cutting the {'stage' if len(working) == 1 else 'stages'} of {', '.join(working)}"
        else:
            now = f"It runs at once; no stage is working on {env} now"
        f["consequences"] = {"now": now}
    return f


def step_due(es, entries, env):
    """The group of steps whose card crew raises next on env, one step card at a time on an environment (record 0031
    §5, Decision 5), from the drive's ops entries and this host's card entries (entries, oldest first): while no step
    card naming env is open (step_cards), of the groups naming env whose row key (group_key) has had no card, the one
    with the earliest first-recorded step among those whose every environment has no step card open, so two shared
    steps recorded in opposite orders on two hosts raise one and then the other. (the group with its row key as row,
    None); (None, the open card's key) while one names env; (None, None)."""
    import cards  # its decisions only: what the run record shows posted and closed
    opened = step_cards(es, entries)
    busy = {}
    for o in opened:
        for x in o["envs"]:
            busy.setdefault(x, o["key"])
    if env in busy:
        return None, busy[env]
    had = {c["key"] for c in cards.posted_cards(entries)}
    for g in groups(es):
        envs = {s[0] for _, s, _ in g["steps"]}
        key = group_key(g, opened)
        if env in envs and key not in had and not envs & busy.keys():
            return dict(g, row=key), None
    return None, None


def step_point(es, entries, key):
    """Whether the point of the step card keyed op/<env>/<n> has come (record 0031 §5): its row's group waits on the
    user, and its card is open, to be raised again or changed, or it is the next due on one of its environments while
    no step card is open on any of them (step_due), from the drive's ops entries and this host's card entries. (the
    group with its row key as row, None), or (None, why not), naming the card that asks its step now when its row was
    folded into another's."""
    opened = step_cards(es, entries)
    gs = [dict(g, row=group_key(g, opened)) for g in groups(es)]
    g = next((g for g in gs if g["row"] == key), None)
    if not g:
        mine = key_step(numbered(state(es)[2]), key)
        other = next((x["row"] for x in gs if any(s == mine for _, s, _ in x["steps"])), None) if mine else None
        return None, f"its step is asked on {other}" if other else "its step no longer waits on the user"
    if any(o["key"] == key for o in opened):
        return g, None
    envs = list(dict.fromkeys(s[0] for _, s, _ in g["steps"]))
    for x in envs:
        due, open_ = step_due(es, entries, x)
        if open_:
            return None, f"card {open_} is open: this step's card is raised when it closes"
        if due and due["row"] == key:
            return g, None
    return None, "its step waits on no one, or another's card comes first"


# What a step's card shows of it, by what a change note names: its words and fields, its doer, its hold.
SHOWN = (("its words", ("text", "why", "where", "commands", "done")), ("its doer", ("doer",)), ("its hold", ("held",)))


def step_again(es, entries, k, label):
    """What becomes of the open step card that carries the step k, (env, to, key), once it is recorded (record 0031 §3,
    Decision 7), from the drive's ops entries (es) and this host's entries in the order written (entries): None when no
    card of main-level ops's carries it, the card of its group (group_key) or one that names it (card_steps); else
    {key, card, envs, answered, close, note, kind_changed, left}. A card the user answered is left as it is (answered),
    a step recorded since waiting for its settle. A card no step it names still waits on is closed with k's state
    (close). A card whose heads, the steps it names (shown_heads), differ from its group's is changed in place with a
    note: "<env> waits on it too" for a step that joined, "<env>'s is recorded <state>" for one that left, left whether
    k's environment is no longer among those it names. Otherwise the card shows the step's latest entry before its last
    post or change, and is changed when its words, its doer or its hold differ from the step as recorded now
    (step_facts, but for what a held step cuts, read as it is raised), the note naming which, None when none; its kind,
    a `do` for the user's step and a choice for an agent's held, changes when its doer changes between the user and an
    agent. A card whose step's entry this host's record no longer reaches before it is changed to the step as recorded,
    since what it shows can't be read (read.1)."""
    import cards  # its decisions only: what the run record shows posted and closed
    steps = state(es)[2]
    if k not in steps:
        return None
    opened = [o for o in step_cards(es, entries) if o["by"] == f"{label}-ops"]
    gs = groups(es)
    mine = next((g for g in gs if any(s == k for _, s, _ in g["steps"])), None)
    key = group_key(mine, opened) if mine else None
    hit = next((o for o in opened if o["key"] == key), None) or next((o for o in opened if k in o["named"]), None)
    if not hit:
        return None
    key, card, named = hit["key"], hit["card"], hit["named"]
    out = dict(key=key, card=card, envs=hit["envs"], answered=False, close=None, note=None, kind_changed=False, left=False)
    if any(e.get("Act") == "card.answer" and e.get("Card") == card and not e.get("Refused") for e in entries):
        return dict(out, answered=True)
    g = mine or next((g for g in gs if any(s in named for _, s, _ in g["steps"])), None)
    now = [s for _, s, _ in g["steps"]] if g else []
    if not now:
        said = steps[k].get("State")
        return dict(out, close=CLOSED.get(said) or f"Recorded {said}.")
    if {head_word(s) for s in now} != {head_word(s) for s in named}:
        joined = [s for s in now if s not in named]
        gone = [s for s in named if s not in now]
        note = "; ".join([f"{s[0]} waits on it too" for s in joined] + [f"{s[0]}'s is recorded {steps[s].get('State')}" for s in gone if s in steps])
        return dict(out, note=note or "Its hosts changed", left=k[0] not in {s[0] for s in now})
    env = k[0]
    latest, shown = None, None
    for e in entries:
        if e.get("Act") == "ops.step" and (env_of(e), e.get("Head") or "", e.get("Key")) == k:
            latest = e
        elif e.get("Act") in ("card.post", "card.update") and not e.get("Refused") and (e.get("Card"), e.get("Key")) == (card, key):
            shown = latest
    if shown is None:
        return dict(out, note="Recorded again")
    was, now_ = step_facts(env, 0, shown, label), step_facts(env, 0, steps[k], label)
    what = [w for w, fields in SHOWN if any(was[f] != now_[f] for f in fields)]
    return dict(out, note="Recorded again: " + cards.joined(what) + " changed" if what else None,
                kind_changed=(was["doer"] == "user") != (now_["doer"] == "user"))


def word_stands(key, es):
    """Whether a row's card under key outlives its row: a deploy's, deploy/<env>, once the user's word for it is given
    and no deploy's end has spent it yet (spends), the end that spends it closing it with the outcome (record 0031 §1),
    from the drive's entries; the rail's sweep leaves it, and lists it as no stray."""
    kind, _, env = (key or "").partition("/")
    return kind == "deploy" and env in state(es)[1]


def kept(label, env, to):
    """Where an offer keeps the files it was handed, on the main level's host, so its card is built again the same:
    never in the run record (record.3)."""
    return record.ROOT / label / "ops" / env / to


def kept_text(path):
    try:
        return path.read_text()
    except OSError:
        return None


def ops_where(fleet, label):
    """Where main-level ops's cards are asked from and filed: the drive's blueprints checkout, its own place."""
    import plan
    p = crew.drive_of(fleet, label)
    return plan.card_where({"main": p["checkout"], "repo": p["blueprints"][0]})


def waited_card(es, entries, env, offer, waited, by):
    """The step card a deploy's card follows once each step it waited on is done (record 0070): the newest step card
    in by's name closed since the offer (offer's At) whose named steps (card_steps) hold one of env's the deploy waited
    on (waited, waited_on's), from the drive's ops entries and this host's card entries; its id, or None."""
    mine = {(env, w["to"] or "", w["key"]) for w in waited if w["key"]}
    closed = {e["Card"]: e["At"] for e in entries if e.get("Act") == "card.close" and e.get("Card") and not e.get("Refused")}
    keys = {e["Card"]: e.get("Key") or "" for e in entries if e.get("Act") == "card.post" and e.get("By") == by and e.get("Card")
            and not e.get("Refused")}
    hits = [(at, card) for card, at in closed.items() if keys.get(card, "").startswith("op/") and at >= offer["At"]
            and card_steps(es, entries, keys[card], card) & mine]
    return max(hits)[1] if hits else None


def raise_deploy(fleet, row, acts=None, note=None):
    """Raise the deploy's card of the rail row deploy/<env> of row["label"] (record 0031 §1, plan.14 as record 0070
    amends it): posted in main-level ops's name, a hold-to-approve, following the card follows_of names, the step card
    it waited on once each such step is done (waited_card), or changed in place when the card ops holds asks for an
    older offer still unanswered, or for this one when it is offered again with other files, note naming what changed;
    once the user answered it, left as it is unless a newer head is offered since the head it asked about, when it is
    followed by a new card (cards.head_anew); a card that follows one the user answered, declined or approved, saying
    first what they answered and that the offer is now at another head, or that the commit offered was handed other
    files (note), or that each step it waited on is done, and withheld when none, their answer standing
    (cards.deploy_since, plan.card_posted); posted again when Pending You no longer finds it, and saying first that an
    older copy was lost when the rail's sweep hands it the older copy this host can't reach as the row's dead
    (plan.built_again); built from the open offer, the files it was handed and the drive's run record, the steps it
    waited on among them (waited_on). While a step of the user's it waits on is open (deploy_waits), no card: one ops
    holds that the user has not answered is withdrawn naming the step's card (deploy_move), and a card posted as boxes
    before record 0070 (cards.form_asked) is withdrawn the same way, or followed by the hold-to-approve once none is
    open, Pending You changing no card's kind. None, saying why, when no offer waits on a card; the offer's own call
    and the rail's sweep alike. A card not posted or changed is said and recorded, and the offer stands. The card's
    id, or None."""
    import cards, plan
    acts = acts or plan.CardActs(fleet)
    label, key = row["label"], row["key"]
    env, owner = key.split("/", 1)[1], f"{label}-ops"
    es, mine = entries(label), acts.entries(label)
    held = cards.card_under(mine, key, owner)
    offer = state(es)[0].get(env)
    d = kept(label, env, offer["Head"]) if offer else None
    steps, _ = handed_steps(kept_text(d / "steps.txt"), env, label) if d else ([], None)
    waits = deploy_waits(es, env, steps) if offer else []
    answered = bool(held) and any(e.get("Act") == "card.answer" and e.get("Card") == held and not e.get("Refused") for e in mine)
    move, said = deploy_move(es, env, held, waits, keyed(es, mine), answered)
    if move == "withdraw":
        plan.row_card_close(fleet, label, owner, key, reason=said, acts=acts)
        return None
    said = note if move == "change" and note else said
    if not move:
        print(f"card {key}: {said}")
        return None
    since = (datetime.datetime.now(datetime.timezone.utc).date() - datetime.timedelta(days=DAYS)).isoformat()
    gathered, _ = record.gather(fleet, [label], since)
    lands = sorted({e["Id"]: e for e in es + [e for e in gathered if e.get("Act") == "bolt.land"]}.values(),
                   key=lambda e: (e["At"], e["Id"]))
    base = offer.get("Base")
    ranged = kit_range(fleet, label, base, offer["Head"]) if base not in (None, "", "none") else (None, None, None)
    waited = waited_on(steps, es, env)
    facts = deploy_facts(env, offer, lands, ranged, kept_text(d / "notes.md"), steps, waited)
    after = waited_card(es, mine, env, offer, waited, owner) if waited else None
    facts["follows"] = cards.follows_of("deploy", {"env": env, "head": offer["Head"], "after": after}, gathered, owner)
    anew = cards.head_anew(mine, held, offer["Head"])
    if after and facts["follows"] == after:
        since = [f"Each step of yours the deploy of {offer['Head'][:7]} to {env} waited on is done, and it waits on your word."]
    else:
        earlier = cards.head_asked(mine, facts["follows"]) if facts["follows"] else (anew or {}).get("approved")
        since = cards.deploy_since(earlier, offer["Head"])
    since += [note] if note else []
    build = plan.built_again(cards.deploy_card) if row.get("dead") else cards.deploy_card
    moved = bool(held) and cards.form_asked(mine, held) == "boxes"
    return plan.row_card_change(fleet, label, owner, build, facts, said or "Raised again", ops_where(fleet, label), acts,
                                kind_changed=moved, anew=anew, since=since)


def places_working(fleet, label, env):
    """The Flume places of the drive whose stage works on env's host, as the drive's runner there carries
    Flume's status of them (runner.working), a list, none where no runner of the drive answers there, since none
    of its places runs there; or why crew could not tell, a string (read.1)."""
    import plan
    try:
        repo, ref = plan.state_of(fleet, label)
        plan.tip_of(repo, ref)
        reading = runner.of_host(plan.runners(repo, label), label, env)
    except Refusal as e:
        return str(e)
    if reading["tip"] is None:
        return []
    if reading["why"]:
        return reading["why"]
    names, why = runner.working(reading)
    return why or names


def answered_card(es, entries, group, by):
    """The last step card in by's name the user answered, closed after their answer, that named a step of group's
    under its key (card_steps), from the drive's ops entries and this host's card entries: its id, which the card of a
    host that recorded the step after that answer follows (record 0070); None when there is none."""
    import cards  # its decisions only: what the run record shows posted and closed
    for c in reversed(cards.posted_cards(entries)):
        if (c["by"] == by and c["state"] == "closed" and c["key"].startswith("op/")
                and any(s[2] == group["key"] for s in card_steps(es, entries, c["key"], c["card"]))):
            return c["card"]
    return None


def raise_step(fleet, row, acts=None, note="Raised again", kind_changed=False):
    """Raise the card of the rail row op/<env>/<n> of row["label"], a group of steps that waits on the user, one step
    card at a time on an environment (record 0031 §5, Decision 5): posted in main-level ops's name over the whole
    group (step_facts), its heads recorded, once its point has come (step_point), following the card the user answered
    of the same step for a host that recorded it after that answer (answered_card), else the deploy's card or the step
    card before it on its first-recorded environment (cards.follows_of), and posted again when Pending You no longer
    finds it, saying first that an older copy was lost when the rail's sweep hands it the older copy this host can't
    reach as the row's dead (plan.built_again); while its card is open, changed with note, or followed by a new card
    when its kind changed (step_again). A card that follows one the user answered says first what they answered and
    what changed since: the same step recorded by other hosts, the deploy ended, or the step before behind them
    (cards.step_since); one following its own card the user answered, its note (plan.row_card_change). None, saying
    why, before then; the step's own call and the rail's sweep alike. The card's id, or None."""
    import cards, plan
    acts = acts or plan.CardActs(fleet)
    label, key = row["label"], row["key"]
    owner, es, mine = f"{label}-ops", entries(label), acts.entries(label)
    g, why = step_point(es, mine, key)
    if not g:
        print(f"card {key}: {why}")
        return None
    env, n = key.split("/")[1], int(key.split("/")[2])
    _, (first, _, _), e = g["steps"][0]
    offers = state(es)[0]
    waited = {w["k"] for x in dict.fromkeys(s[0] for _, s, _ in g["steps"]) if x in offers
              for w in deploy_waits(es, x, offered_steps(label, x, es)) if w["k"]} if g["shared"] else set()
    facts = step_facts(env, n, e, label, places_working(fleet, label, env) if held(e) else None, g["steps"], waited)
    facts["key"] = key
    answered = answered_card(es, mine, g, owner) if g["shared"] else None
    facts["follows"] = cards.follows_of("step", {"env": first, "key": key, "answered": answered}, mine, owner)
    followed = next((x.get("Key") for x in mine if x.get("Act") == "card.post" and x.get("Card") == facts["follows"]
                     and not x.get("Refused")), None) if facts["follows"] else None
    since = None if cards.card_under(mine, key, owner) else cards.step_since(
        followed, env, n, facts.get("to"), facts["hosts"] if answered and facts["follows"] == answered else None)
    build = plan.built_again(cards.step_card) if row.get("dead") else cards.step_card
    return plan.row_card_change(fleet, label, owner, build, facts, note, ops_where(fleet, label), acts, kind_changed, since=since)


def raise_next_step(fleet, label, env, k=None):
    """Once the step k, (env, to, key), is recorded: the open step card that carries it changed or closed (step_again),
    changed in place when what it shows differs, the line that adopts it printed either way, as a raise prints it,
    closed with k's state once no step it names still waits, and left as it is once the user answered it; then the
    card of the group due next raised on each environment a card closed named, or on env, unless a step card naming it
    is open (step_due). The card's id that carries k, or the first raised, or None."""
    import plan
    acts, owner = plan.CardActs(fleet), f"{label}-ops"
    es, mine = entries(label), acts.entries(label)
    again = step_again(es, mine, k, label) if k else None
    envs = [env]
    if again and again["answered"]:
        print(f"card {again['key']}: {again['card']} is answered: a step recorded since is asked once the user's answer is settled")
        return again["card"]
    if again and again["close"]:
        plan.row_card_close(fleet, label, owner, again["key"], outcome=again["close"], acts=acts)
        envs = list(dict.fromkeys(again["envs"] + [env]))
    elif again:
        key, card, note = again["key"], again["card"], again["note"]
        if not note:
            print(f"card {key}: {card} shows the step as recorded, so it is not changed")
        new = raise_step(fleet, {"label": label, "key": key}, acts, note, again["kind_changed"]) if note else None
        if new in (None, card):
            plan.card_heard(acts, key, card, owner)
        if not again["left"]:
            return new or card
    raised = None
    for x in envs:
        due, open_ = step_due(entries(label), acts.entries(label), x)
        if open_:
            print(f"card {open_} is open: the next step's card is raised when it closes")
        elif due:
            raised = raise_step(fleet, {"label": label, "key": due["row"]}, acts) or raised
    return raised


def emit(label, act, env, why, refused=None, **fields):
    eid = record.emit(label, act, [f"env/{env}"], why=f"ops({env}): {why}", refused=refused, **fields)
    eid or fail(f"the operation's {act} could not be recorded in {label}'s run record")


def handed(path, what):
    """A file the deployer hands an offer, as text; refused naming it when it can't be read, nothing offered (read.1)."""
    try:
        return pathlib.Path(path).read_text()
    except (OSError, UnicodeDecodeError) as e:
        fail(f"the {what} file {path} can't be read: {getattr(e, 'strerror', None) or e}; nothing is offered")


def carried_texts(text):
    """The notes' and the steps' text an offer forwarded from another host carries on its stdin, as forwarded writes
    them: (notes, steps), each None when not handed; or (None, None, why) naming what can't be read (read.2)."""
    try:
        got = json.loads(text or "")
    except ValueError as e:
        return None, None, f"it is not JSON: {e}"
    if not isinstance(got, dict) or set(got) != {"notes", "steps"} or not all(v is None or isinstance(v, str) for v in got.values()):
        return None, None, 'it is not {"notes", "steps"}, each text or null'
    return got["notes"], got["steps"], None


def offered_texts(a):
    """What an offer was handed, (notes, steps), each None when not handed: the files --notes and --steps name, read
    on this host, or their text carried on stdin by an offer forwarded here (--handed -); refused, naming what can't be
    read, the file or a step's line, with nothing offered (read.1), before the offer runs here or is forwarded."""
    if getattr(a, "handed", None):
        notes, steps, why = carried_texts(sys.stdin.read())
        why is None or fail(f"what the offer was handed can't be read from its stdin: {why}; nothing is offered")
    else:
        notes = handed(a.notes, "release notes") if a.notes else None
        steps = handed(a.steps, "steps") if a.steps else None
    _, why = handed_steps(steps, a.env, a.label)
    why is None or fail(f"{f'the steps file {a.steps}' if a.steps else 'the steps handed'} can't be read: {why}; nothing is offered")
    return notes, steps


def handed_changed(kept_notes, kept_steps, notes, steps):
    """What an offer of the commit already offered changes of what its card shows (code.7): its release notes, its
    after-deploy steps, or both, as a change note names them, from the files kept with the offer and the text handed
    now, an empty text alike with none; [] when both are the same, and the offer then changes nothing."""
    return [what for what, was, now in (("its release notes", kept_notes, notes), ("its after-deploy steps", kept_steps, steps))
            if (was or None) != (now or None)]


def forwarded(a, argv, notes, steps, rows=None, text=None):
    """The ops command as it is run on the drive's main level's host, and what it reads there on its stdin
    (code.3): an offer handed --notes or --steps, files of this host, carries their text as JSON, {"notes", "steps"},
    in --handed -, a record handed --rows carries the rows (recorded_rows') in --rows -, and a step handed --text
    carries its text (stepped_text's) in --text -, since the files do not reach that host; any other command runs as
    it was given, with nothing."""
    if a.cmd == "record" and a.rows:
        return without(argv, "--rows") + ["--rows", "-"], rows
    if a.cmd == "step" and a.text:
        return without(argv, "--text") + ["--text", "-"], text
    if a.cmd != "offer" or not (a.notes or a.steps):
        return list(argv), None
    return (["offer", a.env, "--label", a.label, "--to", a.to, "--from", getattr(a, "from"), "--handed", "-"],
            json.dumps({"notes": notes, "steps": steps}))


def without(argv, flag):
    """argv with flag and its value left out, given as `flag value` or `flag=value`."""
    out, value = [], False
    for x in argv:
        if value:
            value = False
        elif x == flag:
            value = True
        elif not x.startswith(flag + "="):
            out.append(x)
    return out


def offer_move(offers, env, to, changed, held):
    """What an offer of env's deploy of `to` does (plan.14, code.7), from the open offers (state's), what it changes of
    the files the open offer was handed (handed_changed's) and whether main-level ops holds a card under deploy/<env>:
    "offer" when `to` is not the open offer's head, the offer recorded and its card raised; "change" when it is and it
    was handed other notes or steps, its card changed in place; "post" when it is, nothing changed, and ops holds no
    card, as when Pending You refused its post, the card posted again and no second offer recorded; None when it is,
    nothing changed and the card is held, and nothing is done."""
    if offers.get(env, {}).get("Head") != to:
        return "offer"
    if changed:
        return "change"
    return None if held else "post"


def offer(fleet, a):
    import cards, plan
    notes, steps = a.texts
    offers, _, _ = state(entries(a.label))
    d, key = kept(a.label, a.env, a.to), f"deploy/{a.env}"
    same = offers.get(a.env, {}).get("Head") == a.to
    changed = handed_changed(kept_text(d / "notes.md"), kept_text(d / "steps.txt"), notes, steps) if same else None
    held = same and cards.card_under(plan.CardActs(fleet).entries(a.label), key, f"{a.label}-ops") is not None
    move = offer_move(offers, a.env, a.to, changed, held)
    if not move:
        return
    if move != "post":
        try:
            d.mkdir(parents=True, exist_ok=True)
            for name, text in (("notes.md", notes), ("steps.txt", steps)):
                (d / name).unlink(missing_ok=True)
                text is None or (d / name).write_text(text)
        except OSError as e:
            fail(f"crew can't keep what the offer was handed in {d}: {e.strerror or e}; nothing is offered")
    if move == "change":
        raise_deploy(fleet, {"label": a.label, "key": key}, note=f"Offered again: {cards.joined(changed)} changed")
        return
    if move == "offer":
        emit(a.label, "ops.offer", a.env, f"offer a deploy of {a.to[:7]}", Head=a.to, Base=getattr(a, "from"))
    raise_deploy(fleet, {"label": a.label, "key": key})


def offered_steps(label, env, es):
    """The steps env's open offer was handed, as handed_steps reads them from the file kept beside it (kept): [] when
    nothing is offered or the offer was handed no steps; refused, naming what can't be read (read.1)."""
    offer = state(es)[0].get(env)
    if not offer:
        return []
    steps, why = handed_steps(kept_text(kept(label, env, offer["Head"]) / "steps.txt"), env, label)
    why is None or fail(f"the steps kept with {env}'s offer of {offer['Head'][:7]} can't be read: {why}")
    return steps or []


def approve(fleet, a):
    import plan
    es = entries(a.label)
    offers, _, _ = state(es)
    why = approve_refusal(offers, a.env, a.to)
    if why:
        emit(a.label, "ops.approve", a.env, f"approve a deploy of {a.to[:7]}", refused=why, Head=a.to)
        fail(f"{why}: crew ops approve answers the offer the rail shows (crew rail --label {a.label})")
    why = waited_refusal(a.env, a.to, deploy_waits(es, a.env, offered_steps(a.label, a.env, es)),
                         keyed(es, plan.CardActs(fleet).entries(a.label)))
    if why:
        emit(a.label, "ops.approve", a.env, f"approve a deploy of {a.to[:7]}", refused=why, Head=a.to)
        fail(why)
    emit(a.label, "ops.approve", a.env, f"approve a deploy of {a.to[:7]}", Head=a.to)
    print(f"the deploy of {a.env} to {a.to[:7]} is approved: the deployer runs it at its next run")


def waited_refusal(env, to, waits, rowed):
    """Why the user's approval of the deploy of env to to is refused for the steps of theirs it waits on, or None
    (record 0070, roles.3): from each such step not done (deploy_waits'), named by its words and the card it is asked
    on (rowed, keyed's), or that its deployer has not recorded it on env yet; the user's hold of the deploy's card is
    the word only once each is done, its card raised only then."""
    if not waits:
        return None
    return (f"the deploy of {env} to {to[:7]} waits on {waits_said(env, waits, rowed)}: its card is raised, and your "
            f"word given, once {'that step is' if len(waits) == 1 else 'each is'} done")


def approve_refusal(offers, env, to):
    """Why the user's approval of a deploy of env to to is refused, or None: it answers only the offer open now."""
    e = offers.get(env)
    if not e:
        return f"no deploy of {env} is offered"
    return None if e["Head"] == to else f"the deploy of {env} offered is to {e['Head'][:7]}, not {to[:7]}"


def word(fleet, a):
    _, words, _ = state(entries(a.label))
    e = words.get(a.env)
    if not e:
        print(f"no word is given for a deploy of {a.env}: the user gives it by holding the offer's card", file=sys.stderr)
        sys.exit(1)
    print(e["Head"])


def recorded_rows(a):
    """The rows a record was handed, as compact JSON, or None when it was handed none: the file --rows names, read on
    this host, or the rows a record forwarded here carries on its stdin (--rows -); refused, naming what can't be
    read, with nothing recorded (read.1), before the record runs here or is forwarded."""
    if not a.rows:
        return None
    where = "carried on the stdin" if a.rows == "-" else f"file {a.rows}"
    try:
        return json.dumps(json.loads(sys.stdin.read() if a.rows == "-" else pathlib.Path(a.rows).read_text()), separators=(",", ":"))
    except (OSError, ValueError) as e:
        fail(f"the rows {where} can't be read as JSON: {e}")


def record_cmd(fleet, a):
    rows_ = a.rows_json
    _, words, _ = state(entries(a.label))
    emit(a.label, "ops.deploy", a.env, f"deploy {a.to[:7]}: {a.act}" + (f" {a.step}" if a.step else ""), Head=a.to,
         Base=getattr(a, "from"), Phase=a.act, Step=a.step, Outcome=a.outcome, Log=a.log, Rows=rows_, Does=a.does)
    if a.act != "end":
        return
    import plan
    es = entries(a.label)
    was = words.get(a.env)
    if was and a.env not in state(es)[1]:
        plan.row_card_close(fleet, a.label, f"{a.label}-ops", f"deploy/{a.env}",
                            outcome=deploy_outcome(es, a.env, a.to, a.outcome, a.log, a.does, was["Head"]))
    if state(es)[0].get(a.env):
        raise_deploy(fleet, {"label": a.label, "key": f"deploy/{a.env}"})


CLOSED = {"done": "Done.", "declined": "Skipped."}  # what a step's card closes with when the step is marked so


def stepped_text(a):
    """The text a step was handed, or None when it was handed none: the file --text names, read on this host, or the
    text a step forwarded here carries on its stdin (--text -); refused, naming what can't be read, with nothing
    recorded (read.1), before the step runs here or is forwarded."""
    if not a.text:
        return None
    try:
        return sys.stdin.read() if a.text == "-" else pathlib.Path(a.text).read_text()
    except (OSError, UnicodeDecodeError) as e:
        where = "carried on the stdin" if a.text == "-" else a.text
        fail(f"the step's text {where} can't be read: {getattr(e, 'strerror', None) or e}")


def settled_steps(es, entries, key, card):
    """The steps crew ops settle records the user's answer on (Decision 6), from the drive's ops entries and this
    host's card entries: those the card under key named at its last post or change (card), when one is open, each that
    still waits on the user; with no card, those the row keyed so carries (groups, group_key). ([(env, to, key)], None),
    or (None, why) when no row and no card holds key, nothing then recorded (read.1)."""
    steps = state(es)[2]
    if card:
        named = card_steps(es, entries, key, card)
        words = shown_heads(entries, card)
        order = [s for w in words for s in named if head_word(s) == w] if words else sorted(named)
        return [s for s in dict.fromkeys(order) if s in steps and waits_on_user(steps[s])], None
    opened = step_cards(es, entries)
    g = next((g for g in groups(es) if group_key(g, opened) == key), None)
    if not g:
        return None, f"no step's row or card holds {key}"
    return [s for _, s, _ in g["steps"]], None


def settle(fleet, a):
    """crew ops settle: the user's answer on a step's card, recorded on every step it named (Decision 6)."""
    import cards, plan
    acts, owner = plan.CardActs(fleet), f"{a.label}-ops"
    es, mine = entries(a.label), acts.entries(a.label)
    card = cards.card_under(mine, a.key, owner)
    ks, why = settled_steps(es, mine, a.key, card)
    why is None or fail(f"{why}: crew ops settle answers a step's card the rail shows (crew rail --label {a.label})")
    steps = state(es)[2]
    offers = state(es)[0]
    waited = {env: {w["k"] for w in deploy_waits(es, env, offered_steps(a.label, env, es)) if w["k"]} for env in offers}
    for k in ks:
        x = steps[k]
        emit(a.label, "ops.step", k[0], f"{k[2]} {a.state}", Head=k[1] or None, Key=k[2], State=a.state, Doer="user",
             When=x.get("When") or "", Note=f"answered on {a.key}")
    if card:
        plan.row_card_close(fleet, a.label, owner, a.key, outcome=CLOSED[a.state], acts=acts)
    envs = list(dict.fromkeys([k[0] for k in ks] + (cards.heads_envs(mine, card, a.key) if card else [])))
    print(f"step {a.key}: recorded {a.state} on " + (cards.joined([head_word(k) for k in ks]) if ks else "no step, none waiting"))
    for env in envs:
        raise_next_step(fleet, a.label, env)
    es = entries(a.label)
    for env in envs:
        if env in offers and waited.get(env) & set(ks) and not deploy_waits(es, env, offered_steps(a.label, env, es)):
            raise_deploy(fleet, {"label": a.label, "key": f"deploy/{env}"})


def step(fleet, a):
    es = entries(a.label)
    offers, _, _ = state(es)
    handed = offered_steps(a.label, a.env, es)
    k = (a.env, a.to or "", a.key)
    waited = {w["k"] for w in deploy_waits(es, a.env, handed)} if a.env in offers else set()
    before = marked_before(a.doer, a.step_text, handed) if a.doer == "user" and a.step_text else False
    emit(a.label, "ops.step", a.env, f"{a.key} {a.state}", Head=a.to, Key=a.key, State=a.state, Doer=a.doer, Agent=a.agent,
         When=" ".join(w for w in (a.when, "held" if a.held else None, BEFORE if before else None) if w), Text=a.step_text,
         Changes=a.changes, Note=a.note)
    if before:
        print(f"step {a.key}: the deploy of {a.env} offered waits on it, so the deploy's card is raised once the step is done")
    if a.state in CLOSED or a.state == "failed" or a.state == "waiting" and (a.doer == "user" or a.held):
        raise_next_step(fleet, a.label, a.env, k)
    if a.env in offers and (before or a.state == "waiting" and k in waited):
        raise_deploy(fleet, {"label": a.label, "key": f"deploy/{a.env}"})  # a card it held unanswered withdrawn (deploy_move)
    elif a.env in offers and a.state == "done" and k in waited and not deploy_waits(entries(a.label), a.env, handed):
        raise_deploy(fleet, {"label": a.label, "key": f"deploy/{a.env}"})


def steps(fleet, a):
    _, _, st = state(entries(a.label))
    print(json.dumps([dict(to=to, key=key, state=e.get("State"), by=e.get("By"), at=e["At"], note=e.get("Note"))
                      for (env, to, key), e in ordered(st) if env == a.env]))


# What `quiet` runs on the environment's host: how many of crew's tests hold a test slot there (tests/slot).
SLOTS = r"""import fcntl, glob, os, sys
busy = 0
for f in glob.glob(os.path.expanduser("~/.cache/crew/test-slots/slot-*")):
    fd = os.open(f, os.O_RDWR)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        busy += 1
    finally:
        os.close(fd)
print(busy)
"""


def quiet(fleet, a):
    """Whether the environment's host is quiet: no Flume place of the drive's with a stage working there
    (places_working), and no test of crew's running."""
    a.env in fleet["hosts"] or fail(f"{a.env} is no host the teams file's hosts name. hosts: " + (" ".join(sorted(fleet["hosts"])) or "none"))
    working = places_working(fleet, a.label, a.env)
    not isinstance(working, str) or fail(f"crew can't tell whether a place works on {a.env}: {working}")
    said = [f"{w} is working" for w in working]
    r = crew.on_machine(fleet, a.env, ["python3", "-c", SLOTS])
    if r.returncode or not r.stdout.strip().isdigit():
        fail(f"crew can't tell whether a test runs on {a.env}: " + (crew.unanswered(a.env, r) or (r.stderr or "").strip() or "no answer"))
    if int(r.stdout.strip()):
        said.append(f"{r.stdout.strip()} of crew's tests are running on {a.env}")
    if said:
        print("; ".join(said))
        sys.exit(1)


COMMANDS = {"offer": offer, "approve": approve, "word": word, "record": record_cmd, "step": step, "settle": settle, "steps": steps,
            "quiet": quiet}


def parser():
    ap = argparse.ArgumentParser(prog="crew ops", description="The operations on a drive's environments, a deploy being one kind.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    def cmd(name, to=True):
        p = sub.add_parser(name)
        p.add_argument("env")
        p.add_argument("--label", required=True)
        p.add_argument("--to", required=to)
        return p
    p = cmd("offer")
    p.add_argument("--from", required=True)
    p.add_argument("--notes")
    p.add_argument("--steps")
    p.add_argument("--handed", choices=("-",), help=argparse.SUPPRESS)  # an offer forwarded here: forwarded's
    cmd("approve")
    cmd("word", to=False)
    p = cmd("record")
    p.add_argument("--act", required=True, choices=ACTS)
    p.add_argument("--from")
    p.add_argument("--step", choices=("machine", "guests", "suite"))
    p.add_argument("--outcome", choices=("ok", "failed", "done"))
    p.add_argument("--log")
    p.add_argument("--rows")
    p.add_argument("--does")  # the deployer's words of what the user does about a failure, taken on every act
    p = cmd("step", to=False)
    p.add_argument("--key", required=True)
    p.add_argument("--state", required=True, choices=STATES)
    p.add_argument("--doer", choices=DOERS)
    p.add_argument("--agent")
    p.add_argument("--when", choices=("deployed", "quiet"))
    p.add_argument("--held", action="store_true")
    p.add_argument("--text")
    p.add_argument("--changes")
    p.add_argument("--note")
    p = sub.add_parser("settle")
    p.add_argument("key")
    p.add_argument("--label", required=True)
    p.add_argument("--state", required=True, choices=("done", "declined"))
    p = cmd("steps", to=False)
    p.add_argument("--json", action="store_true", required=True)
    cmd("quiet", to=False)
    return ap


def args_refusal(fleet, a):
    """Why crew ops refuses what it was given, or None: an environment's name, a drive of the teams file, a
    commit as a sha in hex (--from none for nothing deployed), a step key crew takes, a step card's key, op/<env>/<n>,
    for crew ops settle, and --held only on an agent's step, since a user's waits on the user already."""
    if getattr(a, "env", None) is not None and not NAME.match(a.env):
        return f"{a.env} is no environment's name: lowercase words and dashes"
    if a.cmd == "settle" and not STEP_CARD.match(a.key):
        return f"{a.key} is no step card's key: op/<env>/<n>, as the rail shows it"
    if a.label not in fleet["drives"]:
        return f"no drive {a.label} in the teams file. drives: " + " ".join(fleet["drives"])
    for f in ("to", "from"):
        v = getattr(a, f, None)
        if v and not (v == "none" and f == "from") and not SHA.match(v):
            return f"--{f} {v} is no commit: a sha in hex"
    if a.cmd == "step" and not STEP_KEY.match(a.key):
        return f"--key {a.key} is no step key crew takes"
    if getattr(a, "held", False) and a.doer in (None, "user"):
        return "--held marks an agent's step held for the user's word: give its --doer, main-ops"
    if getattr(a, "handed", None) and (a.notes or a.steps):
        return "--handed carries the text of the files --notes and --steps name, so it is given in their place"
    return None


def main(argv):
    ap = parser()
    crew.answer_usage(ap, argv)
    a = ap.parse_args(argv)
    fleet = crew.load()
    why = args_refusal(fleet, a)
    why is None or fail(why)
    machine = crew.drive_of(fleet, a.label)["machine"]
    a.texts = offered_texts(a) if a.cmd == "offer" else None
    a.rows_json = recorded_rows(a) if a.cmd == "record" else None
    a.step_text = stepped_text(a) if a.cmd == "step" else None
    if a.cmd != "quiet" and machine != crew.this_host():
        args, carried = forwarded(a, argv, *(a.texts or (None, None)), rows=a.rows_json, text=a.step_text)
        r = crew.on_machine(fleet, machine, crew.crew_argv(fleet, machine, "ops", *args), input=carried)
        sys.stdout.write(r.stdout), sys.stderr.write(r.stderr)
        if r.returncode == 255 and crew.unanswered(machine, r):
            sys.exit(f"{a.label}'s operations are kept on {machine}, which did not answer: {crew.unanswered(machine, r)}")
        sys.exit(r.returncode)
    COMMANDS[a.cmd](fleet, a)


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except Refusal as e:
        sys.exit(str(e))
