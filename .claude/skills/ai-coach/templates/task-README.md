# {{task-id}}: {{Title}}

*Week {{N}} · topics {{topic-ids}} · estimated {{h}} h · estimated API cost {{$x.xx}} · pass mark 70/100*

## Goal

{{One paragraph: what you build and the real-world AI-engineering skill it trains.}}

## Context

{{Why this matters in production; where you'd meet it at work. A Java parallel if useful.}}

## Requirements

1. {{Functional requirement}}
2. {{…}}

### Constraints

- Python 3.13, managed with uv. Type hints everywhere{{; mypy --strict clean (week 2+)}}.
- {{Inject dependencies (LLM client, HTTP client, clock, config) so tests can pass fakes.}}
- {{Model: `claude-haiku-…` (cheapest current). Reason if different: …}}
- No API keys in code. Load them from `.env` (see the repo's `.env.example`).

### Out of scope

- {{what not to build}}

## Acceptance criteria

| # | Criterion | Checked by |
|:--|:--|:--|
| AC1 | {{observable behavior}} | `tests/test_{{x}}.py::test_{{y}}` |
| AC2 | | |

The grader also runs its own edge-case checks beyond these tests (boundaries, errors, malformed model output and similar), so think about those too.

## Estimated API cost

{{"$0.00: offline; tests use fakes." or the arithmetic: calls × (in tokens × price + out tokens × price) / 1M × 2 margin = $x.xx, at prices verified YYYY-MM-DD.}}

## Grading (out of 100)

| Category | Weight | What earns it |
|:--|:--|:--|
| Correctness | {{40}} | Provided tests pass, edge cases handled, requirements met |
| Code quality and Pythonic style | {{20}} | Idiomatic, typed, readable, ruff-clean; no Java-isms |
| Design and efficiency | {{20}} | Clear structure, testable seams, sensible complexity, no wasted work or calls |
| AI-specific quality | {{20}} | Prompt design, output validation, stop-reason/error handling, token and cost control, eval results |

Gates (needed to pass regardless of total): all provided offline tests pass, provided tests unmodified, no secrets committed, and no requirement above clearly broken.

## Run

```bash
cd tasks/{{dir}}
uv run pytest -q                                   # offline suite (free)
uv run --env-file ../../.env pytest -q --live      # paid tests, ≈ {{$x.xx}} (only if listed above)
uvx ruff check . && uvx ruff format --check .
```

## Submit

Commit-ready code in `src/`, then tell the coach `submit {{task-id}}`. Stuck? `hint {{task-id}}`.
