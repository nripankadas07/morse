"""morse — International Morse Code encoder/decoder with prosigns and Farnsworth timing.

Public API::

    from morse import (
        encode,
        decode,
        is_valid,
        to_timing,
        TimingElement,
        MORSE_CODE,
        REVERSE_CODE,
        PROSIGNS,
        MorseError,
        EncodeError,
        DecodeError,
        TimingError,
    )

The encoder takes plain text and emits a Morse string with ``" / "``
between words and a single space between letters.  Embedded prosign
tags (``<AR>``, ``<SK>``, ``<SOS>``, ...) are emitted as a single token
with no internal space, so they survive a round trip back through
:func:`decode` with ``prosigns=True``.

The Farnsworth helper :func:`to_timing` returns the duration of every
dit, dah, and gap in milliseconds at the requested character / effective
word-per-minute speeds.
"""

from ._data import (
    MORSE_CODE,
    MORSE_TO_PROSIGN,
    PROSIGN_TO_MORSE,
    PROSIGNS,
    REVERSE_CODE,
)
from ._decode import decode, is_valid
from ._encode import encode
from ._errors import DecodeError, EncodeError, MorseError, TimingError
from ._timing import TimingElement, to_timing

__all__ = [
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
]

__version__ = "0.1.0"
