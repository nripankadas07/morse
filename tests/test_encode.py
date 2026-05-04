"""Tests for :func:`morse.encode`."""

from __future__ import annotations

import pytest

from morse import EncodeError, encode


class TestEncodeBasic:
    def test_encode_empty_returns_empty(self) -> None:
        assert encode("") == ""

    def test_encode_single_letter(self) -> None:
        assert encode("E") == "."

    def test_encode_lowercase_is_uppercased(self) -> None:
        assert encode("e") == "."

    def test_encode_word_uses_single_space(self) -> None:
        assert encode("ABC") == ".- -... -.-."

    def test_encode_two_words_uses_slash(self) -> None:
        assert encode("HI MOM") == ".... .. / -- --- --"

    def test_encode_collapses_multiple_spaces(self) -> None:
        assert encode("HI    MOM") == ".... .. / -- --- --"

    def test_encode_strips_leading_trailing_whitespace(self) -> None:
        assert encode("  HI  ").strip().count("/") == 0

    def test_encode_handles_tabs_and_newlines(self) -> None:
        assert encode("HI\tMOM") == encode("HI MOM")
        assert encode("HI\nMOM") == encode("HI MOM")


class TestEncodeDigitsAndPunct:
    def test_encode_digits(self) -> None:
        assert encode("123") == ".---- ..--- ...--"

    def test_encode_period_and_comma(self) -> None:
        assert encode(",.") == "--..-- .-.-.-"

    def test_encode_question_mark(self) -> None:
        assert encode("?") == "..--.."

    def test_encode_at_sign(self) -> None:
        assert encode("@") == ".--.-."


class TestEncodeUnknownChars:
    def test_strict_raises_on_unknown(self) -> None:
        with pytest.raises(EncodeError, match="no Morse code"):
            encode("HI~")

    def test_strict_error_carries_index(self) -> None:
        with pytest.raises(EncodeError) as exc:
            encode("HI~")
        assert exc.value.character == "~"
        assert exc.value.index == 2

    def test_ignore_drops_unknown_silently(self) -> None:
        assert encode("HI~", errors="ignore") == ".... .."

    def test_replace_substitutes_question(self) -> None:
        assert encode("HI~", errors="replace") == ".... .. ..--.."

    def test_invalid_errors_value_raises(self) -> None:
        with pytest.raises(ValueError, match="errors must be"):
            encode("HI", errors="bogus")


class TestEncodeProsigns:
    def test_prosign_emits_single_token(self) -> None:
        assert encode("HI <AR>") == ".... .. / .-.-."

    def test_prosign_disabled_treats_as_unknown(self) -> None:
        with pytest.raises(EncodeError):
            encode("<AR>", prosigns=False)

    def test_prosign_unknown_tag_treated_as_chars(self) -> None:
        # ``<ZZ>`` is not a known prosign; brackets are unknown chars,
        # so strict mode raises on the first ``<``.
        with pytest.raises(EncodeError):
            encode("<ZZ>")

    def test_prosign_sos(self) -> None:
        assert encode("<SOS>") == "...---..."

    def test_prosign_at_start_no_leading_word_sep(self) -> None:
        assert encode("<AR>HI") == ".-.-. .... .."

    def test_prosign_lowercased_input_works(self) -> None:
        assert encode("<ar>") == ".-.-."


class TestEncodeWordSeparators:
    def test_no_letters_means_no_separators(self) -> None:
        assert encode("   ") == ""

    def test_trailing_word_sep_has_no_effect(self) -> None:
        assert encode("HI   ") == ".... .."

    def test_leading_word_sep_has_no_effect(self) -> None:
        assert encode("   HI") == ".... .."
