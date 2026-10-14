# ruff, VS Code, the REPL, PEP 723 scripts and pytest

*Week 1 · day 5 · 2026-10-14 · 70 min · topic `w01-py-tooling` (part 2 of 2) · facts verified 2026-10-14 on uv 0.12.24 (0.13.1 on PyPI), ruff 0.17.0, pytest 9.1.1*

**You'll be able to:** say which Python tool replaces which Java tool; lint, auto-fix and format a project with ruff and configure its rules; point VS Code at a project's `.venv`; explore objects in the REPL; write a single-file script with its own dependencies (and lock them); run pytest.
**Builds on:** [d2: uv projects and venvs](d2-uv-projects-and-venvs.md). Practice happens in `~/ai-engineer-course/playground/hello-uv`.
**Adapted from:** the 10-14 recap quiz. The Python ↔ Java tool map (uv vs ruff) and "which interpreter runs" were missed, so section 1 restates the map and section 3 shows interpreter selection in the editor. Lock resolution was missed twice, so section 5 shows a lock for a single script.

---

## 1. Your Java toolbox, translated

| Job | Java | Python (this course) | Command |
|:--|:--|:--|:--|
| Install/pick the runtime | SDKMAN, `JAVA_HOME`, toolchains | **uv** | `uv python install 3.13`, `.python-version` |
| Build tool + dependency resolution | Maven/Gradle (+ wrapper) | **uv** | `uv add`, `uv lock`, `uv sync`, `uv run` |
| Lockfile | Gradle lockfiles (Maven: none by default) | **uv** → `uv.lock` | `uv lock --check` |
| Lint (find bugs and smells) | Checkstyle, PMD, SpotBugs, Error Prone | **ruff** | `uv run ruff check` |
| Format | Spotless, google-java-format | **ruff** | `uv run ruff format` |
| Tests | JUnit 5 + AssertJ | **pytest** | `uv run pytest` |
| Type checking | `javac` (built in) | **mypy** / Pylance (from week 2) | `uv run mypy` |
| Run a one-file program with deps | JBang (`//DEPS`) | **uv + PEP 723** | `uv run script.py` |
| Interactive shell | `jshell` | **python REPL** | `uv run python` |

Rule of thumb: **uv manages Pythons, dependencies and environments; ruff reads your code.** Both come from the same company (Astral), which is the only reason they get confused.

Where the analogy breaks: Java's compiler catches whole classes of errors (types, unused checked exceptions, missing symbols) before anything runs. Python has no compile step, so the linter and type checker are your compiler. Skipping ruff in Python is like turning off `javac` errors.

**Check:** which tool would you run to (a) pin Python 3.13 for a project, (b) catch an unused import, (c) re-wrap a 160-character line, (d) record the exact transitive versions?

## 2. ruff: lint, fix, format

**Java bridge**

```xml
<plugin><artifactId>maven-checkstyle-plugin</artifactId>
  <configuration><configLocation>checkstyle.xml</configLocation></configuration></plugin>
<plugin><groupId>com.diffplug.spotless</groupId><artifactId>spotless-maven-plugin</artifactId></plugin>
```

```toml
# pyproject.toml: the same job, one tool, one table
[tool.ruff]
line-length = 100

[tool.ruff.lint]
select = ["E", "F", "W", "I", "N", "B", "UP", "SIM", "RUF"]
```

Rule codes are families: `F` pyflakes (real bugs: unused imports, undefined names), `E`/`W` pycodestyle, `I` import sorting, `N` pep8-naming (flags camelCase Java habits), `B` bugbear (likely bugs, e.g. mutable defaults), `UP` pyupgrade (modern syntax), `SIM` simplifications, `RUF` ruff's own. **This is the exact set every course task uses**, and ruff findings cost code-quality points.

Two details that matter:
- **`select` replaces the defaults; `extend-select` adds to them.** ruff 0.17.0 (released 2026-10-09) ships a broader default set than older tutorials describe, so check what's active with `uv run ruff check --show-settings` when in doubt.
- **Fixes are safe or unsafe.** `--fix` applies only fixes that can't change behavior. `x != None` → `x is not None` is marked *unsafe*, because a class can override `__eq__` (you'll see why on Thursday with `is` vs `==`).

**Run it:** copy the messy example into `hello-uv` and lint it:

```bash
cp ~/ai-engineer-course/.claude/worktrees/uv-section-4-c0d0e3/lessons/week-01/examples/02_ruff_demo.py ~/ai-engineer-course/playground/hello-uv/src/hello_uv/messy.py
cd ~/ai-engineer-course/playground/hello-uv && uv run ruff check --statistics
```

Then add the `[tool.ruff]` tables above to `hello-uv/pyproject.toml`, and run `uv run ruff check --statistics` again, then `uv run ruff check --fix`, then `uv run ruff format`, then `uv run ruff check` once more.

Look for: the count going up when you select the course rules (N, E7xx and E501 appear), `--fix` removing the mechanical problems (unused imports, `List` → `list`, `Optional[X]` → `X | None`, import order), `ruff format` re-wrapping the long line and adding the blank line between methods, and **what's left**: the findings that need a human (naming, bare `except`, the mutable default, `== None`, `== True`, an unused variable).

**Try it (5 min):** fix the remaining findings by hand. Rename to `parse_status_codes`, `LogSummary`, `error_count`; replace `except:` with `except (IndexError, ValueError):`; delete `seen=[]` and `tmp`. Run `uv run ruff check` until it says `All checks passed!`.

**Check:** ruff can auto-fix an unused import but refuses to auto-fix `except:`. Why is the second one a human decision?

## 3. VS Code: trust, interpreter, format on save

1. **Trust the folder.** Restricted Mode (Workspace Trust) disables the Python and Pylance extensions, so nothing below works until you trust it (banner → **Manage** → **Trust**).
2. **Pick the interpreter**: `Cmd+Shift+P` → **Python: Select Interpreter** → `./.venv/bin/python` (VS Code usually suggests it once the folder is trusted). The status bar shows the active one. This is the editor's version of "which Python runs": a wrong pick gives red squiggles under `import httpx` even though `uv run` works. That's section 4 of d2, inside the editor.
3. **Ruff on save** (the `charliermarsh.ruff` extension is already installed). In user settings JSON:

```json
"[python]": {
  "editor.defaultFormatter": "charliermarsh.ruff",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll": "explicit",
    "source.organizeImports": "explicit"
  }
}
```

**Java bridge:** this is IntelliJ's Project SDK plus "Reformat code" and "Optimize imports" on save.

**Try it (3 min):** open `messy.py` (or a fresh copy), add `import os` at the top, and save. It should vanish.

**Check:** `uv run hello-uv` works, but VS Code underlines `import httpx` in red. What's the first thing you check?

## 4. The REPL: your `jshell`

```bash
cd ~/ai-engineer-course/playground/hello-uv && uv run python
```

Python 3.13's REPL has colors, multi-line editing and history, and `exit` works without parentheses. Use it to explore, not to write programs:

```python
>>> from hello_uv.stats import mean
>>> mean([1, 2, 3, 4])
>>> type(mean)
>>> dir("abc")[-10:]        # what can a str do? (like IntelliJ's completion list)
>>> help(str.split)         # the docstring; q to quit
>>> import httpx; httpx.__file__   # where did this module come from?
```

`uv run python -i some_script.py` runs a script and then drops you into the REPL with its variables still live, which is handy for poking at a parser's output.

**Java bridge:** `jshell`, but with every library in the project's `.venv` importable and with `help()` and `dir()` instead of opening the Javadoc.

**Try it (3 min):** predict `type(mean([2, 4]))` before you press Enter.

**Check:** `httpx.__file__` printed a path. Inside which folder, and why does that prove `uv run python` used the project's environment?

## 5. PEP 723: single-file scripts with their own dependencies

**Java bridge**

```java
///usr/bin/env jbang "$0" "$@" ; exit $?
//DEPS com.squareup.okhttp3:okhttp:4.12.0
```

```python
# /// script
# requires-python = ">=3.13"
# dependencies = ["httpx>=0.28.1"]
# ///
```

The comment block at the top is **inline metadata** (PEP 723). `uv run script.py` reads it, builds (and caches) a throwaway environment with those dependencies, and runs the script. That's the `~/.cache/uv/environments-v2/...` env you saw in d2's Run A. No project, no `pyproject.toml`.

```bash
uv init --script status.py --python 3.13    # creates the file with the header
uv add --script status.py httpx             # edits the header, not a pyproject
uv run status.py                            # builds the cached env, runs it
uv lock --script status.py                  # writes status.py.lock next to it
```

Lock resolution works exactly as it does for projects: `httpx>=0.28.1` is a **floor**, so without a lock each fresh environment gets the newest httpx that satisfies it. `uv lock --script` pins the exact tree in `status.py.lock`. Once that file exists, `uv run` and `uv add --script` reuse it and keep it updated.

**Run it:** in `~/ai-engineer-course/playground/`, create `status.py` with the commands above, then replace its `main()` with a call to a public endpoint, for example `httpx.get("https://httpbin.org/status/418")`, and print the status code.

**Try it (3 min):** before running `uv lock --script`, predict whether `status.py.lock` already exists after `uv add --script`. Then check with `ls`.

**Check:** a script header says `dependencies = ["httpx>=0.28.1"]` and there is no lock file. You run it today, and a teammate runs it in three months. Can you get different httpx versions? What one command stops that?

## 6. pytest: a first run (full lesson in week 2)

```java
@Test void meanOfFour() { assertEquals(2.5, Stats.mean(List.of(1, 2, 3, 4)), 1e-9); }
```

```python
# tests/test_stats.py
from hello_uv.stats import mean


def test_mean_of_four():
    assert mean([1, 2, 3, 4]) == 2.5
```

- No class, no annotations: pytest collects `test_*.py` files and `test_*` functions.
- A plain `assert`. pytest rewrites it so a failure shows both sides (`assert 2.0 == 2.5`), with no `assertEquals` needed.
- `uv run pytest -q` uses the project's `.venv`, where pytest is a dev dependency.

**Try it (5 min):** create `tests/test_stats.py` in `hello-uv`, run `uv run pytest -q`, then add `test_mean_of_empty` that calls `mean([])`. Predict what happens before running (diagnostic B3's cousin: what does `0 / 0` do in Python?).

**Check:** in JUnit a test class needs `@Test` on each method. What makes pytest decide a function is a test?

---

## Pitfalls for Java developers

- **Treating ruff as optional.** With no compiler, ruff and the type checker are your first line of defense; every task is graded ruff-clean.
- **Expecting `select` to add rules.** It replaces the active set; use `extend-select` to add.
- **Running `--unsafe-fixes` blindly.** Unsafe fixes can change behavior; read the diff first.
- **Fighting the formatter.** Like Spotless, don't hand-format and don't argue with it; let `ruff format` own whitespace.
- **The wrong interpreter in VS Code**: red squiggles for installed packages. Select `.venv/bin/python`.
- **Copying PEP 723 scripts around without a lock** and expecting identical behavior later.
- **Naming test files `stats_test.py`** (JUnit-style `*Test`): pytest's default pattern is `test_*.py` or `*_test.py`, but stick to `test_*.py` as the course does.

## Summary

- uv = runtimes + dependencies + environments (SDKMAN + Maven); ruff = lint + format (Checkstyle + Spotless); pytest = JUnit.
- ruff config lives in `pyproject.toml`; `select` replaces defaults; `--fix` applies only safe fixes; `ruff format` owns whitespace.
- VS Code must trust the folder and use `.venv/bin/python`, or it disagrees with `uv run`.
- The REPL (`uv run python`, `help`, `dir`, `type`, `-i`) is for exploring objects in the project's environment.
- PEP 723 headers + `uv run` = JBang for Python; `uv lock --script` pins a script the way `uv.lock` pins a project.

## Docs

- [ruff: configuring Ruff](https://docs.astral.sh/ruff/configuration/) and [rules](https://docs.astral.sh/ruff/rules/) (verified 2026-10-14, ruff 0.17.0; default rule set changed in 0.17.0 per the [changelog](https://github.com/astral-sh/ruff/blob/main/CHANGELOG.md))
- [ruff VS Code extension: format and fix on save](https://github.com/astral-sh/ruff-vscode#configuring-vs-code) (verified 2026-10-14)
- [uv: running scripts](https://docs.astral.sh/uv/guides/scripts/) (`uv init/add/lock --script` verified locally on uv 0.12.24, 2026-10-14)
- [PEP 723: inline script metadata](https://peps.python.org/pep-0723/)
- [pytest: get started](https://docs.pytest.org/en/stable/getting-started.html) (pytest 9.1.1)
- [VS Code: Python environments](https://code.visualstudio.com/docs/python/environments)
