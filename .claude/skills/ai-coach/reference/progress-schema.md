# progress.json schema

Single source of truth for course state, at `~/ai-engineer-course/private/progress.json`, in the private repo (SKILL.md rule 11). Keep keys stable (`schema_version: 1`). Dates are `YYYY-MM-DD`; times are local `HH:MM`. Write after every state change and validate with `python3 -m json.tool private/progress.json > /dev/null`.

```jsonc
{
  "schema_version": 1,
  "student": { "background": "...", "goal": "...", "machine": "...", "plan": "..." },

  "course": {
    "status": "not_started",            // not_started | in_progress | finished
    "start_date": "2026-10-10",
    "end_date": "2027-01-08",
    "total_weeks": 13,
    "session_hours": { "mon": 3, "tue": 2, "wed": 2, "thu": 2, "fri": 3, "sat": 3, "sun": 3 },
    "schedule_overrides": { "2026-11-26": 0 },   // date -> hours (0 = day off)
    "pass_mark": 70,
    "default_weights": { "correctness": 40, "code_quality": 20, "design": 20, "ai_quality": 20 }
  },

  "current": {                           // where the student is
    "week": 1, "day": 2,
    "topic_id": "w01-py-core",
    "lesson_file": "lessons/week-01/d2-names-and-functions.md",
    "active_tasks": ["w01-t1"]
  },

  "diagnostic": {
    "completed": true, "date": "2026-10-10",
    "results": { "python_transfer": 5, "concepts": 3.5, "tooling": { "docker": 1, "ci": 2 }, "notes": "..." },
    "adjustments": ["Docker primer added to week 5"]
  },

  "syllabus": { "version": 1, "approved": true, "last_updated": "2026-10-10" },

  "weeks": {
    "1": {
      "status": "in_progress",           // planned | in_progress | done
      "goal": "...",
      "plan_file": "lessons/week-01/README.md",
      "planned_hours": 17, "actual_hours": 5.5,
      "adaptations": ["..."],
      "retro": null                      // short text, filled at next kickoff
    }
  },

  "topics": {
    "w01-py-core": {
      "week": 1, "title": "Core syntax for Java developers", "priority": "P1",
      "status": "taught",                // planned | in_progress | taught | done | compressed | cut
      "first_taught": "2026-10-11",
      "lesson_files": ["lessons/week-01/d2-names-and-functions.md"],
      "revision": "revision/w01-py-core.md",
      "pdf": "pdfs/w01-py-core.pdf",
      "last_quizzed": "2026-10-13"
    }
  },

  "tasks": {
    "w01-t1": {
      "dir": "tasks/w01-t1-log-insights",
      "title": "log-insights CLI", "week": 1, "topic_ids": ["w01-py-collections"],
      "status": "needs_fix",             // not_started | in_progress | submitted | needs_fix | passed | deferred | descoped
      "weights": { "correctness": 50, "code_quality": 30, "design": 20, "ai_quality": 0 },
      "estimate_hours": 4, "estimate_cost_usd": 0.0, "model": null,
      "scaffold_commit": "abc1234",
      "attempts": [
        {
          "n": 1, "date": "2026-10-12", "commit": "def5678",
          "score": 64,
          "breakdown": { "correctness": [36, 50], "code_quality": [17, 30], "design": [11, 20], "ai_quality": [0, 0] },
          "passed": false,
          "gates": { "provided_tests_pass": false, "tests_unmodified": true, "no_secrets": true, "requirements_met": true },
          "live_run": false, "live_cost_usd": 0.0,
          "report": "private/tasks/w01-t1-log-insights/attempts/attempt-1.md"
        }
      ],
      "best_score": 64,
      "hints": [ { "date": "2026-10-12", "level": 1, "about": "streaming large files" } ],
      "reference_released": false
    }
  },

  "sessions": [
    {
      "date": "2026-10-10", "start": "09:05", "end": "12:10",   // first segment's start, last segment's end
      "segments": [ { "start": "09:05", "end": "10:20" }, { "start": "10:40", "end": "12:10" } ],
      "planned_hours": 3, "actual_hours": 2.75,                 // sum of segments, nearest 0.25 h
      "status": "done",                  // in_progress | paused | done
      "week": 1, "day": 1,
      "covered": ["diagnostic", "w01-py-tooling"],
      "quiz": null,                      // or index into quiz_history
      "tasks_touched": [],
      "resume": null,                    // written by pause session, see below
      "notes": "..."
    }
  ],
  // sessions[].resume while status is "paused":
  // {
  //   "paused_at": "10:20",
  //   "lesson_file": "lessons/week-01/d4-strings-match-functions.md",
  //   "section": "3. Functions: defaults evaluated once",
  //   "last_step": "explained the None-sentinel fix; asked for a prediction",
  //   "pending": "Predict the output of calling append_to(1) twice",   // word for word, or null
  //   "agenda_left": [ { "segment": "core part 2 (rest)", "minutes": 30 }, { "segment": "wrap", "minutes": 5 } ],
  //   "notes": "student wants to revisit keyword-only parameters"
  // }

  "quiz_history": [
    {
      "date": "2026-10-11", "kind": "recap",   // recap | on_demand
      "score": 3, "total": 4,
      "items": [ { "topic_id": "w01-py-core", "format": "predict_output", "correct": false, "misconception": "thinks default args are re-evaluated per call" } ]
    }
  ],

  "weak_areas": [
    {
      "id": "mutable-defaults", "topic_id": "w01-py-core",
      "description": "Mutable default arguments",
      "evidence": ["quiz 2026-10-11", "w01-t1 attempt 1"],
      "opened": "2026-10-11", "status": "open",  // open | resolved
      "streak_correct": 0, "resolved": null
    }
  ],

  "missed_days": [ { "date": "2026-10-14", "planned_hours": 2, "reason": null, "replanned": true } ],

  "replans": [
    {
      "date": "2026-10-15", "trigger": "missed 2026-10-14", "deficit_hours": 2,
      "absorbed_through": "2026-10-14",   // last day whose shortfall this plan absorbs
      "missed_days": ["2026-10-14"],
      "cut": [], "compressed": ["w02-pydantic-fastapi 4.5h → 3.5h"], "moved": [], "buffer_used_hours": 1
    }
  ],

  "api_spend": {
    "monthly_budget_usd": 20,
    "by_month": { "2026-10": { "estimated_usd": 0.42, "console_reported_usd": 0.47, "console_checked": "2026-10-26" } },
    "total_estimated_usd": 0.42,
    "notes": []
  },

  "pdfs": { "combined_last_built": "2026-10-17" }
}
```

## Rules

- Append to history arrays (`attempts`, `sessions`, `quiz_history`, `replans`, `missed_days`); never rewrite or delete past entries. Fix mistakes with a new entry or a `notes` field.
- `replans[].absorbed_through` marks the shortfall up to that day as absorbed: yesterday for a re-plan before today's session, today if today's hours were already logged. `tools/course_calendar.py` reports `deficit_hours` from the days after the latest `absorbed_through` only, plus `raw_deficit_hours` (planned minus done since the start) and `absorbed_through`. An entry without the field counts as absorbing up to the day before its `date`. Same-day re-plans that supersede each other share one `absorbed_through`, so nothing is counted twice.
- A `sessions[]` entry is `in_progress` while the student studies, `paused` after `pause session`, and `done` after `end session`. Each stretch of study is one `segments[]` item, and `actual_hours` is their sum, written at every pause and at the end, so the calendar counts a paused day's hours. An entry without `segments` (from before pausing existed) counts as one segment from `start` to `end`.
- If a session stops without a pause or an end, `actual_hours` stays null, the calendar counts that day as 0 h done, and it lists the date in `unclosed_sessions` (past entries that aren't `paused` or `done`, or have no `actual_hours`). Start session closes those entries before it checks `deficit_hours` (SKILL.md, Start session step 3).
- The calendar lists the dates of `paused` entries, today's included, in `paused_sessions`. Continue session reopens today's and closes earlier ones (SKILL.md, Continue session).
- `best_score` is the maximum over attempts. `status: "passed"` requires an attempt with `passed: true`.
- Tasks with `ai_quality` weight 0 record it as `[0, 0]`.
- Percentage of syllabus done = topics with status `taught` or `done`, plus passed tasks, divided by all non-cut topics and tasks.
- `current` reflects the next thing to do, not the last thing done.
