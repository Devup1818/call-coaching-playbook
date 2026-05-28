# Setup Guide — Call Analyzer System

## What You Have

```
TASK CETE/
├── analyze_calls.py          ← The brain — scores calls, generates reports
├── whatsapp_sender.py        ← Sends WhatsApp messages (needs API setup)
├── counselor-playbook.md     ← Call script & objection handling
├── call-analysis-real.md     ← Your real call analyzed in detail
├── call-analysis-template.md ← Scoring rubric template
├── future-business-plan.md   ← Full business strategy
├── tech-architecture.md      ← How everything connects
├── config.example.json       ← Template for your WhatsApp API keys
├── calls/                    ← Drop Superleap JSON files here
│   └── QU9jGk_....json       ← Your sample call
├── reports/                  ← Daily reports are saved here
│   └── report-2026-05-26.txt ← Today's report
└── .processed_files.txt      ← Tracks which files are done
```

---

## Daily Workflow

### Step 1: Get JSON files from Superleap
- Ask Superleap support for **daily JSON export** of completed calls
- OR if they give you API access, the script can auto-fetch
- Save the `.json` files into the `calls/` folder

### Step 2: Run the analyzer
```bash
cd /path/to/TASK\ CETE
python3 analyze_calls.py
```

This processes all NEW JSON files and generates a report in `reports/`

### Step 3: Read the report
Open the report file:
```bash
open reports/report-2026-05-26.txt
```

It shows:
- Each counselor's score
- Top mistakes this period
- Coaching priorities

---

## Commands Reference

```bash
# Process all new calls
python3 analyze_calls.py

# Analyze a single file
python3 analyze_calls.py --file call.json

# Generate fresh report from ALL calls (not just new)
python3 analyze_calls.py --report

# Keep watching the folder (processes new files automatically)
python3 analyze_calls.py --watch
```

---

## WhatsApp Setup (Optional)

To get reports on your phone automatically:

1. Go to https://developers.facebook.com
2. Create a Business App → Add WhatsApp product
3. Copy your **Phone Number ID** and **Access Token**
4. Create `config.json` (copy from `config.example.json`):

```json
{
    "whatsapp_token": "EAAx...your-token...",
    "phone_number_id": "123456789012345",
    "manager_phone": "+9198XXXXXXXX"
}
```

5. Test it:
```bash
python3 whatsapp_sender.py --test
```

6. Send today's report to your phone:
```bash
python3 whatsapp_sender.py --report
```

---

## What To Ask Superleap

Copy-paste this to Superleap support:

> We need call data & coaching features for our Lakmé Academy center (Noida Sector 18).
>
> **First** — Do we have access to your built-in **AI Call Analysis** features? (sentiment scoring, call summaries, coaching flags, talk-time metrics). If yes, please enable them.
>
> Additionally we need:
> 1. **API access** to fetch call recordings, transcripts, and metadata
> 2. **Webhooks** — notify us when a call completes
> 3. OR **Daily JSON export** of all completed calls
>
> Happy to test with a small scope first.

---

## System Diagram

```
Superleap (daily JSON export)
        │
        ▼
calls/ folder ──► python3 analyze_calls.py ──► reports/report.txt
        │                                         │
        │                                         ▼
        │                                    Manager reads it
        │
        ▼ (if WhatsApp API configured)
whatsapp_sender.py ──► WhatsApp report to manager's phone
                         Brochure to leads
                         Visit reminders
```
