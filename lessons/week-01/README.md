# Week 1: Python for Java developers I

*2026-10-10 – 2026-10-16 · 15 h available (3 h missed on Sat 10-10) · syllabus v2*

## Goal

By Friday you can create and run a uv project, read and write idiomatic core Python without tripping on its reference, truthiness and generator semantics, and start a streaming log-analysis CLI.

Success criteria:
- Explain in two sentences each: what `uv.lock` is for, why a venv replaces the classpath, and what a generator is.
- On the week 1 review quiz, predict-the-output accuracy ≥ 70%.
- `w01-t1` scaffolded, with its provided tests running (`uv run pytest`) and the first stats implemented.

## Adaptations

| Change | Evidence |
|:--|:--|
| Recap quizzes are 5 questions, with predict-the-output drills and one LLM concept card each | Diagnostic; student wants thorough quizzes |
| The core lessons drill the classic Java-to-Python traps directly: mutable defaults, aliasing and `is`, `//` vs `/`, truthiness of `"0"`, generator exhaustion | Diagnostic |
| `w01-py-testing` moved to week 2 day 1 (3 h). `w01-t1` mostly carries into week 2 day 1 | Missed Saturday plus a longer diagnostic. The student chose to extend the course rather than compress |
| A real-world angle in every lesson (logs, configs, service code) | Student prefers reading with real-world examples |

## Schedule

| Day | Date | Weekday | Hours | Topics | Agenda (minutes) |
|:--|:--|:--|:--|:--|:--|
| d1 | 10-10 | Sat | 0 (missed) | – | – |
| d2 | 10-11 | Sun | 3 | diagnostic, `w01-py-tooling` | diagnostic and syllabus 90 · tooling part 1 75 · wrap 15 |
| d3 | 10-12 | Mon | 3 | `w01-py-tooling`, `w01-py-core` | recap quiz 15 · **finish d2 lesson (sections 1–5) 70** · tooling part 2 70 · core part 1 20 · wrap 5 *(updated 10-11: d2 lesson carried over; the start-of-session re-plan moves the remaining core time)* |
| d4 | 10-13 | Tue | 2 | `w01-py-core` | recap quiz 15 · core part 2 100 · wrap 5 |
| d5 | 10-14 | Wed | 2 | `w01-py-core`, `w01-py-collections` | recap quiz 15 · core part 3 80 · collections part 1 20 · wrap 5 |
| d6 | 10-15 | Thu | 2 | `w01-py-collections` | recap quiz 15 · collections part 2 100 · wrap 5 |
| d7 | 10-16 | Fri | 3 | `w01-py-collections`, `w01-t1` | weekly review quiz 25 · collections part 3 100 · w01-t1 scaffold and start 50 · wrap 5 |

Carried into week 2: about 3 h of `w01-t1` (1 h was already planned there). Week 2 absorbs this with its slack, and week 3 has 1.5 h spare.

## Session outlines

### d2 · uv projects, pyproject.toml and virtual environments (`w01-py-tooling`, part 1)
- **Objectives:** create a uv project; explain what each generated file does next to its Maven counterpart; add runtime and dev dependencies; run code and tools with `uv run`.
- **Key points:** Python versions on your Mac (several of them, like several JDKs) and `.python-version`; `uv init` (with `--python 3.13`); `pyproject.toml` vs `pom.xml`; `uv add` vs `uv add --dev` (dependency groups vs `<scope>test</scope>`); `uv.lock` vs Maven's lack of a lockfile; `.venv` vs the classpath and `~/.m2`; `uv run` vs `mvn exec:java`; the src layout and `[project.scripts]` vs a `Main-Class` manifest entry.
- **Java bridges:** `mvn archetype:generate` → `uv init`; `pom.xml` → `pyproject.toml`; `~/.m2` + classpath → `.venv`; `<scope>test</scope>` → `[dependency-groups] dev`; `mvnw` pinning → `.python-version` + `uv.lock`.
- **Examples:** the student runs commands in `~/ai-engineer-course/playground/hello-uv` (gitignored); `examples/01_where_am_i.py` prints the interpreter, venv and `sys.path`.
- **Check questions:** what breaks if you commit `.venv` but not `uv.lock`? What is `sys.path` the equivalent of?
- **Task link:** every task is a uv project, and `w01-t1` is created this way.
- **Docs to verify:** uv projects guide; local `uv init` behavior on uv 0.12.24.

### d3 · ruff, VS Code, REPL, PEP 723, running pytest (`w01-py-tooling`, part 2) + names, objects and types (`w01-py-core`, part 1)
- **Objectives:** lint and format with ruff; set the VS Code interpreter; use the REPL to explore; run a single-file script with inline dependencies; run pytest. Explain names vs variables, `is` vs `==`, dynamic but strong typing, `None`, and truthiness.
- **Key points:** `ruff check --fix`, `ruff format`, rule selection in `pyproject.toml` vs Checkstyle/Spotless; Pylance and interpreter selection; `python -i`, `help()`, `dir()`; PEP 723 `uv run script.py` and `uv add --script`; `uv run pytest -q`. Then: every value is an object, names are references (diagnostic B2), `is`/`==` vs `==`/`.equals()`, `int` has no overflow, `//` floors toward −∞ (B3), truthiness table (B4).
- **Java bridges:** Checkstyle + Spotless → ruff; `jshell` → REPL; `Object` references → names; `Integer` cache surprise vs small-int caching (don't rely on `is` for values).
- **Examples:** `examples/02_ruff_demo.py` (intentionally messy file), `examples/03_names_and_objects.py`, `examples/04_numbers_truthiness.py`.
- **Check questions:** predict `[] == []` and `[] is []`; predict `-7 // 2` and `-7 % 2`; what's the truthiness of `"False"`?
- **Task link:** ruff must be clean on every task (code-quality points).

### d4 · Strings, `match`, functions (`w01-py-core`, part 2)
- **Objectives:** use f-strings and the common str methods; write `match` with patterns; design function signatures with defaults, `*args`, `**kwargs` and keyword-only parameters; avoid the mutable default trap.
- **Key points:** strings are immutable, `join` vs `StringBuilder`, f-string format specs, `match` on structure (not just values), positional-only and keyword-only parameters, defaults evaluated once (B1) and the `None` sentinel fix, functions as first-class objects, lambda limits, type hints are not enforced.
- **Java bridges:** overloading → defaults and keyword args; varargs → `*args`; builder pattern → keyword arguments; `switch` expressions → `match`.
- **Examples:** `examples/05_strings_fstrings.py`, `examples/06_match.py`, `examples/07_functions_args.py`, `examples/08_mutable_default.py`.
- **Check questions:** fix the B1 function; which call is invalid for `def f(a, /, b, *, c)`?
- **Task link:** `w01-t1`'s parser and CLI options.

### d5 · Scope, exceptions, modules (`w01-py-core`, part 3) + core collections (`w01-py-collections`, part 1)
- **Objectives:** reason about LEGB scope and closures; raise and handle exceptions idiomatically (EAFP); structure modules and imports; know `if __name__ == "__main__"`. Choose between list, tuple, dict and set.
- **Key points:** `global`/`nonlocal`, late-binding closures in loops, no checked exceptions, custom exception hierarchies, `raise ... from`, `try/except/else/finally`, context of imports (modules are singletons, import side effects, circular imports), packages and `__init__.py`. Collections: big-O of the core four, hashability, dict insertion order (B5).
- **Java bridges:** checked exceptions → documented exceptions; `throw new X(e)` → `raise X(...) from e`; static fields → module globals; `ArrayList`/`List.of`/`LinkedHashMap`/`HashSet` → list/tuple/dict/set.
- **Examples:** `examples/09_scope_closures.py`, `examples/10_exceptions.py`, `examples/11_core_collections.py`.
- **Check questions:** predict the late-binding closure loop; why is `except Exception: pass` worse in Python than in Java?
- **Task link:** `w01-t1` skips malformed lines and handles a missing file cleanly.

### d6 · Comprehensions, slicing, unpacking, iterators and generators (`w01-py-collections`, part 2)
- **Objectives:** translate stream pipelines into comprehensions and generator expressions; slice and unpack fluently; write generators with `yield` to process data lazily; explain exhaustion (B6).
- **Key points:** list/dict/set comprehensions vs `collect()`; generator expressions vs `Stream`; the iterator protocol (`__iter__`, `__next__`, `StopIteration`); `yield` and pipelines of generators over a large file; slicing with steps and negative indices; star unpacking; `enumerate`, `zip`.
- **Java bridges:** `stream().filter().map().collect()` → comprehension; `Stream` single-use → generator exhaustion; `Iterator` → iterator protocol; `IntStream.range` → `range`.
- **Examples:** `examples/12_comprehensions_vs_streams.py`, `examples/13_generators_pipeline.py` (stream a generated 200k-line log with flat memory).
- **Check questions:** B6 again with a twist; translate a `groupingBy` pipeline (B7).
- **Task link:** `w01-t1`'s streaming parser is a generator pipeline.

### d7 · itertools, collections, sorting, copying (`w01-py-collections`, part 3) + `w01-t1` kickoff
- **Objectives:** use `Counter`, `defaultdict`, `deque`, `itertools` (`islice`, `groupby`, `chain`, `batched`); sort with `key=`; tell shallow from deep copies.
- **Key points:** `Counter.most_common`, `defaultdict(list)` vs `computeIfAbsent`, `deque(maxlen=)` as a ring buffer, `sorted(key=, reverse=)` with tuple keys vs `Comparator.comparing().thenComparing()`, stable sorts, `copy.copy` vs `copy.deepcopy`, list-of-lists aliasing.
- **Java bridges:** `Collectors.counting()` → `Counter`; `Comparator` chains → key tuples; `ArrayDeque` → `deque`.
- **Examples:** `examples/14_collections_module.py`, `examples/15_sorting_copying.py`.
- **Check questions:** B7 in one line; predict `[[0]*2]*2` after one assignment.
- **Task link:** scaffold `w01-t1` log-insights, run the provided tests, and implement the parser.

## Tasks

| ID | Title | Hours | Est. API cost | Model | Weights (C/Q/D/AI) |
|:--|:--|:--|:--|:--|:--|
| `w01-t1` | log-insights: streaming access-log stats CLI | 4 (≈1 h this week, 3 h week 2 d1) | $0.00 (offline) | – | 50/30/20/0 |

## Docs verified

| Library / API | Version | Source | Date |
|:--|:--|:--|:--|
| uv | 0.12.24 installed (0.13.0 on PyPI) | [uv projects guide](https://docs.astral.sh/uv/guides/projects/), local `uv init` / `uv init --package` / `uv init --script` runs | 2026-10-11 |
| ruff | 0.17.0 | [PyPI](https://pypi.org/project/ruff/), resolved by `uv add --dev ruff` | 2026-10-11 |
| pytest | 9.1.1 | [PyPI](https://pypi.org/project/pytest/), resolved by `uv add --dev pytest` | 2026-10-11 |
| CPython | 3.13.16 (uv-managed), 3.14.8 (Homebrew default) | `uv python list --only-installed` | 2026-10-11 |
