"""Compute element-by-element timing for a Morse rendering.

The unit of time at "character speed" is the dit duration::

    dit_ms = 1200 / character_wpm

Standard timing has dit:dah:intra:letter:word = 1:3:1:3:7 dits.
Farnsworth timing keeps the dit:dah:intra ratio at character speed but
stretches the letter and word gaps so that the **effective** word rate
matches ``wpm``.  The classical PARIS-derived formula gives::

    x = (60 c - 37.2 f) / (7.6 f)         (dits per letter gap)
    letter_ms = x * dit_ms_at_char
    word_ms   = (7 x / 3) * dit_ms_at_char

(with ``f`` = effective_wpm and ``c`` = character_wpm).  At ``c == f``
this reduces to ``x = 3``, i.e. the 3:7 letter:word ratio of standard
timing.
"""

from __future__ import annotations

from typing import List, Optional, Tuple

from ._encode import encode
from ._errors import TimingError

__all__ = ["to_timing", "TimingElement"]

TimingElement = Tuple[str, float]


def to_timing(
    text: str,
    *,
    wpm: float,
    character_wpm: Optional[float] = None,
    prosigns: bool = True,
) -> List[TimingElement]:
    """Render ``text`` and return its timing as ``[(kind, duration_ms), ...]``.

    ``kind`` is one of ``"dit"``, ``"dah"``, ``"intra"`` (within-letter
    gap), ``"letter"`` (between-letter gap), or ``"word"``.
    """
    char_wpm = _validate(wpm, character_wpm)
    morse = encode(text, prosigns=prosigns)
    return _build_timing(morse, char_wpm=char_wpm, eff_wpm=wpm)


def _validate(wpm: float, character_wpm: Optional[float]) -> float:
    if wpm <= 0:
        raise TimingError(f"wpm must be positive, got {wpm}")
    char_wpm = character_wpm if character_wpm is not None else wpm
    if char_wpm <= 0:
        raise TimingError(
            f"character_wpm must be positive, got {char_wpm}"
        )
    if char_wpm < wpm:
        raise TimingError(
            "character_wpm must be >= wpm "
            f"(got character_wpm={char_wpm}, wpm={wpm})"
        )
    return char_wpm


def _build_timing(
    morse: str, *, char_wpm: float, eff_wpm: float
) -> List[TimingElement]:
    dit_ms = 1200.0 / char_wpm
    letter_ms, word_ms = _farnsworth_gaps(char_wpm, eff_wpm, dit_ms)
    out: List[TimingElement] = []
    pending: Optional[TimingElement] = None
    for token in morse.split(" "):
        if token == "":
            continue
        if token == "/":
            # ``encode`` never emits a leading or doubled ``/``, so
            # ``pending`` is always a letter gap here — promote it to
            # a word gap and move on.
            pending = ("word", word_ms)
            continue
        if pending is not None:
            out.append(pending)
        _emit_letter(out, token, dit_ms)
        pending = ("letter", letter_ms)
    return out


def _farnsworth_gaps(
    char_wpm: float, eff_wpm: float, dit_ms: float
) -> tuple[float, float]:
    if eff_wpm == char_wpm:
        return 3.0 * dit_ms, 7.0 * dit_ms
    x = (60.0 * char_wpm - 37.2 * eff_wpm) / (7.6 * eff_wpm)
    return x * dit_ms, (7.0 * x / 3.0) * dit_ms


def _emit_letter(
    out: List[TimingElement], token: str, dit_ms: float
) -> None:
    for index, ch in enumerate(token):
        if index > 0:
            out.append(("intra", dit_ms))
        if ch == ".":
            out.append(("dit", dit_ms))
        else:
            out.append(("dah", 3.0 * dit_ms))
