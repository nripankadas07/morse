"""Morse -> text decoder.

Letters are separated by whitespace (any number of consecutive
``" "``/``"\\t"``); words are separated by a ``"/"`` token (with or
without surrounding whitespace).  When ``prosigns=True``, multi-letter
Morse runs that match a known prosign are emitted as ``<XX>``.
"""

from __future__ import annotations

from typing import Iterable, List

from ._data import MORSE_TO_PROSIGN, REVERSE_CODE
from ._errors import DecodeError

__all__ = ["decode", "is_valid"]


_VALID_ERRORS = ("strict", "ignore", "replace")
_DOT_DASH = set(".-")


def decode(
    morse: str,
    *,
    prosigns: bool = True,
    errors: str = "strict",
) -> str:
    """Decode ``morse`` into text using International Morse Code."""
    if errors not in _VALID_ERRORS:
        raise ValueError(
            f"errors must be one of {_VALID_ERRORS}, got {errors!r}"
        )
    out: List[str] = []
    for word_index, word in enumerate(_split_words(morse)):
        if word_index > 0:
            out.append(" ")
        out.extend(_decode_word(word, prosigns=prosigns, errors=errors))
    return "".join(out)


def is_valid(morse: str) -> bool:
    """Return ``True`` if ``morse`` decodes cleanly under default rules."""
    try:
        decode(morse)
    except DecodeError:
        return False
    return True


def _split_words(morse: str) -> Iterable[List[str]]:
    """Yield each word as a list of dot/dash tokens.

    Empty words (e.g. produced by leading/trailing ``/``) are skipped.
    """
    current: List[str] = []
    for token in _iter_tokens(morse):
        if token == "/":
            if current:
                yield current
                current = []
            continue
        current.append(token)
    if current:
        yield current


def _iter_tokens(morse: str) -> Iterable[str]:
    """Tokenise ``morse`` into letter codes and ``"/"`` separators."""
    buf: List[str] = []
    for ch in morse:
        if ch in _DOT_DASH:
            buf.append(ch)
            continue
        if buf:
            yield "".join(buf)
            buf.clear()
        if ch == "/":
            yield "/"
            continue
        if ch.isspace():
            continue
        # Anything else is an invalid byte; pass through as a token so
        # ``_decode_letter`` can raise/ignore/replace per ``errors``.
        yield ch
    if buf:
        yield "".join(buf)


def _decode_word(
    word: List[str], *, prosigns: bool, errors: str
) -> Iterable[str]:
    for index, token in enumerate(word):
        letter = _resolve(token, index, prosigns=prosigns, errors=errors)
        if letter is not None:
            yield letter


def _resolve(
    token: str, index: int, *, prosigns: bool, errors: str
) -> str | None:
    if prosigns and token in MORSE_TO_PROSIGN:
        return f"<{MORSE_TO_PROSIGN[token]}>"
    letter = REVERSE_CODE.get(token)
    if letter is not None:
        return letter
    if errors == "ignore":
        return None
    if errors == "replace":
        return "?"
    raise DecodeError(
        f"unknown Morse token {token!r} at letter index {index}",
        token=token,
        index=index,
    )
