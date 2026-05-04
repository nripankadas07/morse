"""Exception hierarchy for the :mod:`morse` package."""

from __future__ import annotations

__all__ = [
    "MorseError",
    "EncodeError",
    "DecodeError",
    "TimingError",
]


class MorseError(ValueError):
    """Base class for every error raised by :mod:`morse`."""


class EncodeError(MorseError):
    """Raised by :func:`morse.encode` for unknown characters under ``errors='strict'``.

    The unknown character is stored on :attr:`character` and the input
    index is stored on :attr:`index`.
    """

    def __init__(self, message: str, *, character: str, index: int) -> None:
        super().__init__(message)
        self.character = character
        self.index = index


class DecodeError(MorseError):
    """Raised by :func:`morse.decode` for unknown tokens under ``errors='strict'``.

    The unknown token is stored on :attr:`token` and its position
    (letter index in the input stream) on :attr:`index`.
    """

    def __init__(self, message: str, *, token: str, index: int) -> None:
        super().__init__(message)
        self.token = token
        self.index = index


class TimingError(MorseError):
    """Raised when timing parameters are inconsistent (e.g. ``f > c``)."""
