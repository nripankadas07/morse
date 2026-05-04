"""Exception-hierarchy tests."""

from __future__ import annotations

import pytest

from morse import (
    DecodeError,
    EncodeError,
    MorseError,
    TimingError,
    decode,
    encode,
    to_timing,
)


def test_morse_error_is_value_error() -> None:
    assert issubclass(MorseError, ValueError)


def test_subclasses_chain_through_morse_error() -> None:
    for cls in (EncodeError, DecodeError, TimingError):
        assert issubclass(cls, MorseError)


def test_encode_error_carries_position() -> None:
    with pytest.raises(EncodeError) as exc:
        encode("HI~")
    assert exc.value.character == "~"
    assert exc.value.index == 2


def test_decode_error_carries_token_and_index() -> None:
    with pytest.raises(DecodeError) as exc:
        decode(". .-.-.-.-.")
    assert exc.value.token == ".-.-.-.-."
    assert exc.value.index == 1


def test_timing_error_message() -> None:
    with pytest.raises(TimingError, match=">= wpm"):
        to_timing("E", wpm=20, character_wpm=10)


def test_value_error_alias_catches_everything() -> None:
    with pytest.raises(ValueError):
        encode("HI~")
    with pytest.raises(ValueError):
        decode(".---.--.")
    with pytest.raises(ValueError):
        to_timing("E", wpm=0)
