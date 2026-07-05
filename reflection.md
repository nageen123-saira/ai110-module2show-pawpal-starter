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

I used AI throughout the project: brainstorming the initial class design and 
UML diagram, generating skeleton code from that design, implementing the 
core scheduling logic, drafting pytest tests, and writing documentation. 
The most helpful prompts were specific ones that pointed at a real file, 
like asking my AI assistant to review my class skeleton for missing 
relationships and logic bottlenecks before I wrote any real logic — that 
caught several issues early instead of after I'd already built on top of 
a flawed design.

**b. Judgment and verification**

Before implementing Phase 2, I asked my AI assistant to review my 
pawpal_system.py skeleton. It flagged seven real issues, including that my 
original conflict-detection design only caught tasks with identical start 
times, not actual overlapping time ranges (e.g. an 08:00 task and an 08:15 
task with overlapping durations would have been missed). Rather than 
accepting a "good enough" fix, I had it walk through the tradeoffs of a 
few different approaches (greedy vs. optimal packing for the time budget, 
for example) and made an explicit decision for each one, documenting the 
reasoning in reflection.md 1b. I verified the fix worked by writing a 
specific test (test_detect_conflicts_flags_overlapping_fixed_time_tasks) 
and running it against the real implementation rather than just trusting 
that the suggested code was correct.



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

### a. What went well

I'm most satisfied with the scheduling logic in the `Scheduler` class. In particular, `build_daily_plan()`, `sort_by_priority()`, and `detect_conflicts()` work together to transform a simple list of tasks into an organized daily plan that respects the available time budget, explains its decisions, and warns about scheduling conflicts. The most rewarding moment was seeing everything work together in the Streamlit interface—adding two tasks with the same scheduled time and immediately seeing the conflict warning appear automatically. It showed that the design and implementation were working together as intended.

### b. What you would improve

If I had another iteration, I would improve the greedy-by-priority scheduling strategy. While it is simple, predictable, and easy to explain, it also has an important limitation: one long, high-priority task can consume the available time budget and prevent several shorter tasks from being scheduled, even though those smaller tasks might provide more overall value. I would also assign each `Pet` a stable unique ID instead of relying on unique names. My AI design review identified this as a potential issue early in the project, but I chose not to implement it because it was outside the required project scope.

### c. Key takeaway

The biggest lesson I learned is that AI is most valuable during the design phase rather than after implementation. Having my class structure reviewed before writing the application logic helped identify important design concerns—such as interval-based conflict detection, recurrence requiring a date anchor, and the risks of returning mutable objects—that would have been much more difficult to fix later. This project also reinforced that AI should be treated as a design partner rather than the decision-maker. My role was to evaluate its suggestions, understand the tradeoffs, and make the final architectural decisions, such as choosing a greedy scheduling approach instead of pursuing a more complex optimal algorithm.
