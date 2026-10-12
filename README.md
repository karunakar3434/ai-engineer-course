# AI Engineer Course

A 14-week, hands-on path from experienced Java backend developer to applied AI Engineer: building production LLM applications with the Claude API, RAG, agents, MCP, evals and deployment. Every topic ends in a tested mini-project, graded out of 100 against a fixed rubric.

**Dates:** 2026-10-10 → 2027-01-15 · **Pace:** ~18 h/week · **Pass mark:** 70/100

## What's here

| Path | Contents |
|---|---|
| [`syllabus.md`](syllabus.md) | Week-by-week plan, written after the diagnostic and adjusted as the course goes |
| [`lessons/`](lessons/) | Weekly plans and lessons, with runnable examples |
| [`tasks/`](tasks/) | One project per task: spec, code and tests |
| [`revision/`](revision/), [`pdfs/`](pdfs/) | Revision notes per topic as Markdown and PDF, plus a combined course PDF |
| [`tools/`](tools/) | Course calendar, PDF builder, API spend report |
| `private/` | Not published: a separate private repo with the course state (progress, scores, diagnostic, grading reports). Gitignored here |

## Progress

| Week | Focus | Tasks passed |
|---|---|---|
| 1–3 | Python for Java developers: tooling, core, testing, async, FastAPI, data access | – |
| 4–5 | LLM fundamentals, Claude API, prompting, structured output, tool use | – |
| 6–7 | Embeddings, vector databases, RAG, retrieval evals | – |
| 8–9 | Agents by hand, MCP, Claude Agent SDK | – |
| 10 | Evals, observability, guardrails, prompt-injection defense | – |
| 11 | Docker, streaming, prompt caching, cost and latency, open-weight models | – |
| 12–13 | Capstone | – |
| 14 | Portfolio and interview prep | – |

## Setup

```bash
brew install uv pandoc typst      # Python toolchain and PDF tooling
git config core.hooksPath .githooks   # blocks commits containing API keys or private/
git clone git@github.com:karunakar3434/ai-engineer-course-private.git private   # course state (private repo)
git -C private config core.hooksPath ../.githooks
cp .env.example .env              # add keys from week 3; .env is gitignored
```

Each course session runs in its own git worktree and reaches `private/` through a link to the main checkout. To let sessions write it without permission prompts, add the main checkout's `private/` folder to `permissions.additionalDirectories` in `~/.claude/settings.json`.

- Tasks: `cd tasks/<task> && uv run pytest`
- Paid API tests: `uv run --env-file ../../.env pytest --live`
- Revision PDFs: `python3 tools/build_pdf.py --all --combined`

## How it's run

Study sessions run in Claude Code through a personal `/ai-coach` skill. It plans each week from the previous week's results, teaches with Java-to-Python comparisons, writes each task's spec and test suite before the work starts, and keeps the course state in `private/progress.json` current. Submissions are graded by a separate read-only grader subagent: provided tests, its own edge-case checks, a code review, and a score out of 100 (correctness, code quality and Pythonic style, design and efficiency, AI-specific quality), with hints first and a reference solution only after a pass.

API usage runs on a capped Claude Console key (the cheapest Haiku model by default, $20/month limit), with per-call token and cost logging.

### Claude agents & skills

The skill and subagent that run the course live only in this repo's `.claude/`, so they load when Claude Code is opened in `~/ai-engineer-course`. Don't add copies under `~/.claude/skills` or `~/.claude/agents`: a personal skill with the same name overrides the project's, so a stray `~/.claude/skills/ai-coach` would silently replace the committed coach.

| Name | Type | What it does |
|---|---|---|
| `ai-coach` | skill (`.claude/skills/ai-coach/`) | Runs study sessions, writes lessons and task specs, keeps `private/progress.json` current |
| `ai-coach-grader` | subagent (`.claude/agents/ai-coach-grader.md`) | Grades `submit <task-id>` read-only — provided tests, its own edge-case checks, code review, score out of 100 |

The grader's read-only guard (`.claude/skills/ai-coach/scripts/grader_bash_guard.py`) runs from this repo. If the file is missing, `python3` exits with status 2, which Claude Code treats as a block, so grader Bash commands fail closed rather than run unguarded.

## License

MIT. See [LICENSE](LICENSE).
