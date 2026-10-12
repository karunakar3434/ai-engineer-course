# uv projects, pyproject.toml and virtual environments

*Week 1 · day 2 · 2026-10-11 · 75 min · topic `w01-py-tooling` (part 1 of 2) · facts verified 2026-10-11 on uv 0.12.24*

**You'll be able to:** create a uv project and explain every generated file next to its Maven counterpart; add runtime and dev dependencies; explain what `uv.lock` and `.venv` are for; run code and tools with `uv run`.
**Builds on:** your Maven/Gradle and Spring Boot experience. Part 2 (Mon) covers ruff, VS Code, the REPL, PEP 723 scripts and pytest.

---

## 1. Many Pythons on one Mac, like many JDKs

**Java bridge**

```bash
# Java: several JDKs installed, one picked per project
/usr/libexec/java_home -V          # list JDKs
sdk use java 21-tem                 # or JAVA_HOME / toolchains / mvnw
```

```bash
# Python: several interpreters installed, one picked per project
uv python list --only-installed     # list interpreters uv can see
cat .python-version                 # the project's pin (like a toolchain)
```

Where the analogy breaks: in Java, the JDK version and the libraries on your classpath are separate concerns. In Python, **packages are installed into a specific interpreter's environment**, so "which python" decides which libraries exist.

Your Mac currently has 3.14 (Homebrew, the default `python3`), 3.13 (uv-managed) and two 3.11 installs. The course uses **3.13**, pinned per project.

**Run it:** `uv python list --only-installed`. Look for which install each path comes from (Homebrew, `~/.local/share/uv`, `/usr/local`).

**Check:** if you type `python3` in a new terminal, which version runs, and why does that make bare `python3` a bad way to run project code?

## 2. `uv init`: the project skeleton

**Java bridge**

```bash
mvn archetype:generate -DgroupId=com.acme -DartifactId=hello -DarchetypeArtifactId=maven-archetype-quickstart
```

```bash
uv init --package --python 3.13 hello-uv
```

| Generated | What it is | Maven counterpart |
|:--|:--|:--|
| `pyproject.toml` | Project metadata, dependencies, tool config (ruff, pytest) | `pom.xml` |
| `.python-version` | Interpreter pin (`3.13`) | `maven.compiler.release` + toolchain |
| `src/hello_uv/__init__.py` | The package; the folder makes `hello_uv` importable | `src/main/java/com/acme/hello/` |
| `README.md`, `.gitignore`, `.git/` | As you'd expect | same |
| `uv.lock` *(after the first `uv add`/`uv run`)* | Exact resolved versions + hashes of every transitive dependency | no default equivalent (closest: dependency lock plugins, Gradle lockfiles) |
| `.venv/` *(after the first `uv run`/`uv sync`)* | The project's private interpreter + installed packages | your classpath + `~/.m2` cache, combined, per project |

Note the naming: the project is `hello-uv` (dashes, like an artifactId), but the importable package is `hello_uv` (underscores; a dash isn't valid in a Python identifier).

The generated `pyproject.toml` (abridged):

```toml
[project]
name = "hello-uv"
version = "0.1.0"
requires-python = ">=3.13"
dependencies = []                  # like <dependencies> with compile scope

[project.scripts]
hello-uv = "hello_uv:main"         # like Main-Class: a command that calls hello_uv.main()

[build-system]                     # how to package it (like maven-jar-plugin)
requires = ["uv_build>=0.12.24,<0.13.0"]
build-backend = "uv_build"
```

**Run it:**

```bash
mkdir -p ~/ai-engineer-course/playground && cd ~/ai-engineer-course/playground
uv init --package --python 3.13 hello-uv
cd hello-uv && ls -a && cat pyproject.toml .python-version
uv run hello-uv
```

Look for: `.venv` appearing only **after** `uv run`, and the `Hello from hello-uv!` line.

**Try it (3 min):** open `src/hello_uv/__init__.py`, change the message, and predict whether you need a "rebuild" step before `uv run hello-uv` shows it. (Answer: no. The project is installed in *editable* mode, so the venv points at your source, like running from `target/classes` with hot reload.)

**Check:** why is `--python 3.13` worth passing? (Without it, uv picked the Homebrew 3.14 here and wrote `requires-python = ">=3.14"`.)

## 3. Dependencies: `uv add`, dev groups and `uv.lock`

**Java bridge**

```xml
<dependency>
  <groupId>com.squareup.okhttp3</groupId><artifactId>okhttp</artifactId><version>4.12.0</version>
</dependency>
<dependency>
  <groupId>org.junit.jupiter</groupId><artifactId>junit-jupiter</artifactId><version>5.11.0</version>
  <scope>test</scope>
</dependency>
```

```bash
uv add httpx                 # runtime dependency → [project] dependencies
uv add --dev pytest ruff     # dev-only → [dependency-groups] dev (like <scope>test</scope>)
uv remove httpx
```

Result in `pyproject.toml`:

```toml
dependencies = ["httpx>=0.28.1"]

[dependency-groups]
dev = ["pytest>=9.1.1", "ruff>=0.17.0"]
```

Where the analogy breaks: Maven pins **exact** versions in the POM, and transitive versions come from "nearest wins" mediation, re-resolved on each machine. Python projects write **ranges** in `pyproject.toml` (`>=0.28.1`) and record the exact resolution, including every transitive package and its hash, in **`uv.lock`**. Commit `uv.lock`; never edit it by hand. Everyone, including CI and the grader, then gets byte-identical environments.

| Command | Does | Java-ish |
|:--|:--|:--|
| `uv lock` | Resolve ranges → write `uv.lock` | `mvn dependency:resolve` + a lockfile |
| `uv sync` | Make `.venv` match `uv.lock` exactly (installs and removes) | `mvn dependency:go-offline`, but exact |
| `uv run <cmd>` | Lock + sync if needed, then run inside `.venv` | `mvn exec:java`, but always in sync |
| `uv lock --check` | Fail if `uv.lock` is stale (CI and pre-submit check) | `mvn enforcer` |
| `uv lock --upgrade-package httpx` | Bump one package | `versions:use-latest-versions` for one artifact |

**Run it:** in `hello-uv`, `uv add httpx` and then `uv add --dev pytest ruff`. Then `git diff pyproject.toml` and `grep -c '^\[\[package\]\]' uv.lock`. Look for: three direct dependencies in `pyproject.toml`, but many more packages in the lockfile (the transitive tree).

**Check:** a teammate clones your repo with `pyproject.toml` but you forgot to commit `uv.lock`. What could differ on their machine?

## 4. `.venv` vs the classpath, and why you always `uv run`

**Java bridge**

```bash
java -cp target/classes:~/.m2/repository/.../okhttp-4.12.0.jar:... com.acme.Main
```

```bash
uv run python -m hello_uv     # or: uv run hello-uv
```

A **virtual environment** is a directory (`.venv/`) with a small interpreter shim plus its own `site-packages/`, where the project's packages are installed. Python finds modules by walking **`sys.path`** in order, which is the classpath equivalent. `uv run` executes your command with `.venv`'s interpreter, so `sys.path` contains *this project's* packages and nothing from other projects.

The trap for Java developers: there's no `-cp` flag per run. If you run plain `python3 main.py`, you get the global Homebrew interpreter and its packages, not your project's. That's the classic `ModuleNotFoundError: No module named 'httpx'` even though you "installed it".

**Run it:**

```bash
cd ~/ai-engineer-course
uv run lessons/week-01/examples/01_where_am_i.py
cd playground/hello-uv && uv run python ../../lessons/week-01/examples/01_where_am_i.py
```

Look for: `Environment` and `site-packages` pointing at a uv **cache** env for the standalone script (it has its own inline dependency list; more on that Monday) vs `playground/hello-uv/.venv` for the project run. Also check which Python version each one used.

**Try it (3 min):** in `hello-uv`, run `python3 -c "import httpx"` and then `uv run python -c "import httpx; print(httpx.__version__)"`. Predict both results first.

**Check:** what is `sys.path` the equivalent of, and what decides its contents?

## 5. The src layout and entry points

```
hello-uv/
├── pyproject.toml
├── src/
│   └── hello_uv/          ← package (like com/acme/hello)
│       ├── __init__.py    ← runs on `import hello_uv`; holds main() here
│       └── stats.py       ← module: `from hello_uv.stats import mean`
└── tests/
    └── test_stats.py      ← pytest finds test_*.py files
```

- **A module is one `.py` file; a package is a folder of modules.** No class-per-file rule: a module can hold many functions and classes, like a Kotlin file more than a Java class.
- **Why `src/`:** tests import the *installed* package rather than whatever happens to be in the current directory, which catches packaging mistakes early. This is the same reason Maven separates `src/main` from `src/test`.
- **Entry points:** `[project.scripts] hello-uv = "hello_uv:main"` creates a `hello-uv` command in `.venv/bin`. `uv run python -m hello_uv` runs `hello_uv/__main__.py` if it exists, like `java -m`.

**Try it (5 min):** create `src/hello_uv/stats.py` with `def mean(xs): return sum(xs) / len(xs)`. Then, from `__init__.py`'s `main()`, import it and print `mean([1, 2, 3, 4])`. Predict the output type. (It's `2.5`, a float, because `/` is true division; diagnostic B3.)

**Check:** why is the project folder `hello-uv` but the import `hello_uv`?

---

## Pitfalls for Java developers

- **Running bare `python3`**: you get the wrong interpreter and no project packages → `ModuleNotFoundError`. Fix: `uv run …`.
- **`pip install` into the global Python**: this pollutes Homebrew's Python (and modern Homebrew Python refuses with "externally-managed-environment"). Fix: `uv add`.
- **Not committing `uv.lock`**: you get non-reproducible builds. Fix: commit it, and check with `uv lock --check`.
- **Committing `.venv`**: it's machine-specific and huge, like committing `~/.m2`. It's already gitignored.
- **Dashes in import names**: `import hello-uv` is a syntax error; use `hello_uv`.
- **Activating venvs manually and forgetting**: `source .venv/bin/activate` works, but `uv run` is explicit and can't go stale.

## Summary

- Each project pins its interpreter (`.python-version`) and gets a private `.venv`; packages live *inside* an interpreter's environment.
- `pyproject.toml` ≈ `pom.xml` with version ranges; `uv.lock` records the exact resolved tree, so commit it.
- `uv add` / `uv add --dev` ≈ compile vs test scope (`[dependency-groups] dev`).
- `sys.path` ≈ the classpath, and `uv run` guarantees it's this project's, in sync with the lock.
- Use the src layout, packages are folders, and `[project.scripts]` ≈ `Main-Class`.

## Docs

- [uv: working on projects](https://docs.astral.sh/uv/guides/projects/) (verified 2026-10-11)
- [uv: managing dependencies](https://docs.astral.sh/uv/concepts/projects/dependencies/) (verified 2026-10-11)
- [Python Packaging User Guide: writing pyproject.toml](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/)
