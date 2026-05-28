# Call Analysis & Coaching Engine

Based on the real Superleap call JSON — a prospect asking about makeup, bridal, hair, chemical, and cosmetology courses.

---

## The Call — What Actually Happened

### Lead Profile
- **Intent**: High — repeatedly asked about pricing, course inclusions, bridal course
- **Knowledge**: Semi-informed, possibly already in beauty space
- **Questions**: "What's included in ₹30,000?", "What is the bridal course?", "What is the full course?", "What is the total price?"

### Counselor Performance

| Parameter | Rating | Notes |
|-----------|--------|-------|
| Opening | ❌ Weak | No identity confirmation, jumped into listing |
| Discovery | ❌ Weak | Didn't ask goal, current level, budget comfort |
| Recommendation | ❌ Course dumping | "48 types of courses" — overwhelming |
| Fee handling | ❌ Reactive | Let customer lead pricing discussion |
| Objection handling | ⚠️ Moderate | Tried but slipped into long explanations |
| Closing | ❌ None | No visit booking, no firm next step |
| WhatsApp follow-up | ⚠️ Promised but weak | No confirmation of when/what to send |

### Transcript Pattern
```
Counselor: *lists all courses*
Prospect: "What about [specific question]?"
Counselor: *explains broadly instead of answering directly*
Prospect: "And what is the price for this?"
Counselor: *gives range instead of specific*
...continues without narrowing down...
Call ends: No visit booked.
```

### Root Issues
1. **Catalogue-mode selling** — listing everything instead of diagnosing and matching
2. **No qualification** — didn't establish goal, urgency, or budget before pitching
3. **No value framing** — discussed price before building course value
4. **No close** — call ended without a confirmed next step

---

## The Coaching Framework (Reusable for Every Call)

### Auto-Score Rubric (from Superleap JSON)

| Score Area | What to Check | Weight |
|-----------|---------------|--------|
| **Opening** | Did they greet by name, confirm source, ask a specific question? | 10% |
| **Discovery** | Did they ask goal/level/timeline before recommending? | 20% |
| **Clarity** | Was the recommendation specific (one course), not a list? | 20% |
| **Fee handling** | Did they build value before price? Was EMI mentioned? | 15% |
| **Objection handling** | Did they acknowledge and redirect smoothly? | 15% |
| **Closing** | Did they book a visit or confirm a specific follow-up? | 20% |

**Score per call**: 0-100. Anything below 60 = needs coaching.

### Manager Note (Auto-Generated from this Call)
> "Counselor should stop listing too many courses. Ask 3 qualification questions first, then recommend one best-fit course. Close for visit or at minimum confirm a WhatsApp template + callback time."

---

## What Superleap JSON Enables

| Field in JSON | Coaching Use |
|---------------|-------------|
| `agent_speak_time` vs `customer_speak_time` | Is counselor dominating? Should be 40:60 ratio |
| `dead_air` | Awkward pauses = counselor lost |
| `longest_agent_monologue` | Course dumping detected (>60 sec = bad) |
| `longest_customer_story` | Customer engaged or frustrated? |
| `interactivity` | Back-and-forth = good; monologue = bad |
| `text` (transcript) | Full conversation for QA scoring |
| `timestamped_segments` | Pinpoint exactly where the call went wrong |

### Build This Dashboard
```
Superleap JSON per call
        │
        ▼
Parse & Score (rubric above)
        │
        ├── Call Score: 45/100
        ├── Flags: Course Dumping, No Close
        ├── Manager Note: [auto-generated]
        └── Coach Action: Retrain on qualification questions
```

---

## The Bigger Picture

### What We Now Know (From Real Data)

| Layer | Status |
|-------|--------|
| **Lead generation** | ✅ Working (Meta, Website, Google) |
| **Lead capture** | ✅ Working (IVR → Superleap) |
| **Call recording** | ✅ Working (Rich JSON with full analytics) |
| **Counselor quality** | ❌ Broken (course-dumping, no close) |
| **Follow-up process** | ❌ Broken (no structured cadence) |
| **Conversion tracking** | ❌ Missing (no "Admitted" stage visible) |

### The Product Opportunity

You can build a **Call Coaching Engine** on top of Superleap data:
1. Every call JSON → auto-scored
2. Low-scoring calls → flagged for manager review
3. Pattern detection: "Sonia struggles with closing" → targeted retraining
4. Weekly report: counselor scores, conversion correlation, coaching ROI

Single center pilot → replicate across all 3 Noida centers → expand to all 150+ LAPA centers.

---

> **Next Build**: Parse one real JSON, generate an auto-score, and build the manager dashboard mockup.
