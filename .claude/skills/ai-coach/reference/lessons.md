# Week plans, lessons and teaching style

## Week plan: `lessons/week-NN/README.md`

Written at the first session of the week (template: `templates/week-plan.md`). It is the contract for the week: detailed enough that each session's full lesson can be written from it in a few minutes, and adapted from the previous week's evidence. It contains:

- Weekly goal (one sentence: what the student can build by Friday) and 3–5 success criteria.
- **Adaptations** from last week, each with its source but no scores ("w02-t2 attempt 1: coupling → DI exercise added on day 2").
- A day-by-day table: course day, date, weekday, hours, topic IDs, agenda in minutes. The total must match the calendar's `remaining_by_week` hours for the week, minus about 1 h slack.
- A **detailed outline per session**: objectives (2–4, phrased as "can do"), key points in teaching order, Java bridges, the examples to write (filenames), 2–3 check questions, which task it feeds, and the docs to verify.
- Tasks this week: ID, title, hours, estimated API cost, model, weights.
- Docs verified: library or API, version, URL, date.
- No retro section: the retro holds scores, so it goes in the week's `weeks` entry in `private/progress.json`.

## Lesson file: `lessons/week-NN/dD-<slug>.md`

Written at the start of the session it's taught in (template: `templates/lesson.md`):

1. Header: week, course day, date, time budget, objectives, prerequisites, "verified YYYY-MM-DD" for fast-moving facts.
2. Sections in teaching order. Each section has:
   - **Java bridge**: the Java the student would write, next to the idiomatic Python, plus where the analogy breaks.
   - The idea, explained concisely and concretely. Show, don't lecture.
   - **Run it**: a runnable example (`uv run lessons/week-NN/examples/NN_slug.py`) and what to look for in the output.
   - **Try it** (2–5 min): a small change for the student to make and predict.
   - **Check**: one question to confirm understanding.
3. Pitfalls (the ones Java developers hit).
4. Summary in 5 bullets, and the docs links.

Depth calibration: skip anything a senior Java engineer already knows (what a loop is, what an interface is for, HTTP basics, SQL). Spend the time on differences, idioms, failure modes and production concerns. For ML/LLM theory, give intuition plus the one formula that matters (for example, cosine similarity), never derivations, unless the student asks.

## Examples: `lessons/week-NN/examples/`

- Self-contained `NN_slug.py` files with PEP 723 inline metadata so `uv run <file>` just works:

  ```python
  # /// script
  # requires-python = ">=3.13"
  # dependencies = ["anthropic>=<verified version>"]
  # ///
  ```
- Each one prints something meaningful and finishes in seconds. No hidden setup.
- Run every free example yourself before presenting it. Never run paid examples yourself without the student's yes (rule 7); usually the student runs them.
- Examples that call the Claude API use the cheapest current Haiku and a small `max_tokens`, print `response.usage` and the computed cost, and log through the student's cost meter once w03-t1 exists. Without a key they exit with a clear message (`ANTHROPIC_API_KEY not set: see .env.example`) instead of a stack trace. They load the key with `uv run --env-file .env <file>` from the repo root, or with python-dotenv, never from shell exports.

## Teaching style in the chat

- Small chunks: at most about 25 lines of explanation before the student does something (runs, predicts, answers, edits).
- Ask "predict the output" before running examples; prediction errors are the best teaching moments.
- Socratic for concepts, direct for syntax.
- When the student is stuck, ask what they've tried and what they expected before explaining.
- Watch the clock: at segment boundaries, check `date` against the agenda and say if you're over.
- Be specific in feedback: name the idiom, the line, and the Java habit behind it.
- End each lesson segment by linking it to the task ("you'll use `defaultdict` in w01-t1's per-status counts").

## Quiz bank rules

- Questions come from taught material only: lesson files, examples, grader findings.
- Mix of formats (see SKILL.md § Quiz). At least one Java-to-Python or production-judgment question per quiz once week 3 starts.
- Record each question's `topic_id`, format, correct or not, and a short note on the misconception when wrong. The misconceptions feed `weak_areas` and the revision notes' pitfalls section.
- Spaced review uses `topics[*].first_taught`: prefer topics taught about 1, 3, 7 and 14+ days ago that haven't been quizzed recently.
