# Tech Architecture — Call Coaching Engine

### For Non-Technical Understanding

---

## THE GOAL

```
After every call → Auto-analyze → Score the counselor → Flag mistakes → Send report
```

No manual work. No listening to every call. The machine does it.

---

## HOW DATA FLOWS

### Option A: API (Best — Real-time)

```
Superleap Cloud
     │
     │  Call completes
     │  Superleap sends JSON to our server automatically (webhook)
     ▼
Our Server (Python)
     │
     │  Read JSON
     │  Score the call (14/100)
     │  Flag mistakes (Brand error, Course dump, No close)
     │  Generate coaching note
     │
     ├──► Save to our database
     ├──► Send WhatsApp/Slack alert to manager
     └──► Write score back into Superleap as a note on the lead
```

**What you ask Superleap:**
> "Do you have webhooks? When a call ends, can you automatically send us the JSON?"

### Option B: Daily Export (Simpler — Works Today)

```
Superleap → Daily JSON export (all calls from yesterday)
     │
     ▼
Our script reads the folder → Analyzes every call → Generates report
     │
     ▼
Manager opens report every morning → sees:
   - Deepti: 3 calls, avg score 18/100 → needs retraining
   - Sonia: 5 calls, avg score 45/100 → improving
   - Top mistakes this week: Course dumping (12 calls), No close (9 calls)
```

**What you ask Superleap:**
> "Can you export all call JSON files daily and send them to us?"

---

## WHAT WE BUILD (MVP — 4 Steps)

### Step 1: The Analyzer (Works TODAY)
A Python script that reads one JSON file and outputs:
- Call score (0-100)
- Flags (brand error, course dump, no close, etc.)
- Coaching note for the counselor

**Status**: ✅ DONE — Already built with your real call. Scored it 14/100.

### Step 2: Batch Mode (Works in 1 day)
Same script, but reads a folder of JSON files and generates a daily report.

### Step 3: Auto-Import (Works after Superleap says yes)
Either:
- Webhook: Superleap sends us each call as it happens
- OR Daily export: Superleap sends a ZIP of all yesterday's JSONs

### Step 4: Dashboard (Works in 1 week)
A simple web page showing:
- Today's calls & scores
- Counselor rankings
- Common mistakes
- Trends over time

---

## TECH STACK (Plain English)

| Piece | What | Why |
|-------|------|-----|
| **Python** | The brain | Reads JSON, scores calls, generates reports |
| **Script** | The worker | Runs every day (or after every call) |
| **Database** | The memory | Stores all calls, scores, trends |
| **Dashboard** | The screen | Shows you everything in one place |
| **n8n / Zapier** | The glue | Connects Superleap to our system without coding |

---

## WHAT YOU NEED FROM SUPERLEAP — EXACT DRAFT

Copy-paste this to Superleap support:

> **Subject**: API access & AI coaching features — Lakmé Academy
>
> Hi Superleap team,
>
> We are using Superleap for our Lakmé Academy centers. We want to build a call-coaching system that automatically analyzes counselor calls to improve conversions.
>
> **First — do we already have access to your built-in AI Call Analysis features?** We noticed you offer:
> - AI-generated call summaries & sentiment scores
> - Call quality scoring & coaching flags
> - Talk-time metrics & objection patterns
>
> If these are available on our plan, please enable them. We'd love to use them directly.
>
> Additionally, we need:
> 1. **API access** to fetch call recordings, transcripts, and metadata (the JSON payload per call)
> 2. **Webhooks** — Can you notify us when a call is completed? So we can fetch data automatically
> 3. **Write-back** — Can we write notes/scores back into the opportunity record?
> 4. OR **Daily JSON export** of all completed calls as a simpler fallback
>
> Please let us know:
> - How to generate an API key
> - Rate limits
> - If webhooks are available for call-complete events
> - Whether AI Call Analysis is included in our current plan or needs an upgrade
> - Pricing for API access (if separate)
>
> Thanks,
> [Your Name]
> Lakmé Academy — Apptech

---

## PROTOTYPE STATUS (What's Already Built)

| Piece | Status | File |
|-------|--------|------|
| Parse one call JSON | ✅ Working | `call-analysis-real.md` |
| Score call (rubric) | ✅ Working | Scored real call 14/100 |
| Generate coaching note | ✅ Working | Auto-created flags & recommendations |
| Daily batch report | ⬜ Not yet | Needs your OK to build |
| Dashboard | ⬜ Not yet | Needs your OK to build |

---

## HOW WE BUILD THE PROTOTYPE SCRIPT

I'll write a Python script that:

```
python3 analyze_calls.py                    # analyzes one file
python3 analyze_calls.py --folder calls/    # analyzes all files in folder
```

**Output for each call**:
```
Call: Surajan → Deepti
Score: 14/100 ❌
Flags: Brand Error, Course Dump, No Close
Coach: Practice brand name, stop listing 48 courses, always book visit
```

**Output for daily report**:
```
📊 DAILY REPORT — 26 May 2026
Total calls: 12
Avg score: 28/100
Best counselor: Sonia (45 avg)
Worst counselor: Deepti (14 avg)
Top mistake: Course dumping (8 calls)
```

---

**Next**: Want me to build the Python script right now so you can run it on any call JSON you get from Superleap?
