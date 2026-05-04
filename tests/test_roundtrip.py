"""End-to-end encode/decode round trips."""

from __future__ import annotations

import pytest

from morse import decode, encode


@pytest.mark.parametrize(
    "text",
    [
        "HELLO",
        "HELLO WORLD",
        "SOS",
        "ATTACK AT DAWN",
        "MEET ME AT 5 PM",
        "PRICE 1234.56",
        "WHO ARE YOU?",
        "FAST FOX, LAZY DOG.",
        "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG",
    ],
)
def test_text_roundtrip(text: str) -> None:
    assert decode(encode(text)) == text


@pytest.mark.parametrize(
    "text",
    [
        "<SOS> HELP",
        "MESSAGE 1 <BT> MESSAGE 2",
        "OVER <KN>",
        "<AR>",
        "<AS> WAIT",
    ],
)
def test_prosign_roundtrip(text: str) -> None:
    assert decode(encode(text)) == text


def test_lowercase_input_roundtrips_to_upper() -> None:
    assert decode(encode("hello world")) == "HELLO WORLD"


def test_extra_spaces_collapse_on_roundtrip() -> None:
    assert decode(encode("HI    THERE")) == "HI THERE"
