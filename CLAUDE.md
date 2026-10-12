# AI Engineer course repo

A 14-week applied AI Engineer course, run by the project-level `/ai-coach` skill (`.claude/skills/ai-coach/`) and graded by the project-level `ai-coach-grader` subagent (`.claude/agents/`). Edit only these copies; there are no user-level copies in `~/.claude`. `private/progress.json` holds all course state; `syllabus.md` holds the plan.

- Python 3.13 with uv. Each task in `tasks/<id>-<slug>/` is its own uv project (src layout, pytest, ruff). Run tests from the task dir with `uv run pytest`.
- This repo is public on GitHub. `private/` is gitignored and is its own private repo (progress, diagnostic, grading reports, reference solutions). Scores, diagnostic or quiz answers, session notes, study times and job details never go in public files or public commit messages.
- Course sessions run in one worktree per session and merge to `main` through a PR with a merge commit, never squash: `private/progress.json` records commit SHAs the grader needs later. Worktrees have no `private/`; link it with `ln -s "$HOME/ai-engineer-course/private" private`.
- Never read, print or commit `.env`. Keys load per process (`uv run --env-file .env …`), never from shell exports.
- Exercise code defaults to the cheapest current Claude Haiku model. Check the current model ID and prices in the official docs rather than from memory.
- Tests that call paid APIs are marked `live` and need `--live`. Agent SDK tests are marked `agent_sdk`, need `--agent-sdk`, and must run with `ANTHROPIC_API_KEY` unset (Max login).
- Don't edit a task's provided tests (`tests/` files from the scaffold commit). Add new test files instead.
- Helpers: `python3 tools/course_calendar.py`, `python3 tools/build_pdf.py`, `python3 tools/spend.py`.
