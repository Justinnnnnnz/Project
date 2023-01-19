# coding=utf-8
#
# This file is part of Hypothesis, which may be found at
# https://github.com/HypothesisWorks/hypothesis/
#
# Most of this work is copyright (C) 2013-2019 David R. MacIver
# (david@drmaciver.com), but it contains contributions by others. See
# CONTRIBUTING.rst for a full list of people who may hold copyright, and
# consult the git log if you need to determine who owns an individual
# contribution.
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at https://mozilla.org/MPL/2.0/.
#
# END HEADER

from __future__ import absolute_import, division, print_function

from collections import defaultdict

import attr

from hypothesis.internal.compat import hbytes, hrange, int_from_bytes, int_to_bytes
from hypothesis.internal.conjecture.data import ConjectureResult, Overrun, Status
from hypothesis.internal.conjecture.floats import (
    DRAW_FLOAT_LABEL,
    float_to_lex,
    lex_to_float,
)
from hypothesis.internal.conjecture.junkdrawer import (
    binary_search,
    pop_random,
    replace_all,
)
from hypothesis.internal.conjecture.shrinking import Float, Integer, Lexical, Ordering
from hypothesis.internal.conjecture.shrinking.common import find_integer

if False:
    from typing import Dict  # noqa


def sort_key(buffer):
    """Returns a sort key such that "simpler" buffers are smaller than
    "more complicated" ones.

    We define sort_key so that x is simpler than y if x is shorter than y or if
    they have the same length and x < y lexicographically. This is called the
    shortlex order.

    The reason for using the shortlex order is:

    1. If x is shorter than y then that means we had to make fewer decisions
       in constructing the test case when we ran x than we did when we ran y.
    2. If x is the same length as y then replacing a byte with a lower byte
       corresponds to reducing the value of an integer we drew with draw_bits
       towards zero.
    3. We want a total order, and given (2) the natural choices for things of
       the same size are either the lexicographic or colexicographic orders
       (the latter being the lexicographic order of the reverse of the string).
       Because values drawn early in generation potentially get used in more
       places they potentially have a more significant impact on the final
       result, so it makes sense to prioritise reducing earlier values over
       later ones. This makes the lexicographic order the more natural choice.
    """
    return (len(buffer), buffer)


SHRINK_PASS_DEFINITIONS = {}  # type: Dict[str, ShrinkPassDefinition]


@attr.s()
class ShrinkPassDefinition(object):
    """A shrink pass bundles together a large number of local changes to
    the current shrink target.

    Each shrink pass is defined by some function and some arguments to that
    function. The ``generate_arguments`` function returns all arguments that
    might be useful to run on the current shrink target.

    The guarantee made by methods defined this way is that after they are
    called then *either* the shrink target has changed *or* each of
    ``fn(*args)`` has been called for every ``args`` in ``generate_arguments(self)``.
    No guarantee is made that all of these will be called if the shrink target
    changes.
    """

    run_step = attr.ib()
    generate_arguments = attr.ib()

    @property
    def name(self):
        return self.run_step.__name__

    def __attrs_post_init__(self):
        assert self.name not in SHRINK_PASS_DEFINITIONS, self.name
        SHRINK_PASS_DEFINITIONS[self.name] = self


def defines_shrink_pass(generate_arguments):
    """A convenient decorator for defining shrink passes."""

    def accept(run_step):
        definition = ShrinkPassDefinition(
            generate_arguments=generate_arguments, run_step=run_step
        )

        def run(self):
            return self.run_shrink_pass(definition.name)

        run.__name__ = run_step.__name__
        run.is_shrink_pass = True
        return run

    return accept


class Shrinker(object):
    """A shrinker is a child object of a ConjectureRunner which is designed to
    manage the associated state of a particular shrink problem. That is, we
    have some initial ConjectureData object and some property of interest
    that it satisfies, and we want to find a ConjectureData object with a
    shortlex (see sort_key above) smaller buffer that exhibits the same
    property.

    Currently the only property of interest we use is that the status is
    INTERESTING and the interesting_origin takes on some fixed value, but we
    may potentially be interested in other use cases later.
    However we assume that data with a status < VALID never satisfies the predicate.

    The shrinker keeps track of a value shrink_target which represents the
    current best known ConjectureData object satisfying the predicate.
    It refines this value by repeatedly running *shrink passes*, which are
    methods that perform a series of transformations to the current shrink_target
    and evaluate the underlying test function to find new ConjectureData
    objects. If any of these satisfy the predicate, the shrink_target
    is updated automatically. Shrinking runs until no shrink pass can
    improve the shrink_target, at which point it stops. It may also be
    terminated if the underlying engine throws RunIsComplete, but that
    is handled by the calling code rather than the Shrinker.

    =======================
    Designing Shrink Passes
    =======================

    Generally a shrink pass is just any function that calls
    cached_test_function and/or incorporate_new_buffer a number of times,
    but there are a couple of useful things to bear in mind.

    A shrink pass *makes progress* if running it changes self.shrink_target
    (i.e. it tries a shortlex smaller ConjectureData object satisfying
    the predicate). The desired end state of shrinking is to find a
    value such that no shrink pass can make progress, i.e. that we
    are at a local minimum for each shrink pass.

    In aid of this goal, the main invariant that a shrink pass much
    satisfy is that whether it makes progress must be deterministic.
    It is fine (encouraged even) for the specific progress it makes
    to be non-deterministic, but if you run a shrink pass, it makes
    no progress, and then you immediately run it again, it should
    never succeed on the second time. This allows us to stop as soon
    as we have run each shrink pass and seen no progress on any of
    them.

    This means that e.g. it's fine to try each of N deletions
    or replacements in a random order, but it's not OK to try N random
    deletions (unless you have already shrunk at least once, though we
    don't currently take advantage of this loophole).

    Shrink passes need to be written so as to be robust against
    change in the underlying shrink target. It is generally safe
    to assume that the shrink target does not change prior to the
    point of first modification - e.g. if you change no bytes at
    index ``i``, all examples whose start is ``<= i`` still exist,
    as do all blocks, and the data object is still of length
    ``>= i + 1``. This can only be violated by bad user code which
    relies on an external source of non-determinism.

    When the underlying shrink_target changes, shrink
    passes should not run substantially more test_function calls
    on success than they do on failure. Say, no more than a constant
    factor more. In particular shrink passes should not iterate to a
    fixed point.

    This means that shrink passes are often written with loops that
    are carefully designed to do the right thing in the case that no
    shrinks occurred and try to adapt to any changes to do a reasonable
    job. e.g. say we wanted to write a shrink pass that tried deleting
    each individual byte (this isn't an especially good choice,
    but it leads to a simple illustrative example), we might do it
    by iterating over the buffer like so:

    .. code-block:: python

        i = 0
        while i < len(self.shrink_target.buffer):
            if not self.incorporate_new_buffer(
                self.shrink_target.buffer[: i] +
                self.shrink_target.buffer[i + 1 :]
            ):
                i += 1

    The reason for writing the loop this way is that i is always a
    valid index into the current buffer, even if the current buffer
    changes as a result of our actions. When the buffer changes,
    we leave the index where it is rather than restarting from the
    beginning, and carry on. This means that the number of steps we
    run in this case is always bounded above by the number of steps
    we would run if nothing works.

    Another thing to bear in mind about shrink pass design is that
    they should prioritise *progress*. If you have N operations that
    you need to run, you should try to order them in such a way as
    to avoid stalling, where you have long periods of test function
    invocations where no shrinks happen. This is bad because whenever
    we shrink we reduce the amount of work the shrinker has to do
    in future, and often speed up the test function, so we ideally
    wanted those shrinks to happen much earlier in the process.

    Sometimes stalls are inevitable of course - e.g. if the pass
    makes no progress, then the entire thing is just one long stall,
    but it's helpful to design it so that stalls are less likely
    in typical behaviour.

    The two easiest ways to do this are:

    * Just run the N steps in random order. As long as a
      reasonably large proportion of the operations suceed, this
      guarantees the expected stall length is quite short. The
      book keeping for making sure this does the right thing when
      it succeeds can be quite annoying.
    * When you have any sort of nested loop, loop in such a way
      that both loop variables change each time. This prevents
      stalls which occur when one particular value for the outer
      loop is impossible to make progress on, rendering the entire
      inner loop into a stall.

    However, although progress is good, too much progress can be
    a bad sign! If you're *only* seeing successful reductions,
    that's probably a sign that you are making changes that are
    too timid. Two useful things to offset this:

    * It's worth writing shrink passes which are *adaptive*, in
      the sense that when operations seem to be working really
      well we try to bundle multiple of them together. This can
      often be used to turn what would be O(m) successful calls
      into O(log(m)).
    * It's often worth trying one or two special minimal values
      before trying anything more fine grained (e.g. replacing
      the whole thing with zero).

    """

    def derived_value(fn):
        """It's useful during shrinking to have access to derived values of
        the current shrink target.

        This decorator allows you to define these as cached properties. They
        are calculated once, then cached until the shrink target changes, then
        recalculated the next time they are used."""

        def accept(self):
            try:
                return self.__derived_values[fn.__name__]
            except KeyError:
                return self.__derived_values.setdefault(fn.__name__, fn(self))

        accept.__name__ = fn.__name__
        return property(accept)

    def __init__(self, engine, initial, predicate):
        """Create a shrinker for a particular engine, with a given starting
        point and predicate. When shrink() is called it will attempt to find an
        example for which predicate is True and which is strictly smaller than
        initial.

        Note that initial is a ConjectureData object, and predicate
        takes ConjectureData objects.
        """
        self.__engine = engine
        self.__predicate = predicate
        self.__shrinking_prefixes = set()
        self.__derived_values = {}
        self.__pending_shrink_explanation = None

        self.initial_size = len(initial.buffer)

        # We keep track of the current best example on the shrink_target
        # attribute.
        self.shrink_target = None
        self.update_shrink_target(initial)
        self.shrinks = 0

        self.initial_calls = self.__engine.call_count

        self.passes_by_name = {}
        self.passes = []

    def explain_next_call_as(self, explanation):
        self.__pending_shrink_explanation = explanation

    def clear_call_explanation(self):
        self.__pending_shrink_explanation = None

    def add_new_pass(self, run):
        """Creates a shrink pass corresponding to calling ``run(self)``"""

        definition = SHRINK_PASS_DEFINITIONS[run]

        p = ShrinkPass(
            run_with_arguments=definition.run_step,
            generate_arguments=definition.generate_arguments,
            shrinker=self,
            index=len(self.passes),
        )
        self.passes.append(p)
        self.passes_by_name[p.name] = p
        return p

    def shrink_pass(self, name):
        """Return the ShrinkPass object for the pass with the given name."""
        if name not in self.passes_by_name:
            self.add_new_pass(name)
        return self.passes_by_name[name]

    @property
    def calls(self):
        """Return the number of calls that have been made to the underlying
        test function."""
        return self.__engine.call_count

    def consider_new_buffer(self, buffer):
        """Returns True if after running this buffer the result would be
        the current shrink_target."""
        buffer = hbytes(buffer)
        return buffer.startswith(self.buffer) or self.incorporate_new_buffer(buffer)

    def incorporate_new_buffer(self, buffer):
        """Either runs the test function on this buffer and returns True if
        that changed the shrink_target, or determines that doing so would
        be useless and returns False without running it."""

        buffer = hbytes(buffer[: self.shrink_target.index])
        # Sometimes an attempt at lexicographic minimization will do the wrong
        # thing because the buffer has changed under it (e.g. something has
        # turned into a write, the bit size has changed). The result would be
        # an invalid string, but it's better for us to just ignore it here as
        # it turns out to involve quite a lot of tricky book-keeping to get
        # this right and it's better to just handle it in one place.
        if sort_key(buffer) >= sort_key(self.shrink_target.buffer):
            return False

        if self.shrink_target.buffer.startswith(buffer):
            return False

        previous = self.shrink_target
        self.cached_test_function(buffer)
        return previous is not self.shrink_target

    def incorporate_test_data(self, data):
        """Takes a ConjectureData or Overrun object updates the current
        shrink_target if this data represents an improvement over it,
        returning True if it is."""
        if data is Overrun or data is self.shrink_target:
            return
        if self.__predicate(data) and sort_key(data.buffer) < sort_key(
            self.shrink_target.buffer
        ):
            self.update_shrink_target(data)
            self.__shrinking_block_cache = {}
            return True
        return False

    def cached_test_function(self, buffer):
        """Returns a cached version of the underlying test function, so
        that the result is either an Overrun object (if the buffer is
        too short to be a valid test case) or a ConjectureData object
        with status >= INVALID that would result from running this buffer."""

        if self.__pending_shrink_explanation is not None:
            self.debug(self.__pending_shrink_explanation)
            self.__pending_shrink_explanation = None

        buffer = hbytes(buffer)
        result = self.__engine.cached_test_function(buffer)
        self.incorporate_test_data(result)
        return result

    def debug(self, msg):
        self.__engine.debug(msg)

    @property
    def random(self):
        return self.__engine.random

    def run_shrink_pass(self, sp):
        """Runs the function associated with ShrinkPass sp and updates the
        relevant metadata.

        Note that sp may or may not be a pass currently associated with
        this shrinker. This does not handle any requeing that is
        required.
        """
        sp = self.shrink_pass(sp)

        self.debug("Shrink Pass %s" % (sp.name,))
        try:
            sp.runs += 1

            steps = sp.generate_steps()
            self.random.shuffle(steps)
            for s in steps:
                sp.run_step(s)
        finally:
            self.debug("Shrink Pass %s completed." % (sp.name,))

    def shrink(self):
        """Run the full set of shrinks and update shrink_target.

        This method is "mostly idempotent" - calling it twice is unlikely to
        have any effect, though it has a non-zero probability of doing so.
        """
        # We assume that if an all-zero block of bytes is an interesting
        # example then we're not going to do better than that.
        # This might not technically be true: e.g. for integers() | booleans()
        # the simplest example is actually [1, 0]. Missing this case is fairly
        # harmless and this allows us to make various simplifying assumptions
        # about the structure of the data (principally that we're never
        # operating on a block of all zero bytes so can use non-zeroness as a
        # signpost of complexity).
        if not any(self.shrink_target.buffer) or self.incorporate_new_buffer(
            hbytes(len(self.shrink_target.buffer))
        ):
            return

        try:
            self.greedy_shrink()
        finally:
            if self.__engine.report_debug_info:

                def s(n):
                    return "s" if n != 1 else ""

                total_deleted = self.initial_size - len(self.shrink_target.buffer)

                self.debug("---------------------")
                self.debug("Shrink pass profiling")
                self.debug("---------------------")
                self.debug("")
                calls = self.__engine.call_count - self.initial_calls
                self.debug(
                    (
                        "Shrinking made a total of %d call%s "
                        "of which %d shrank. This deleted %d byte%s out of %d."
                    )
                    % (
                        calls,
                        s(calls),
                        self.shrinks,
                        total_deleted,
                        s(total_deleted),
                        self.initial_size,
                    )
                )
                for useful in [True, False]:
                    self.debug("")
                    if useful:
                        self.debug("Useful passes:")
                    else:
                        self.debug("Useless passes:")
                    self.debug("")
                    for p in sorted(
                        self.passes,
                        key=lambda t: (-t.calls, -t.runs, t.deletions, t.shrinks),
                    ):
                        if p.calls == 0:
                            continue
                        if (p.shrinks != 0) != useful:
                            continue

                        self.debug(
                            (
                                "  * %s ran %d time%s, making %d call%s of which "
                                "%d shrank, deleting %d byte%s."
                            )
                            % (
                                p.name,
                                p.runs,
                                s(p.runs),
                                p.calls,
                                s(p.calls),
                                p.shrinks,
                                p.deletions,
                                s(p.deletions),
                            )
                        )
                self.debug("")

    def greedy_shrink(self):
        """Run a full set of greedy shrinks (that is, ones that will only ever
        move to a better target) and update shrink_target appropriately.

        This method iterates to a fixed point and so is idempontent - calling
        it twice will have exactly the same effect as calling it once.
        """

        # The two main parts of shortlex optimisation are of course making
        # the test case "short" and "lex" (that is to say, lexicographically.
        # smaller). Sometimes these are intertwined and it's hard to do one
        # without the other, but as far as we can we *vastly* prefer to make
        # the test case shorter over making it lexicographically smaller.
        # The reason for this is that we can only make O(n) progress on
        # reducing the size, but at a fixed size there are O(256^n)
        # lexicographically smaller values. As a result it's easier to
        # reach a fixed point on size and also every reduction we make
        # in size reduces the amount of work we have to do lexicographically.
        # On top of that, reducing the size makes generation much faster,
        # so even if reducing the size earlier doesn't reduce the number
        # of test cases we run it may still result in significantly faster
        # tests.
        #
        # As a result of this we start by running a bunch of operations
        # that are primarily designed to reduce the size of the test.
        #
        # These fall into two categories:
        #
        # * "structured" ones respect the boundaries of draw calls and are
        #   likely to correspond to semantically meaningful transformations
        #   of the generated test case (e.g. deleting an element of a list,
        #   replacing a tree node with one of its children).
        # * "unstructured" ones will often not correspond to any meaningful
        #   transformation but may succeed by accident or because they happen
        #   to correspond to an unexpectedly meaningful operation (e.g.
        #   merging two adjacent lists).
        #
        # Generally we expect unstructured ones to succeed early on when
        # the test case has a lot of redundancy because they have plenty
        # of opportunity to work by accident, and after that they're mostly
        # unlikely work. As a result we do a slightly odd thing where we
        # run unstructured deletions as part of the initial pass, but then
        # we hold off on running them to a fixed point until we've turned
        # the emergency passes on later.
        unstructured_deletions = [block_program("X" * i) for i in hrange(5, 0, -1)]
        structured_deletions = ["pass_to_descendant", "adaptive_example_deletion"]
        self.fixate_shrink_passes(unstructured_deletions + structured_deletions)

        # "fine" passes are ones that are primarily concerned with lexicographic
        # reduction. They may still delete data (either deliberately or by accident)
        # but the distinguishing feature is that it is possible for them to
        # succeed without the length of the test case changing.
        # As a result we only start running them after we've hit a fixed point
        # for the deletion passes at least once.
        fine = [
            "alphabet_minimize",
            "zero_examples",
            "reorder_examples",
            "minimize_floats",
            "minimize_duplicated_blocks",
            "minimize_individual_blocks",
        ]

        self.fixate_shrink_passes(structured_deletions + fine)

        # "emergency" shrink passes are ones that handle cases that we
        # can't currently handle more elegantly - either they're slightly
        # weird hacks that happen to work or they're expensive passes to
        # run. Generally we hope that the emergency passes don't do anything
        # at all. We also re-enable the unstructured deletions at this point
        # in case new ones have been unlocked since we last ran them, but
        # don't expect that to be a common occurrence..
        emergency = [block_program("-XX"), "example_deletion_with_block_lowering"]

        self.fixate_shrink_passes(
            unstructured_deletions + structured_deletions + fine + emergency
        )

    def fixate_shrink_passes(self, passes):
        """Run steps from each pass in ``passes`` until the current shrink target
        is a fixed point of all of them."""
        passes = list(map(self.shrink_pass, passes))

        initial = None
        while initial is not self.shrink_target:
            initial = self.shrink_target
            for sp in passes:
                sp.runs += 1

            # We run remove_discarded after every step to do cleanup
            # keeping track of whether that actually works. Either there is
            # no discarded data and it is basically free, or it reliably works
            # and deletes data, or it doesn't work. In that latter case we turn
            # it off for the rest of this loop through the passes, but will
            # try again once all of the passes have been run.
            can_discard = self.remove_discarded()

            passes_with_steps = [(sp, None) for sp in passes]

            while passes_with_steps:
                to_run_next = []

                for sp, steps in passes_with_steps:
                    if steps is None:
                        steps = sp.generate_steps()

                    failures = 0
                    max_failures = 3

                    while steps and failures < max_failures:
                        prev_calls = self.calls
                        prev = self.shrink_target
                        sp.run_step(pop_random(self.random, steps))
                        if prev_calls != self.calls:
                            if can_discard:
                                can_discard = self.remove_discarded()
                            if prev is self.shrink_target:
                                failures += 1
                    if steps:
                        to_run_next.append((sp, steps))
                passes_with_steps = to_run_next

        for sp in passes:
            sp.fixed_point_at = self.shrink_target

    @property
    def buffer(self):
        return self.shrink_target.buffer

    @property
    def blocks(self):
        return self.shrink_target.blocks

    @property
    def examples(self):
        return self.shrink_target.examples

    def all_block_bounds(self):
        return self.shrink_target.blocks.all_bounds()

    @derived_value
    def examples_by_label(self):
        """An index of all examples grouped by their label, with
        the examples stored in their normal index order."""

        examples_by_label = defaultdict(list)
        for ex in self.examples:
            examples_by_label[ex.label].append(ex)
        return dict(examples_by_label)

    def calculate_descents(self):
        """Returns a list of all pairs (i, j) such that
        self.examples[i] is an ancestor of self.examples[j] and
        they have the same label.
        """
        result = []

        for ls in self.examples_by_label.values():
            if len(ls) <= 1:
                continue

            for i, ex in enumerate(ls[:-1]):
                hi = len(ls)
                lo = i + 1
                if ls[lo].start >= ex.end:
                    continue
                while lo + 1 < hi:
                    mid = (lo + hi) // 2
                    if ls[mid].start >= ex.end:
                        hi = mid
                    else:
                        lo = mid
                id1 = self.stable_identifier_for_example(ex)
                result.extend(
                    [
                        (id1, self.stable_identifier_for_example(ls[j]))
                        for j in hrange(i + 1, hi)
                    ]
                )
        return result

    @defines_shrink_pass(calculate_descents)
    def pass_to_descendant(self, ancestor_id, descendant_id):
        """Attempt to replace each example with a descendant example.

        This is designed to deal with strategies that call themselves
        recursively. For example, suppose we had:

        binary_tree = st.deferred(
            lambda: st.one_of(
                st.integers(), st.tuples(binary_tree, binary_tree)))

        This pass guarantees that we can replace any binary tree with one of
        its subtrees - each of those will create an interval that the parent
        could validly be replaced with, and this pass will try doing that.

        This is pretty expensive - it takes O(len(intervals)^2) - so we run it
        late in the process when we've got the number of intervals as far down
        as possible.
        """

        ancestor = self.example_for_stable_identifier(ancestor_id)
        descendant = self.example_for_stable_identifier(descendant_id)
        if descendant is None:
            return
        assert ancestor is not None

        self.incorporate_new_buffer(
            self.buffer[: ancestor.start]
            + self.buffer[descendant.start : descendant.end]
            + self.buffer[ancestor.end :]
        )

    def is_shrinking_block(self, i):
        """Checks whether block i has been previously marked as a shrinking
        block.

        If the shrink target has changed since i was last checked, will
        attempt to calculate if an equivalent block in a previous shrink
        target was marked as shrinking.
        """
        if not self.__shrinking_prefixes:
            return False
        try:
            return self.__shrinking_block_cache[i]
        except KeyError:
            pass
        t = self.shrink_target
        return self.__shrinking_block_cache.setdefault(
            i, t.buffer[: t.blocks[i].start] in self.__shrinking_prefixes
        )

    def lower_common_block_offset(self):
        """Sometimes we find ourselves in a situation where changes to one part
        of the byte stream unlock changes to other parts. Sometimes this is
        good, but sometimes this can cause us to exhibit exponential slow
        downs!

        e.g. suppose we had the following:

        m = draw(integers(min_value=0))
        n = draw(integers(min_value=0))
        assert abs(m - n) > 1

        If this fails then we'll end up with a loop where on each iteration we
        reduce each of m and n by 2 - m can't go lower because of n, then n
        can't go lower because of m.

        This will take us O(m) iterations to complete, which is exponential in
        the data size, as we gradually zig zag our way towards zero.

        This can only happen if we're failing to reduce the size of the byte
        stream: The number of iterations that reduce the length of the byte
        stream is bounded by that length.

        So what we do is this: We keep track of which blocks are changing, and
        then if there's some non-zero common offset to them we try and minimize
        them all at once by lowering that offset.

        This may not work, and it definitely won't get us out of all possible
        exponential slow downs (an example of where it doesn't is where the
        shape of the blocks changes as a result of this bouncing behaviour),
        but it fails fast when it doesn't work and gets us out of a really
        nastily slow case when it does.
        """
        if len(self.__changed_blocks) <= 1:
            return

        current = self.shrink_target

        blocked = [current.buffer[u:v] for u, v in self.all_block_bounds()]

        changed = [
            i
            for i in sorted(self.__changed_blocks)
            if not self.shrink_target.blocks[i].trivial
        ]

        if not changed:
            return

        ints = [int_from_bytes(blocked[i]) for i in changed]
        offset = min(ints)
        assert offset > 0

        for i in hrange(len(ints)):
            ints[i] -= offset

        def reoffset(o):
            new_blocks = list(blocked)
            for i, v in zip(changed, ints):
                new_blocks[i] = int_to_bytes(v + o, len(blocked[i]))
            return self.incorporate_new_buffer(hbytes().join(new_blocks))

        Integer.shrink(offset, reoffset, random=self.random)
        self.clear_change_tracking()

    def mark_shrinking(self, blocks):
        """Mark each of these blocks as a shrinking block: That is, lowering
        its value lexicographically may cause less data to be drawn after."""
        t = self.shrink_target
        for i in blocks:
            if self.__shrinking_block_cache.get(i) is True:
                continue
            self.__shrinking_block_cache[i] = True
            prefix = t.buffer[: t.blocks[i].start]
            self.__shrinking_prefixes.add(prefix)

    def clear_change_tracking(self):
        self.__last_checked_changed_at = self.shrink_target
        self.__all_changed_blocks = set()

    def mark_changed(self, i):
        self.__changed_blocks.add(i)

    @property
    def __changed_blocks(self):
        if self.__last_checked_changed_at is not self.shrink_target:
            prev_target = self.__last_checked_changed_at
            new_target = self.shrink_target
            assert prev_target is not new_target
            prev = prev_target.buffer
            new = new_target.buffer
            assert sort_key(new) < sort_key(prev)

            if (
                len(new_target.blocks) != len(prev_target.blocks)
                or new_target.blocks.endpoints != prev_target.blocks.endpoints
            ):
                self.__all_changed_blocks = set()
            else:
                blocks = new_target.blocks

                # Index of last block whose contents have been modified, found
                # by checking if the tail past this point has been modified.
                last_changed = binary_search(
                    0,
                    len(blocks),
                    lambda i: prev[blocks.start(i) :] != new[blocks.start(i) :],
                )

                # Index of the first block whose contents have been changed,
                # because we know that this predicate is true for zero (because
                # the prefix from the start is empty), so the result must be True
                # for the bytes from the start of this block and False for the
                # bytes from the end, hence the change is in this block.
                first_changed = binary_search(
                    0,
                    len(blocks),
                    lambda i: prev[: blocks.start(i)] == new[: blocks.start(i)],
                )

                # Between these two changed regions we now do a linear scan to
                # check if any specific block values have changed.
                for i in hrange(first_changed, last_changed + 1):
                    u, v = blocks.bounds(i)
                    if i not in self.__all_changed_blocks and prev[u:v] != new[u:v]:
                        self.__all_changed_blocks.add(i)
            self.__last_checked_changed_at = new_target
        assert self.__last_checked_changed_at is self.shrink_target
        return self.__all_changed_blocks

    def update_shrink_target(self, new_target):
        assert isinstance(new_target, ConjectureResult)
        if self.shrink_target is not None:
            self.shrinks += 1
        else:
            self.__all_changed_blocks = set()
            self.__last_checked_changed_at = new_target

        self.shrink_target = new_target
        self.__shrinking_block_cache = {}
        self.__derived_values = {}

    def try_shrinking_blocks(self, blocks, b):
        """Attempts to replace each block in the blocks list with b. Returns
        True if it succeeded (which may include some additional modifications
        to shrink_target).

        May call mark_shrinking with b if this causes a reduction in size.

        In current usage it is expected that each of the blocks currently have
        the same value, although this is not essential. Note that b must be
        < the block at min(blocks) or this is not a valid shrink.

        This method will attempt to do some small amount of work to delete data
        that occurs after the end of the blocks. This is useful for cases where
        there is some size dependency on the value of a block.
        """
        initial_attempt = bytearray(self.shrink_target.buffer)
        for i, block in enumerate(blocks):
            if block >= len(self.blocks):
                blocks = blocks[:i]
                break
            u, v = self.blocks[block].bounds
            n = min(self.blocks[block].length, len(b))
            initial_attempt[v - n : v] = b[-n:]

        if not blocks:
            return False

        start = self.shrink_target.blocks[blocks[0]].start
        end = self.shrink_target.blocks[blocks[-1]].end

        initial_data = self.cached_test_function(initial_attempt)

        if initial_data.status == Status.INTERESTING:
            self.lower_common_block_offset()
            return initial_data is self.shrink_target

        # If this produced something completely invalid we ditch it
        # here rather than trying to persevere.
        if initial_data.status < Status.VALID:
            return False

        # We've shrunk inside our group of blocks, so we have no way to
        # continue. (This only happens when shrinking more than one block at
        # a time).
        if len(initial_data.buffer) < v:
            return False

        lost_data = len(self.shrink_target.buffer) - len(initial_data.buffer)

        # If this did not in fact cause the data size to shrink we
        # bail here because it's not worth trying to delete stuff from
        # the remainder.
        if lost_data <= 0:
            return False

        self.mark_shrinking(blocks)

        # We now look for contiguous regions to delete that might help fix up
        # this failed shrink. We only look for contiguous regions of the right
        # lengths because doing anything more than that starts to get very
        # expensive. See example_deletion_with_block_lowering for where we
        # try to be more aggressive.
        regions_to_delete = {(end, end + lost_data)}

        for j in (blocks[-1] + 1, blocks[-1] + 2):
            if j >= min(len(initial_data.blocks), len(self.blocks)):
                continue
            # We look for a block very shortly after the last one that has
            # lost some of its size, and try to delete from the beginning so
            # that it retains the same integer value. This is a bit of a hyper
            # specific trick designed to make our integers() strategy shrink
            # well.
            r1, s1 = self.shrink_target.blocks[j].bounds
            r2, s2 = initial_data.blocks[j].bounds
            lost = (s1 - r1) - (s2 - r2)
            # Apparently a coverage bug? An assert False in the body of this
            # will reliably fail, but it shows up as uncovered.
            if lost <= 0 or r1 != r2:  # pragma: no cover
                continue
            regions_to_delete.add((r1, r1 + lost))

        for ex in self.shrink_target.examples:
            if ex.start > start:
                continue
            if ex.end <= end:
                continue

            replacement = initial_data.examples[ex.index]

            in_original = [c for c in ex.children if c.start >= end]

            in_replaced = [c for c in replacement.children if c.start >= end]

            if len(in_replaced) >= len(in_original) or not in_replaced:
                continue

            # We've found an example where some of the children went missing
            # as a result of this change, and just replacing it with the data
            # it would have had and removing the spillover didn't work. This
            # means that some of its children towards the right must be
            # important, so we try to arrange it so that it retains its
            # rightmost children instead of its leftmost.
            regions_to_delete.add(
                (in_original[0].start, in_original[-len(in_replaced)].start)
            )

        for u, v in sorted(regions_to_delete, key=lambda x: x[1] - x[0], reverse=True):
            try_with_deleted = bytearray(initial_attempt)
            del try_with_deleted[u:v]
            if self.incorporate_new_buffer(try_with_deleted):
                return True
        return False

    def remove_discarded(self):
        """Try removing all bytes marked as discarded.

        This is primarily to deal with data that has been ignored while
        doing rejection sampling - e.g. as a result of an integer range, or a
        filtered strategy.

        Such data will also be handled by the adaptive_example_deletion pass,
        but that pass is necessarily more conservative and will try deleting
        each interval individually. The common case is that all data drawn and
        rejected can just be thrown away immediately in one block, so this pass
        will be much faster than trying each one individually when it works.

        returns False if there is discarded data and removing it does not work,
        otherwise returns True.
        """
        while self.shrink_target.has_discards:
            discarded = []

            for ex in self.shrink_target.examples:
                if (
                    ex.length > 0
                    and ex.discarded
                    and (not discarded or ex.start >= discarded[-1][-1])
                ):
                    discarded.append((ex.start, ex.end))

            # This can happen if we have discards but they are all of
            # zero length. This shouldn't happen very often so it's
            # faster to check for it here than at the point of example
            # generation.
            if not discarded:
                break

            attempt = bytearray(self.shrink_target.buffer)
            for u, v in reversed(discarded):
                del attempt[u:v]

            if not self.incorporate_new_buffer(attempt):
                return False
        return True

    @derived_value
    def stable_identifier_arguments(self):
        return [(self.stable_identifier_for_example(ex),) for ex in self.examples]

    @defines_shrink_pass(lambda self: self.stable_identifier_arguments)
    def adaptive_example_deletion(self, example_id):
        """Attempts to delete every example from the test case.

        That is, it is logically equivalent to trying ``self.buffer[:ex.start] +
        self.buffer[ex.end:]`` for every example ``ex``. The order in which
        examples are tried is randomized, and when deletion is successful it
        will attempt to adapt to delete more than one example at a time.
        """
        example = self.example_for_stable_identifier(example_id)

        if example is None or not self.incorporate_new_buffer(
            self.buffer[: example.start] + self.buffer[example.end :]
        ):
            return

        # If we successfully deleted one example there may be a useful
        # deletable region around here.

        original = self.shrink_target
        endpoints = set()
        for ex in original.examples:
            if ex.depth <= example.depth:
                endpoints.add(ex.start)
                endpoints.add(ex.end)

        partition = sorted(endpoints)
        j = partition.index(example.start)

        def delete_region(a, b):
            assert a <= j <= b
            if a < 0 or b >= len(partition) - 1:
                return False
            return self.consider_new_buffer(
                original.buffer[: partition[a]] + original.buffer[partition[b] :]
            )

        to_right = find_integer(lambda n: delete_region(j, j + n))

        if to_right > 0:
            find_integer(lambda n: delete_region(j - n, j + to_right))

    def try_zero_example(self, ex):
        u = ex.start
        v = ex.end
        attempt = self.cached_test_function(
            self.buffer[:u] + hbytes(v - u) + self.buffer[v:]
        )

        if attempt is Overrun:
            return False

        in_replacement = attempt.examples[ex.index]
        used = in_replacement.length

        if attempt is not self.shrink_target:
            if in_replacement.end < len(attempt.buffer) and used < ex.length:
                self.incorporate_new_buffer(
                    self.buffer[:u] + hbytes(used) + self.buffer[v:]
                )
        return self.examples[ex.index].trivial

    @defines_shrink_pass(lambda self: self.stable_identifier_arguments)
    def zero_examples(self, ex_id):
        """Attempt to replace each example with a minimal version of itself."""
        ex = self.example_for_stable_identifier(ex_id)
        """Attempt to replace each example with a minimal version of itself."""
        # If the example is already trivial, assume there's nothing to do here.
        # We could attempt to use it as an adaptive replacement for other
        # similar examples, but that seems to be ineffective, resulting mostly
        # in redundant work rather than helping.
        if ex is None or ex.trivial:
            return

        if not self.try_zero_example(ex):
            return

        # If we zeroed the example we need to get the new one that replaced it.
        ex = self.examples[ex.index]

        original = self.shrink_target
        group = self.examples_by_label[ex.label]
        i = group.index(ex)
        replacement = self.buffer[ex.start : ex.end]

        # We first expand to cover the trivial region surrounding this group.
        # This avoids a situation where the adaptive phase "succeeds" a lot by
        # virtue of not doing anything and then goes into a galloping phase
        # where it does a bunch of useless work.
        def all_trivial(a, b):
            if a < 0 or b > len(group):
                return False
            return all(e.trivial for e in group[a:b])

        start, end = expand_region(all_trivial, i, i + 1)

        # If we've got multiple trivial examples of different lengths then
        # this isn't going to work as a replacement for all of them and so we
        # skip out early.
        if any(e.length != len(replacement) for e in group[start:end]):
            return

        def can_zero(a, b):
            if a < 0 or b > len(group):
                return False
            regions = []
            for e in group[a:b]:
                t = (e.start, e.end, replacement)
                if not regions or t[0] >= regions[-1][1]:
                    regions.append(t)
            return self.consider_new_buffer(replace_all(original.buffer, regions))

        expand_region(can_zero, start, end)

    @derived_value
    def blocks_by_non_zero_suffix(self):
        """Returns a list of blocks grouped by their non-zero suffix,
        as a list of (suffix, indices) pairs, skipping all groupings
        where there is only one index.

        This is only used for the arguments of minimize_duplicated_blocks.
        """
        duplicates = defaultdict(list)
        for block in self.blocks:
            duplicates[non_zero_suffix(self.buffer[block.start : block.end])].append(
                block.index
            )
        return duplicates

    @defines_shrink_pass(
        lambda self: [(b,) for b in sorted(self.blocks_by_non_zero_suffix)]
    )
    def minimize_duplicated_blocks(self, block):
        """Find blocks that have been duplicated in multiple places and attempt
        to minimize all of the duplicates simultaneously.

        This lets us handle cases where two values can't be shrunk
        independently of each other but can easily be shrunk together.
        For example if we had something like:

        ls = data.draw(lists(integers()))
        y = data.draw(integers())
        assert y not in ls

        Suppose we drew y = 3 and after shrinking we have ls = [3]. If we were
        to replace both 3s with 0, this would be a valid shrink, but if we were
        to replace either 3 with 0 on its own the test would start passing.

        It is also useful for when that duplication is accidental and the value
        of the blocks doesn't matter very much because it allows us to replace
        more values at once.
        """
        targets = self.blocks_by_non_zero_suffix[block]
        if len(targets) <= 1:
            return
        Lexical.shrink(
            block,
            lambda b: self.try_shrinking_blocks(targets, b),
            random=self.random,
            full=False,
        )

    @defines_shrink_pass(lambda self: self.stable_identifier_arguments)
    def minimize_floats(self, ex_id):
        """Some shrinks that we employ that only really make sense for our
        specific floating point encoding that are hard to discover from any
        sort of reasonable general principle. This allows us to make
        transformations like replacing a NaN with an Infinity or replacing
        a float with its nearest integers that we would otherwise not be
        able to due to them requiring very specific transformations of
        the bit sequence.

        We only apply these transformations to blocks that "look like" our
        standard float encodings because they are only really meaningful
        there. The logic for detecting this is reasonably precise, but
        it doesn't matter if it's wrong. These are always valid
        transformations to make, they just don't necessarily correspond to
        anything particularly meaningful for non-float values.
        """
        ex = self.example_for_stable_identifier(ex_id)
        if ex is None or not (
            ex.label == DRAW_FLOAT_LABEL
            and len(ex.children) == 2
            and ex.children[0].length == 8
        ):
            return
        u = ex.children[0].start
        v = ex.children[0].end
        buf = self.shrink_target.buffer
        b = buf[u:v]
        f = lex_to_float(int_from_bytes(b))
        b2 = int_to_bytes(float_to_lex(f), 8)
        if b == b2 or self.consider_new_buffer(buf[:u] + b2 + buf[v:]):
            Float.shrink(
                f,
                lambda x: self.consider_new_buffer(
                    self.shrink_target.buffer[:u]
                    + int_to_bytes(float_to_lex(x), 8)
                    + self.shrink_target.buffer[v:]
                ),
                random=self.random,
            )

    @defines_shrink_pass(lambda self: [(i,) for i in hrange(len(self.blocks))])
    def minimize_individual_blocks(self, i):
        """Attempt to minimize each block in sequence.

        This is the pass that ensures that e.g. each integer we draw is a
        minimum value. So it's the part that guarantees that if we e.g. do

        x = data.draw(integers())
        assert x < 10

        then in our shrunk example, x = 10 rather than say 97.
        """
        if i >= len(self.blocks):
            return
        block = self.blocks[i]
        u, v = block.bounds
        i = block.index
        Lexical.shrink(
            self.shrink_target.buffer[u:v],
            lambda b: self.try_shrinking_blocks((i,), b),
            random=self.random,
            full=False,
        )

    @defines_shrink_pass(
        lambda self: [
            (i, self.stable_identifier_for_example(ex))
            for i in hrange(len(self.blocks))
            if self.is_shrinking_block(i)
            for ex in self.examples
            if ex.length > 0 and ex.start >= self.blocks[i].end
        ]
    )
    def example_deletion_with_block_lowering(self, block_i, ex_id):
        """Sometimes we get stuck where there is data that we could easily
        delete, but it changes the number of examples generated, so we have to
        change that at the same time.

        We handle most of the common cases in try_shrinking_blocks which is
        pretty good at clearing out large contiguous blocks of dead space,
        but it fails when there is data that has to stay in particular places
        in the list.

        This pass exists as an emergency procedure to get us unstuck. For every
        example and every block not inside that example it tries deleting the
        example and modifying the block's value by one in either direction.
        """
        if block_i >= len(self.blocks):
            return
        block = self.blocks[block_i]
        ex = self.example_for_stable_identifier(ex_id)
        if ex is None:
            return
        u, v = block.bounds

        n = int_from_bytes(self.shrink_target.buffer[u:v])
        if n == 0:
            return

        buf = bytearray(self.shrink_target.buffer)
        buf[u:v] = int_to_bytes(n - 1, v - u)
        del buf[ex.start : ex.end]
        self.incorporate_new_buffer(buf)

    @defines_shrink_pass(
        lambda self: [
            (self.stable_identifier_for_example(e), l)
            for e in self.examples
            for l in sorted({c.label for c in e.children}, key=str)
        ]
    )
    def reorder_examples(self, ex_id, label):
        """This pass allows us to reorder the children of each example.

        For example, consider the following:

        .. code-block:: python

            import hypothesis.strategies as st
            from hypothesis import given

            @given(st.text(), st.text())
            def test_not_equal(x, y):
                assert x != y

        Without the ability to reorder x and y this could fail either with
        ``x=""``, ``y="0"``, or the other way around. With reordering it will
        reliably fail with ``x=""``, ``y="0"``.
        """
        ex = self.example_for_stable_identifier(ex_id)
        if ex is None:
            return
        group = [c for c in ex.children if c.label == label]
        if len(group) <= 1:
            return

        st = self.shrink_target
        pieces = [st.buffer[ex.start : ex.end] for ex in group]
        endpoints = [(ex.start, ex.end) for ex in group]

        Ordering.shrink(
            pieces,
            lambda ls: self.consider_new_buffer(
                replace_all(st.buffer, [(u, v, r) for (u, v), r in zip(endpoints, ls)])
            ),
            random=self.random,
        )

    @defines_shrink_pass(lambda self: [(c,) for c in hrange(256)])
    def alphabet_minimize(self, c):
        """Attempts to minimize the "alphabet" - the set of bytes that
        are used in the representation of the current buffer. The main
        benefit of this is that it significantly increases our cache hit rate
        by making things that are equivalent more likely to have the same
        representation, but it's also generally a rather effective "fuzzing"
        step that gives us a lot of good opportunities to slip to a smaller
        representation of the same bug.
        """

        buf = self.buffer

        if c not in buf:
            return

        def can_replace_with(d):
            if d < 0:
                return False

            if self.consider_new_buffer(hbytes([d if b == c else b for b in buf])):
                if d <= 1:
                    # For small values of d if this succeeds we take this
                    # as evidence that it is worth doing a a bulk replacement
                    # where we replace all values which are close
                    # to c but smaller with d as well. This helps us substantially
                    # in cases where we have a lot of "dead" bytes that don't really do
                    # much, as it allows us to replace many of them in one go rather
                    # than one at a time. An example of where this matters is
                    # test_minimize_multiple_elements_in_silly_large_int_range_min_is_not_dupe
                    # in test_shrink_quality.py
                    def replace_range(k):
                        if k > c:
                            return False

                        def should_replace_byte(b):
                            return c - k <= b <= c and d < b

                        return self.consider_new_buffer(
                            hbytes([d if should_replace_byte(b) else b for b in buf])
                        )

                    find_integer(replace_range)
                return True

        if (
            # If we cannot replace the current byte with its predecessor,
            # assume it is already minimal and continue on. This ensures
            # we make no more than one call per distinct byte value in the
            # event that no shrinks are possible here.
            not can_replace_with(c - 1)
            # We next try replacing with 0 or 1. If this works then
            # there is nothing else to do here.
            or can_replace_with(0)
            or can_replace_with(1)
            # Finally we try to replace with c - 2 before going on to the
            # binary search so that in cases which were already nearly
            # minimal we don't do log(n) extra work.
            or not can_replace_with(c - 2)
        ):
            return

        # Now binary search to find a small replacement.

        # Invariant: We cannot replace with lo, we can replace with hi.
        lo = 1
        hi = c - 2
        while lo + 1 < hi:
            mid = (lo + hi) // 2
            if can_replace_with(mid):
                hi = mid
            else:
                lo = mid

    def stable_identifier_for_example(self, example):
        """A stable identifier is one that we can reasonably reliably
        count on referring to "logically the same" example between two
        different test runs. It is currently represented as a path from
        the root."""
        return example.index

    def example_for_stable_identifier(self, identifier):
        """Returns the example in the current shrink target corresponding
        to this stable identifier, or None if no such example exists."""
        if identifier >= len(self.examples):
            return None
        return self.shrink_target.examples[identifier]

    def run_block_program(self, i, description, original, repeats=1):
        """Block programs are a mini-DSL for block rewriting, defined as a sequence
        of commands that can be run at some index into the blocks

        Commands are:

            * "-", subtract one from this block.
            * "X", delete this block

        If a command does not apply (currently only because it's - on a zero
        block) the block will be silently skipped over.

        This method runs the block program in ``description`` at block index
        ``i`` on the ConjectureData ``original``. If ``repeats > 1`` then it
        will attempt to approximate the results of running it that many times.

        Returns True if this successfully changes the underlying shrink target,
        else False.
        """
        if i + len(description) > len(original.blocks) or i < 0:
            return False
        attempt = bytearray(original.buffer)
        for _ in hrange(repeats):
            for k, d in reversed(list(enumerate(description))):
                j = i + k
                u, v = original.blocks[j].bounds
                if v > len(attempt):
                    return False
                if d == "-":
                    value = int_from_bytes(attempt[u:v])
                    if value == 0:
                        return False
                    else:
                        attempt[u:v] = int_to_bytes(value - 1, v - u)
                elif d == "X":
                    del attempt[u:v]
                else:  # pragma: no cover
                    assert False, "Unrecognised command %r" % (d,)
        return self.incorporate_new_buffer(attempt)


def block_program(description):
    """Mini-DSL for block rewriting. A sequence of commands that will be run
    over all contiguous sequences of blocks of the description length in order.
    Commands are:

        * ".", keep this block unchanged
        * "-", subtract one from this block.
        * "0", replace this block with zero
        * "X", delete this block

    If a command does not apply (currently only because it's - on a zero
    block) the block will be silently skipped over. As a side effect of
    running a block program its score will be updated.
    """
    name = "block_program(%r)" % (description,)

    if name not in SHRINK_PASS_DEFINITIONS:
        """Defines a shrink pass that runs the block program ``description``
        at every block index."""
        n = len(description)

        def generate_arguments(self):
            return [(i,) for i in hrange(len(self.blocks))]

        def run(self, i):
            """Adaptively attempt to run the block program at the current
            index. If this successfully applies the block program ``k`` times
            then this runs in ``O(log(k))`` test function calls."""
            if i + n >= len(self.shrink_target.blocks):
                return

            # First, run the block program at the chosen index. If this fails,
            # don't do any extra work, so that failure is as cheap as possible.
            if not self.run_block_program(i, description, original=self.shrink_target):
                return

            # Because we run in a random order we will often find ourselves in the middle
            # of a region where we could run the block program. We thus start by moving
            # left to the beginning of that region if possible in order to to start from
            # the beginning of that region.
            def offset_left(k):
                return i - k * n

            i = offset_left(
                find_integer(
                    lambda k: self.run_block_program(
                        offset_left(k), description, original=self.shrink_target
                    )
                )
            )

            original = self.shrink_target

            # Now try to run the block program multiple times here.
            find_integer(
                lambda k: self.run_block_program(
                    i, description, original=original, repeats=k
                )
            )

        run.__name__ = name

        defines_shrink_pass(generate_arguments)(run)
        assert name in SHRINK_PASS_DEFINITIONS
    return name


@attr.s(slots=True, cmp=False)
class ShrinkPass(object):
    run_with_arguments = attr.ib()
    generate_arguments = attr.ib()
    index = attr.ib()
    shrinker = attr.ib()

    fixed_point_at = attr.ib(default=None)
    successes = attr.ib(default=0)
    runs = attr.ib(default=0)
    calls = attr.ib(default=0)
    shrinks = attr.ib(default=0)
    deletions = attr.ib(default=0)

    def generate_steps(self):
        if self.fixed_point_at is self.shrinker.shrink_target:
            return []
        return list(self.generate_arguments(self.shrinker))

    def run_step(self, args):
        initial_shrinks = self.shrinker.shrinks
        initial_calls = self.shrinker.calls
        size = len(self.shrinker.shrink_target.buffer)
        self.shrinker.explain_next_call_as(
            "%s(%s)" % (self.name, ", ".join(map(repr, args)))
        )
        try:
            self.run_with_arguments(self.shrinker, *args)
        finally:
            self.calls += self.shrinker.calls - initial_calls
            self.shrinks += self.shrinker.shrinks - initial_shrinks
            self.deletions += size - len(self.shrinker.shrink_target.buffer)
            self.shrinker.clear_call_explanation()

    @property
    def name(self):
        return self.run_with_arguments.__name__


def non_zero_suffix(b):
    """Returns the longest suffix of b that starts with a non-zero
    byte."""
    i = 0
    while i < len(b) and b[i] == 0:
        i += 1
    return b[i:]


def expand_region(f, a, b):
    """Attempts to find u, v with u <= a, v >= b such that f(u, v) is true.
    Assumes that f(a, b) is already true.
    """
    b += find_integer(lambda k: f(a, b + k))
    a -= find_integer(lambda k: f(a - k, b))
    return (a, b)
