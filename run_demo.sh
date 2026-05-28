#!/bin/bash

# ═══════════════════════════════════════════════════════════════
#  LAKMÉ ACADEMY — Call Analyzer Demo
#  Run this to see the full system in action (no API keys needed)
# ═══════════════════════════════════════════════════════════════

clear
echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║     LAKMÉ ACADEMY CALL ANALYZER — DEMO          ║"
echo "║     See the full system in 60 seconds            ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""

# Step 1: Show what's in the system
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  STEP 1: What's in your system"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  📁 calls/ ─── has 1 real Superleap JSON file"
echo "  🐍 analyze_calls.py ─── the scoring engine"
echo "  🐍 whatsapp_sender.py ─── WhatsApp (needs API key)"
echo "  📄 counselor-playbook.md ─── call script"
echo "  📄 reports/ ─── where reports are saved"
echo ""

read -p "  Press Enter to analyze the call → "
clear

# Step 2: Run the analyzer
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  STEP 2: Analyzing the call..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

python3 analyze_calls.py

echo ""
read -p "  Press Enter to see the report → "
clear

# Step 3: Show the report
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  STEP 3: The Daily Report (auto-generated)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Show the latest report
latest_report=$(ls -t reports/report-*.txt 2>/dev/null | head -1)
if [ -n "$latest_report" ]; then
    cat "$latest_report"
else
    echo "  No report found. Run: python3 analyze_calls.py"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  ✅ DEMO COMPLETE"
echo ""
echo "  What you just saw:"
echo "    • 1 real call from Superleap → scored automatically"
echo "    • Score: 8/100 (Critical)"
echo "    • 8 flags detected (brand error, course dump, no close...)"
echo "    • Coaching notes generated"
echo "    • Report saved to reports/ folder"
echo ""
echo "  To run this daily:"
echo "    1. Get JSON files from Superleap"
echo "    2. Drop them in the calls/ folder"
echo "    3. Run: python3 analyze_calls.py"
echo "    4. Open reports/report-YYYY-MM-DD.txt"
echo ""
echo "  To get WhatsApp reports on your phone:"
echo "    • Get WhatsApp API key from Meta (free)"
echo "    • Add to config.json"
echo "    • Run: python3 whatsapp_sender.py --report"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
