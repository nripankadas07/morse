# morse

International Morse Code encoder, decoder, and Farnsworth timing
helper for Python 3.8+. Zero dependencies.

* Letters A-Z, digits 0-9, and the standard ITU punctuation set.
* Round-trip-safe prosigns wrapped as `<AR>`, `<SK>`, `<SOS>`, `<BT>`,
  `<KN>`, `<AS>`, `<BK>`, `<HH>`, `<AA>`.
* Configurable error handling: `strict`, `ignore`, or `replace`.
* Element-by-element timing in milliseconds, with optional Farnsworth
  spacing.

## Install

```bash
pip install morse
```

Or from a clone:

```bash
pip install -e .
```

## Quick start

```python
from morse import encode, decode, to_timing

encode("Hello world")        # '.... . .-.. .-.. --- / .-- --- .-. .-.. -..'
decode(".... . .-.. .-.. ---")  # 'HELLO'

# Prosigns survive a round trip:
encode("<SOS> please")
# '...---... / .--. .-.. . .- ... .'
decode("...---... / .--. .-.. . .- ... .")
# '<SOS> PLEASE'

# Element-by-element timing at 20 wpm (dit = 60 ms):
to_timing("HI", wpm=20)
# [('dit', 60.0), ('intra', 60.0), ('dit', 60.0), ('intra', 60.0),
#  ('dit', 60.0), ('intra', 60.0), ('dit', 60.0),
#  ('letter', 180.0),
#  ('dit', 60.0), ('intra', 60.0), ('dit', 60.0)]

# Farnsworth: characters at 18 wpm, perceived speed at 10 wpm:
to_timing("HELLO WORLD", wpm=10, character_wpm=18)
```

## API reference

### `encode(text, *, prosigns=True, errors="strict") -> str`

Encode text to Morse. Output uses a single space between letters and
`" / "` between words. Lowercase input is uppercased.

* `prosigns=True` recognises `<AR>` / `<SK>` / `<SOS>` / `<BT>` / etc.
  in input and emits each as a single concatenated token.
* `errors`:
  - `"strict"` (default) raises `EncodeError` on unknown characters.
  - `"ignore"` drops them silently.
  - `"replace"` substitutes the Morse code for `?` (`..--..`).

### `decode(morse, *, prosigns=True, errors="strict") -> str`

Decode a Morse string. Letters are separated by whitespace; words are
separated by `/` (with or without surrounding whitespace).

* `prosigns=True` (default) emits known multi-letter Morse runs as
  `<XX>`. Set to `False` to look up only the single-character table.
* `errors` works identically to `encode`. With `"strict"` the decoder
  raises `DecodeError` on the first unknown token; with `"replace"`
  unknown tokens become `"?"`.

### `is_valid(morse) -> bool`

`True` if `decode(morse)` would succeed under default settings.

### `to_timing(text, *, wpm, character_wpm=None, prosigns=True) -> list[tuple[str, float]]`

Render `text` and return a list of `(kind, duration_ms)` pairs. `kind`
is one of:

| Kind     | Meaning                                |
| -------- | -------------------------------------- |
| `dit`    | A short element (1 dit duration).      |
| `dah`    | A long element (3 dits).               |
| `intra`  | Within-letter gap between elements.    |
| `letter` | Between-letter gap.                    |
| `word`   | Between-word gap.                      |

Trailing letter and word gaps are omitted, so the list ends on a
`dit` / `dah`.

#### Farnsworth timing

Farnsworth keeps the dits and dahs at the **character** speed but
stretches the inter-letter and inter-word gaps so that the **effective**
word-per-minute rate matches `wpm`.

For ``wpm = effective_wpm`` and ``character_wpm = c``:

* `dit_ms = 1200 / c`
* `letter_gap_ms = x * dit_ms`, where
  `x = (60 c - 37.2 effective_wpm) / (7.6 effective_wpm)`
* `word_gap_ms = (7 x / 3) * dit_ms`

When `character_wpm == wpm` (or `None`) this reduces to the standard
3:7 letter:word ratio. `character_wpm < wpm` raises `TimingError`.

## Errors

All errors descend from `MorseError`, which subclasses `ValueError`.

| Class           | Raised when                                      |
| --------------- | ------------------------------------------------ |
| `EncodeError`   | `encode` saw an unknown character (strict mode). |
| `DecodeError`   | `decode` saw an unknown Morse token (strict).    |
| `TimingError`   | Bad `wpm` / `character_wpm` arguments.           |

`EncodeError` carries `.character` and `.index`; `DecodeError` carries
`.token` and `.index`.

## Constants

* `MORSE_CODE: dict[str, str]` — character → dot/dash.
* `REVERSE_CODE: dict[str, str]` — dot/dash → character.
* `PROSIGNS: tuple[str, ...]` — known prosign names.
* `PROSIGN_TO_MORSE`, `MORSE_TO_PROSIGN` — both directions for prosigns.

## Running tests

```bash
pip install pytest pytest-cov mypy
PYTHONPATH=src pytest --cov=morse --cov-branch
mypy --strict src/morse
```

The bundled suite has 99 tests with 100% line + 100% branch coverage
across all six source modules.

## License

MIT — see `LICENSE`.
