"""Lock down the public surface of the :mod:`morse` package."""

from __future__ import annotations

import morse


_EXPECTED = {
    "encode",
    "decode",
    "is_valid",
    "to_timing",
    "TimingElement",
    "MORSE_CODE",
    "REVERSE_CODE",
    "PROSIGNS",
    "PROSIGN_TO_MORSE",
    "MORSE_TO_PROSIGN",
    "MorseError",
    "EncodeError",
    "DecodeError",
    "TimingError",
}


def test_dunder_all_matches_expected() -> None:
    assert set(morse.__all__) == _EXPECTED


def test_every_name_in_all_is_exported() -> None:
    for name in morse.__all__:
        assert hasattr(morse, name), name


def test_no_unexpected_public_names() -> None:
    public = {
        name for name in dir(morse)
        if not name.startswith("_") and name != "annotations"
    }
    extra = public - _EXPECTED
    assert extra == set(), f"unexpected public names: {extra}"


def test_version_string_has_dots() -> None:
    assert isinstance(morse.__version__, str)
    assert morse.__version__.count(".") >= 1
