"""
Call Analyzer — Superleap JSON Call Scoring Engine
Batch processes all call JSONs and generates daily reports.

Usage:
    python3 analyze_calls.py                    Process all new calls in calls/ folder
    python3 analyze_calls.py --report           Generate today's summary report
    python3 analyze_calls.py --master           Generate master report (all centers, all calls, Do's & Don'ts)
    python3 analyze_calls.py --watch            Keep running, process files as they appear
    python3 analyze_calls.py --file x.json      Analyze a single file
"""

import json
import os
import sys
import glob
import time
import re
from datetime import datetime
from collections import Counter, defaultdict

CALLS_DIR = os.path.join(os.path.dirname(__file__), "calls")
REPORTS_DIR = os.path.join(os.path.dirname(__file__), "reports")
PROCESSED_LOG = os.path.join(os.path.dirname(__file__), ".processed_files.txt")

CENTER_KEYWORDS = {
    "sector18": ["sector 18", "sector 18 noida", "sec 18", "sector eighteen"],
    "sector62": ["sector 62", "sector 62 noida", "sec 62", "sector sixty two"],
    "greater-noida": ["greater noida", "gr noida", "gr. noida", "greater noida"],
}


def load_processed():
    if os.path.exists(PROCESSED_LOG):
        with open(PROCESSED_LOG, "r") as f:
            return set(line.strip() for line in f if line.strip())
    return set()


def mark_processed(filename):
    with open(PROCESSED_LOG, "a") as f:
        f.write(filename + "\n")


def detect_center(text, folder_name=""):
    text_lower = text.lower()
    folder_lower = folder_name.lower().replace("-", "").replace(" ", "")
    # Direct folder name match (both sides normalized)
    for center in CENTER_KEYWORDS:
        if center.replace("-", "").replace(" ", "") == folder_lower:
            return center
        if center.replace("-", "").replace(" ", "") in folder_lower:
            return center
    # Then keyword match in folder name
    for center, kws in CENTER_KEYWORDS.items():
        if any(kw in folder_lower for kw in kws):
            return center
    # Then keyword match in text
    for center, kws in CENTER_KEYWORDS.items():
        if any(kw in text_lower for kw in kws):
            return center
    return "unknown"


def detect_counselor_name(text, sales_person=""):
    stop_words = {"i", "am", "this", "is", "a", "an", "the", "you", "he", "she",
                  "it", "we", "they", "my", "your", "his", "her", "calling",
                  "speaking", "from", "to", "are", "do", "did", "have", "has",
                  "talking", "telling", "only", "even", "now", "any", "been",
                  "being", "also", "just", "here", "there", "not", "no", "some",
                  "actually", "then", "very", "really", "studying", "lakme",
                  "lakmé", "lacme", "lakshmi", "academy", "sir", "ma'am", "mam",
                  "mr", "mrs", "ms", "miss", "i'm", "im", "dear", "hey"}
    all_lines = text.split(".")
    # Two-pass: first try sales_person lines, then all lines
    for pass_type in ["preferred", "all"]:
        for line in all_lines:
            line = line.strip()
            if not line or "?" in line:
                continue
            if pass_type == "preferred" and sales_person:
                if not line.lstrip().startswith(sales_person + ":"):
                    continue
            # Strip speaker label prefix
            content = re.sub(r'^SPEAKER_\d+:\s*', '', line).strip()
            lower_content = content.lower()

            # Pattern 1: "I am <Name> / This is <Name> ... from/speaking" (most specific)
            for trigger in ["speaking from", "calling from", "from", "speaking"]:
                if trigger not in lower_content:
                    continue
                idx = lower_content.index(trigger)
                before = content[:idx].strip()
                for prefix in ["i am", "this is"]:
                    pi = before.lower().rfind(prefix)
                    if pi < 0:
                        continue
                    name_text = before[pi + len(prefix):].strip().strip(".,!?:;")
                    if not name_text:
                        continue
                    words = name_text.split()
                    if len(words) > 3:
                        continue
                    clean = []
                    for w in words:
                        wc = w.strip(".,!?:;\"'")
                        if wc.lower() in stop_words:
                            break
                        clean.append(wc)
                    if clean:
                        name = clean[0].capitalize()
                        if len(name) > 1:
                            return name

            # Pattern 2: bare "Name speaking from" / "Name calling from" at start of utterance
            for trigger in ["speaking from", "calling from"]:
                if trigger not in lower_content:
                    continue
                before = content[:lower_content.index(trigger)].strip().strip(".,!?:;")
                if not before:
                    continue
                first_word = before.split()[0].strip(".,!?:;\"'") if before.split() else ""
                if first_word and first_word.lower() not in stop_words and len(first_word) > 1:
                    name = first_word.capitalize()
                    if name.lower() not in ("hello", "hi", "yes", "no", "okay", "ok",
                                             "sir", "ma'am", "mam", "mr", "mrs", "ms", "miss",
                                             "i'm", "im", "dear", "hey"):
                        return name
    return "Unknown"


def score_call(data):
    text = data.get("text", "").lower()
    agent_time = data.get("agent_speak_time", 0)
    cust_time = data.get("customer_speak_time", 0)
    longest_mono = data.get("longest_agent_monologue", 0)
    total_time = agent_time + cust_time
    dead_air = data.get("dead_air", 0)

    score = 0
    flags = []
    coach_notes = []
    dos_observed = []

    opening_score = 0
    if "lakshmi" in text:
        flags.append("Said 'Lakshmi Academy' instead of 'Lakme Academy'")
        coach_notes.append("Practice saying 'Lakme Academy' — brand name is critical")
    elif "lakme" in text or "lakmé" in text:
        opening_score = 5
        dos_observed.append("Correctly used brand name 'Lakme Academy'")
    else:
        opening_score = 2
        flags.append("Brand name not clearly mentioned")

    if any(g in text for g in ["hello", "hi", "good morning", "good evening"]):
        opening_score += 5
        dos_observed.append("Greeted the customer warmly")
    score += opening_score

    discovery_kws = ["makeup artist", "beginner", "experience", "currently",
                     "goal", "looking for", "interested in", "want to do"]
    matched = [kw for kw in discovery_kws if kw in text]
    discovery_score = min(len(matched) * 3, 18)

    if len(matched) >= 3:
        dos_observed.append("Asked qualification questions to understand the prospect")

    if "makeup artist" in text:
        flags.append("Customer IS a makeup artist — should upsell advanced courses")
        coach_notes.append("When customer says they're a pro, pitch advanced/international only")

    if not matched:
        flags.append("No discovery questions asked — didn't qualify the lead")
        coach_notes.append("Always ask: current level? goal? timeline? budget?")
    score += discovery_score

    clarity_score = 10
    if "48" in text or "many courses" in text:
        clarity_score -= 6
        flags.append("Course dumping — overwhelmed customer with too many options")
        coach_notes.append("Don't list all courses. Ask first, recommend ONE.")

    if any(kw in text for kw in ["suggest you", "recommend", "best for you"]):
        clarity_score += 5
        dos_observed.append("Gave a specific course recommendation instead of listing all")

    if longest_mono > 30:
        clarity_score -= 4
        flags.append(f"{longest_mono}s monologue — too long, lost the customer")
        coach_notes.append("Keep explanations under 20 seconds. Ask a question.")
    score += max(clarity_score, 0)

    fee_score = 5
    for kw in ["placement", "certification", "job", "career", "brand"]:
        if kw in text:
            fee_score += 2

    if any(kw in text for kw in ["placement", "certification", "job", "career"]):
        dos_observed.append("Built value by mentioning placement/career outcomes")

    price_words = ["30,000", "50,000", "90,000", "1,20,000", "25,000", "1,50,000", "2.5 lakh"]
    price_count = sum(1 for p in price_words if p in text)
    if price_count > 3:
        flags.append(f"{price_count} different prices mentioned — confusing")
        coach_notes.append("Give max 3 tiers: Basic -> Pro -> Global. Keep simple.")
        fee_score -= 4

    early_price = False
    for pw in ["rupees", "rs", "price", "cost", "fee"] + price_words:
        idx = text.find(pw)
        if 0 <= idx < 200:
            early_price = True
            break
    if early_price:
        flags.append("Price mentioned too early — establish value first")
        coach_notes.append("Build course value before discussing price")
        fee_score -= 3

    if not early_price and any(kw in text for kw in ["placement", "certification", "brand"]):
        dos_observed.append("Built value before discussing price")

    score += max(fee_score, 2)

    close_score = 0
    for kw in ["visit", "come", "center", "studio", "see", "meet"]:
        if kw in text:
            close_score += 4

    if not any(kw in text for kw in ["visit", "come", "center"]):
        flags.append("No visit booked — biggest miss")
        coach_notes.append("Goal of every call is a visit. Ask: 'Come see the center at 4?'")
        close_score = 0

    if any(kw in text for kw in ["visit", "come", "center"]):
        dos_observed.append("Attempted to book a center visit")

    if "tomorrow" in text or "today" in text:
        close_score += 4
        dos_observed.append("Used specific time anchors (today/tomorrow) for closing")

    if any(kw in text for kw in ["check and report", "let me know", "revert"]):
        flags.append("Passive ending — put ball in customer's court")
        coach_notes.append("End with firm next step: 'I'll call you tomorrow at 11. OK?'")
        close_score -= 4

    score += max(min(close_score, 20), 0)

    if total_time > 0:
        ratio = agent_time / total_time
        if ratio > 0.65:
            flags.append(f"Agent speaking {ratio*100:.0f}% of time — listen more")
            coach_notes.append("60:40 ratio is ideal. Ask more questions.")
            score -= 10
        elif ratio > 0.60:
            score -= 5
        else:
            score += 5
            dos_observed.append("Maintained good talk/listen ratio (60:40 or better)")

    if dead_air > 20:
        flags.append(f"{dead_air}s dead air — awkward silence")
        coach_notes.append("If stuck: 'Let me check the best option for you...'")
        score -= 5

    score = max(0, min(100, score))

    if score >= 80:
        grade = "Excellent"
    elif score >= 60:
        grade = "Good — needs polish"
    elif score >= 40:
        grade = "Average — needs retraining"
    elif score >= 20:
        grade = "Poor — urgent coaching"
    else:
        grade = "Critical — immediate intervention"

    agent_name = detect_counselor_name(data.get("text", ""), data.get("sales_person", ""))

    return {
        "score": score,
        "grade": grade,
        "flags": flags,
        "coach_notes": coach_notes,
        "dos_observed": dos_observed,
        "agent_speak_pct": round(agent_time / total_time * 100, 1) if total_time else 0,
        "dead_air": dead_air,
        "longest_monologue": longest_mono,
        "duration_mins": round(total_time / 60, 1),
        "agent_name": agent_name,
    }


def analyze_file(filepath):
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
    except Exception as e:
        print(f"  Error reading {os.path.basename(filepath)}: {e}")
        return None

    if isinstance(data, list) and len(data) > 0:
        data = data[0]

    result = score_call(data)
    result["file"] = os.path.basename(filepath)
    result["timestamp"] = datetime.now().strftime("%d %b %Y, %I:%M %p")
    result["center"] = detect_center(data.get("text", ""), os.path.basename(os.path.dirname(filepath)))
    return result


def generate_daily_report(analyses):
    if not analyses:
        print("No calls to report.")
        return

    scores = [a["score"] for a in analyses]
    avg_score = sum(scores) / len(scores)
    all_flags = []
    all_coach = []
    for a in analyses:
        all_flags.extend(a["flags"])
        all_coach.extend(a["coach_notes"])

    flag_counts = Counter(all_flags)
    coach_counts = Counter(all_coach)

    date_str = datetime.now().strftime("%d %b %Y")
    filename = f"report-{datetime.now().strftime('%Y-%m-%d')}.txt"
    filepath = os.path.join(REPORTS_DIR, filename)

    lines = []
    lines.append("=" * 60)
    lines.append(f"  DAILY CALL REPORT — {date_str}")
    lines.append("=" * 60)
    lines.append("")
    lines.append(f"  Total calls analyzed: {len(analyses)}")
    lines.append(f"  Average score:        {avg_score:.0f}/100")
    lines.append(f"  Best call:            {max(scores)}/100")
    lines.append(f"  Worst call:           {min(scores)}/100")
    lines.append("")

    lines.append("-" * 60)
    lines.append("  PER-CALL BREAKDOWN")
    lines.append("-" * 60)
    for a in sorted(analyses, key=lambda x: x["score"], reverse=True):
        emoji = ""
        if a["score"] >= 80:
            emoji = ""
        elif a["score"] >= 50:
            emoji = ""
        elif a["score"] >= 30:
            emoji = ""
        else:
            emoji = ""

        lines.append(f"  {emoji} {a['agent_name']:15s}  {a['score']:2d}/100  {a['grade']}")
        lines.append(f"     File: {a['file']}")
        lines.append(f"     Center: {a.get('center', 'unknown')}  |  Duration: {a['duration_mins']} min  |  Agent: {a['agent_speak_pct']}%  |  Dead air: {a['dead_air']}s")
        if a["flags"]:
            for f in a["flags"][:3]:
                lines.append(f"     Flag: {f}")
        lines.append("")

    lines.append("-" * 60)
    lines.append("  TOP MISTAKES THIS PERIOD")
    lines.append("-" * 60)
    for flag, count in flag_counts.most_common(8):
        bar = "#" * count
        lines.append(f"  {flag:50s} ({count}x) {bar}")

    lines.append("")
    lines.append("-" * 60)
    lines.append("  COACHING PRIORITIES")
    lines.append("-" * 60)
    for note, count in coach_counts.most_common(5):
        lines.append(f"  > {note}")

    lines.append("")
    lines.append("=" * 60)
    lines.append(f"  Report saved: {filename}")
    lines.append("=" * 60)

    report_text = "\n".join(lines)
    with open(filepath, "w") as f:
        f.write(report_text)

    print(report_text)
    return filepath


def generate_master_report(all_analyses):
    if not all_analyses:
        print("No calls to report.")
        return

    scores = [a["score"] for a in all_analyses]
    avg_score = sum(scores) / len(scores)

    all_flags = []
    all_coach = []
    all_dos = []
    for a in all_analyses:
        all_flags.extend(a["flags"])
        all_coach.extend(a["coach_notes"])
        all_dos.extend(a.get("dos_observed", []))

    flag_counts = Counter(all_flags)
    coach_counts = Counter(all_coach)
    dos_counts = Counter(all_dos)

    centers = defaultdict(list)
    counselors = defaultdict(list)
    for a in all_analyses:
        centers[a.get("center", "unknown")].append(a)
        counselors[a["agent_name"]].append(a)

    top_calls = sorted(all_analyses, key=lambda x: x["score"], reverse=True)[:5]
    bottom_calls = sorted(all_analyses, key=lambda x: x["score"])[:5]
    top_count = max(1, len(all_analyses) // 5)

    date_str = datetime.now().strftime("%d %b %Y")
    filename_txt = f"master-report-{datetime.now().strftime('%Y-%m-%d')}.txt"
    filepath_txt = os.path.join(REPORTS_DIR, filename_txt)

    lines = []
    lines.append("=" * 60)
    lines.append(f"  MASTER QUALITY REPORT — {date_str}")
    lines.append("=" * 60)
    lines.append("")
    lines.append(f"  Total calls analyzed: {len(all_analyses)}")
    lines.append(f"  Average score:        {avg_score:.0f}/100")
    lines.append(f"  Best call:            {max(scores)}/100")
    lines.append(f"  Worst call:           {min(scores)}/100")
    lines.append("")

    lines.append("-" * 60)
    lines.append("  CENTER-WISE BREAKDOWN")
    lines.append("-" * 60)
    for center, c_calls in sorted(centers.items()):
        c_scores = [c["score"] for c in c_calls]
        c_avg = sum(c_scores) / len(c_scores)
        lines.append(f"  {center:20s}  {len(c_calls):2d} calls  avg {c_avg:.0f}/100  best {max(c_scores)}  worst {min(c_scores)}")
    lines.append("")

    lines.append("-" * 60)
    lines.append("  COUNSELOR RANKINGS")
    lines.append("-" * 60)
    for counselor, c_calls in sorted(counselors.items()):
        c_scores = [c["score"] for c in c_calls]
        c_avg = sum(c_scores) / len(c_scores)
        lines.append(f"  {counselor:20s}  {len(c_calls):2d} calls  avg {c_avg:.0f}/100  best {max(c_scores)}  worst {min(c_scores)}")
    lines.append("")

    lines.append("=" * 60)
    lines.append("  DON'TS — TOP MISTAKES ACROSS ALL CALLS")
    lines.append("=" * 60)
    for flag, count in flag_counts.most_common(15):
        pct = round(count / len(all_analyses) * 100)
        bar = chr(9608) * (pct // 5 + 1)
        lines.append(f"  {pct:2d}%  {bar}  {flag} ({count}x)")
    lines.append("")

    lines.append("=" * 60)
    lines.append("  DO'S — WHAT HIGH SCORERS DO DIFFERENTLY")
    lines.append("=" * 60)
    top_10_pct = sorted(all_analyses, key=lambda x: x["score"], reverse=True)[:max(1, len(all_analyses)//10)]
    top_dos = Counter()
    for a in top_10_pct:
        for d in a.get("dos_observed", []):
            top_dos[d] += 1
    for do_action, count in top_dos.most_common(10):
        lines.append(f"  - {do_action}")
    if not top_dos:
        lines.append("  (Not enough high-scoring calls to identify patterns)")
    lines.append("")

    lines.append("=" * 60)
    lines.append("  CHEAT SHEET: DO'S & DON'TS")
    lines.append("=" * 60)
    lines.append("")
    lines.append("  DON'T:")
    for flag, count in flag_counts.most_common(10):
        lines.append("    " + flag)
    lines.append("")
    lines.append("  DO:")
    seen_dos = set()
    for do_action, count in top_dos.most_common(10):
        if do_action not in seen_dos:
            lines.append(f"    {do_action}")
            seen_dos.add(do_action)
    if not top_dos:
        lines.append("    (Patterns will emerge after processing more calls)")
    lines.append("")

    lines.append("=" * 60)
    lines.append("  COACHING PRIORITIES (by frequency)")
    lines.append("=" * 60)
    for note, count in coach_counts.most_common(10):
        pct = round(count / len(all_analyses) * 100)
        lines.append(f"  {pct:2d}%  {note}")
    lines.append("")

    lines.append("=" * 60)
    lines.append("  PER-CALL DETAILS")
    lines.append("=" * 60)
    for a in sorted(all_analyses, key=lambda x: x["score"]):
        emoji = ""
        if a["score"] >= 80:
            emoji = ""
        elif a["score"] >= 50:
            emoji = ""
        elif a["score"] >= 30:
            emoji = ""
        else:
            emoji = ""
        lines.append(f"  {emoji} {a['agent_name']:15s}  {a['score']:2d}/100  [{a.get('center', '?')}]  {a['grade']}")
        lines.append(f"      {a['file']}  |  {a['duration_mins']} min  |  Agent {a['agent_speak_pct']}%  |  Flags: {len(a['flags'])}")
        if a["flags"]:
            for f in a["flags"]:
                lines.append(f"       - {f}")
    lines.append("")
    lines.append("=" * 60)
    lines.append(f"  Report saved: {filename_txt}")
    lines.append("=" * 60)

    report_text = "\n".join(lines)
    with open(filepath_txt, "w") as f:
        f.write(report_text)
    print(report_text)

    json_path = os.path.join(REPORTS_DIR, f"master-data-{datetime.now().strftime('%Y-%m-%d')}.json")
    export = {
        "generated_at": date_str,
        "total_calls": len(all_analyses),
        "avg_score": round(avg_score, 1),
        "best_score": max(scores),
        "worst_score": min(scores),
        "centers": {
            center: {
                "total": len(c_calls),
                "avg_score": round(sum(c["score"] for c in c_calls) / len(c_calls), 1),
                "best": max(c["score"] for c in c_calls),
                "worst": min(c["score"] for c in c_calls),
            }
            for center, c_calls in sorted(centers.items())
        },
        "counselors": {
            name: {
                "total": len(c_calls),
                "avg_score": round(sum(c["score"] for c in c_calls) / len(c_calls), 1),
                "best": max(c["score"] for c in c_calls),
                "worst": min(c["score"] for c in c_calls),
            }
            for name, c_calls in sorted(counselors.items())
        },
        "top_mistakes": [{"mistake": f, "count": c, "pct": round(c/len(all_analyses)*100)}
                         for f, c in flag_counts.most_common(15)],
        "dos": [{"action": d, "count": c} for d, c in dos_counts.most_common(10)],
        "coaching_priorities": [{"note": n, "count": c} for n, c in coach_counts.most_common(10)],
        "calls": [{
            "agent_name": a["agent_name"],
            "score": a["score"],
            "grade": a["grade"],
            "center": a.get("center", "unknown"),
            "file": a["file"],
            "duration_mins": a["duration_mins"],
            "agent_speak_pct": a["agent_speak_pct"],
            "dead_air": a["dead_air"],
            "flags": a["flags"],
            "coach_notes": a["coach_notes"],
        } for a in sorted(all_analyses, key=lambda x: x["score"], reverse=True)],
    }
    with open(json_path, "w") as f:
        json.dump(export, f, indent=2)
    print(f"\nJSON data exported: {json_path}")

    return filepath_txt, json_path


def scan_all_calls():
    if not os.path.exists(CALLS_DIR):
        os.makedirs(CALLS_DIR)
        return []

    all_analyses = []

    top_jsons = sorted(glob.glob(os.path.join(CALLS_DIR, "*.json")))
    for f in top_jsons:
        r = analyze_file(f)
        if r:
            all_analyses.append(r)

    for item in os.listdir(CALLS_DIR):
        sub = os.path.join(CALLS_DIR, item)
        if os.path.isdir(sub):
            for f in sorted(glob.glob(os.path.join(sub, "*.json"))):
                r = analyze_file(f)
                if r:
                    all_analyses.append(r)

    return all_analyses


def process_all(show_report=True):
    if not os.path.exists(CALLS_DIR):
        os.makedirs(CALLS_DIR)
        print(f"Created calls/ folder. Put your Superleap JSON files in there.")
        return

    all_analyses = scan_all_calls()

    if not all_analyses:
        print("No JSON files found in calls/ folder.")
        return

    processed = load_processed()
    new_analyses = []

    for a in all_analyses:
        fname = a["file"]
        if fname in processed:
            continue
        new_analyses.append(a)
        mark_processed(fname)

    if not new_analyses:
        print("No new calls to process. All files already analyzed.")
        return

    print(f"\nProcessed {len(new_analyses)} new call(s).\n")
    for a in new_analyses:
        emoji = "" if a["score"] >= 50 else ""
        print(f"  {emoji} {a['agent_name']:15s}  {a['score']:2d}/100  {a['grade']}")

    if show_report and new_analyses:
        print("\n" + "=" * 60)
        generate_daily_report(new_analyses)

    return new_analyses


def watch_mode():
    print("Watching calls/ folder for new JSON files... (Ctrl+C to stop)")
    while True:
        process_all(show_report=False)
        time.sleep(30)


if __name__ == "__main__":
    if "--file" in sys.argv:
        idx = sys.argv.index("--file")
        path = sys.argv[idx + 1]
        if os.path.exists(path):
            r = analyze_file(path)
            if r:
                print(f"\n  Counselor: {r['agent_name']}")
                print(f"  Center: {r.get('center', 'unknown')}")
                print(f"  Score: {r['score']}/100 — {r['grade']}")
                print(f"  Duration: {r['duration_mins']} min | Agent: {r['agent_speak_pct']}% | Dead air: {r['dead_air']}s")
                print(f"  Flags ({len(r['flags'])}):")
                for f in r['flags']:
                    print(f"    - {f}")
                if r['coach_notes']:
                    print(f"  Coaching:")
                    for n in r['coach_notes']:
                        print(f"    > {n}")
        else:
            print(f"File not found: {path}")

    elif "--master" in sys.argv:
        print("Scanning all calls across all centers...")
        all_analyses = scan_all_calls()
        if all_analyses:
            generate_master_report(all_analyses)
            # Auto-build training.html + embed data
            try:
                import subprocess
                base = os.path.dirname(__file__)
                build_script = os.path.join(base, "build_training_complete.py")
                embed_script = os.path.join(base, "embed_data.py")
                subprocess.run(["python3", build_script], capture_output=True)
                subprocess.run(["python3", embed_script], capture_output=True)
                print("  Training playbook built: training.html (ready to share)")
                print("  Report:                  master-report.html")
            except Exception as e:
                print(f"  Build/embed warning: {e}")
                print("  Run python3 -m http.server to view the HTML report.")
        else:
            print("No calls found.")

    elif "--report" in sys.argv:
        all_analyses = scan_all_calls()
        if all_analyses:
            generate_daily_report(all_analyses)
        else:
            print("No calls to report.")

    elif "--watch" in sys.argv:
        watch_mode()

    else:
        process_all()
