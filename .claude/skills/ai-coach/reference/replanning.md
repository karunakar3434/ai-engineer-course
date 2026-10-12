# Re-planning

## Triggers

- **Automatic** at session start: the calendar reports `new_missed_days`, or `deficit_hours ≥ 2`. `deficit_hours` counts only days after the latest re-plan's `absorbed_through`, so hours already re-planned never trigger another re-plan. `raw_deficit_hours` is the gap since the course start: report it, but don't trigger on it. Close any `unclosed_sessions` first (SKILL.md, Start session step 3) and re-run the calendar: an unclosed session counts as 0 h done, so the deficit it causes isn't real yet.
- **Manual**: the student says `re-plan`, or declares future days off or a changed weekly schedule.
- **Proposed, not automatic**: a P1 task failed twice, or the student is clearly faster or slower than planned. Suggest a re-plan and wait for a yes.

## Principles

- Sessions stay sized to each day's hours. **Never pile missed work onto future days.**
- Absorb in this order: (1) the final-week buffer, (2) cut P3 items, (3) compress P2 items, (4) merge related tasks, (5) shrink capstone scope while keeping every required component, (6) compress P1 lessons but keep P1 tasks.
- Never drop: the core P1 topics (Claude API, prompting/tools, RAG, agents, evals, production), grading of P1 tasks, or a minimum of 8 h of interview prep in the final week.
- Prefer compressing lessons over shrinking tasks, because hands-on work is what makes the student job-ready.

## Procedure

1. Run `python3 tools/course_calendar.py` to get `remaining_by_week` and the deficit. If it lists `unclosed_sessions`, close them first (SKILL.md, Start session step 3) and run it again.
2. **Available** = remaining hours × 0.92 (keep slack).
3. **Needed** = the sum of hours of unfinished syllabus items (topics plus tasks; in-progress items count their remaining share).
4. If needed ≤ available: shift items forward and shrink the buffer. Done.
5. Otherwise apply the absorption order until needed ≤ available. Compressing means: lesson time × 0.5–0.7 (fewer examples; the rest moves to "read on your own if curious", which is optional, not homework); for a task, a smaller scope with fewer acceptance criteria, keeping the core skill.
6. Rebuild the week-by-week table for the remaining weeks. If the current week's `lessons/week-NN/README.md` exists, update its remaining day plans.
7. Record and report:
   - private/progress.json: append to `replans` (`date`, `trigger`, `deficit_hours`, `absorbed_through`, `missed_days`, `cut[]`, `compressed[]`, `moved[]`, `buffer_used_hours`); set `replanned: true` on the missed days it accounted for. `absorbed_through` is the last day whose shortfall this plan absorbs: yesterday when you re-plan before today's session, today when today's hours are already logged (for example at `end session`). Because step 3 counts every unfinished item, a re-plan absorbs the whole shortfall up to that day.
   - syllabus.md: update the affected weeks and add a changelog row.
   - Tell the student in at most 12 lines:

     ```
     Re-plan: missed <n> days (<h> h). Remaining: <R> h over <W> weeks.
     Cut:        <item> (P3) …
     Compressed: <item> <before>h → <after>h (<how>) …
     Moved:      <item> week X → week Y …
     Buffer:     final week now <h> h (was <h> h)
     ```
8. Cuts that touch P1 or P2 items need the student's OK before you apply them. Buffer use and P3 cuts can be applied and reported.
9. Commit: `replan(<date>): <short reason>`.

## Schedule changes

- Day off or reduced day: `course.schedule_overrides["YYYY-MM-DD"] = <hours>`.
- New weekly pattern: update `course.session_hours`, then re-plan.
- If the deficit can't be absorbed even after all six steps, say so plainly and offer two options: extend the end date (and by how much), or drop named P2 topics.
