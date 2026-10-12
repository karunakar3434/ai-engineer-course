#!/usr/bin/env python3
"""Course calendar: where the course is today, how much time is left, which days were missed.

Reads private/progress.json (course.start_date, course.total_weeks, course.session_hours,
course.schedule_overrides, sessions[], missed_days[], replans[]) and prints a JSON summary.

deficit_hours counts only days after the latest replans[].absorbed_through, so hours a re-plan
already absorbed don't trigger another one. raw_deficit_hours is the gap since the course start.
unclosed_sessions lists past days whose session was never closed (status not "done" or "paused",
or no actual_hours). Those count as 0 h done, so close them before trusting deficit_hours.
paused_sessions lists days whose session is paused (today included); their hours so far count.

    python3 tools/course_calendar.py                 # today
    python3 tools/course_calendar.py --date 2026-10-20 --compact

Stdlib only (Python 3.9+) so it works before the uv lessons.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, timedelta
from pathlib import Path
from typing import Iterator

WEEKDAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
DEFAULT_PROGRESS = Path(__file__).resolve().parent.parent / "private" / "progress.json"


def planned_hours(day: date, course: dict) -> float:
    """Hours scheduled for a day: a dated override wins over the weekday default."""
    override = course.get("schedule_overrides", {}).get(day.isoformat())
    if override is not None:
        return float(override)
    return float(course["session_hours"][WEEKDAYS[day.weekday()]])


def days(start: date, end: date) -> Iterator[date]:
    """Every date from start to end, inclusive."""
    current = start
    while current <= end:
        yield current
        current += timedelta(days=1)


def absorbed_through(replans: list[dict], today: date) -> date | None:
    """Last day a re-plan absorbed. An entry without absorbed_through covers up to the day before its date."""
    covered = [
        date.fromisoformat(r["absorbed_through"]) if r.get("absorbed_through")
        else date.fromisoformat(r["date"]) - timedelta(days=1)
        for r in replans
        if r["date"] <= today.isoformat()
    ]
    return max(covered, default=None)


def summarize(progress: dict, today: date) -> dict:
    course = progress["course"]
    start = date.fromisoformat(course["start_date"])
    total_weeks = int(course["total_weeks"])
    end = start + timedelta(weeks=total_weeks) - timedelta(days=1)
    yesterday = today - timedelta(days=1)

    sessions = progress.get("sessions", [])
    session_dates = {s["date"] for s in sessions}
    recorded_missed = {m["date"] for m in progress.get("missed_days", [])}

    if today < start:
        status, week, day_in_week = "not_started", 0, 0
    elif today > end:
        status, week, day_in_week = "finished", total_weeks, 7
    else:
        offset = (today - start).days
        status, week, day_in_week = "in_progress", offset // 7 + 1, offset % 7 + 1

    past_end = min(yesterday, end)
    past_days = list(days(start, past_end)) if past_end >= start else []
    missed = [
        {"date": d.isoformat(), "weekday": d.strftime("%A"), "planned_hours": planned_hours(d, course)}
        for d in past_days
        if planned_hours(d, course) > 0 and d.isoformat() not in session_dates
    ]
    planned_before_today = sum(planned_hours(d, course) for d in past_days)
    done_before_today = sum(
        float(s.get("actual_hours") or 0) for s in sessions if s["date"] < today.isoformat()
    )
    absorbed = absorbed_through(progress.get("replans", []), today)
    after = absorbed.isoformat() if absorbed else ""
    planned_unabsorbed = sum(planned_hours(d, course) for d in past_days if d.isoformat() > after)
    done_unabsorbed = sum(
        float(s.get("actual_hours") or 0) for s in sessions if after < s["date"] < today.isoformat()
    )
    unclosed = sorted(
        {
            s["date"]
            for s in sessions
            if s["date"] < today.isoformat()
            and (s.get("status") not in ("done", "paused") or s.get("actual_hours") is None)
        }
    )
    paused = sorted({s["date"] for s in sessions if s.get("status") == "paused"})

    remaining_from = max(today, start)
    remaining_by_week = []
    for w in range(max(week, 1), total_weeks + 1):
        w_start = start + timedelta(weeks=w - 1)
        w_end = w_start + timedelta(days=6)
        from_day = max(w_start, remaining_from)
        if from_day > w_end:
            continue
        remaining_by_week.append(
            {
                "week": w,
                "start": w_start.isoformat(),
                "end": w_end.isoformat(),
                "remaining_hours": sum(planned_hours(d, course) for d in days(from_day, w_end)),
            }
        )

    return {
        "today": today.isoformat(),
        "weekday": today.strftime("%A"),
        "planned_hours_today": planned_hours(today, course) if start <= today <= end else 0,
        "course_status": status,
        "course_week": week,
        "course_day": day_in_week,
        "days_until_start": max((start - today).days, 0),
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
        "week_start": (start + timedelta(weeks=week - 1)).isoformat() if week else None,
        "week_end": (start + timedelta(weeks=week - 1, days=6)).isoformat() if week else None,
        "session_already_logged_today": today.isoformat() in session_dates,
        "last_session_date": max(session_dates) if session_dates else None,
        "missed_days_total": len(missed),
        "new_missed_days": [m for m in missed if m["date"] not in recorded_missed],
        "hours_planned_before_today": planned_before_today,
        "hours_done_before_today": done_before_today,
        "raw_deficit_hours": round(planned_before_today - done_before_today, 2),
        "absorbed_through": after or None,
        "deficit_hours": round(planned_unabsorbed - done_unabsorbed, 2),
        "unclosed_sessions": unclosed,
        "paused_sessions": paused,
        "remaining_hours_including_today": sum(r["remaining_hours"] for r in remaining_by_week),
        "remaining_by_week": remaining_by_week,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--progress", type=Path, default=DEFAULT_PROGRESS, help="path to progress.json")
    parser.add_argument("--date", help="treat this YYYY-MM-DD as today (for testing)")
    parser.add_argument("--compact", action="store_true", help="print one-line JSON")
    args = parser.parse_args()

    try:
        progress = json.loads(args.progress.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        print(f"course_calendar: cannot read {args.progress}: {exc}", file=sys.stderr)
        return 1
    today = date.fromisoformat(args.date) if args.date else date.today()
    summary = summarize(progress, today)
    print(json.dumps(summary, separators=(",", ":")) if args.compact else json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
