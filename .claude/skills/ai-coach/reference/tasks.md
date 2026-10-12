# Tasks: scaffolding, tests, submission and grading

Every topic ends with a hands-on task. The coach writes the README and the test suite **before** the student starts, and the `ai-coach-grader` subagent grades submissions.

## IDs and layout

Task ID `wNN-tK` (capstone `c-mK`); folder `tasks/<id>-<slug>/`, e.g. `tasks/w01-t1-log-insights/`. Each task is its own uv project:

```
tasks/w01-t1-log-insights/
├── README.md            # the spec (template: templates/task-README.md)
├── pyproject.toml       # uv project, pytest/ruff/mypy config
├── uv.lock
├── src/log_insights/    # starter stubs: signatures, docstrings, raise NotImplementedError
└── tests/               # provided suite; the student must not edit it (they may add files)
    ├── conftest.py      # from templates/conftest.py (--live / --agent-sdk switches)
    └── test_*.py
```

Grader reports carry scores and reference solutions are coach-written, so both live in the private repo (SKILL.md rule 11):

```
private/tasks/w01-t1-log-insights/
├── attempts/            # attempt-1.md, attempt-2.md: grader reports, written by the coach
└── reference/           # reference solution, only after a pass or an explicit request
```

## Scaffolding a task

1. **Spec.** Write `README.md` from the template. Make requirements precise and testable, because the grader treats a clearly broken requirement as a failed gate. The template contains: goal, context (why this matters in real AI-engineering work), requirements, acceptance criteria (numbered; each maps to tests), constraints, out of scope, time estimate, **estimated API cost with the arithmetic** (see models-and-costs.md), the model and why, grading weights, how to run tests, and how to submit. Say that the grader runs extra edge-case checks beyond the provided tests.
2. **Project.** `uv init --lib --name <package> --python 3.13 tasks/<dir>`. Replace the generated README. Then `uv add --dev pytest` (plus `pytest-asyncio`, `respx` and so on as needed) and runtime deps in the task dir. Append this config to `pyproject.toml`:

   ```toml
   [tool.pytest.ini_options]
   testpaths = ["tests"]
   addopts = "-ra --strict-markers"

   [tool.ruff]
   line-length = 100

   [tool.ruff.lint]
   select = ["E", "F", "W", "I", "N", "B", "UP", "SIM", "RUF"]   # N = pep8-naming: flags camelCase Java habits

   [tool.mypy]          # from week 2 on
   strict = true
   ```
3. **Starter code.** Weeks 1–4: signatures with type hints and docstrings, bodies `raise NotImplementedError`. From week 5 on, give less scaffolding: interfaces only, and the student designs the internals. Capstone: no starter code.
4. **Tests.** Write the provided suite following the rules below. Copy `templates/conftest.py` into `tests/conftest.py`.
5. **Validate the suite.** Copy the task folder to `$TMPDIR/ai-coach-ref/<id>/`, write a quick reference implementation there, and run the tests until they pass. Fix any test that is wrong or flaky. Then delete that copy. The student never sees it. Back in the real task dir, `uv run pytest -q` must collect cleanly and fail (red) on the stubs.
6. **Record and commit.** Commit the task dir as `task(<id>): scaffold` and note the SHA. Add `tasks[id]` to `private/progress.json` (see the schema) with that SHA as `scaffold_commit`, then commit `private/` with the same message.
7. Walk the student through the README in 2–3 minutes: what done looks like, and the first step.

## Test design rules

- Tests are the acceptance criteria. Name them as specs (`test_counts_status_codes_across_multiple_files`), and add a comment with the criterion number.
- **Offline by default.** The student's code must accept its LLM client, HTTP client, clock and config as parameters or FastAPI dependencies. Tests pass fakes. For SDK-level behavior, mock HTTP with `respx` (the anthropic SDK uses httpx) and return realistic JSON bodies, including `usage`, `stop_reason: "max_tokens"`, `"refusal"`, 429 and 529 errors. Check SDK response shapes against the installed version.
- **Paid tests** are marked `@pytest.mark.live`, run only with `--live`, use the cheapest Haiku, small inputs and `max_tokens`, and print usage. The README gives their cost. Evals that hit the API are live tests with explicit thresholds.
- **Agent SDK tests** are marked `@pytest.mark.agent_sdk`, run only with `--agent-sdk`, and refuse to run while `ANTHROPIC_API_KEY` is set. Use few turns and tiny prompts.
- Deterministic: no real network, no wall-clock dependence (inject a clock), `tmp_path` for files, fixed seeds.
- Cover the happy path, boundaries, error paths, and for LLM code: malformed model output, `max_tokens` truncation, refusals, rate limits and retries, cost and token guards. Leave a few obvious edge cases untested; the grader checks those.
- Keep the suite fast: under 10 s offline.

## Grading weights

Default 40/20/20/20 = correctness / code quality and Pythonic style / design and efficiency / AI-specific quality. Weights per task are in curriculum.md; set them in the README and in `tasks[id].weights`. Rough guide:

| Kind of task | Weights |
|---|---|
| Pure Python (weeks 1–2) | 50/30/20/0 (FastAPI service: 45/25/30/0) |
| Standard LLM feature | 40/20/20/20 |
| Eval- or prompt-heavy | 35/15/20/30 |
| Security/evals (week 9) | 30/15/20/35 |
| Capstone milestones | see curriculum.md |

## Submitting and grading

On `submit <id>`:

1. Read `tasks[id]`; `n = len(attempts) + 1`.
2. In the task dir: `uv lock --check`. If the lock is stale, run `uv lock` and say so ("next time use `uv add`; it updates the lock").
3. If the README lists live tests or evals, ask: "Include live tests? Estimated $X." Record the answer. For Agent SDK tests, ask the same way (they use Max limits, not money).
4. `git add tasks/<dir> && git commit -m "submit(<id>): attempt <n>"`, and record the SHA.
5. Call the Agent tool with `subagent_type: "ai-coach-grader"` and `description: "Grade <id> attempt <n>"`, using exactly this prompt (filled in, no commentary on the code):

   ```
   Grade task <id>, attempt <n>.
   Course root: <absolute path of the session worktree root: git rev-parse --show-toplevel>
   Task dir: tasks/<dir>
   Submission commit: <sha>
   Scaffold commit: <scaffold_commit>
   Pass mark: <course.pass_mark>
   Weights: correctness <a>, code_quality <b>, design <c>, ai_quality <d>
   Live tests: <not approved | approved, budget $<x>, command: <from README>>
   Agent SDK tests: <not approved | approved>
   Reference solution: <include only if the attempt passes | student requested it: include regardless>
   Previous attempt reports: <paths, or none>
   Course week: <N> (the student is a Java developer, <weeks of Python so far> weeks into Python)
   ```
6. The grader's reply ends with a `json` block. If it's missing or invalid, ask the same grader to resend only the JSON (SendMessage to its agent ID, if that tool is available; otherwise re-run it with a note saying the JSON block was missing). If `status` is `"blocked"`, fix the environment issue it names (usually the lockfile) and re-run the grader; don't count a blocked run as an attempt.
7. Write the full report to `private/tasks/<dir>/attempts/attempt-<n>.md`, with a header line: date, commit, score, live run yes/no.
8. Update `private/progress.json`: append to `tasks[id].attempts` (`n`, `date`, `commit`, `score`, `breakdown`, `passed`, `gates`, `live_run`, `live_cost_usd`, `report`); set `status` to `"passed"` or `"needs_fix"`; set `best_score`; merge the grader's `weak_areas` (with evidence `"<id> attempt <n>"`); add any live cost to `api_spend`.
9. If the report contains a reference solution, write each file to `private/tasks/<dir>/reference/<path>` and set `reference_released: true`.
10. Show the student the report's score table, gates, hints and optimizations, unedited and unsoftened. If they passed, offer to compare their solution with the reference. If they failed, list the top three things to fix (from the report) and offer `hint <id>`.
11. Commit in `private/` only, since the message carries the score: `git -C private add -A && git -C private commit -m "grade(<id>): attempt <n>, <score>/100"`.

A request for the reference solution before passing ("show me the solution for w04-t1") is allowed: confirm once ("this ends hint-based learning for this task; you can still submit for a score"), then run the grader with "student requested it", or write a reference yourself if no grading is needed, and record `reference_released`.

## Late or abandoned tasks

If a re-plan cuts or shrinks a task, mark it `"status": "deferred"` or `"descoped"` with the reason. Never delete attempts.
