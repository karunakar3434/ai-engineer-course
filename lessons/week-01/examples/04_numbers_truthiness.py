# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///
"""Strong dynamic typing, numbers and truthiness, with the Java habits that break.

Run one part at a time so you can predict first:
    uv run lessons/week-01/examples/04_numbers_truthiness.py types
Parts: types, ints, division, floats, truthy, andor (no argument runs them all).
"""

import math
import sys
from decimal import Decimal


def dynamic_typing() -> None:
    x = 42
    print("type(x):", type(x).__name__)
    x = "forty-two"  # the name has no type; the object does
    print("type(x):", type(x).__name__)

    print('"3" * 4       ->', repr("3" * 4))
    print('int("3") + 4  ->', int("3") + 4)
    try:
        print('"3" + 4       ->', "3" + 4)  # Java gives "34"
    except TypeError as e:
        print('"3" + 4       -> TypeError:', e)

    print("True + True   ->", True + True)  # bool is a subclass of int
    print("1 == 1.0      ->", 1 == 1.0)


def ints() -> None:
    java_int_max = 2**31 - 1
    print("2**31 - 1 + 1 ->", java_int_max + 1, "(Java int wraps to -2147483648)")
    print("2**100        ->", 2**100)
    total_tokens = 1_250_000  # underscores in literals, as in Java
    print("1_250_000     ->", total_tokens)


def division() -> None:
    print(" 7 / 2  ->", 7 / 2, "|  6 / 3  ->", 6 / 3)
    print(" 7 // 2 ->", 7 // 2, "|  7 % 2  ->", 7 % 2)
    print("-7 // 2 ->", -7 // 2, "| -7 % 2  ->", -7 % 2, "(Java: -3 and -1)")
    print("int(-3.7) ->", int(-3.7), "| math.floor(-3.7) ->", math.floor(-3.7))

    # Real world: bucket event timestamps (seconds relative to a deploy) into minutes.
    for t in (-61, -1, 0, 59, 60):
        print(f"  t={t:>4}s -> minute bucket {t // 60:>2}")


def floats() -> None:
    print("0.1 + 0.2        ->", 0.1 + 0.2)
    print("0.1 + 0.2 == 0.3 ->", 0.1 + 0.2 == 0.3)
    print("math.isclose     ->", math.isclose(0.1 + 0.2, 0.3))
    print("round(2.5), round(3.5) ->", round(2.5), round(3.5), "(Java Math.round: 3 4)")
    print('Decimal("0.1") + Decimal("0.2") ->', Decimal("0.1") + Decimal("0.2"))
    print("Decimal(0.1)     ->", Decimal(0.1))  # noqa: RUF032 (the new BigDecimal(0.1) trap)
    try:
        print(0.0 / 0.0)
    except ZeroDivisionError as e:
        print("0.0 / 0.0        -> ZeroDivisionError:", e, "(Java double: NaN)")


def truthy() -> None:
    values = [None, False, 0, 0.0, "", [], {}, set(), "0", "False", " ", [0], [[]], float("nan")]
    for v in values:
        print(f"  bool({v!r:>14}) -> {bool(v)}")


def complete(prompt: str, temperature: float | None = None) -> str:
    temperature = temperature or 0.7  # BUG: 0 is falsy, so 0.0 becomes 0.7
    return f"calling model with temperature={temperature}"


def complete_fixed(prompt: str, temperature: float | None = None) -> str:
    if temperature is None:
        temperature = 0.7
    return f"calling model with temperature={temperature}"


def andor() -> None:
    region = ""
    print('region = ""      ; region or "us-east"  ->', repr(region or "us-east"))
    region = "eu-west"
    print('region = "eu-west"; region or "us-east"  ->', repr(region or "us-east"))
    errors = 0
    print("errors = 0; errors and 100 / errors     ->", errors and 100 / errors)  # 100/0 never runs
    hits: list[str] = []
    print("hits = []; hits or None                 ->", hits or None)
    print("complete(temperature=0.0)      ->", complete("hi", temperature=0.0))
    print("complete_fixed(temperature=0.0)->", complete_fixed("hi", temperature=0.0))


PARTS = {
    "types": dynamic_typing,
    "ints": ints,
    "division": division,
    "floats": floats,
    "truthy": truthy,
    "andor": andor,
}

if __name__ == "__main__":
    chosen = sys.argv[1:] or list(PARTS)
    for name in chosen:
        print(f"--- {name} ---")
        PARTS[name]()
