"""
WhatsApp Sender — Meta Cloud API Integration

Sends messages via Meta's official WhatsApp Cloud API (free tier).
Use this to:
  - Send daily call reports to manager
  - Send brochures to leads after call analysis
  - Send visit reminders

SETUP:
  1. Go to https://developers.facebook.com → Create App → Business
  2. Add WhatsApp → Get your Phone Number ID & Access Token
  3. Put them in config.json (see config.example.json)
  4. Test: python3 whatsapp_sender.py --test

USAGE:
    python3 whatsapp_sender.py --report              Send daily report to manager
    python3 whatsapp_sender.py --brochure "+9199..."  Send brochure to a lead
    python3 whatsapp_sender.py --message "+9199..." "Your message here"
"""

import json
import os
import sys
import requests
from datetime import datetime

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")


def load_config():
    if not os.path.exists(CONFIG_FILE):
        print(f"❌ config.json not found. Create one with:")
        print(f'  {{')
        print(f'    "whatsapp_token": "your-access-token",')
        print(f'    "phone_number_id": "your-phone-number-id",')
        print(f'    "manager_phone": "+9198XXXXXXXX"')
        print(f'  }}')
        sys.exit(1)

    with open(CONFIG_FILE, "r") as f:
        return json.load(f)


def send_whatsapp(phone, message, preview_url=False):
    """Send a plain text WhatsApp message."""
    config = load_config()
    token = config["whatsapp_token"]
    phone_id = config["phone_number_id"]

    url = f"https://graph.facebook.com/v18.0/{phone_id}/messages"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    data = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "text",
        "text": {"body": message, "preview_url": preview_url},
    }

    try:
        resp = requests.post(url, headers=headers, json=data, timeout=10)
        if resp.status_code == 200:
            print(f"  ✓ Message sent to {phone}")
            return True
        else:
            print(f"  ✗ Failed ({resp.status_code}): {resp.text}")
            return False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def send_template(phone, template_name, params=None):
    """Send a pre-approved WhatsApp template message."""
    config = load_config()
    token = config["whatsapp_token"]
    phone_id = config["phone_number_id"]

    url = f"https://graph.facebook.com/v18.0/{phone_id}/messages"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    components = []
    if params:
        components.append({
            "type": "body",
            "parameters": [{"type": "text", "text": p} for p in params]
        })

    data = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "template",
        "template": {
            "name": template_name,
            "language": {"code": "en"},
        },
    }
    if components:
        data["template"]["components"] = components

    try:
        resp = requests.post(url, headers=headers, json=data, timeout=10)
        if resp.status_code == 200:
            print(f"  ✓ Template sent to {phone}")
            return True
        else:
            print(f"  ✗ Failed ({resp.status_code}): {resp.text}")
            return False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def send_brochure(phone):
    """Send course brochure (as text with link) to a lead."""
    message = (
        "Hi! Here's the Lakmé Academy course brochure:\n"
        "https://www.lakme-academy.com/courses\n\n"
        "Foundation, Advanced, Bridal & International courses available.\n"
        "Visit us at Sector 18, Noida for a free demo!\n"
        "Call: +91-XXXXXXXXXX"
    )
    return send_whatsapp(phone, message)


def send_visit_reminder(phone, date, time):
    """Send a visit reminder."""
    message = (
        f"Reminder: Your visit to Lakmé Academy is confirmed for "
        f"{date} at {time}.\n"
        f"📍 Sector 18, Noida (near metro)\n"
        f"See you there!"
    )
    return send_whatsapp(phone, message)


def send_daily_report(analyses):
    """Send daily call report to manager's WhatsApp."""
    config = load_config()
    manager_phone = config.get("manager_phone", "")
    if not manager_phone:
        print("❌ manager_phone not set in config.json")
        return

    if not analyses:
        send_whatsapp(manager_phone, "📊 No calls today.")
        return

    scores = [a["score"] for a in analyses]
    avg = sum(scores) / len(scores)
    worst = min(analyses, key=lambda x: x["score"])

    # Short summary (WhatsApp-friendly)
    message = (
        f"📊 DAILY CALL REPORT\n"
        f"{datetime.now().strftime('%d %b %Y')}\n"
        f"━━━━━━━━━━━━━━━━━\n"
        f"Calls: {len(analyses)}\n"
        f"Avg score: {avg:.0f}/100\n"
        f"Best: {max(scores)}/100\n"
        f"Worst: {worst['score']}/100 ({worst['agent_name']})\n"
    )

    # Add per-call scores
    for a in sorted(analyses, key=lambda x: x["score"]):
        icon = "" if a["score"] >= 50 else ""
        message += f"\n{icon} {a['agent_name']}: {a['score']}/100"

    # Top flags
    from collections import Counter
    all_flags = []
    for a in analyses:
        all_flags.extend(a["flags"])
    if all_flags:
        top = Counter(all_flags).most_common(3)
        message += "\n\n🔴 TOP ISSUES:"
        for flag, count in top:
            message += f"\n  {flag} ({count}x)"

    send_whatsapp(manager_phone, message)


def test_connection():
    """Test if WhatsApp API credentials are working."""
    config = load_config()
    token = config["whatsapp_token"]
    phone_id = config["phone_number_id"]

    url = f"https://graph.facebook.com/v18.0/{phone_id}"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            print(f"  ✓ Connected! Phone: {data.get('display_phone_number', 'Unknown')}")
            print(f"  ✓ Name: {data.get('display_name', 'Unknown')}")
            return True
        else:
            print(f"  ✗ Connection failed ({resp.status_code}): {resp.text}")
            return False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


if __name__ == "__main__":
    if "--test" in sys.argv:
        test_connection()

    elif "--report" in sys.argv:
        # Import analyzer and run
        sys.path.insert(0, os.path.dirname(__file__))
        from analyze_calls import analyze_file
        import glob

        calls_dir = os.path.join(os.path.dirname(__file__), "calls")
        analyses = []
        for f in sorted(glob.glob(os.path.join(calls_dir, "*.json"))):
            r = analyze_file(f)
            if r:
                analyses.append(r)
        send_daily_report(analyses)

    elif "--brochure" in sys.argv:
        idx = sys.argv.index("--brochure")
        phone = sys.argv[idx + 1]
        send_brochure(phone)

    elif "--message" in sys.argv:
        idx = sys.argv.index("--message")
        phone = sys.argv[idx + 1]
        msg = " ".join(sys.argv[idx + 2:])
        send_whatsapp(phone, msg)

    elif "--reminder" in sys.argv:
        idx = sys.argv.index("--reminder")
        phone = sys.argv[idx + 1]
        date = sys.argv[idx + 2]
        time = sys.argv[idx + 3]
        send_visit_reminder(phone, date, time)

    else:
        print("""
Usage:
  python3 whatsapp_sender.py --test                 Test API connection
  python3 whatsapp_sender.py --report               Send daily report to manager
  python3 whatsapp_sender.py --brochure "+9199..."  Send brochure to lead
  python3 whatsapp_sender.py --message "+9199..." "Hi there"
  python3 whatsapp_sender.py --reminder "+9199..." "27 May" "4 PM"

First time setup:
  1. Create a Meta Business account
  2. Get WhatsApp Cloud API credentials
  3. Create config.json (see config.example.json)
""")
