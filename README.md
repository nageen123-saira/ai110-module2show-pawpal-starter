# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build
## ✨ Features

- **Owner & pet setup** — enter an owner's name, their daily available care 
  time, and add one or more pets (name + species).
- **Task management** — add care tasks per pet with a description, duration, 
  priority (high/medium/low), an optional fixed time, and a frequency 
  (once/daily/weekly).
- **Smart daily planning** — `Scheduler.build_daily_plan()` sorts tasks by 
  priority, greedily fits them into the owner's available time budget, and 
  returns a plain-language explanation for each task included.
- **Conflict warnings** — `Scheduler.detect_conflicts()` flags any tasks 
  whose fixed times actually overlap (interval-based, not just identical 
  start times), so you catch scheduling collisions before they happen.
- **Recurring tasks** — daily/weekly tasks automatically generate their next 
  occurrence when marked complete, anchored to a real `start_date`.
- **Filtering** — view tasks by pet or completion status.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output


=== Today's Plan for Jordan (budget: 90 min) ===
  [08:00] Morning walk (30 min, high priority)
      -> high priority, fits in remaining budget (90 min left before this task)
  [08:15] Feeding (10 min, high priority)
      -> high priority, fits in remaining budget (60 min left before this task)
  [09:00] Feeding (10 min, high priority)
      -> high priority, fits in remaining budget (50 min left before this task)
  [flexible] Litter box cleaning (10 min, medium priority)
      -> medium priority, fits in remaining budget (40 min left before this task)
  [flexible] Play time (20 min, medium priority)
      -> medium priority, fits in remaining budget (30 min left before this task)

=== Conflict Warnings ===
  ! Conflict: 'Morning walk' (08:00, 30 min) overlaps with 'Feeding' (08:15, 10 min)

=== Filter Demo: Mochi's tasks only ===
  - Morning walk (high)
  - Feeding (high)
  - Brushing (low)

=== Recurring Task Demo ===
  Before: 'Play time' completed=False, start_date=2026-07-04
  After marking complete: completed=True
  Next occurrence created: start_date=2026-07-05, completed=False

```

---
## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:
================================= test session starts =======================================
platform win32 -- Python 3.13.7, pytest-9.0.3, pluggy-1.6.0
rootdir: C:\Users\nagee\ai110-module2show-pawpal-starter
plugins: anyio-4.13.0
collected 11 items                                                                                 

tests\test_pawpal.py ...........                                                             [100%]

================================= 11 passed in 0.09s ========================================

---

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---|---|---|
| Task sorting | `Scheduler.sort_by_priority()` | Sorts by priority rank (high → medium → low), then by fixed time within the same priority |
| Filtering | `Scheduler.filter_tasks()` | Filters by completion status and/or pet name |
| Conflict handling | `Scheduler.detect_conflicts()` | Compares time intervals `[time, time+duration)`, not just exact start times; flexible tasks are excluded |
| Recurring tasks | `Task.mark_complete()` / `Task.next_occurrence()` | Each occurrence is its own object; completing a daily/weekly task generates the next one with an advanced `start_date` |

## 📸 Demo Walkthrough



## 📸 Demo Walkthrough

1. Open the app and set the owner's name and available minutes per day for 
   pet care.
2. Add a pet by entering its name and species, then click **Add pet**.
3. Add a few tasks for that pet — mix it up with different priorities, a 
   couple of fixed times (try two tasks at the same time to see conflict 
   detection), and one task set to "daily" frequency.
4. Review the **Current tasks** table to confirm everything was added 
   correctly.
5. Click **Generate schedule** to see today's plan: tasks appear in 
   priority order, each with an explanation of why it was included, and 
   any time conflicts are flagged with a warning banner above the plan.

**Sample CLI output** (from running `python main.py`):

\`\`\`
=== Today's Plan for Jordan (budget: 90 min) ===
  [08:00] Morning walk (30 min, high priority)
      -> high priority, fits in remaining budget (90 min left before this task)
  [08:15] Feeding (10 min, high priority)
      -> high priority, fits in remaining budget (60 min left before this task)
  [09:00] Feeding (10 min, high priority)
      -> high priority, fits in remaining budget (50 min left before this task)
  [flexible] Litter box cleaning (10 min, medium priority)
      -> medium priority, fits in remaining budget (40 min left before this task)
  [flexible] Play time (20 min, medium priority)
      -> medium priority, fits in remaining budget (30 min left before this task)

=== Conflict Warnings ===
  ! Conflict: 'Morning walk' (08:00, 30 min) overlaps with 'Feeding' (08:15, 10 min)

=== Filter Demo: Mochi's tasks only ===
  - Morning walk (high)
  - Feeding (high)
  - Brushing (low)

=== Recurring Task Demo ===
  Before: 'Play time' completed=False, start_date=2026-07-04
  After marking complete: completed=True
  Next occurrence created: start_date=2026-07-05, completed=False
\`\`\`

**Screenshot Here **



 ->
