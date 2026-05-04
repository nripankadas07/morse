"""Sanity checks on the Morse code tables themselves."""

from __future__ import annotations

from morse import (
    MORSE_CODE,
    MORSE_TO_PROSIGN,
    PROSIGN_TO_MORSE,
    PROSIGNS,
    REVERSE_CODE,
)


def test_letters_present() -> None:
    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        assert letter in MORSE_CODE


def test_digits_present() -> None:
    for digit in "0123456789":
        assert digit in MORSE_CODE


def test_morse_only_contains_dot_dash() -> None:
    for code in MORSE_CODE.values():
        assert set(code) <= set(".-")


def test_codes_are_unique() -> None:
    assert len(set(MORSE_CODE.values())) == len(MORSE_CODE)


def test_reverse_table_matches_forward() -> None:
    for letter, code in MORSE_CODE.items():
        assert REVERSE_CODE[code] == letter


def test_known_letter_codes() -> None:
    assert MORSE_CODE["A"] == ".-"
    assert MORSE_CODE["B"] == "-..."
    assert MORSE_CODE["S"] == "..."
    assert MORSE_CODE["O"] == "---"
    assert MORSE_CODE["E"] == "."


def test_known_digit_codes() -> None:
    assert MORSE_CODE["0"] == "-----"
    assert MORSE_CODE["5"] == "....."
    assert MORSE_CODE["9"] == "----."


def test_prosigns_round_trip_through_tables() -> None:
    for name in PROSIGNS:
        code = PROSIGN_TO_MORSE[name]
        assert MORSE_TO_PROSIGN[code] == name


def test_sos_prosign_is_concatenation_of_s_o_s() -> None:
    assert PROSIGN_TO_MORSE["SOS"] == "...---..."
