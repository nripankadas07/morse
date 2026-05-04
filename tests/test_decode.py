"""Tests for :func:`morse.decode` and :func:`morse.is_valid`."""

from __future__ import annotations

import pytest

from morse import DecodeError, decode, is_valid


class TestDecodeBasic:
    def test_decode_empty_returns_empty(self) -> None:
        assert decode("") == ""

    def test_decode_single_letter(self) -> None:
        assert decode(".") == "E"

    def test_decode_word_letter_separated(self) -> None:
        assert decode(".... ..") == "HI"

    def test_decode_two_words(self) -> None:
        assert decode(".... .. / -- --- --") == "HI MOM"

    def test_decode_collapses_extra_spaces(self) -> None:
        # Many spaces between letters are still one separator.
        assert decode("....    ..") == "HI"

    def test_decode_is_case_preserving_ish(self) -> None:
        # Output is uppercase because that's what the table holds.
        assert decode(".") == "E"


class TestDecodeProsigns:
    def test_prosign_round_trip(self) -> None:
        assert decode(".-.-.") == "<AR>"

    def test_prosign_disabled_decodes_as_unknown(self) -> None:
        # ``...---...`` is the SOS prosign and has no single-character
        # mapping, so disabling prosigns turns it into a decode error.
        with pytest.raises(DecodeError):
            decode("...---...", prosigns=False)

    def test_decode_sos(self) -> None:
        assert decode("...---...") == "<SOS>"


class TestDecodeWordSeparators:
    def test_slash_with_or_without_spaces(self) -> None:
        # Slash without surrounding whitespace still acts as a word
        # separator, but the dot/dash runs on either side must be
        # complete letters (here ``....`` = H twice).
        assert decode("..../....") == decode(".... / ....")

    def test_leading_slash_does_not_emit_space(self) -> None:
        assert decode("/ .") == "E"

    def test_trailing_slash_does_not_emit_space(self) -> None:
        assert decode(". /") == "E"


class TestDecodeUnknown:
    def test_strict_raises_on_unknown_token(self) -> None:
        with pytest.raises(DecodeError, match="unknown Morse"):
            decode(". .---.--.")

    def test_strict_carries_token_and_index(self) -> None:
        with pytest.raises(DecodeError) as exc:
            decode(".---.--.")
        assert exc.value.token == ".---.--."
        assert exc.value.index == 0

    def test_ignore_drops_unknown(self) -> None:
        assert decode(". .---.--. .", errors="ignore") == "EE"

    def test_replace_substitutes_question(self) -> None:
        assert decode(". .---.--. .", errors="replace") == "E?E"

    def test_invalid_errors_value_raises(self) -> None:
        with pytest.raises(ValueError, match="errors must be"):
            decode(".", errors="bogus")

    def test_unknown_byte_in_input_raises(self) -> None:
        with pytest.raises(DecodeError):
            decode(". X .")


class TestIsValid:
    def test_is_valid_true_on_clean_input(self) -> None:
        assert is_valid(".... .. / -- --- --")

    def test_is_valid_false_on_unknown_token(self) -> None:
        assert not is_valid(".---.--.")

    def test_is_valid_true_on_empty(self) -> None:
        assert is_valid("")
