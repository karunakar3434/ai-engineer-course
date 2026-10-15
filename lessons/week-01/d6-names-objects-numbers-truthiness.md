# Names, objects, equality, numbers and truthiness

*Week 1 · day 6 · 2026-10-15 · 70 min · topic `w01-py-core` (part 1 of 3) · facts verified 2026-10-15 by running the examples on CPython 3.13.16*

**You'll be able to:** predict what aliasing does to a list shared by two names; choose between `==` and `is`; say what "dynamic but strong typing" rules out; predict `/`, `//` and `%` on negative numbers; spot the "falsy zero" bug in config and LLM-call code.
**Builds on:** [d5: the REPL](d5-ruff-vscode-repl-scripts-pytest.md#4-the-repl-your-jshell), which is the fastest way to test each prediction below.
**Adapted from:** the diagnostic. Its aliasing (B2), `//` and `%` (B3) and truthiness (B4) items each get their own section and a predict-first drill. The last section ties truthiness to LLM call parameters, which come back in week 4.

Run the examples from the repo root, one part at a time, so you can predict before you look:

```bash
uv run lessons/week-01/examples/03_names_and_objects.py aliasing
```

---

## 1. Names are labels, not boxes

**Java bridge**

```java
List<Integer> defaults = new ArrayList<>(List.of(1, 2, 4));
List<Integer> forRequest = defaults;   // same object, two references
forRequest.add(8);                     // defaults now has 8 too
```

```python
default_retries = [1, 2, 4]
request_retries = default_retries      # same object, two names
request_retries.append(8)              # default_retries now has 8 too
```

Where the analogy breaks: Java has two worlds, primitives (copied by value) and objects (shared by reference). Python has only objects. Every name is a reference, even `x = 5`. You don't notice with `int`, `str` and `tuple` because they're **immutable**: nothing can change them in place, so sharing them is harmless.

The rules:
- `=` never copies. It binds a name to an object.
- **Mutating** (`.append`, `[i] = …`, `+=` on a list) changes the object, so every name sees it.
- **Rebinding** (`x = something_else`) moves one name and leaves the object alone.
- Function arguments work exactly like Java: the function gets a reference. Mutating it is visible to the caller; rebinding the parameter isn't.
- Copy explicitly: `list(xs)`, `xs.copy()` or `xs[:]` (shallow copies; deep copies come in week 2).

**Run it:** parts `aliasing`, `augmented` and `args` of `03_names_and_objects.py`. Look for `id()` printing the same number twice, and for `+=` and `= … +` behaving differently.

**Try it (3 min):** predict both lines before you run `augmented`:

```python
a = [1, 2]; b = a; b += [3]       # a is now?
a = [1, 2]; b = a; b = b + [3]    # a is now?
```

**Check:** diagnostic B2 again. `a = [1, 2]`, `b = a`, `b.append(3)`. What do `print(a)` and `print(a is b)` show, and which Java line is `a is b`?

## 2. `==` vs `is`, and `None`

**Java bridge**

| Question | Java | Python |
|:--|:--|:--|
| Same value? | `a.equals(b)` | `a == b` (calls `__eq__`) |
| Same object? | `a == b` | `a is b` |
| Is it null? | `x == null` | `x is None` |

Where the analogy breaks: Java taught you to distrust `==` on strings. In Python `==` is the value comparison and the one you want almost always. Use `is` only for singletons, and in practice that means `None`.

There's a familiar trap here too. Java caches `Integer` objects from −128 to 127, so `Integer a = 127, b = 127; a == b` is `true` but 128 isn't. CPython caches small ints from −5 to 256, so `int("256") is int("256")` is `True` and `int("257") is int("257")` is `False`. Same lesson as Java: never use identity for values. Python 3.13 even warns you: `x is 1` gives `SyntaxWarning: "is" with 'int' literal. Did you mean "=="?`.

`None` is Python's `null`, but it's a real object (the only instance of `NoneType`), and a function without `return` returns it. That's why `x != None` → `x is not None` was an *unsafe* ruff fix on day 5: a class can override `__eq__` to say it equals `None`, but nothing can fake `is`.

**Run it:** part `identity`.

**Try it (2 min):** predict `[] == []` and `[] is []`.

**Check:** a teammate writes `if status_code is 200:`. Why might it pass every test and still be wrong?

## 3. Dynamic, but strong

**Java bridge**

```java
String s = "3" + 4;     // "34": Java converts the int for you
int n = "3";            // compile error: the variable has a type
```

```python
s = "3" + 4             # TypeError at runtime: no silent conversion
n = 3; n = "three"      # fine: the name has no type, the object does
```

Python is **dynamically typed**: names have no declared type, and checks happen at runtime. It's also **strongly typed**: an object's type never changes, and Python doesn't convert between unrelated types for you. Java is static *and* strong; JavaScript is dynamic *and* weak (`"3" + 4 === "34"`, `"3" * 4 === 12`).

Some conversions it does make: `int` and `float` mix (`1 == 1.0` is `True`), and `bool` is a subclass of `int` (`True + True == 2`). Operators are defined per type, so `"3" * 4` is `"3333"` (repetition), not 12.

The production angle: without a compiler, a type error waits until that line runs, maybe at 3 a.m. on the one code path your tests skipped. Type hints plus a type checker (from week 2) give you some of `javac` back.

**Run it:** part `types` of `04_numbers_truthiness.py`.

**Try it (2 min):** predict `"3" * 4`, `int("3") + 4` and `"3" + 4`.

**Check:** is `x = 5; x = "five"` dynamic typing or weak typing? What would weak typing look like?

## 4. Numbers: unbounded ints, three kinds of division, floats

**Java bridge**

| Expression | Java (`int`) | Python |
|:--|:--|:--|
| `Integer.MAX_VALUE + 1` | `-2147483648` (silent overflow) | `2147483648` (ints grow as needed) |
| `7 / 2` | `3` | `3.5` (`/` is always true division) |
| `-7 / 2` (integer) | `-3` (truncates toward 0) | `-7 // 2` → `-4` (floors toward −∞) |
| `-7 % 2` | `-1` (sign of the dividend) | `1` (sign of the divisor) |
| Floor versions | `Math.floorDiv`, `Math.floorMod` | `//` and `%` already are |
| `(int) -3.7` | `-3` | `int(-3.7)` → `-3` (truncates; `math.floor` gives `-4`) |
| `Math.round(2.5)` | `3` | `round(2.5)` → `2` (rounds half to even) |
| `new BigDecimal("0.1")` | exact | `Decimal("0.1")` (and `Decimal(0.1)` has the same float trap) |

Floats are the same IEEE 754 doubles as Java's `double`, so `0.1 + 0.2 == 0.3` is `False` in both. Compare with `math.isclose`. One difference: `0.0 / 0.0` is `NaN` in Java but raises `ZeroDivisionError` in Python.

Why `//` floors: it keeps `(a // b) * b + a % b == a` true *and* makes `%` land in `0..b-1` for positive `b`. That's what you want for sharding (`user_id % shards` is never negative) and for time buckets: with `t // 60`, second −1 lands in minute −1, not minute 0.

The production angle for this course: token costs are small floats (`tokens * price_per_million / 1_000_000`). Floats are fine for logging and budgets; use `Decimal` if you ever bill someone.

**Run it:** parts `ints`, `division` and `floats`.

**Try it (3 min):** predict diagnostic B3 before you run `division`: `-7 // 2`, `-7 % 2`, `7 / 2`.

**Check:** `len(xs) / 2` as a list index raises `TypeError: list indices must be integers or slices, not float`. Which operator fixes it, and why didn't Java need one?

## 5. Truthiness, and `and`/`or` return values

**Java bridge**

```java
if (name != null && !name.isEmpty()) { ... }   // only booleans allowed in a condition
```

```python
if name: ...                                    # None and "" are both falsy
```

Where the analogy breaks: Java's `if` only takes a `boolean`. Python's `if` takes any object and asks `bool(obj)`.

**Falsy:** `None`, `False`, zero of any number type (`0`, `0.0`), and empty containers (`""`, `[]`, `()`, `{}`, `set()`, `range(0)`).
**Everything else is truthy**, including `"0"`, `"False"`, `" "`, `[0]`, `[[]]` and `float("nan")`. Diagnostic B4 was the string `"0"`: it's a non-empty string, so it's truthy.

`and` and `or` don't return booleans. They return **one of their operands**: `a or b` gives `a` if `a` is truthy, else `b`; `a and b` gives `a` if `a` is falsy, else `b`. Both short-circuit. That's where the common `value or default` idiom comes from, and where its classic bug comes from:

```python
def complete(prompt, temperature=None):
    temperature = temperature or 0.7    # BUG: temperature=0.0 is falsy -> becomes 0.7
```

Someone asks for the most predictable output with `temperature=0.0` and silently gets 0.7. The same bug hits `timeout or 30` (0 meaning "no wait"), `max_tokens or 1024`, `retries or 3` and `port or 8080`. The fix: when 0, `""` or `[]` are valid values, test `is None`.

```python
    if temperature is None:
        temperature = 0.7
```

Rule of thumb: `if not items:` is idiomatic for "empty list". Use `is None` when you mean "not provided".

**Run it:** parts `truthy` and `andor`.

**Try it (3 min):** predict `bool("0")`, `bool("False")`, `bool([0])`, and `"" or "us-east"`.

**Check:** a config loader does `retries = config.get("retries") or 3`. The YAML says `retries: 0`. How many retries happen, and what's the one-line fix?

---

## Pitfalls for Java developers

- **Assuming `=` copies**: two names share one list, and a "local" change leaks out. Copy explicitly.
- **`+=` on a list is a mutation**, not a new list. On `str`, `int` and `tuple` it rebinds.
- **Using `is` for values**: it works for small ints and some strings by accident, then breaks at 257. Use `is` only for `None`.
- **Expecting `"id: " + 42` to work**: use an f-string (`f"id: {42}"`, day 7) or `str(42)`.
- **Porting integer division with `/`**: `/` returns a float. Use `//`, and remember it floors negatives.
- **Porting `Math.round`**: `round(2.5) == 2`. Use `Decimal` with an explicit rounding mode when it matters.
- **`x or default` when 0 or `""` is valid**: the falsy-zero bug. Use `if x is None`.

## Summary

- Every value is an object and every name is a reference. Mutation is shared, rebinding isn't, and `=` never copies.
- `==` compares values (like `equals`), `is` compares identity (like Java's `==`). Use `is` only for `None`.
- Dynamic (names have no types) but strong (no silent `"3" + 4`). Type errors surface at runtime.
- `int` never overflows; `/` is always float; `//` and `%` floor toward −∞ (Java's `floorDiv`/`floorMod`); `round` rounds half to even.
- Empty and zero are falsy, everything else is truthy; `and`/`or` return operands. Use `is None` when 0 is a valid value.

## Docs

- [Data model: objects, values and types](https://docs.python.org/3.13/reference/datamodel.html#objects-values-and-types) (verified 2026-10-15)
- [Identity comparisons (`is`)](https://docs.python.org/3.13/reference/expressions.html#is-not) and [value comparisons](https://docs.python.org/3.13/reference/expressions.html#value-comparisons)
- [Truth value testing](https://docs.python.org/3.13/library/stdtypes.html#truth-value-testing) and [Boolean operations](https://docs.python.org/3.13/library/stdtypes.html#boolean-operations-and-or-not)
- [Numeric types, including `//` and `%`](https://docs.python.org/3.13/library/stdtypes.html#numeric-types-int-float-complex) and [`round()`](https://docs.python.org/3.13/library/functions.html#round)
- [`decimal`](https://docs.python.org/3.13/library/decimal.html)
- [Small-int cache: `PyLong_FromLong`](https://docs.python.org/3.13/c-api/long.html#c.PyLong_FromLong) (CPython detail, −5 to 256)
- Java: [`Math.floorMod`](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Math.html#floorMod(int,int)), [`Integer.valueOf` cache](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Integer.html#valueOf(int))
