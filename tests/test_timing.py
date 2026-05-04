"""Tests for :func:`morse.to_timing`."""

from __future__ import annotations

import math

import pytest

from morse import TimingError, to_timing


def _kinds(elements):
    return [k for k, _ in elements]


def _total_ms(elements):
    return sum(d for _, d in elements)


class TestStandardTiming:
    def test_empty_input_yields_no_elements(self) -> None:
        assert to_timing("", wpm=20) == []

    def test_single_e_is_one_dit(self) -> None:
        elements = to_timing("E", wpm=20)
        assert _kinds(elements) == ["dit"]
        assert math.isclose(elements[0][1], 60.0)  # 1200/20

    def test_single_t_is_one_dah(self) -> None:
        elements = to_timing("T", wpm=20)
        assert _kinds(elements) == ["dah"]
        assert math.isclose(elements[0][1], 180.0)

    def test_letter_a_is_dit_intra_dah(self) -> None:
        # A = .-
        elements = to_timing("A", wpm=20)
        assert _kinds(elements) == ["dit", "intra", "dah"]
        assert math.isclose(elements[0][1], 60.0)
        assert math.isclose(elements[1][1], 60.0)
        assert math.isclose(elements[2][1], 180.0)

    def test_letter_gap_appears_between_letters(self) -> None:
        # AB = .- _LETTER_ -...
        elements = to_timing("AB", wpm=20)
        assert "letter" in _kinds(elements)

    def test_word_gap_appears_between_words(self) -> None:
        elements = to_timing("HI MOM", wpm=20)
        assert "word" in _kinds(elements)

    def test_no_trailing_letter_or_word_gap(self) -> None:
        elements = to_timing("AB", wpm=20)
        last = elements[-1][0]
        assert last not in ("letter", "word")


class TestParisTotal:
    """At standard timing, ``"PARIS "`` should take 60/wpm seconds.

    We approximate by encoding ``"PARIS PARIS"`` and checking the total
    excludes the implicit trailing word gap.  A 12-wpm clock gives
    5000ms per word; two words minus one omitted trailing gap should be
    ~ 2 * 5000 - 7 * 100 = 9300ms (one word = 5000ms inclusive).
    """

    def test_paris_word_total_at_12_wpm(self) -> None:
        # 12 wpm => dit = 100ms; PARIS = 50 dits; word time = 5000ms;
        # without the trailing word gap (7 dits = 700ms), it's 4300ms.
        elements = to_timing("PARIS", wpm=12)
        total = _total_ms(elements)
        assert math.isclose(total, 4300.0, rel_tol=1e-9)


class TestFarnsworth:
    def test_character_speed_speeds_up_dits(self) -> None:
        slow = to_timing("E", wpm=10, character_wpm=20)
        # The dit is taken from character speed, not effective speed.
        assert math.isclose(slow[0][1], 60.0)  # 1200/20

    def test_letter_gap_stretches_under_farnsworth(self) -> None:
        std = to_timing("AB", wpm=18)
        farn = to_timing("AB", wpm=10, character_wpm=18)
        std_letter = next(d for k, d in std if k == "letter")
        farn_letter = next(d for k, d in farn if k == "letter")
        assert farn_letter > std_letter

    def test_word_gap_stretches_under_farnsworth(self) -> None:
        std = to_timing("A B", wpm=18)
        farn = to_timing("A B", wpm=10, character_wpm=18)
        std_word = next(d for k, d in std if k == "word")
        farn_word = next(d for k, d in farn if k == "word")
        assert farn_word > std_word

    def test_character_wpm_equal_to_wpm_matches_standard(self) -> None:
        a = to_timing("AB", wpm=18, character_wpm=18)
        b = to_timing("AB", wpm=18)
        assert a == b

    def test_character_wpm_below_wpm_raises(self) -> None:
        with pytest.raises(TimingError, match="character_wpm must be >= wpm"):
            to_timing("E", wpm=20, character_wpm=10)

    def test_zero_wpm_raises(self) -> None:
        with pytest.raises(TimingError):
            to_timing("E", wpm=0)

    def test_negative_character_wpm_raises(self) -> None:
        with pytest.raises(TimingError, match="character_wpm"):
            to_timing("E", wpm=10, character_wpm=-1)


class TestProsignsInTiming:
    def test_prosign_emits_no_internal_letter_gap(self) -> None:
        # A standalone <AR> is one token of 5 elements with intra gaps,
        # no letter gaps in the middle.
        elements = to_timing("<AR>", wpm=20)
        # .-.-.  -> 5 elements + 4 intra gaps
        assert _kinds(elements) == [
            "dit", "intra", "dah", "intra", "dit", "intra", "dah",
            "intra", "dit",
        ]


class TestKindLabels:
    def test_kinds_are_only_known_labels(self) -> None:
        elements = to_timing("HELLO WORLD", wpm=15)
        assert {k for k, _ in elements} <= {
            "dit", "dah", "intra", "letter", "word",
        }
