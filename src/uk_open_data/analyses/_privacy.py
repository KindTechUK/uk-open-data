"""Hiding small counts so a table of totals cannot point at a person."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from uk_open_data.analyses._model import Figure

DEFAULT_SUPPRESS_BELOW = 5
# Every analysis says this in its privacy notes, so a reader does not take every
# hidden count for a small one.
SECOND_COUNT_NOTE = (
    "A hidden count is not always small. When only one count in a table is "
    "small, a second is hidden with it, so the first cannot be worked out "
    "from the total."
)
# The analyses about people say this in their privacy notes too.
LEFT_OUT_NOTE = (
    "People left out, such as those who live outside the area you serve, are "
    "counted like any group. When they are few, their number is not given, "
    "and a total that would give it away is hidden."
)
HIDDEN_TOTAL = "Hidden so a small number of people left out cannot be worked out."


def is_small(count: int, threshold: int) -> bool:
    """Return True when a count is above zero but below the threshold."""
    return 0 < count < threshold


@dataclass(frozen=True)
class LeftOut:
    """How totals of people, and the people left out of them, may be shown.

    Made by :func:`hide_totals`. A hidden total never has the value of a
    total that is shown, so a total is known by its value.
    """

    threshold: int
    hidden: frozenset[int] = frozenset()

    def total(self, count: int) -> int | None:
        """A total as it may be shown: itself, or None when it is hidden."""
        return None if count in self.hidden else count

    def count(self, count: int) -> str:
        """A count of people left out as it may be said: "12" or "fewer than 5"."""
        return (
            f"fewer than {self.threshold}"
            if is_small(count, self.threshold)
            else str(count)
        )

    def figure(self, figure_id: str, label: str, count: int, note: str = "") -> Figure:
        """A figure for a total of people, hidden like any other when it must be."""
        if self.total(count) is None:
            return Figure(
                figure_id, label, None, "people", note=HIDDEN_TOTAL, suppressed=True
            )
        return Figure(figure_id, label, count, "people", note=note)


def hide_totals(
    base: int, left_out: Sequence[Sequence[int]], threshold: int
) -> LeftOut:
    """Decide which totals of people to hide, so nobody left out can be found.

    The totals are nested. The first is the base, the people the figures are
    about, and it is always shown. Each total after it adds people who are
    left out: those outside the area you serve, say, or those who could not be
    placed. Each group left out is a cell, so a small one is never given as a
    number.

    Going from the base out, a total is shown when its difference from every
    total shown so far is 0 or at least the threshold. It is hidden too when
    the groups it adds since the last total shown hold exactly one small
    count, because the others are given exactly and would give that one away.

    Args:
        base: The people the figures are about.
        left_out: For each total after the base, the counts of the groups of
            people it adds, each given on its own in a warning or the working.
        threshold: Counts above zero and below this are small.
    """
    kept = [base]
    since: list[int] = []
    hidden: set[int] = set()
    total = base
    for groups in left_out:
        total += sum(groups)
        since += groups
        alone = sum(is_small(count, threshold) for count in since) == 1
        if alone or any(is_small(total - shown, threshold) for shown in kept):
            hidden.add(total)
        else:
            kept.append(total)
            since = []
    return LeftOut(threshold, frozenset(hidden))


def cells_to_hide(
    counts: list[int],
    threshold: int,
    groups: tuple[tuple[int, ...], ...] = (),
) -> list[bool]:
    """Decide which cells of a table to hide when its total is published.

    A cell from 1 to ``threshold - 1`` is hidden. If exactly one cell is hidden
    it could be worked out by taking the others from the total, so the smallest
    remaining cell above zero is hidden with it.

    Args:
        counts: The counts in the table, one per cell.
        threshold: Counts below this (and above zero) are hidden.
        groups: Sets of cell positions that are also published as a sum. The
            second cell is taken from the same group as the first when it can
            be, so the group's sum gives neither away and can still be shown.

    Returns:
        One boolean per cell, True where the cell must be hidden.
    """
    hide = [is_small(count, threshold) for count in counts]
    if sum(hide) != 1:
        return hide
    first = hide.index(True)
    candidates = [
        (count, index)
        for index, count in enumerate(counts)
        if count > 0 and not hide[index]
    ]
    same_group = [
        (count, index)
        for count, index in candidates
        if any(first in group and index in group for group in groups)
    ]
    if candidates:
        _, partner = min(same_group or candidates)
        hide[partner] = True
    return hide


def group_hidden(
    counts: list[int], hide: list[bool], positions: tuple[int, ...], threshold: int
) -> bool:
    """Decide whether a figure for a group of cells must be hidden.

    The total is published, so a figure for a group also gives the figure for
    every cell outside it. Each side is checked: a side gives a cell away
    when its own count is small, or when exactly one of its cells is hidden in
    the table.
    """
    outside = tuple(i for i in range(len(counts)) if i not in positions)
    for side in (positions, outside):
        total = sum(counts[position] for position in side)
        hidden_cells = sum(hide[position] for position in side)
        if is_small(total, threshold) or hidden_cells == 1:
            return True
    return False


def count_band(count: int, threshold: int) -> str:
    """Put a count in a band so a map never shows an exact small number.

    The lowest band covers zero up to ``threshold - 1``, so an area with nobody
    in it looks the same as an area with a few people.
    """
    edges = [threshold, threshold * 2, threshold * 4, threshold * 10]
    if count < edges[0]:
        return f"fewer than {edges[0]}"
    for lower, upper in zip(edges, edges[1:], strict=False):
        if count < upper:
            return f"{lower} to {upper - 1}"
    return f"{edges[-1]} or more"


def band_labels(threshold: int) -> list[str]:
    """Return every band label, lowest first, for a map legend."""
    edges = [0, threshold, threshold * 2, threshold * 4, threshold * 10]
    return [count_band(edge, threshold) for edge in edges]
