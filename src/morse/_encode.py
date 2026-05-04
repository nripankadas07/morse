"""Text -> Morse encoder.

Word separator on output is ``" / "``; letter separator is a single
space.  Prosigns may be embedded in the input as ``<XX>`` (e.g.
``<AR>`` for end-of-message) — these are emitted as a single Morse
token with no internal space, which keeps them recoverable on decode.
"""

from __future__ import annotations

import re
from typing import Iterable, List, Tuple

from ._data import MORSE_CODE, PROSIGN_TO_MORSE
from ._errors import EncodeError

__all__ = ["encode"]


_PROSIGN_TAG = re.compile(r"<([A-Z]+)>")
_VALID_ERRORS = ("strict", "ignore", "replace")


def encode(
    text: str,
    *,
    prosigns: bool = True,
    errors: str = "strict",
) -> str:
    """Encode ``text`` to a Morse-code string.

    ``" / "`` separates words; a single space separates letters.  Set
    ``prosigns=False`` to disable ``<XX>`` tag handling and treat the
    angle brackets as unknown characters.
    """
    if errors not in _VALID_ERRORS:
        raise ValueError(
            f"errors must be one of {_VALID_ERRORS}, got {errors!r}"
        )
    tokens = list(_tokenise(text, prosigns=prosigns))
    return " ".join(_emit(tokens, errors=errors))


def _tokenise(text: str, *, prosigns: bool) -> Iterable[Tuple[str, str, int]]:
    """Yield ``(kind, value, source_index)`` triples.

    ``kind`` is one of ``"prosign"`` (full-word morse, no internal
    space), ``"char"`` (single character), or ``"word_sep"``.
    """
    upper = text.upper()
    pos = 0
    while pos < len(upper):
        ch = upper[pos]
        if ch.isspace():
            yield ("word_sep", "", pos)
            pos = _skip_whitespace(upper, pos)
            continue
        if prosigns and ch == "<":
            match = _PROSIGN_TAG.match(upper, pos)
            if match and match.group(1) in PROSIGN_TO_MORSE:
                yield ("prosign", match.group(1), pos)
                pos = match.end()
                continue
        yield ("char", ch, pos)
        pos += 1


def _skip_whitespace(upper: str, pos: int) -> int:
    while pos < len(upper) and upper[pos].isspace():
        pos += 1
    return pos


def _emit(
    tokens: List[Tuple[str, str, int]], *, errors: str
) -> Iterable[str]:
    pending_word_sep = False
    seen_letter = False
    for kind, value, index in tokens:
        if kind == "word_sep":
            if seen_letter:
                pending_word_sep = True
            continue
        code = _resolve_token(kind, value, index, errors)
        if code is None:
            continue
        if pending_word_sep:
            yield "/"
            pending_word_sep = False
        yield code
        seen_letter = True


def _resolve_token(
    kind: str, value: str, index: int, errors: str
) -> str | None:
    if kind == "prosign":
        return PROSIGN_TO_MORSE[value]
    code = MORSE_CODE.get(value)
    if code is not None:
        return code
    if errors == "ignore":
        return None
    if errors == "replace":
        # Substitute the Morse code for "?" so output stays
        # in the dot/dash alphabet.
        return MORSE_CODE["?"]
    raise EncodeError(
        f"no Morse code for character {value!r} at index {index}",
        character=value,
        index=index,
    )
