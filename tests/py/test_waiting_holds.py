"""A started bolt waiting on the user is held under words naming what for (the change
a-bolt-waiting-on-the-user-waits-under-words; bolt-teams "A started bolt waiting on the user is held under words naming
what for", "A waiting bolt's hold is posted once for its words, and again as its bound nears" and "A wait that ends
ends crew's hold"): whether a hold of a bolt's base place is due, from crew's requests and Flume's status of the place
as the runner carried it (runner.hold_due), on flume 0.26.0's shapes (tests/py/flume-0.26.0/). Each on plain facts
(code.7)."""
import pytest

from facts import ran
import plan
import runner

AT, BY = "2026-11-16T12:00:00Z", "madswan-ops"
# A bolt's own launch, its base place, as a start appends it (runner.bolt_launch).
BOLT = dict(Repo="afterthought/crew", Kind="crew/bolt", Name="z", Base="main", Priority=2, Intent="madswan/z", Recipient="madswan/ops")
SEND = "the user, by their send of its row on crew's landings card, land/crew: it is marked to stay"
LIFT = """the user, by lifting the hold on crew's landings ("Cutover") with crew plan go: it then lands on proof"""
# The hold standing on the base place in tests/py/flume-0.26.0/bolt-held.json: SEND's words, since and bound.
SINCE, DAY = 1794700300, 86400


def rec(n, act, **given):
    return plan.Rec("Request", runner.request_fields(n, act, "bolt/z", dict(BOLT, **given) if act == "launch" else given, AT, BY))


def requests(*more):
    """requests.rec's records: request 1 the launch of bolt/z, then each given (act, {fields}), numbered in turn."""
    return [rec(1, "launch")] + [rec(n, act, **given) for n, (act, given) in enumerate(more, start=2)]


def hold(words=SEND, bound=runner.HOLD_BOUND):
    return ("hold", dict(Of=1, Words=words, Bound=bound))


def due(rs, reads, words: "str | None" = SEND, now=SINCE + DAY):
    return runner.hold_due(rs[0], words, rs, reads, now)


def base(name, done=(), **more):
    """The runner on deneb as crew reads it, having launched request 1 at the base place
    tests/py/flume-0.26.0/<name>.json stands at, and answered each request in done done."""
    return ran({1: f"flume-0.26.0/{name}"}, done=done, **more)


def waiting_on_nothing(reads):
    """reads with the base place waiting on no move of its caller's, as when a fix is live on its branch."""
    reads["deneb"]["places"][1]["status"]["status"]["places"][0]["waiting_on"] = None
    return reads


class TestHoldDue:
    """runner.hold_due: a base place waiting on crew is due crew's words, again past half their bound or once lapsed,
    an end where crew's own words stand and nothing waits on the user, and nothing while a hold waits on the runner's
    answer, a land stands, the place waits on no move, or the hold standing is not crew's (design Decisions 3 and 4)."""

    def test_a_base_place_waiting_under_no_hold_is_due_the_words(self):
        """bolt-teams, Marked to stay: its base place waits on crew for a retry of its submission under no hold."""
        assert due(requests(), base("bolt-unsubmitted")) == ("hold", SEND)

    def test_the_same_words_standing_with_more_than_half_their_bound_left_are_due_nothing(self):
        """bolt-teams, Read again: the hold crew posted stands with the same words, posted a day before."""
        assert due(requests(hold()), base("bolt-held", done=[2]), now=SINCE + DAY) is None
        assert due(requests(hold()), base("bolt-held", done=[2]), now=SINCE + 3 * DAY) is None

    def test_the_same_words_past_half_their_bound_are_due_again(self):
        """bolt-teams, Past half its bound: taken four days before."""
        assert due(requests(hold()), base("bolt-held", done=[2]), now=SINCE + 4 * DAY) == ("hold", SEND)
        assert due(requests(hold()), base("bolt-held", done=[2]), now=SINCE + runner.HOLD_BOUND // 2) == ("hold", SEND)

    def test_a_lapsed_hold_is_due_the_words_again(self):
        """bolt-teams, Lapsed."""
        assert due(requests(hold()), base("bolt-held-lapsed", done=[2]), now=SINCE + 8 * DAY) == ("hold", SEND)

    def test_new_words_replace_the_standing_ones(self):
        """bolt-teams, The wait changes: the user put a hold on crew while z waited on their send under crew's hold."""
        words = SEND + """; then by lifting the hold on crew's landings ("Cutover") with crew plan go"""
        assert due(requests(hold()), base("bolt-held", done=[2]), words=words) == ("hold", words)
        assert due(requests(hold()), base("bolt-held", done=[2]), words=LIFT) == ("hold", LIFT)

    def test_a_hold_the_runner_has_not_answered_holds_back_any_other(self):
        """bolt-teams, Waiting on the runner's answer: whatever z waits on, nothing more is posted, so a runner that
        does not carry holds yet is asked once."""
        rs = requests(hold())
        for name in ("bolt-unsubmitted", "bolt-held", "bolt-held-lapsed"):
            assert due(rs, base(name)) is None
            assert due(rs, base(name), words=LIFT) is None
            assert due(rs, base(name), words=None) is None
        assert due(requests(hold(), hold(LIFT)), base("bolt-held-lapsed", done=[2]), words=SEND) is None

    def test_a_land_asked_or_submitted_is_due_no_hold(self):
        """bolt-teams, A land standing: asked, unanswered, or submitted, the move made; a land the runner refused is
        stopped, and the bolt waits on the user's send again."""
        land = ("land", dict(Of=1))
        assert due(requests(land), base("bolt-unsubmitted")) is None
        assert due(requests(land), ran({1: "flume-0.17.0/bolt-submitted"}, done=[2])) is None
        assert due(requests(land), ran({1: "flume-0.17.0/bolt-submitted"}, done=[2]), words=None) is None
        assert due(requests(land), base("bolt-unsubmitted", refused={2: "a place on bolt/z is live"})) == ("hold", SEND)

    def test_a_base_place_waiting_on_no_move_is_due_no_hold(self):
        """bolt-teams, A base place that waits on nothing of crew's: Flume refuses a hold of a place that waits on none."""
        assert due(requests(), waiting_on_nothing(base("bolt-unsubmitted"))) is None
        assert due(requests(hold()), waiting_on_nothing(base("bolt-held", done=[2])), words=None) is None

    def test_crews_standing_words_with_no_wait_are_due_an_end(self):
        """bolt-teams, The bolt no longer waits on the user: crew's hold ends with a hold of bound 0."""
        assert due(requests(hold()), base("bolt-held", done=[2]), words=None) == ("end", runner.HOLD_ENDED)
        assert due(requests(hold(LIFT), hold()), base("bolt-held", done=[2, 3]), words=None) == ("end", runner.HOLD_ENDED)

    def test_after_an_end_nothing_more_is_due(self):
        """The end is the newest hold crew posted: nothing more is posted for it, whether Flume has let it lapse yet or
        not, and no end is posted where no hold stands."""
        ended = requests(hold(), hold(runner.HOLD_ENDED, 0))
        assert due(ended, base("bolt-held", done=[2, 3]), words=None) is None
        assert due(ended, base("bolt-held-lapsed", done=[2, 3]), words=None) is None
        assert due(ended, base("bolt-unsubmitted", done=[2, 3]), words=None) is None
        assert due(requests(hold()), base("bolt-held-lapsed", done=[2]), words=None) is None
        assert due(requests(), base("bolt-unsubmitted"), words=None) is None

    def test_a_hold_crew_never_posted_is_left(self):
        """bolt-teams, A hold not crew's: words crew never posted of the launch stand on the place."""
        assert due(requests(hold(LIFT)), base("bolt-held", done=[2]), words=None) is None
        assert due(requests(), base("bolt-held"), words=None) is None

    def test_no_launch_or_an_unread_runner_is_due_nothing(self):
        """read.1: a bolt from before bolts were base places, a launch no runner crew read has taken, two runners that
        took it, or a runner crew can't read."""
        rs = requests()
        assert runner.hold_due(None, SEND, rs, base("bolt-unsubmitted"), SINCE) is None
        assert due(rs, ran(label="madswan")) is None
        assert due(rs, {}) is None
        assert due(rs, dict(base("bolt-unsubmitted"), **ran({1: "flume-0.26.0/bolt-unsubmitted"}, host="mac-studio"))) is None
        unread = {"mac-studio": {"host": "mac-studio", "why": "no branch madswan/runner/mac-studio", "answers": {}, "places": {}}}
        assert due(rs, dict(ran(label="madswan"), **unread)) is None
        assert due(rs, ran(held={1: "no room"})) is None


CUTOVER = {"kit": "crew", "why": "Cutover"}


def facts(can=True, how="proof", stays=False, left=False, stop=None, hold=None, batches=(), known=True):
    """A land row's bolt's facts as rail_rows hands user_wait them."""
    return dict(can=can, how=how, stays=stays, left=left, stop=stop, hold=hold, batches=list(batches), known=known)


class TestUserWait:
    """plan.user_wait: a bolt of a land row waits on the user's send, their lift of a hold or their answer to batches,
    on nothing of theirs, or on what crew can't tell (design Decision 2)."""

    def test_a_bolt_marked_to_stay_waits_on_the_send(self):
        """bolt-teams, Marked to stay."""
        assert plan.user_wait(facts(how="send", stays=True)) == {"on": "send", "why": "stays", "hold": None}

    def test_a_left_bolt_and_a_stopped_one_wait_on_the_send_saying_why(self):
        """bolt-teams, Left by the user; Its land stopped."""
        assert plan.user_wait(facts(how="send", left=True)) == {"on": "send", "why": "left", "hold": None}
        assert plan.user_wait(facts(how="send", stop="a place on bolt/y is live")) == {"on": "send", "why": "stopped", "hold": None}

    def test_a_bolt_marked_to_stay_under_a_hold_waits_on_both(self):
        """bolt-teams, Marked to stay under a hold: lands_by reads send under a hold, and the wait names both."""
        assert plan.user_wait(facts(how="send", stays=True, hold=CUTOVER)) == {"on": "send", "why": "stays", "hold": CUTOVER}

    def test_a_bolt_due_a_land_on_proof_under_a_hold_waits_on_its_lift(self):
        """bolt-teams, Under a hold on its kit."""
        assert plan.user_wait(facts(how="hold", hold=CUTOVER)) == {"on": "hold", "hold": CUTOVER}

    def test_a_bolt_kept_only_by_unanswered_batches_waits_on_them(self):
        """bolt-teams, Waiting on a batch: rail_rows hands the batches only where they alone keep it."""
        assert plan.user_wait(facts(can=False, batches=[5])) == {"on": "batch", "batches": [5], "hold": None}
        assert plan.user_wait(facts(can=False, how="hold", batches=[5, 4], hold=CUTOVER)) == {"on": "batch", "batches": [4, 5], "hold": CUTOVER}

    def test_a_bolt_landing_on_proof_or_waiting_on_crew_waits_on_nothing_of_the_users(self):
        """bolt-teams, Waiting on nothing of the user's; A change in no batch yet: its verification not green, a change
        in no batch, a fix in flight, main to take first or a landing in flight, each giving the row no batches."""
        assert plan.user_wait(facts()) == {"on": "none"}
        assert plan.user_wait(facts(can=False)) == {"on": "none"}
        assert plan.user_wait(facts(can=False, how="send", stays=True)) == {"on": "none"}
        assert plan.user_wait(facts(can=False, how="hold", hold=CUTOVER)) == {"on": "none"}

    def test_a_fact_crew_cant_read_is_unknown(self):
        """bolt-teams, What crew can't read (read.1)."""
        why = "its verification can't be read: no landing of its work at abc1234 can be read"
        assert plan.user_wait(facts(can=False, known=why)) == {"on": "unknown", "why": why}
        assert plan.user_wait(facts(how="send", stays=True, known=why)) == {"on": "unknown", "why": why}


class TestWaitWords:
    """plan.wait_words: each wait in crew's words, naming who makes the move, how, and where the user answers it, word
    for word as bolt-teams' scenarios give them (design Decision 2)."""
    HEAD = "abc1234" + "0" * 33

    def words(self, wait, label="swancloud", kit="crew"):
        return plan.wait_words(label, kit, wait, self.HEAD)

    def test_the_send_words_say_why(self):
        """bolt-teams, Marked to stay; Left by the user; Its land stopped."""
        assert self.words({"on": "send", "why": "stays", "hold": None}) == SEND
        assert self.words({"on": "send", "why": "left", "hold": None}) == (
            "the user, by their send of its row on crew's landings card, land/crew: they left it unticked on an earlier send")
        assert self.words({"on": "send", "why": "stopped", "hold": None}) == (
            "the user, by their send of its row on crew's landings card, land/crew: its land at abc1234 was stopped")

    def test_the_hold_words_name_the_hold_and_its_why(self):
        """bolt-teams, Under a hold on its kit; and a hold on the whole drive."""
        assert self.words({"on": "hold", "hold": CUTOVER}) == LIFT
        assert self.words({"on": "hold", "hold": {"kit": None, "why": "Freeze"}}) == (
            """the user, by lifting the hold on the landings of swancloud's every kit ("Freeze") with crew plan go: it then lands on proof""")

    def test_the_batch_words_name_each_batch_and_its_card(self):
        """bolt-teams, Waiting on a batch."""
        assert self.words({"on": "batch", "batches": [5], "hold": None}) == "the user, by answering review batch 5 on its card, batch/5"
        assert self.words({"on": "batch", "batches": [4, 5], "hold": None}) == (
            "the user, by answering review batches 4 and 5 on their cards, batch/4 and batch/5")
        assert self.words({"on": "batch", "batches": [3, 4, 5], "hold": None}) == (
            "the user, by answering review batches 3, 4 and 5 on their cards, batch/3, batch/4 and batch/5")

    def test_a_send_or_batch_under_a_hold_names_the_hold_after(self):
        """bolt-teams, Marked to stay under a hold: the send on land/crew, then the lift of the hold on crew's landings."""
        lift = """; then by lifting the hold on crew's landings ("Cutover") with crew plan go"""
        assert self.words({"on": "send", "why": "stays", "hold": CUTOVER}) == SEND + lift
        assert self.words({"on": "batch", "batches": [5], "hold": CUTOVER}) == "the user, by answering review batch 5 on its card, batch/5" + lift

    def test_no_words_for_none_or_unknown(self):
        assert self.words({"on": "none"}) is None
        assert self.words({"on": "unknown", "why": "its verification can't be read"}) is None
