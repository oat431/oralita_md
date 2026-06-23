# Time Management

> *Source: The Clean Coder by Robert C. Martin, Chapter 9 (pp. 121–133)*

---

## Core Principle

> **Professional developers diligently manage their time and focus. They understand the true cost of meetings, guard their concentration as a finite resource, and have the courage to abandon dead ends and growing messes before they consume the project.**

---

## The Rules

### 1. Treat Meetings as Expensive Investments

Meetings cost roughly $200 per hour per attendee (salaries, benefits, facilities). They are simultaneously necessary *and* huge time wasters. Professionals evaluate every meeting invitation against the value it provides to their current work.

- **Decline ruthlessly.** Accept only when your participation is immediately and significantly necessary to the job you are doing *now*. The person inviting you is not responsible for your time — you are.
- **Leave when it stops being useful.** If the agenda gets hijacked or the discussion no longer benefits you, politely negotiate your exit. Remaining in a useless meeting is unprofessional — you are wasting your employer's money.
- **Demand an agenda and a goal.** Before accepting, know what will be discussed, how much time is allotted, and what outcome is expected. No clear answers? Decline.
- **Your manager's job includes keeping you out of meetings.** A good manager will defend your decision to decline.

### 2. Run Agile Ceremonies Lean

- **Stand-Up Meetings:** Participants stand, each answers three questions in ≤20 seconds each: (1) What did I do yesterday? (2) What will I do today? (3) What's in my way? Even a 10-person team should finish in under 10 minutes.
- **Iteration Planning:** Should consume no more than 5% of the iteration's total time (≈2 hours for a one-week iteration). Spend 5–10 minutes per backlog item; schedule longer discussions separately.
- **Retrospective + Demo:** Schedule 45 minutes before quitting time on the last day — 20 minutes for retro, 25 minutes for demo. After only a week or two, there shouldn't be much to discuss.

### 3. Settle Arguments with Data, Not Force

Kent Beck's rule: **Any argument that can't be settled in five minutes can't be settled by arguing.** Prolonged disagreements lack evidence — they are religious, not factual.

- Stop arguing. Go get data: run an experiment, build a simulation, or flip a coin and set a timebox with criteria for when to abandon the chosen path.
- Reject force-of-character tactics (yelling, condescension) and passive-aggressive agreement (saying "yes" then sabotaging). Both are unprofessional.
- For must-settle arguments: give each side 5 minutes to present, then have the team vote. The whole process takes under 15 minutes.

### 4. Protect Your Focus-Manna

Focus is a **finite, decaying resource** — like "manna" in role-playing games. You can feel it when it's present and when it's gone. Professional developers write code when focus-manna is high and do less demanding tasks when it isn't.

- **Sleep is the primary recharge.** Seven hours of sleep can yield a full day's worth of focus-manna. Manage your sleep schedule to top up before work.
- **Caffeine helps, but respect the trade-off.** Moderate doses increase efficiency; too much creates a jitter that wastes an entire day hyper-focusing on the wrong things.
- **De-focus to recharge.** Walking, conversation, staring out a window, power naps, meditation, podcasts — 30–60 minutes of unfocused activity can partially restore your manna.
- **Muscle focus recharges mental focus.** Physical disciplines (martial arts, cycling, carpentry, gardening) use a different kind of concentration that actually enhances capacity for intellectual work.
- **Input balances output.** Reading science fiction or other creative works stimulates your own creative capacity for software.

### 5. Use Time Boxing and the Pomodoro Technique

The Pomodoro Technique divides time into 25-minute, uninterrupted work intervals ("tomatoes") separated by short breaks.

- **During a tomato:** Let nothing interfere. Defer phone calls, questions, and interruptions — few things are so urgent they can't wait 25 minutes.
- **When the timer dings:** Stop immediately. Handle deferred interruptions, then take a ~5-minute break.
- **Every fourth tomato:** Take a longer break (≈30 minutes).
- **Measure your output.** Count tomatoes per day (12–14 on a good day, 2–3 on a bad day). This gives you honest visibility into how much time you actually spend producing.

The real power is the aggressively defended 25-minute window of productive time.

### 6. Avoid Priority Inversion

Priority inversion is the lie you tell yourself: elevating a less important task to avoid the one that truly needs doing — because it's scary, uncomfortable, boring, or likely to force a confrontation. Professionals evaluate priorities dispassionately and execute tasks in true priority order, regardless of personal fear or desire.

### 7. Recognize and Escape Blind Alleys

Every craftsman occasionally makes a decision that leads nowhere. The skill is **recognizing it quickly** and having the courage to turn back.

- **The Rule of Holes:** When you're in one, stop digging.
- The more you've staked your reputation on a decision, the harder it is to abandon — and the longer you'll wander.
- Keep an open mind about alternative solutions so that when you hit a dead end, you still have options.

### 8. Flee Messes Before They Become Swamps

Messes are *worse* than blind alleys because you can always see the way forward, and it always looks shorter than the way back — but it isn't. You can make progress through brute force, but every step forward sinks you deeper.

- **The inflection point:** The moment you realize you made a wrong design choice and the code doesn't scale in the direction requirements are moving. Going back looks expensive because of rework, but it will *never* be easier than right now.
- **Moving forward through a swamp, when you know it's a swamp, is the worst kind of priority inversion.** You are lying to yourself, your team, your company, and your customers.
- Professionals fear messes more than blind alleys. They stay on the lookout for unbounded growth in complexity and expend all necessary effort to escape early.

---

## Summary Checklist

- [ ] Evaluate every meeting invitation — accept only when your participation is immediately and significantly necessary to current work
- [ ] Leave meetings that no longer benefit you; do so politely and at an opportune moment
- [ ] Demand a clear agenda and goal before accepting any meeting
- [ ] Keep stand-ups under 10 minutes; planning under 5% of iteration time; retrospectives under 45 minutes
- [ ] Stop arguments that exceed five minutes — go get data instead
- [ ] Protect your focus-manna: get enough sleep, use caffeine judiciously, de-focus to recharge
- [ ] Incorporate muscle-focus activities (exercise, hands-on hobbies) to strengthen mental focus
- [ ] Use Pomodoro Technique: 25-minute uninterrupted blocks with breaks between
- [ ] Count your daily tomatoes to track real productive time
- [ ] Catch yourself when you invert priorities — execute tasks in true priority order
- [ ] When you realize you're in a blind alley, stop digging and turn back
- [ ] Identify the inflection point where a design choice becomes a mess — go back immediately, don't press forward
- [ ] Never let yourself become so vested in a solution that you cannot abandon it

---

## Related

- [[Coding Discipline]]
- [[Pressure]]
- [[Estimation]]
- [[Collaboration]]
