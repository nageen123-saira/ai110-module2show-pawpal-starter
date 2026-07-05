# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

I designed four classes: `Task`, `Pet`, `Owner`, and `Scheduler`. `Task` holds 
a single care activity (description, duration, priority, optional fixed time, 
frequency, completion status). `Pet` groups tasks for one animal. `Owner` 
manages multiple pets and stores the daily time constraint 
(`available_minutes_per_day`). `Scheduler` is the only class that reasons 
across pets — it builds the daily plan, sorts by priority, filters, and 
detects conflicts, keeping `Pet` and `Owner` as simple data holders.

**Core user actions**
1. Add a pet — the owner can register a pet (name, species) so the system 
   has something to plan care around.
2. Add/edit a task — the owner can create care tasks (e.g. walk, feeding, 
   meds) for a pet, each with a duration and a priority level.
3. View today's plan — the owner can generate a daily schedule that orders 
   tasks sensibly (by priority and time) and briefly explains the ordering.

**b. Design changes**

After AI code review, I made several changes to close gaps between the 
skeleton and what the scheduler actually needs to do:
- `Pet.add_task()` now stamps `task.pet_name` automatically instead of 
  relying on it being set correctly elsewhere.
- Added `Task.start_date` so recurring tasks ("daily"/"weekly") have an 
  actual date to compute the next occurrence from.
- Decided `build_daily_plan()` will use a greedy-by-priority strategy for 
  fitting tasks into the owner's available time, rather than optimal 
  packing — simpler and easier to explain to the user, at the cost of 
  occasionally not using every minute optimally.
- `detect_conflicts()` compares time intervals (start + duration), not 
  just exact start times, so overlapping tasks are actually caught.
- `get_tasks()`/`get_all_tasks()` return copies so external code can't 
  accidentally mutate internal state.
- Accepted a known limitation: pet names are assumed unique per owner; 
  duplicate names would break `filter_tasks(pet_name=...)`.

---

## 2. Scheduling Logic and Tradeoffs


**a. Constraints and priorities**

The scheduler considers two constraints: task priority (high/medium/low) and 
the owner's available_minutes_per_day. Priority mattered most because a busy 
owner needs to know what absolutely can't be skipped, so tasks are sorted by 
priority first and packed greedily until the time budget runs out.

**b. Tradeoffs**

The scheduler uses greedy-by-priority packing instead of optimal knapsack 
packing. This means a single long high-priority task could occasionally 
"use up" the budget and exclude several short lower-priority tasks that 
would have fit better together. I chose greedy because it's simple, fast, 
and easy to explain to the user in plain language ("this task was included 
because it's high priority and fits") — optimal packing would be harder to 
justify in the UI.





---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification


**a. What you tested**

I tested: (1) marking a task complete, (2) adding a task increases a pet's 
task count, (3) sorting orders tasks by priority then time, (4) completing 
a daily task creates a correctly-dated next occurrence while a "once" task 
does not recur, (5) conflict detection flags overlapping and identical 
fixed times but ignores flexible or non-overlapping tasks, and (6) two 
edge cases: a pet with no tasks produces an empty plan, and get_tasks() 
returns a copy so external code can't mutate internal state.

**b. Confidence**

I'm fairly confident (4/5) the core scheduling logic is correct, since the 
riskiest pieces flagged in AI code review (interval-based conflicts, 
priority ranking, recurrence dates) are all directly tested and passing. 
With more time I'd test: multiple pets competing for the same time budget, 
a task priority string that isn't "high"/"medium"/"low", and weekly 
(not just daily) recurrence math.




---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
