"""ITU-R M.1677-1 International Morse Code tables and prosigns."""

from __future__ import annotations

from typing import Dict, Mapping

__all__ = [
    "MORSE_CODE",
    "REVERSE_CODE",
    "PROSIGNS",
    "PROSIGN_TO_MORSE",
    "MORSE_TO_PROSIGN",
]


_MORSE_CODE_RAW: Dict[str, str] = {
    # Letters
    "A": ".-",   "B": "-...", "C": "-.-.", "D": "-..",  "E": ".",
    "F": "..-.", "G": "--.",  "H": "....", "I": "..",   "J": ".---",
    "K": "-.-",  "L": ".-..", "M": "--",   "N": "-.",   "O": "---",
    "P": ".--.", "Q": "--.-", "R": ".-.",  "S": "...",  "T": "-",
    "U": "..-",  "V": "...-", "W": ".--",  "X": "-..-", "Y": "-.--",
    "Z": "--..",
    # Digits
    "0": "-----", "1": ".----", "2": "..---", "3": "...--", "4": "....-",
    "5": ".....", "6": "-....", "7": "--...", "8": "---..", "9": "----.",
    # Punctuation (ITU)
    ".": ".-.-.-",  ",": "--..--",  "?": "..--..",  "'": ".----.",
    "!": "-.-.--",  "/": "-..-.",   "(": "-.--.",   ")": "-.--.-",
    "&": ".-...",   ":": "---...",  ";": "-.-.-.",  "=": "-...-",
    "+": ".-.-.",   "-": "-....-",  "_": "..--.-",  '"': ".-..-.",
    "$": "...-..-", "@": ".--.-.",
}


def _build_tables() -> tuple[Mapping[str, str], Mapping[str, str]]:
    forward = dict(_MORSE_CODE_RAW)
    reverse: Dict[str, str] = {}
    for letter, code in forward.items():
        reverse[code] = letter
    return forward, reverse


MORSE_CODE, REVERSE_CODE = _build_tables()


# Standard prosigns.  Wrapped with ``<>`` in encode/decode output so they
# survive a round trip without colliding with single-letter encodings.
# (e.g. plain ``AR`` would otherwise come back as ``A R`` through a
# straight ``decode``.)
PROSIGNS: tuple[str, ...] = ("AA", "AR", "AS", "BK", "BT", "HH", "KN", "SK", "SOS")


def _build_prosign_tables() -> tuple[Mapping[str, str], Mapping[str, str]]:
    forward: Dict[str, str] = {}
    reverse: Dict[str, str] = {}
    for name in PROSIGNS:
        code = "".join(MORSE_CODE[ch] for ch in name)
        forward[name] = code
        reverse[code] = name
    return forward, reverse


PROSIGN_TO_MORSE, MORSE_TO_PROSIGN = _build_prosign_tables()
