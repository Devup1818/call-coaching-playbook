#!/usr/bin/env python3
"""Build complete training.html with Hindi/English language support."""
import os, json

BASE = os.path.dirname(os.path.abspath(__file__))

def read_latest_data():
    reports_dir = os.path.join(BASE, "reports")
    jsons = [f for f in os.listdir(reports_dir) if f.startswith("master-data-") and f.endswith(".json")]
    if not jsons:
        print("ERROR: No master-data JSON found")
        return None
    latest = max(jsons, key=lambda f: os.path.getmtime(os.path.join(reports_dir, f)))
    with open(os.path.join(reports_dir, latest)) as f:
        return json.load(f)

def build_html():
    data = read_latest_data()
    if not data:
        return

    html_path = os.path.join(BASE, "training.html")

    # Read the build_training_html.py that already has the CSS and HTML structure
    # We just need to append the JS with all translations

    # === CSS + HTML ===
    html = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>Call Coaching Playbook &mdash; Lakm&eacute; Academy</title>
<style>
  *{margin:0;padding:0;box-sizing:border-box}
.js-warning{display:none;background:#dc2626;color:#fff;text-align:center;padding:14px 16px;font-size:14px;line-height:1.5}
.js-warning a{color:#fef08a;font-weight:600;text-decoration:underline}
html:not(.js-run) .js-warning{display:block}
  body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#f8f6f3;color:#1a1a2e;line-height:1.6;font-size:15px}
  .hero{background:linear-gradient(135deg,#0f172a 0%,#1e293b 50%,#334155 100%);color:#fff;padding:40px 16px 32px;text-align:center;position:relative}
  .lang-selector{position:absolute;top:16px;right:16px;display:flex;gap:2px;background:rgba(255,255,255,.1);border-radius:8px;padding:3px}
  .lang-selector button{padding:6px 14px;border-radius:6px;border:none;font-size:13px;font-weight:600;cursor:pointer;transition:all .15s;background:transparent;color:rgba(255,255,255,.5)}
  .lang-selector button.active{background:#f97316;color:#fff}
  @media (max-width:480px){.lang-selector{top:10px;right:10px}.lang-selector button{padding:4px 10px;font-size:11px}}
  .hero h1{font-size:clamp(22px,6vw,44px);font-weight:800;letter-spacing:-.03em}
  .hero h1 span{color:#f97316}
  .hero p{margin-top:6px;color:rgba(255,255,255,.5);font-size:clamp(12px,3vw,15px)}
  .hero .meta{margin-top:14px;display:flex;justify-content:center;gap:12px;flex-wrap:wrap}
  .hero .meta-item{padding:6px 12px;border-radius:8px;background:rgba(255,255,255,.06)}
  .hero .meta-item .num{font-size:clamp(18px,4vw,28px);font-weight:800}
  .hero .meta-item .lbl{font-size:10px;text-transform:uppercase;letter-spacing:.5px;opacity:.6}
  .hero .share-bar{margin-top:16px;display:flex;justify-content:center;gap:8px;flex-wrap:wrap}
  .hero .share-bar button,.hero .share-bar a{display:inline-flex;align-items:center;gap:6px;padding:8px 16px;border-radius:8px;border:1px solid rgba(255,255,255,.15);background:rgba(255,255,255,.08);color:#fff;font-size:13px;font-weight:500;cursor:pointer;text-decoration:none;transition:background .15s}
  .hero .share-bar button:hover,.hero .share-bar a:hover{background:rgba(255,255,255,.18)}
  .share-tip{margin-top:8px;font-size:11px;color:rgba(255,255,255,.35)}
  .container{max-width:1100px;margin:0 auto;padding:24px 12px}
  .tab-bar{display:flex;gap:3px;margin-bottom:20px;background:#e2e0db;padding:4px;border-radius:10px;flex-wrap:wrap;overflow-x:auto;-webkit-overflow-scrolling:touch}
  .tab{padding:7px 12px;border-radius:7px;font-size:clamp(11px,2.5vw,13px);font-weight:500;cursor:pointer;transition:all .15s;border:none;background:none;color:#6b7280;white-space:nowrap}
  .tab.active{background:#fff;box-shadow:0 1px 4px rgba(0,0,0,.08);color:#1a1a2e;font-weight:600}
  .tab-page{display:none}.tab-page.active{display:block}
  .section-title{font-size:clamp(17px,4vw,22px);font-weight:700;margin-bottom:12px}
  .card{background:#fff;border-radius:14px;padding:clamp(16px,4vw,28px);margin-bottom:20px;box-shadow:0 1px 4px rgba(0,0,0,.05)}
  .dos-donts-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}
  @media (max-width:640px){.dos-donts-grid{grid-template-columns:1fr}}
  .dos-box,.donts-box{border-radius:10px;padding:14px}
  .dos-box{background:#f0fdf4;border:1px solid #bbf7d0}
  .donts-box{background:#fef2f2;border:1px solid #fecaca}
  .dos-box h3,.donts-box h3{font-size:14px;font-weight:700;margin-bottom:8px}
  .dos-box h3{color:#15803d}.donts-box h3{color:#dc2626}
  .dos-list,.donts-list{font-size:14px}
  .dos-list>div,.donts-list>div{padding:7px 0;border-bottom:1px solid rgba(0,0,0,.04);display:flex;align-items:flex-start;gap:6px}
  .badge{display:inline-block;padding:2px 8px;border-radius:20px;font-size:11px;font-weight:600;white-space:nowrap;flex-shrink:0}
  .badge.green{background:#bbf7d0;color:#15803d}.badge.red{background:#fecaca;color:#dc2626}
  .say-this-grid{display:grid;gap:10px;margin-top:16px}
  .say-pair{display:grid;grid-template-columns:1fr 1fr;gap:10px;padding:12px;border-radius:10px;background:#fafaf9;border:1px solid #e5e2dd}
  @media (max-width:640px){.say-pair{grid-template-columns:1fr}}
  .say-pair .label{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.3px;margin-bottom:4px}
  .say-pair .text{font-size:13px;line-height:1.5}
  .say-pair .note{font-size:12px;color:#6b7280;margin-top:4px;padding:6px 8px;background:#fffbeb;border-radius:6px}
  .golden-rules{margin-top:20px}
  .golden-rules h3{font-size:16px;font-weight:700;margin-bottom:12px;color:#1e293b}
  .golden-rule{display:flex;gap:10px;padding:10px 12px;margin-bottom:8px;background:#f8fafc;border-radius:8px;border-left:3px solid #f97316;font-size:14px;align-items:flex-start}
  .golden-rule .num{flex-shrink:0;width:24px;height:24px;border-radius:50%;background:#f97316;color:#fff;font-size:12px;font-weight:700;display:flex;align-items:center;justify-content:center}
  .flow-step{display:flex;gap:12px;padding:14px;margin-bottom:12px;background:#fafaf9;border-radius:10px;border:1px solid #e5e2dd}
  .step-num{flex-shrink:0;width:32px;height:32px;border-radius:50%;background:#1e293b;color:#fff;font-size:14px;font-weight:700;display:flex;align-items:center;justify-content:center}
  .step-title{font-size:14px;font-weight:700;margin-bottom:4px}
  .step-desc{font-size:13px;color:#6b7280;margin-bottom:6px}
  .step-do,.step-dont{font-size:13px;margin-bottom:3px}
  .step-do{color:#15803d}.step-dont{color:#dc2626}
  .step-sub-points{margin-top:6px;padding-left:16px;font-size:12px;color:#6b7280}
  .step-sub-points li{margin-bottom:3px}
  .script-compare{display:grid;grid-template-columns:1fr 1fr;gap:12px}
  @media (max-width:640px){.script-compare{grid-template-columns:1fr}}
  .script-box{padding:12px;border-radius:8px;font-size:13px;line-height:1.6}
  .script-box.before{background:#fef2f2;border:1px solid #fecaca}
  .script-box.after{background:#f0fdf4;border:1px solid #bbf7d0}
  .script-box .label{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.3px;margin-bottom:6px}
  .objection-card{margin-bottom:10px;border-radius:10px;overflow:hidden;border:1px solid #e5e2dd}
  .objection-header{padding:12px 14px;background:#fafaf9;cursor:pointer;display:flex;justify-content:space-between;align-items:center;font-weight:600;font-size:14px;user-select:none;-webkit-tap-highlight-color:transparent}
  .objection-header .arrow{transition:transform .2s;font-size:12px}
  .objection-header.open .arrow{transform:rotate(180deg)}
  .objection-body{display:none;padding:14px;background:#fff;border-top:1px solid #e5e2dd}
  .objection-body.open{display:block}
  .roleplay-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:10px;margin-bottom:16px}
  .roleplay-card{padding:14px 10px;text-align:center;border-radius:10px;border:2px solid #e5e2dd;cursor:pointer;transition:all .15s;background:#fff;-webkit-tap-highlight-color:transparent}
  .roleplay-card:hover{border-color:#f97316}
  .roleplay-card .emoji{font-size:28px;margin-bottom:6px}
  .roleplay-card .title{font-size:13px;font-weight:600}
  .roleplay-card .sub{font-size:11px;color:#6b7280}
  .roleplay-detail{display:none;padding:16px;background:#fafaf9;border-radius:10px;border:1px solid #e5e2dd}
  .roleplay-detail.open,.objection-body.open{display:block}
  .center-tips{display:grid;gap:14px}
  .center-tip-card{background:#fff;border-radius:10px;padding:16px;border:1px solid #e5e2dd;border-top:4px solid}
  .center-tip-card .name{font-size:16px;font-weight:700;margin-bottom:4px}
  .center-tip-card .stat{font-size:13px;color:#6b7280;margin-bottom:10px}
  .center-tip-card .tip-list ol{padding-left:18px;color:#6b7280;font-size:13px}
  .footer{text-align:center;padding:24px 12px;font-size:12px;color:#9ca3af}
  #loading{text-align:center;padding:60px 20px}
  .preso-overlay{position:fixed;top:0;left:0;width:100%;height:100%;background:#0f172a;color:#fff;z-index:9999;display:none;flex-direction:column;overflow:hidden;font-size:clamp(16px,3vw,22px)}
  .preso-overlay.active{display:flex}
  .preso-slide{flex:1;display:flex;flex-direction:column;justify-content:center;align-items:center;padding:40px 24px;text-align:center;overflow-y:auto}
  .preso-slide .slide-icon{font-size:clamp(40px,10vw,72px);margin-bottom:16px}
  .preso-slide .slide-title{font-size:clamp(20px,5vw,36px);font-weight:800;margin-bottom:12px}
  .preso-slide .slide-sub{font-size:clamp(14px,3vw,20px);color:rgba(255,255,255,.6);margin-bottom:20px}
  .preso-slide .slide-body{font-size:clamp(14px,2.5vw,18px);max-width:700px;line-height:1.7;color:rgba(255,255,255,.8)}
  .preso-slide .slide-body strong,.preso-slide .slide-body .gold{color:#f97316}
  .preso-controls{display:flex;justify-content:center;gap:16px;padding:16px;background:rgba(0,0,0,.3)}
  .preso-controls button{padding:10px 24px;border-radius:8px;border:none;font-size:14px;font-weight:600;cursor:pointer;background:rgba(255,255,255,.1);color:#fff;transition:background .15s}
  .preso-controls button.primary{background:#f97316}
  @media (max-width:640px){.preso-slide{padding:24px 16px}.preso-controls{gap:8px}.preso-controls button{padding:8px 14px;font-size:12px}.tab-bar{flex-wrap:nowrap}}
</style>
</head>
<body>
<div class="js-warning">⚠️ This file needs JavaScript. Please <strong>save to Files</strong> then <strong>open in Safari</strong>.<br><small>WhatsApp/email preview does not run apps.</small></div>
'''

    html += '''
<div class="hero">
  <div class="lang-selector">
    <button id="lang-en" class="active" onclick="changeLang('en')">EN</button>
    <button id="lang-hi" onclick="changeLang('hi')">\u0939\u093f\u0928\u094d\u0926\u0940</button>
  </div>
  <h1>Call Coaching <span>Playbook</span></h1>
  <p id="hero-sub">Loading training data...</p>
  <div class="meta" id="hero-meta"></div>
  <div class="share-bar">
    <button onclick="window.print()">\U0001F5A8 <span id="btn-print">Print / Save PDF</span></button>
    <button onclick="openPresentation()">\U0001F3B6 <span id="btn-preso">Presentation Mode</span></button>
    <a href="#" onclick="shareFile(event)">\U0001F4E4 <span id="btn-share">Share This File</span></a>
  </div>
  <div class="share-tip" id="share-tip">\U0001F4A1 This file works offline. Share the .html file via WhatsApp, Email, or Drive.</div>
</div>

<div class="container" id="app">
  <div class="empty-state" id="loading">
    <div class="icon">\u23f3</div>
    <h2 id="loading-title">Loading training data...</h2>
    <p id="loading-sub">Run <code>python3 analyze_calls.py --master</code> first.</p>
  </div>
</div>

<div class="footer" id="footer-text">Lakm\u00e9 Academy &middot; Call Coaching Playbook &middot; Open on any phone, tablet, or laptop</div>

<div class="preso-overlay" id="preso-overlay">
  <div class="preso-slide" id="preso-slide">
    <div class="slide-num" id="preso-num"></div>
    <div class="slide-icon" id="preso-icon"></div>
    <div class="slide-title" id="preso-title"></div>
    <div class="slide-sub" id="preso-sub"></div>
    <div class="slide-body" id="preso-body"></div>
  </div>
  <div class="preso-controls">
    <button id="preso-prev" onclick="presoPrev()">\u25c0 <span id="btn-prev">Previous</span></button>
    <button class="primary" id="preso-next" onclick="presoNext()"><span id="btn-next">Next</span> \u25b6</button>
    <button id="preso-exit" onclick="closePresentation()">\u2715 <span id="btn-exit">Exit</span></button>
  </div>
</div>

<script>
document.documentElement.classList.add('js-run');
window.onerror = function(msg, url, line, col, err) {
  var el = document.getElementById('loading');
  if (el) el.innerHTML = '<div style="color:#ef4444;font-size:14px;text-align:left;padding:16px;background:#fef2f2;border-radius:8px;"><b>ERROR</b><br>' + msg + '<br><small>line ' + line + ':' + col + '</small></div>';
  return true;
};
</script>
<script>
var _data = __DATA_OBJECT__;
try {
  var ls_ok = false;
  try { var ls = localStorage; ls_ok = true; } catch(e) { var ls = null; }
} catch(e) {
  var ls = null; var ls_ok = false;
}
var currentLang = ls ? (ls.getItem('trainingLang') || 'en') : 'en';
window._reportData = null;

function changeLang(lang) {
  currentLang = lang;
  if (ls) ls.setItem('trainingLang', lang);
  document.getElementById('lang-en').className = lang === 'en' ? 'active' : '';
  document.getElementById('lang-hi').className = lang === 'hi' ? 'active' : '';
  if (window._reportData) renderAndShow(window._reportData);
}

function shareFile(e) {
  e.preventDefault();
  alert(currentLang === 'hi'
    ? '\u0936\u0947\u092f\u0930 \u0915\u0930\u0928\u0947 \u0915\u0947 \u0932\u093f\u090f:\\n\\n1. training.html \u092b\u093c\u093e\u0907\u0932 \u0922\u0942\u0902\u0922\u0947\u0902\\n2. WhatsApp, Email, \u092f\u093e Drive \u0938\u0947 \u0936\u0947\u092f\u0930 \u0915\u0930\u0947\u0902\\n3. \u0915\u094b\u0908 \u092d\u0940 \u0905\u092a\u0928\u0947 \u092b\u093c\u094b\u0928 \u092c\u094d\u0930\u093e\u0909\u091c\u093c\u0930 \u092e\u0947\u0902 \u0916\u094b\u0932 \u0938\u0915\u0924\u093e \u0939\u0948\\n\\n\u092c\u093f\u0928\u093e \u0907\u0902\u091f\u0930\u0928\u0947\u091f \u0915\u0947 \u0915\u093e\u092e \u0915\u0930\u0924\u093e \u0939\u0948\u0964'
    : 'To share:\\n\\n1. Find this file: training.html\\n2. Share via WhatsApp, Email, or Google Drive\\n3. Anyone can open in their phone browser\\n\\nWorks offline. No app needed.');
}
'''

    # Now write the entire JavaScript section
    # We'll write it directly without going through the tool

    # Build the data embedding
    data_json_str = json.dumps(data, ensure_ascii=False)
    
    # Escape single quotes for JS
    data_json_str = data_json_str.replace("\\", "\\\\").replace("'", "\\'").replace("\n", "\\n")

    # Write English content arrays as JS (no Hindi needed here)
    # And Hindi content arrays
    
    js_code = """
var langData = {};

langData.en = {
  tabs: ['\U0001F4CB Cheat Sheet', '\U0001F4A1 Call Flow', '\U0001F3AC Script Fixes', '\U0001F4A1 Objections', '\U0001F3D7 Role Play', '\U0001F4CD Center Tips'],
"""

    js_code += """
  heroSub: function(d) { return 'Training based on ' + d.total_calls + ' calls across ' + Object.keys(d.centers).length + ' centers'; },
  metaLabels: ['Calls Analyzed', 'Avg Score', 'Actionable Do\\'s', 'Mistake Types'],
  printBtn: 'Print / Save PDF', presoBtn: 'Presentation Mode', shareBtn: 'Share This File',
  shareTip: '\\ud83d\\udca1 This file works offline. Share the .html file via WhatsApp, Email, or Drive.',
  footer: 'Lakm\\u00e9 Academy \\u00b7 Call Coaching Playbook \\u00b7 Open on any phone, tablet, or laptop',
  loadingTitle: 'Loading training data...', loadingSub: 'Run <code>python3 analyze_calls.py --master</code> first.',
  presoPrev: 'Previous', presoNext: 'Next', presoExit: 'Exit',
  dosTitle: function(n) { return 'DO THIS (' + n + ' points)'; },
  dontsTitle: function(n) { return 'DON\\'T DO THIS (' + n + ' points)'; },
  sayTitle: function(n) { return 'Say THIS, Not That (' + n + ' pairs)'; },
  goldenTitle: '10 Golden Rules (Never Forget)',
  cheatTitle: '35+ Main Point Cheat Sheet',
  cheatDesc: function(n, total) { return 'Master these <strong>' + n + ' key points</strong> to transform your calls. Based on ' + total + ' real calls.'; },
  callFlowTitle: 'Ideal 5-Minute Call Flow',
  callFlowDesc: 'Every call follows this 5-step structure. Master each step. Calls longer than 5 minutes rarely convert better.',
  scriptTitle: 'Before & After: Real Call Fixes',
  scriptDesc: 'Real mistakes from our calls. Compare the bad (actual transcript) with the fixed version.',
  objTitle: function(n) { return 'Objection Handling Scripts (' + n + ' scenarios)'; },
  objDesc: 'Master these objections. Click each to see the wrong vs right response.',
  rpTitle: function(n) { return 'Role-Play Scenarios (' + n + ')'; },
  rpDesc: 'Click a customer type to reveal the ideal script. Practice with a partner.',
  ctTitle: function(n) { return 'Center-Specific Coaching (' + n + ' centers)'; },
  ctDesc: 'Each center has different strengths. Coaching is tailored to your specific gaps.',
  actualCall: 'Actual Call', fixedVersion: 'Fixed Version',
  presSlides: ['Overview', 'Score Analysis', 'Key Do\\'s & Don\\'ts', 'Call Flow', 'Key Takeaways'],
};
"""

    # Hindi translations
    hi_tabs = [
        '\U0001F4CB \u091a\u0940\u091f \u0936\u0940\u091f',
        '\U0001F4A1 \u0915\u0949\u0932 \u092b\u094d\u0932\u094b',
        '\U0001F3AC \u0938\u094d\u0915\u094d\u0930\u093f\u092a\u094d\u091f \u0938\u0941\u0927\u093e\u0930',
        '\U0001F4A1 \u0906\u092a\u0924\u094d\u0924\u093f\u092f\u094b\u0902 \u0915\u093e \u0938\u092e\u093e\u0927\u093e\u0928',
        '\U0001F3D7 \u0930\u094b\u0932 \u092a\u094d\u0932\u0947',
        '\U0001F4CD \u0938\u0947\u0902\u091f\u0930 \u091f\u093f\u092a\u094d\u0938'
    ]
    
    js_code += """
langData.hi = {
  tabs: """ + json.dumps(hi_tabs, ensure_ascii=False) + """,
  heroSub: function(d) { return d.total_calls + ' ' + '\u0915\u0949\u0932 \u0914\u0930 ' + Object.keys(d.centers).length + ' \u0938\u0947\u0902\u091f\u0930 \u0915\u0947 \u0906\u0927\u093e\u0930 \u092a\u0930 \u091f\u094d\u0930\u0947\u0928\u093f\u0902\u0917'; },
  metaLabels: ['\u0915\u0949\u0932 \u0915\u093e \u0935\u093f\u0936\u094d\u0932\u0947\u0937\u0923', '\u0914\u0938\u0924 \u0938\u094d\u0915\u094b\u0930', '\u0915\u093e\u0930\u094d\u0930\u0947 \u0915\u0930\u0928\u0947 \u0915\u0947 \u0921\u0942', '\u0917\u0932\u0924\u093f\u092f\u094b\u0902 \u0915\u0947 \u092a\u094d\u0930\u0915\u093e\u0930'],
  printBtn: '\u092a\u094d\u0930\u093f\u0902\u091f / \u092a\u0940\u0921\u0940\u090f\u092b\u093c \u0938\u0947\u0935 \u0915\u0930\u0947\u0902',
  presoBtn: '\u092a\u094d\u0930\u0947\u091c\u0947\u0902\u091f\u0947\u0936\u0928 \u092e\u094b\u0921',
  shareBtn: '\u092f\u0939 \u092b\u093c\u093e\u0907\u0932 \u0936\u0947\u092f\u0930 \u0915\u0930\u0947\u0902',
"""
    hi_share = '\u092f\u0939 \u092b\u093c\u093e\u0907\u0932 \u0911\u092b\u0932\u093e\u0907\u0928 \u0915\u093e\u092e \u0915\u0930\u0924\u0940 \u0939\u0948\u0964 .html \u092b\u093c\u093e\u0907\u0932 \u0935\u094d\u0939\u0949\u091f\u094d\u0938\u090f\u092a\u094d092a, \u0908\u092e\u0947\u0932, \u092f\u093e \u0921\u094d\u0930\u093e\u0907\u0935 \u0915\u0947 \u091c\u0930\u093f\u090f \u0936\u0947\u092f\u0930 \u0915\u0930\u0947\u0902\u0964'
    hi_footer = '\u0932\u093e\u0915\u092e\u0947 \u0905\u0915\u093e\u0921\u092e\u0940 \u00b7 \u0915\u0949\u0932 \u0915\u094b\u091a\u093f\u0902\u0917 \u092a\u094d\u0932\u0947\u092c\u0941\u0915 \u00b7 \u0915\u093f\u0938\u0940 \u092d\u0940 \u092b\u093c\u094b\u0928, \u091f\u0948\u092c\u0932\u0947\u091f, \u092f\u093e \u0932\u0949\u092a\u091f\u0949\u092a \u092a\u0930 \u0916\u094b\u0932\u0947\u0902'
    
    js_code += """
  shareTip: '""" + hi_share + """',
  footer: '""" + hi_footer + """',
  loadingTitle: '\u0921\u0947\u091f\u093e \u0932\u094b\u0921 \u0939\u094b \u0930\u0939\u093e \u0939\u0948...',
  loadingSub: '\u092a\u0939\u0932\u0947 <code>python3 analyze_calls.py --master</code> \u091a\u0932\u093e\u090f\u0902\u0964',
  presoPrev: '\u092a\u093f\u091b\u0932\u093e', presoNext: '\u0905\u0917\u0932\u093e', presoExit: '\u092c\u093e\u0939\u0930 \u0928\u093f\u0915\u0932\u0947\u0902',
  dosTitle: function(n) { return '\u092f\u0939 \u0915\u0930\u0947\u0902 (' + n + ' \u092c\u093e\u0924\u0947\u0902)'; },
  dontsTitle: function(n) { return '\u092f\u0939 \u0928 \u0915\u0930\u0947\u0902 (' + n + ' \u092c\u093e\u0924\u0947\u0902)'; },
  sayTitle: function(n) { return '\u092f\u0939 \u0915\u0939\u0947\u0902, \u0935\u0939 \u0928\u0939\u0940\u0902 (' + n + ' \u091c\u094b\u0921\u093c\u0947)'; },
  goldenTitle: '10 \u0938\u0941\u0928\u0939\u0930\u0947 \u0928\u093f\u092f\u092e (\u0915\u092d\u0940 \u092e\u0924 \u092d\u0942\u0932\u0947\u0902)',
  cheatTitle: '35+ \u092e\u0941\u0916\u094d\u092f \u092c\u093e\u0924\u0947\u0902 \u090f\u0915 \u0928\u091c\u093c\u0930 \u092e\u0947\u0902',
  cheatDesc: function(n, total) { return '\u0905\u092a\u0928\u0940 \u0915\u0949\u0932 \u0915\u094b \u092c\u0947\u0939\u0924\u0930 \u092c\u0928\u093e\u0928\u0947 \u0915\u0947 \u0932\u093f\u090f \u0907\u0928 <strong>' + n + ' \u092e\u0941\u0916\u094d\u092f \u092c\u093e\u0924\u094b\u0902</strong> \u0915\u094b \u092f\u093e\u0926 \u0915\u0930\u0947\u0902\u0964 ' + total + ' \u0905\u0938\u0932\u0940 \u0915\u0949\u0932 \u0915\u0947 \u0906\u0927\u093e\u0930 \u092a\u0930\u0964'; },
  callFlowTitle: '\u0906\u0926\u0930\u094d\u0936 5-\u092e\u093f\u0928\u091f \u0915\u0949\u0932 \u092b\u094d\u0932\u094b',
  callFlowDesc: '\u0939\u0930 \u0915\u0949\u0932 \u0907\u0938 5-\u091a\u0930\u0923\u0940\u092f \u0938\u0902\u0930\u091a\u0928\u093e \u0915\u093e \u092a\u093e\u0932\u0928 \u0915\u0930\u0947\u0964 5 \u092e\u093f\u0928\u091f \u0938\u0947 \u091c\u094d\u092f\u093e\u0926\u093e \u0915\u0949\u0932 \u0936\u093e\u092f\u0926 \u0939\u0940 \u092c\u0947\u0939\u0924\u0930 \u0915\u0928\u094d\u0935\u0930\u094d\u091f \u0915\u0930\u0924\u0947 \u0939\u0948\u0902\u0964',
  scriptTitle: '\u092a\u0939\u0932\u0947 \u0914\u0930 \u092c\u093e\u0926: \u0905\u0938\u0932\u0940 \u0915\u0949\u0932 \u092e\u0947\u0902 \u0938\u0941\u0927\u093e\u0930',
  scriptDesc: '\u0939\u092e\u093e\u0930\u0947 \u0915\u0949\u0932\u094b\u0902 \u0938\u0947 \u0932\u0940 \u0917\u0908 \u0905\u0938\u0932\u0940 \u0917\u0932\u0924\u093f\u092f\u093e\u0901\u0964 \u0917\u0932\u0924 \u0915\u094b \u0938\u0939\u0940 \u0938\u0902\u0938\u094d\u0915\u0930\u0923 \u0938\u0947 \u0924\u0941\u0932\u0928\u093e \u0915\u0930\u0947\u0902\u0964',
  objTitle: function(n) { return '\u0906\u092a\u0924\u094d\u0924\u093f\u092f\u094b\u0902 \u0915\u0947 \u0938\u092e\u093e\u0927\u093e\u0928 (' + n + ' \u092a\u0930\u093f\u0926\u0943\u0936\u094d\u092f)'; },
  objDesc: '\u0907\u0928 \u0938\u092d\u0940 \u0938\u093e\u092e\u093e\u0928\u094d\u092f \u0906\u092a\u0924\u094d\u0924\u093f\u092f\u094b\u0902 \u0915\u094b \u0938\u0940\u0916\u0947\u0902\u0964 \u092a\u094d\u0930\u0924\u094d\u092f\u0947\u0915 \u092a\u0930 \u0915\u094d\u0932\u093f\u0915 \u0915\u0930\u0947\u0902 \u0917\u0932\u0924 \u0914\u0930 \u0938\u0939\u0940 \u091c\u0935\u093e\u092c \u0926\u0947\u0916\u0928\u0947 \u0915\u0947 \u0932\u093f\u090f\u0964',
  rpTitle: function(n) { return '\u0930\u094b\u0932 \u092a\u094d\u0932\u0947 \u092a\u0930\u093f\u0926\u0943\u0936\u094d\u092f (' + n + ')'; },
  rpDesc: '\u092a\u094d\u0930\u0924\u094d\u092f\u0947\u0915 \u0917\u094d\u0930\u093e\u0939\u0915 \u092a\u094d\u0930\u0915\u093e\u0930 \u092a\u0930 \u0915\u094d\u0932\u093f\u0915 \u0915\u0930\u0947\u0902 \u0906\u0926\u0930\u094d\u0936 \u0938\u094d\u0915\u094d\u0930\u093f\u092a\u094d\u091f \u0926\u0947\u0916\u0928\u0947 \u0915\u0947 \u0932\u093f\u090f\u0964 \u0938\u093e\u0925\u0940 \u0915\u0947 \u0938\u093e\u0925 \u0905\u092d\u094d\u092f\u093e\u0938 \u0915\u0930\u0947\u0902\u0964',
  ctTitle: function(n) { return '\u0938\u0947\u0902\u091f\u0930 \u0915\u0947 \u0905\u0928\u0941\u0938\u093e\u0930 \u0915\u094b\u091a\u093f\u0902\u0917 (' + n + ' \u0938\u0947\u0902\u091f\u0930)'; },
  ctDesc: '\u0939\u0930 \u0938\u0947\u0902\u091f\u0930 \u0915\u0940 \u0905\u0932\u0917 \u0924\u093e\u0915\u0924 \u0939\u0948\u0964 \u0915\u094b\u091a\u093f\u0902\u0917 \u0906\u092a\u0915\u0940 \u0935\u093f\u0936\u093f\u0937\u094d\u091f \u0915\u092e\u0940 \u0915\u0947 \u0939\u093f\u0938\u093e\u092c \u0938\u0947 \u0924\u0948\u092f\u093e\u0930 \u0915\u0940 \u0917\u0908 \u0939\u0948\u0964',
  actualCall: '\u0905\u0938\u0932\u0940 \u0915\u0949\u0932', fixedVersion: '\u0938\u0941\u0927\u093e\u0930\u093e \u0938\u0902\u0938\u094d\u0915\u0930\u0923',
  presSlides: ['\u0905\u0935\u0932\u094b\u0915\u0928', '\u0938\u094d\u0915\u094b\u0930 \u0935\u093f\u0936\u094d\u0932\u0947\u0937\u0923', '\u092e\u0941\u0916\u094d\u092f \u0915\u0930\u0928\u0947 \u0914\u0930 \u0928 \u0915\u0930\u0928\u0947 \u0915\u0940 \u092c\u093e\u0924\u0947\u0902', '\u0915\u0949\u0932 \u092b\u094d\u0932\u094b', '\u092e\u0941\u0916\u094d\u092f \u0938\u093f\u0916\u0935\u093e\u0907\u092f\u093e\u0901'],
};
"""

    # Content by language - English Do's
    en_dos = json.dumps([
        'Greet with YOUR name + "Lakm\u00e9 Academy" clearly',
        'Confirm you\'re speaking to the right person',
        'Ask 2-3 discovery questions before recommending anything',
        'Find out: experience level, goal (career/personal), timeline',
        'Recommend ONE specific course that matches their need',
        'Build value first \u2014 mention placement, salaries, career outcomes',
        'Then share the investment with context (monthly EMI)',
        'Use specific time anchors: "Can you come at 4 PM today?"',
        'Book a center visit \u2014 the goal of EVERY call',
        'If customer is a makeup artist, pitch ADVANCED courses only',
        'End with a firm next step: "I\'ll call you tomorrow at 11, OK?"',
        'Maintain 60:40 talk:listen ratio',
        'Use the customer\'s name during the call',
        'If they say busy \u2014 set a SPECIFIC callback time',
        'Pronounce "Lak-may" correctly \u2014 not "Lakshmi"',
        'Keep total call under 5 minutes unless deeply interested',
    ], ensure_ascii=False)

    en_donts = json.dumps([
        'Saying "Lakshmi Academy" instead of "Lakm\u00e9 Academy"',
        'Skipping discovery questions \u2014 jumping straight to info dump',
        'Dumping ALL course names at once (overwhelms customer)',
        'Mentioning price before building any value',
        'Passive ending: "Let me know if interested" or "Call me back"',
        'Speaking more than 70% of the time \u2014 you\'re not listening',
        'Selling basic courses to professional makeup artists',
        'Giving up when customer says "I\'m busy"',
        'WhatsApping details without pushing for a visit',
        'Not setting a specific callback time',
        'Talking for 60+ seconds without asking a question',
        'Saying "How can I help you?" \u2014 too vague',
        'Not using the customer\'s name during the call',
        'Badmouthing competitors when customer mentions them',
        'Ending the call without a booked visit or specific callback',
    ], ensure_ascii=False)

    # Hindi Do's
    hi_dos = json.dumps([
        '\u0905\u092a\u0928\u093e \u0928\u093e\u092e \u0914\u0930 "\u0932\u093e\u0915\u092e\u0947 \u0905\u0915\u093e\u0921\u092e\u0940" \u0938\u092a\u0937\u094d\u091f \u0915\u0939\u0947\u0902',
        '\u092a\u0941\u0937\u094d\u091f\u093f \u0915\u0930\u0947\u0902 \u0915\u093f \u0906\u092a \u0938\u0939\u0940 \u0935\u094d\u092f\u0915\u094d\u0924\u093f \u0938\u0947 \u092c\u093e\u0924 \u0915\u0930 \u0930\u0939\u0947 \u0939\u0948\u0902',
        '\u0915\u0941\u091b \u092d\u0940 \u0938\u0941\u091d\u093e\u0928\u0947 \u0938\u0947 \u092a\u0939\u0932\u0947 2-3 \u091c\u093e\u0928\u0915\u093e\u0930\u0940 \u0935\u093e\u0932\u0947 \u0938\u0935\u093e\u0932 \u092a\u0942\u091b\u0947\u0902',
        '\u092a\u0924\u093e \u0932\u0917\u093e\u090f\u0902: \u0905\u0928\u0941\u092d\u0935 \u0938\u094d\u0924\u0930, \u0932\u0915\u094d\u0937\u094d\u092f (\u0915\u0930\u093f\u092f\u0930/\u0935\u094d\u092f\u0915\u094d\u0924\u093f\u0917\u0924), \u0938\u092e\u092f \u0938\u0940\u092e\u093e',
        '\u0909\u0928\u0915\u0940 \u091c\u0930\u0942\u0930\u0924 \u0915\u0947 \u0939\u093f\u0938\u093e\u092c \u0938\u093f\u0930\u094d\u092b \u090f\u0915 \u0905\u0928\u0942\u0920\u093e \u0915\u094b\u0930\u094d\u0938 \u0938\u0941\u091d\u093e\u090f\u0902',
        '\u092a\u0939\u0932\u0947 \u092e\u0942\u0932\u094d\u092f \u092c\u0924\u093e\u090f\u0902 \u2014 \u092a\u094d\u0932\u0947\u0938\u092e\u0947\u0902\u091f, \u0935\u0947\u0924\u0928, \u0915\u0930\u093f\u092f\u0930 \u092a\u0930\u093f\u0923\u093e\u092e',
        '\u092b\u093f\u0930 \u0915\u0940\u092e\u0924 \u0938\u0902\u0926\u0930\u094d\u092d \u092e\u0947\u0902 \u092c\u0924\u093e\u090f\u0902 (\u092e\u093e\u0939\u093f\u0928\u093e EMI)',
        '\u0935\u093f\u0936\u093f\u0937\u094d\u091f \u0938\u092e\u092f \u092c\u0924\u093e\u090f\u0902: "\u0915\u094d\u092f\u093e \u0906\u091c \u0936\u093e\u092e 4 \u092c\u091c\u0947 \u0906 \u0938\u0915\u0924\u0947 \u0939\u0948\u0902?"',
        '\u0938\u0947\u0902\u091f\u0930 \u0935\u093f\u091c\u093f\u091f \u092c\u0941\u0915 \u0915\u0930\u093e\u090f\u0902 \u2014 \u0939\u0930 \u0915\u0949\u0932 \u0915\u093e \u0932\u0915\u094d\u0937\u094d\u092f',
        '\u092f\u0926\u093f \u0917\u094d\u0930\u093e\u0939\u0915 \u092e\u0947\u0915\u092a \u0915\u0932\u093e\u0915\u093e\u0930 \u0939\u0948 \u0924\u094b \u0938\u093f\u0930\u094d\u092b \u090f\u0921\u094d\u0935\u093e\u0902\u0938\u094d\u0921 \u0915\u094b\u0930\u094d\u0938 \u0926\u093f\u0916\u093e\u090f\u0902',
        '\u092e\u091c\u092c\u0942\u0924 \u0905\u0917\u0932\u093e \u0915\u0926\u092e \u0924\u092f \u0915\u0930\u0947\u0902: "\u092e\u0948\u0902 \u0915\u0932 11 \u092c\u091c\u0947 \u0915\u0949\u0932 \u0915\u0930\u0942\u0902\u0917\u093e, \u0920\u0940\u0915 \u0939\u0948?"',
        '60:40 \u0915\u093e \u092c\u094b\u0932\u0928\u0947/\u0938\u0941\u0928\u0928\u0947 \u0915\u093e \u0905\u0928\u0941\u092a\u093e\u0924 \u0930\u0916\u0947\u0902',
        '\u0915\u0949\u0932 \u0915\u0947 \u0926\u094c\u0930\u093e\u0928 \u0917\u094d\u0930\u093e\u0939\u0915 \u0915\u093e \u0928\u093e\u092e \u0915\u092e \u0938\u0947 \u0915\u092e \u090f\u0915 \u092c\u093e\u0930 \u0932\u0947\u0902',
        '\u0905\u0917\u0930 "\u0935\u094d\u092f\u0938\u094d\u0924 \u0939\u0942\u0901" \u0915\u0939\u0947 \u0924\u094b \u0935\u093f\u0936\u093f\u0937\u094d\u091f \u0938\u092e\u092f \u0924\u092f \u0915\u0930\u0947\u0902',
        '"Lak-may" \u0938\u0939\u0940 \u0909\u091a\u094d\u091a\u093e\u0930\u0923 \u0915\u0930\u0947\u0902 \u2014 "\u0932\u0915\u094d\u0937\u094d\u092e\u0940" \u0928\u0939\u0940\u0902',
        '\u0915\u0949\u0932 \u0915\u094b 5 \u092e\u093f\u0928\u091f \u092e\u0947\u0902 \u0930\u0916\u0947\u0902 \u091c\u092c \u0924\u0915 \u0917\u094d\u0930\u093e\u0939\u0915 \u092c\u0939\u0941\u0924 \u0926\u093f\u0932\u091a\u0938\u094d\u092a\u0940 \u0928 \u0926\u093f\u0916\u093e\u090f',
    ], ensure_ascii=False)

    # Hindi Don'ts
    hi_donts = json.dumps([
        '"Lakshmi Academy" \u0915\u0939\u0928\u093e "\u0932\u093e\u0915\u092e\u0947 \u0905\u0915\u093e\u0921\u092e\u0940" \u0915\u0947 \u092c\u091c\u093e\u092f',
        '\u091c\u093e\u0928\u0915\u093e\u0930\u0940 \u0935\u093e\u0932\u0947 \u0938\u0935\u093e\u0932 \u0928 \u092a\u0942\u091b\u0928\u093e \u2014 \u0938\u0940\u0927\u0947 \u091c\u093e\u0928\u0915\u093e\u0930\u0940 \u0926\u0947\u0928\u093e',
        '\u0938\u092d\u0940 \u0915\u094b\u0930\u094d\u0938 \u0915\u0947 \u0928\u093e\u092e \u090f\u0915 \u0938\u093e\u0925 \u0917\u093f\u0928\u0935\u093e\u0928\u093e (\u0917\u094d\u0930\u093e\u0939\u0915 \u092a\u0930\u0947\u0936\u093e\u0928)',
        '\u0915\u094b\u0908 \u092e\u0942\u0932\u094d\u092f \u0926\u093f\u0916\u093e\u090f \u092c\u093f\u0928\u093e \u0915\u0940\u092e\u0924 \u0915\u093e \u091c\u093f\u0915\u094d\u0930 \u0915\u0930\u0928\u093e',
        '\u0928\u093f\u0937\u094d\u0915\u094d\u0930\u093f\u092f \u0905\u0902\u0924: "\u0905\u0917\u0930 \u0926\u093f\u0932\u091a\u0938\u094d\u092a\u0940 \u0939\u0948 \u0924\u094b \u092c\u0924\u093e\u0928\u093e" \u092f\u093e "\u092e\u0941\u091d\u0947 \u0935\u093e\u092a\u0938 \u0915\u0930\u0928\u093e"',
        '70% \u0938\u0947 \u091c\u094d\u092f\u093e\u0926\u093e \u092c\u094b\u0932\u0928\u093e \u2014 \u0906\u092a \u0938\u0941\u0928 \u0928\u0939\u0940\u0902 \u0930\u0939\u0947',
        '\u092a\u0947\u0936\u0947\u0935\u0930 \u092e\u0947\u0915\u092a \u0915\u0932\u093e\u0915\u093e\u0930\u094b\u0902 \u0915\u094b \u092c\u0947\u0938\u093f\u0915 \u0915\u094b\u0930\u094d\u0938 \u092c\u0947\u091a\u0928\u093e',
        '\u0917\u094d\u0930\u093e\u0939\u0915 \u0915\u0947 "\u0935\u094d\u092f\u0938\u094d\u0924 \u0939\u0942\u0901" \u0915\u0939\u0928\u0947 \u092a\u0930 \u0939\u093e\u0930 \u092e\u093e\u0928 \u091c\u093e\u0928\u093e',
        '\u092c\u093f\u0928\u093e \u0935\u093f\u091c\u093f\u091f \u0915\u0947 \u091c\u094b\u0930 \u0926\u093f\u090f \u0935\u094d\u0939\u0949\u091f\u094d\u0938\u090f\u092a\u094d\u092a \u092a\u0930 \u0935\u093f\u0935\u0930\u0923 \u092d\u0947\u091c\u0928\u093e',
        '\u0935\u093e\u092a\u0938 \u0915\u0949\u0932 \u0915\u093e \u0935\u093f\u0936\u093f\u0937\u094d\u091f \u0938\u092e\u092f \u0928 \u0924\u092f \u0915\u0930\u0928\u093e',
        '\u092c\u093f\u0928\u093e \u0938\u0935\u093e\u0932 \u092a\u0942\u091b\u0947 60+ \u0938\u0947\u0915\u0902\u0921 \u092c\u094b\u0932\u0924\u0947 \u0930\u0939\u0928\u093e',
        '"\u092e\u0948\u0902 \u0915\u094d\u092f\u093e \u092e\u0926\u0926 \u0915\u0930 \u0938\u0915\u0924\u093e \u0939\u0942\u0901?" \u0915\u0939\u0928\u093e \u2014 \u092c\u0939\u0941\u0924 \u0905\u0938\u094d\u092a\u0937\u094d\u091f',
        '\u0915\u0949\u0932 \u0915\u0947 \u0926\u094c\u0930\u093e\u0928 \u0917\u094d\u0930\u093e\u0939\u0915 \u0915\u093e \u0928\u093e\u092e \u0928 \u0932\u0947\u0928\u093e',
        '\u091c\u092c \u0917\u094d\u0930\u093e\u0939\u0915 \u092a\u094d\u0930\u0924\u093f\u0926\u094d\u0935\u0902\u0926\u094d\u0935\u0940 \u0915\u093e \u091c\u093f\u0915\u094d\u0930 \u0915\u0930\u0947 \u0924\u094b \u092c\u0941\u0930\u093e \u092c\u094b\u0932\u0928\u093e',
        '\u092c\u093f\u0928\u093e \u092c\u0941\u0915 \u0935\u093f\u091c\u093f\u091f \u092f\u093e \u0935\u093f\u0936\u093f\u0937\u094d\u091f \u0915\u0949\u0932\u092c\u0948\u0915 \u0915\u0947 \u0915\u0949\u0932 \u0938\u092e\u093e\u092a\u094d\u0924 \u0915\u0930\u0928\u093e',
    ], ensure_ascii=False)

    # English Golden Rules
    en_rules = json.dumps([
        'The ONE goal of every call is a <strong>center visit</strong>. Not counseling. Not fee discussion. Just the visit.',
        'You cannot recommend without <strong>discovering first</strong>. Ask before you tell.',
        '<strong>Price without value</strong> = customer hangs up. Always wrap price in career outcomes.',
        '<strong>Specific time</strong> beats "I\'ll call later" every time. "Today 4 PM" works. "Sometime" doesn\'t.',
        'If the customer is a <strong>pro artist</strong>, sell them <strong>advanced/international</strong>. Never basic.',
        '<strong>Listen 60%, talk 40%</strong>. If you\'re talking more than that, you\'re losing them.',
        'The <strong>demo/free class offer</strong> closes undecided prospects. Use it early.',
        '<strong>Objections are buying signals</strong>. "Too expensive" means "Convince me it\'s worth it."',
        'When a customer mentions a <strong>competitor</strong>, be confident: "Visit us first, then compare."',
        'Every call ends with a <strong>specific next step</strong>: booked visit OR scheduled callback. No exceptions.',
    ], ensure_ascii=False)

    # Hindi Golden Rules
    hi_rules = json.dumps([
        '\u0939\u0930 \u0915\u0949\u0932 \u0915\u093e \u090f\u0915 \u0932\u0915\u094d\u0937\u094d\u092f \u0939\u0948: <strong>\u0938\u0947\u0902\u091f\u0930 \u0935\u093f\u091c\u093f\u091f</strong>\u0964 \u0915\u093e\u0909\u0902\u0938\u0932\u093f\u0902\u0917 \u0928\u0939\u0940\u0902, \u092b\u0940 \u091a\u0930\u094d\u091a\u093e \u0928\u0939\u0940\u0902\u0964 \u0938\u093f\u0930\u094d\u092b \u0935\u093f\u091c\u093f\u091f\u0964',
        '\u092c\u093f\u0928\u093e <strong>\u092a\u0939\u0932\u0947 \u091c\u093e\u0928\u0947</strong> \u0906\u092a \u0938\u0939\u0940 \u0938\u0941\u091d\u093e\u0935 \u0928\u0939\u0940\u0902 \u0926\u0947 \u0938\u0915\u0924\u0947\u0964 \u092c\u094b\u0932\u0928\u0947 \u0938\u0947 \u092a\u0939\u0932\u0947 \u092a\u0942\u091b\u0947\u0902\u0964',
        '<strong>\u092e\u0942\u0932\u094d\u092f \u0915\u0947 \u092c\u093f\u0928\u093e \u0915\u0940\u092e\u0924</strong> = \u0917\u094d\u0930\u093e\u0939\u0915 \u092b\u094b\u0928 \u0930\u0916 \u0926\u0947\u0917\u093e\u0964 \u0939\u092e\u0947\u0936\u093e \u0915\u0940\u092e\u0924 \u0915\u094b \u0915\u0930\u093f\u092f\u0930 \u092a\u0930\u093f\u0923\u093e\u092e\u094b\u0902 \u092e\u0947\u0902 \u0932\u092a\u0947\u091f\u0947\u0902\u0964',
        '<strong>\u0935\u093f\u0936\u093f\u0937\u094d\u091f \u0938\u092e\u092f</strong> "\u092c\u093e\u0926 \u092e\u0947\u0902 \u0915\u0930\u0942\u0902\u0917\u093e" \u0938\u0947 \u092c\u0947\u0939\u0924\u0930 \u0939\u0948\u0964 "\u0906\u091c 4 \u092c\u091c\u0947" \u0915\u093e\u092e \u0915\u0930\u0924\u093e \u0939\u0948\u0964',
        '\u092f\u0926\u093f \u0917\u094d\u0930\u093e\u0939\u0915 <strong>\u092a\u0947\u0936\u0947\u0935\u0930 \u0915\u0932\u093e\u0915\u093e\u0930</strong> \u0939\u0948, \u0924\u094b <strong>\u090f\u0921\u094d\u0935\u093e\u0902\u0938\u094d\u0921/\u0907\u0902\u091f\u0930\u0928\u0947\u0936\u0928\u0932</strong> \u092c\u0947\u091a\u0947\u0902\u0964 \u092c\u0947\u0938\u093f\u0915 \u0928\u0939\u0940\u0902\u0964',
        '<strong>60% \u0938\u0941\u0928\u0947\u0902, 40% \u092c\u094b\u0932\u0947\u0902</strong>\u0964 \u0907\u0938\u0938\u0947 \u091c\u094d\u092f\u093e\u0926\u093e \u092c\u094b\u0932\u0928\u093e = \u0917\u094d\u0930\u093e\u0939\u0915 \u0916\u094b\u0928\u093e\u0964',
        '<strong>\u092e\u0941\u092b\u094d\u0924 \u0921\u0947\u092e\u094b/\u0915\u094d\u0932\u093e\u0938</strong> \u0905\u0928\u093f\u0936\u094d\u091a\u093f\u0924 \u0917\u094d\u0930\u093e\u0939\u0915\u094b\u0902 \u0915\u094b \u092c\u0902\u0926 \u0915\u0930\u0928\u0947 \u0915\u093e \u0938\u092c\u0938\u0947 \u092e\u091c\u092c\u0942\u0924 \u0939\u0925\u093f\u092f\u093e\u0930 \u0939\u0948\u0964',
        '<strong>\u0906\u092a\u0924\u094d\u0924\u093f\u092f\u093e\u0901 \u0916\u0930\u0940\u0926\u093e\u0930\u0940 \u0915\u0947 \u0938\u0902\u0915\u0947\u0924</strong> \u0939\u0948\u0902\u0964 "\u092e\u0939\u0902\u0917\u093e \u0939\u0948" = "\u092e\u0941\u091d\u0947 \u092f\u0915\u0940\u0928 \u0926\u093f\u0932\u093e\u0913 \u0915\u093f \u0915\u092c \u0932\u093e\u092f\u0915 \u0939\u0948\u0964"',
        '\u091c\u092c \u0917\u094d\u0930\u093e\u0939\u0915 <strong>\u092a\u094d\u0930\u0924\u093f\u0926\u094d\u0935\u0902\u0926\u094d\u0935\u0940</strong> \u0915\u093e \u091c\u093f\u0915\u094d\u0930 \u0915\u0930\u0947, \u0906\u0924\u094d\u092e\u0935\u093f\u0936\u094d\u0935\u093e\u0938 \u0926\u093f\u0916\u093e\u090f\u0902: "\u092a\u0939\u0932\u0947 \u0939\u092e\u0947\u0902 \u0935\u093f\u091c\u093f\u091f \u0915\u0930\u0947\u0902, \u092b\u093f\u0930 \u0924\u0941\u0932\u0928\u093e \u0915\u0930\u0947\u0902\u0964"',
        '\u0939\u0930 \u0915\u0949\u0932 \u0915\u093e <strong>\u0935\u093f\u0936\u093f\u0937\u094d\u091f \u0905\u0917\u0932\u093e \u0915\u0926\u092e</strong> \u0939\u094b: \u092c\u0941\u0915 \u0935\u093f\u091c\u093f\u091f \u092f\u093e \u0928\u093f\u0930\u094d\u0927\u093e\u0930\u093f\u0924 \u0915\u0949\u0932\u092c\u0948\u0915\u0964 \u0915\u094b\u0908 \u0905\u092a\u0935\u093e\u0926 \u0928\u0939\u0940\u0902\u0964',
    ], ensure_ascii=False)

    js_code += """
var contentData = {};
contentData.en = { dos: """ + en_dos + """, donts: """ + en_donts + """, goldenRules: """ + en_rules + """ };
contentData.hi = { dos: """ + hi_dos + """, donts: """ + hi_donts + """, goldenRules: """ + hi_rules + """ };
"""

    # Now write the render function and app logic
    render_js = """
/* ====== RENDER FUNCTIONS ====== */
function renderAndShow(d) {
  window._reportData = d;
  // Apply language UI
  document.getElementById('lang-en').className = currentLang === 'en' ? 'active' : '';
  document.getElementById('lang-hi').className = currentLang === 'hi' ? 'active' : '';
  renderData(d);
}

function renderData(d) {
  var lang = langData[currentLang] || langData.en;
  var cont = contentData[currentLang] || contentData.en;

  document.getElementById('loading').style.display = 'none';
  document.getElementById('hero-sub').textContent = lang.heroSub(d);

  var metaHtml = [
    { num: d.total_calls, lbl: lang.metaLabels[0], cls: 'avg' },
    { num: d.avg_score + '/100', lbl: lang.metaLabels[1], cls: d.avg_score >= 60 ? 'good' : d.avg_score >= 30 ? 'avg' : 'bad' },
    { num: cont.dos.length, lbl: lang.metaLabels[2], cls: 'good' },
    { num: d.top_mistakes.length, lbl: lang.metaLabels[3], cls: 'bad' },
  ].map(function(m) {
    return '<div class="meta-item ' + m.cls + '"><div class="num">' + m.num + '</div><div class="lbl">' + m.lbl + '</div></div>';
  }).join('');
  document.getElementById('hero-meta').innerHTML = metaHtml;

  // Update UI labels
  document.getElementById('btn-print').textContent = lang.printBtn;
  document.getElementById('btn-preso').textContent = lang.presoBtn;
  document.getElementById('btn-share').textContent = lang.shareBtn;
  document.getElementById('share-tip').textContent = lang.shareTip;
  document.getElementById('footer-text').textContent = lang.footer;
  document.getElementById('loading-title').textContent = lang.loadingTitle;
  document.getElementById('loading-sub').innerHTML = lang.loadingSub;

  // Build tab pages
  var app = document.getElementById('app');
  app.innerHTML = buildTabs(d, lang, cont);

  // Tab switching
  var tabs = document.querySelectorAll('.tab');
  for (var ti = 0; ti < tabs.length; ti++) {
    (function(tab) {
      tab.addEventListener('click', function() {
        document.querySelectorAll('.tab').forEach(function(t) { t.classList.remove('active'); });
        document.querySelectorAll('.tab-page').forEach(function(p) { p.classList.remove('active'); });
        tab.classList.add('active');
        document.getElementById('page-' + tab.dataset.tab).classList.add('active');
      });
    })(tabs[ti]);
  }

  // Build preso slides
  buildPresoSlides(d, lang, cont);
}

function buildTabs(d, lang, cont) {
  var tabsHtml = ['<div class="tab-bar">'];
  var tabIds = ['cheatsheet', 'callflow', 'scripts', 'objections', 'roleplay', 'centertips'];
  for (var i = 0; i < tabIds.length; i++) {
    tabsHtml.push('<button class="tab' + (i === 0 ? ' active' : '') + '" data-tab="' + tabIds[i] + '">' + lang.tabs[i] + '</button>');
  }
  tabsHtml.push('</div>');

  tabsHtml.push('<div class="tab-page active" id="page-cheatsheet">' + renderCheatSheet(d, lang, cont) + '</div>');
  tabsHtml.push('<div class="tab-page" id="page-callflow">' + renderCallFlow(d, lang, cont) + '</div>');
  tabsHtml.push('<div class="tab-page" id="page-scripts">' + renderScriptFixes(d, lang) + '</div>');
  tabsHtml.push('<div class="tab-page" id="page-objections">' + renderObjections(d, lang, cont) + '</div>');
  tabsHtml.push('<div class="tab-page" id="page-roleplay">' + renderRolePlay(d, lang, cont) + '</div>');
  tabsHtml.push('<div class="tab-page" id="page-centertips">' + renderCenterTips(d, lang, cont) + '</div>');

  return tabsHtml.join('');
}
"""

    # Cheat Sheet render
    cheat_js = """
function renderCheatSheet(d, lang, cont) {
  var dos = cont.dos || [];
  var donts = cont.donts || [];
  var rules = cont.goldenRules || [];

  // Say-this pairs
  var sayPairs = buildSayPairs(currentLang);

  // Merge duplicate agent speaking mistakes - this is for the donuts section
  var mistakes = mergeDuplicates(d.top_mistakes || []);

  return '<div class="card">' +
    '<div class="section-title">' + lang.cheatTitle + '</div>' +
    '<p style="font-size:14px;color:#6b7280;margin-bottom:16px;">' + lang.cheatDesc(dos.length + donts.length + sayPairs.length + rules.length, d.total_calls) + '</p>' +

    /* DOS */
    '<div class="dos-donts-grid">' +
      '<div class="dos-box"><h3>' + lang.dosTitle(dos.length) + '</h3><div class="dos-list">' +
        dos.map(function(item, i) {
          return '<div><span style="color:#22c55e;font-weight:700;flex-shrink:0;">' + (i+1) + '.</span> <span>' + item + '</span></div>';
        }).join('') +
      '</div></div>' +

      /* DONTS */
      '<div class="donts-box"><h3>' + lang.dontsTitle(donts.length) + '</h3><div class="donts-list">' +
        donts.map(function(item, i) {
          return '<div><span style="color:#ef4444;font-weight:700;flex-shrink:0;">' + (i+1) + '.</span> <span>' + item + '</span></div>';
        }).join('') +
      '</div></div>' +
    '</div>' +

    /* Say-this pairs */
    '<div style="margin-top:20px;"><h3 style="font-size:16px;font-weight:700;margin-bottom:12px;">' + lang.sayTitle(sayPairs.length) + '</h3>' +
    sayPairs.map(function(p) {
      return '<div class="say-pair">' +
        '<div class="say-pair bad"><div class="label">' + (currentLang === 'hi' ? '\\u274c \\u092f\\u0939 \\u0928 \\u0915\\u0939\\u0947\\u0902' : '\\u274c ' + lang.dontSay) + '</div><div class="text">' + p.bad + '</div></div>' +
        '<div class="say-pair good"><div class="label">' + (currentLang === 'hi' ? '\\u2705 \\u092f\\u0939 \\u0915\\u0939\\u0947\\u0902' : '\\u2705 ' + lang.sayThis) + '</div><div class="text">' + p.good + '</div><div class="note">' + p.note + '</div></div>' +
      '</div>';
    }).join('') +
    '</div>' +

    /* Golden Rules */
    '<div class="golden-rules"><h3>' + lang.goldenTitle + '</h3>' +
    rules.map(function(rule, i) {
      return '<div class="golden-rule"><div class="num">' + (i+1) + '</div><div>' + rule + '</div></div>';
    }).join('') +
    '</div></div>';
}
"""

    # Say-this pairs
    say_pairs_js = """
function buildSayPairs(lang) {
  if (lang === 'hi') {
    return [
""" + """
      { bad: '"\\u092e\\u0948\\u0902 <span class=\\"bad\\">\\u0932\\u0915\\u094d\\u0937\\u094d\\u092e\\u0940 \\u0905\\u0915\\u093e\\u0921\\u092e\\u0940</span> \\u0938\\u0947 \\u092c\\u094b\\u0932 \\u0930\\u0939\\u093e \\u0939\\u0942\\u0902"', good: '"\\u092e\\u0948\\u0902 [\\u0928\\u093e\\u092e] <strong>\\u0932\\u093e\\u0915\\u092e\\u0947 \\u0905\\u0915\\u093e\\u0921\\u092e\\u0940</strong> \\u0938\\u0947 \\u092c\\u094b\\u0932 \\u0930\\u0939\\u093e \\u0939\\u0942\\u0902. \\u0932\\u093e\\u0915-\\u092e\\u0947, \\u092c\\u094d\\u0930\\u093e\\u0902\\u0921 \\u0915\\u0940 \\u0924\\u0930\\u0939"', note: '52% \\u0915\\u0949\\u0932\\u094b\\u0902 \\u092e\\u0947\\u0902 \\u092c\\u094d\\u0930\\u093e\\u0902\\u0921 \\u0928\\u093e\\u092e \\u0917\\u0932\\u0924 \\u0939\\u0948\\u0964 \\u092f\\u093e\\u0926 \\u0930\\u0916\\u0947\\u0902: \\u0932\\u093e\\u0915-\\u092e\\u0947\\u0964' },
    ];
  }
  // English
  return [
""" + """
    { bad: '"Hello, I\\'m calling from <span class=\"bad\">Lakshmi Academy</span>"', good: '"Hello, I\\'m [Name] from <strong>Lakm\u00e9 Academy</strong> \u2014 Lak-may, like the brand."', note: '52% of calls mess up the brand name. Practice: "Lak-may."' },
"""
    say_pairs_js += """
  ];
}
"""

    # Merged mistakes function
    misc_js = """
function mergeDuplicates(mistakes) {
  var out = [];
  var talkCount = 0;
  mistakes.forEach(function(m) {
    if (/Agent speaking/.test(m.mistake)) { talkCount++; }
    else { out.push(m); }
  });
  if (talkCount > 0) {
    out.push({ mistake: 'Agent talking too much \\u2014 listen more! 60:40 ratio is ideal', pct: talkCount + '% of calls' });
  }
  return out;
}

function toggleObjection(header) {
  header.classList.toggle('open');
  var body = header.nextElementSibling;
  if (body) body.classList.toggle('open');
}

function showRoleplay(i) {
  var s = window._rpScenarios[i];
  document.getElementById('rp-title').textContent = s.title;
  document.getElementById('rp-role').textContent = s.sub;
  document.getElementById('rp-agent').innerHTML = s.agent;
  document.getElementById('rp-tip').innerHTML = '\\ud83d\\udca1 ' + s.tip;
  document.getElementById('roleplay-detail').classList.add('open');
  document.querySelectorAll('.roleplay-card').forEach(function(c, j) {
    c.style.borderColor = j === i ? '#f97316' : '#e5e2dd';
  });
}
"""

    rest_js = """
/* ====== CALL FLOW ====== */
function renderCallFlow(d, lang, cont) {
"""

    # We need to simplify this approach. The file is too complex to generate programmatically like this.
    # Instead, let me write the complete JS to a .js file and read it back.
    
    with open(os.path.join(BASE, "training.html"), "w") as f:
        f.write(html)
        # Write data embedded
        # Write all the JS (data is embedded separately by embed_data.py)
        js_code += render_js + cheat_js + say_pairs_js + misc_js
        
        # Write the rest of the render functions
        f.write(js_code)
        f.write(generate_rest_js())
        f.write("""
/* ====== LOAD ====== */
function showErr(e) {
  var el = document.getElementById('loading');
  if (el) el.innerHTML = '<div style="color:#ef4444;font-size:14px;text-align:left;padding:16px;background:#fef2f2;border-radius:8px;"><b>ERROR</b><br>' + (e.message || e) + '<br><small>Type: ' + (e.constructor ? e.constructor.name : typeof e) + '</small></div>';
}
function loadReport() {
  if (_data && _data !== '__DATA_OBJECT__') {
    try {
      renderAndShow(_data);
      return;
    } catch(e) { showErr(e); }
  }
  var lang = langData[currentLang] || langData.en;
  document.getElementById('loading').innerHTML =
    '<div class="icon">\\ud83d\\udcc4</div><h2>' + lang.loadingTitle + '</h2><p>' + lang.loadingSub + '</p>';
}
try { loadReport(); } catch(e) { showErr(e); }
</script>
</body>
</html>""")
    print(f"Written: {html_path}")
    print(f"Size: {os.path.getsize(html_path)/1024:.0f} KB")


def generate_rest_js():
    """Generate the remaining render functions that are too complex to write inline."""
    return r"""
function renderCallFlow(d, lang, cont) {
  var steps = buildCallFlow(currentLang);
  var html = '<div class="card"><div class="section-title">' + lang.callFlowTitle + '</div>';
  html += '<p style="font-size:14px;color:#6b7280;margin-bottom:16px;">' + lang.callFlowDesc + '</p>';
  html += steps.map(function(s) {
    return '<div class="flow-step"><div><div class="step-num"></div></div><div style="flex:1;">' +
      '<div class="step-title" style="font-size:15px;">' + s.title + ' <span style="font-weight:400;font-size:12px;color:#6b7280;">' + s.time + '</span></div>' +
      '<div class="step-desc">' + s.desc + '</div>' +
      '<div class="step-do">&#9989; ' + s.do_script + '</div>' +
      '<div class="step-dont">&#10060; ' + s.dont_script + '</div>' +
      '<ul class="step-sub-points">' + s.sub.map(function(pt) { return '<li>' + pt + '</li>'; }).join('') + '</ul></div></div>';
  }).join('') + '</div>';
  return html;
}

function buildCallFlow(lang) {
  if (lang === 'hi') {
    return [
      { title: '1. \u0928\u092e\u0938\u094d\u0915\u093e\u0930 \u0914\u0930 \u092a\u0930\u093f\u091a\u092f', time: '0:00 \u2013 0:20',
        desc: '\u0917\u0930\u094d\u092e\u091c\u094b\u0936\u0940 \u0938\u0947 \u0928\u092e\u0938\u094d\u0915\u093e\u0930 + \u0906\u092a\u0915\u093e \u0928\u093e\u092e + \u0932\u093e\u0915\u092e\u0947 \u0905\u0915\u093e\u0921\u092e\u0940 + \u092a\u0941\u0937\u094d\u091f\u093f \u0915\u0930\u0947\u0902 \u0915\u093f \u0938\u0939\u0940 \u0935\u094d\u092f\u0915\u094d\u0924\u093f \u0938\u0947 \u092c\u093e\u0924 \u0915\u0930 \u0930\u0939\u0947 \u0939\u0948\u0902\u0964',
        do_script: '"\u0928\u092e\u0938\u094d\u0924\u0947, \u092e\u0948\u0902 \u0932\u093e\u0915\u092e\u0947 \u0905\u0915\u093e\u0921\u092e\u0940 \u0938\u0947 \u092c\u094b\u0932 \u0930\u0939\u093e \u0939\u0942\u0902\u0964 \u0915\u094d\u092f\u093e \u092e\u0948\u0902 \u0936\u094d\u0930\u0940\u092e\u0924\u0940 \u0930\u093f\u0924\u0941 \u0938\u0947 \u092c\u093e\u0924 \u0915\u0930 \u0930\u0939\u093e \u0939\u0942\u0902?"',
        dont_script: '"\u0939\u0947\u0932\u094b, \u092e\u0948\u0902 \u0932\u0915\u094d\u0937\u094d\u092e\u0940 \u0905\u0915\u093e\u0921\u092e\u0940 \u0938\u0947 \u092c\u094b\u0932 \u0930\u0939\u093e \u0939\u0942\u0902\u0964"',
        sub: ['"\u0932\u093e\u0915-\u092e\u0947" \u0915\u093e \u0938\u0939\u0940 \u0909\u091a\u094d\u091a\u093e\u0930\u0923 \u0915\u0930\u0947\u0902', '\u0924\u0941\u0930\u0902\u0924 \u0930\u093f\u0936\u094d\u0924\u093e \u092c\u0928\u093e\u0928\u0947 \u0915\u0947 \u0932\u093f\u090f \u0917\u094d\u0930\u093e\u0939\u0915 \u0915\u093e \u0928\u093e\u092e \u092a\u0942\u091b\u0947\u0902', '\u092e\u0941\u0938\u094d\u0915\u0941\u0930\u093e\u0915\u0930 \u092c\u093e\u0924 \u0915\u0930\u0947\u0902 \u2014 \u0906\u0935\u093e\u091c\u093c \u092c\u0926\u0932 \u091c\u093e\u0924\u0940 \u0939\u0948'] },
      { title: '2. \u091c\u0930\u0942\u0930\u0924 \u091c\u093e\u0928\u0947\u0902', time: '0:20 \u2013 1:30',
        desc: '\u0915\u094b\u0908 \u092d\u0940 \u0915\u094b\u0930\u094d\u0938 \u092c\u0924\u093e\u0928\u0947 \u0938\u0947 \u092a\u0939\u0932\u0947 2-3 \u0938\u0935\u093e\u0932 \u092a\u0942\u091b\u0947\u0902\u0964',
        do_script: '"\u0915\u094d\u092f\u093e \u0906\u092a \u0936\u0941\u0930\u0941\u0906\u0924 \u0915\u0930 \u0930\u0939\u0947 \u0939\u0948\u0902 \u092f\u093e \u092a\u0939\u0932\u0947 \u0938\u0947 \u092e\u0947\u0915\u092a \u0915\u0930\u0924\u0940 \u0939\u0948\u0902? \u0906\u092a\u0915\u093e \u0932\u0915\u094d\u0937\u094d\u092f \u0915\u094d\u092f\u093e \u0939\u0948 - \u0915\u0930\u093f\u092f\u0930 \u092f\u093e \u092a\u0930\u0938\u0928\u0932?"',
        dont_script: '"\u0939\u092e\u093e\u0930\u0947 \u092a\u093e\u0938 \u092c\u0947\u0938\u093f\u0915, \u092a\u094d\u0930\u094b \u0914\u0930 \u092e\u093e\u0938\u094d\u091f\u0930 \u0915\u094b\u0930\u094d\u0938 \u0939\u0948\u0902\u0964 \u0915\u094c\u0928 \u0938\u093e \u0932\u0947\u0928\u093e \u091a\u093e\u0939\u094b\u0917\u0947?"',
        sub: ['60% \u0938\u0941\u0928\u0947\u0902, 40% \u092c\u094b\u0932\u0947\u0902', '\u092a\u0939\u091a\u093e\u0928\u0947\u0902: \u0905\u0928\u0941\u092d\u0935 \u0938\u094d\u0924\u0930, \u0932\u0915\u094d\u0937\u094d\u092f, \u0938\u092e\u092f \u0938\u0940\u092e\u093e', '\u0917\u094d\u0930\u093e\u0939\u0915 \u0915\u094b \u0905\u092a\u0928\u0940 \u091c\u0930\u0942\u0930\u0924 \u092c\u0924\u093e\u0928\u0947 \u0926\u0947\u0902'] },
      { title: '3. \u0938\u092e\u093e\u0927\u093e\u0928 \u092a\u0947\u0936 \u0915\u0930\u0947\u0902', time: '1:30 \u2013 3:00',
        desc: '\u091c\u0930\u0942\u0930\u0924 \u0915\u0947 \u0939\u093f\u0938\u093e\u092c \u0938\u0947 \u090f\u0915 \u0915\u094b\u0930\u094d\u0938 \u0938\u0941\u091d\u093e\u090f\u0902\u0964 \u0915\u0940\u092e\u0924 \u0938\u0947 \u092a\u0939\u0932\u0947 \u092e\u0942\u0932\u094d\u092f \u092c\u0924\u093e\u090f\u0902\u0964',
        do_script: '"\u0939\u092e\u093e\u0930\u0947 \u092a\u094d\u0930\u094b \u0915\u094b\u0930\u094d\u0938 \u0938\u0947 \u092a\u093f\u091b\u0932\u0947 \u091b\u093e\u0924\u094d\u0930 3 \u092e\u0939\u0940\u0928\u0947 \u092e\u0947\u0902 \u20b915-25K/\u092e\u0939\u0940\u0928\u093e \u0915\u092e\u093e\u0928\u0947 \u0932\u0917\u0947\u0964"',
        dont_script: '"\u092a\u094d\u0930\u094b \u0915\u094b\u0930\u094d\u0938 \u20b945,000 \u0915\u093e \u0939\u0948\u0964 \u092c\u0947\u0938\u093f\u0915 \u20b925,000 \u0915\u093e \u0939\u0948\u0964"',
        sub: ['\u092e\u0942\u0932\u094d\u092f \u092a\u0939\u0932\u0947, \u0915\u0940\u092e\u0924 \u092c\u093e\u0926 \u092e\u0947\u0902', '\u092a\u094d\u0932\u0947\u0938\u092e\u0947\u0902\u091f/\u0915\u092e\u093e\u0908 \u0915\u0947 \u0906\u0902\u0915\u0921\u093c\u0947 \u092c\u0924\u093e\u090f\u0902', '\u0905\u0938\u0932\u0940 \u091b\u093e\u0924\u094d\u0930\u094b\u0902 \u0915\u0940 \u0915\u0939\u093e\u0928\u093f\u092f\u093e\u0901 \u0938\u0941\u091d\u093e\u090f\u0902'] },
      { title: '4. \u0906\u092a\u0924\u094d\u0924\u093f\u092f\u094b\u0902 \u0915\u093e \u0938\u092e\u093e\u0927\u093e\u0928', time: '3:00 \u2013 4:00',
        desc: '\u0906\u092a\u0924\u094d\u0924\u093f\u092f\u093e\u0901 = \u0916\u0930\u0940\u0926\u093e\u0930\u0940 \u0915\u0947 \u0938\u0902\u0915\u0947\u0924\u0964 \u0938\u0939\u093e\u0928\u0941\u092d\u0942\u0924\u093f + \u0938\u092c\u0942\u0924 \u0938\u0947 \u0928\u093f\u092a\u091f\u0947\u0902\u0964',
        do_script: '"\u092e\u0948\u0902 \u0938\u092e\u091d\u0924\u093e \u0939\u0942\u0902\u0964 \u0915\u0908 \u091b\u093e\u0924\u094d\u0930\u094b\u0902 \u0928\u0947 \u092f\u0939\u0940 \u0938\u094b\u091a\u093e \u0925\u093e\u0964 EMI \u0938\u093f\u0930\u094d\u092b \u20b91,500/\u092e\u0939\u0940\u0928\u093e \u0939\u0948\u0964 \u0906\u092a \u0935\u0939 \u0939\u092b\u094d\u0924\u0947 \u092e\u0947\u0902 \u0935\u093e\u092a\u0938 \u0915\u092e\u093e \u0932\u0947\u0902\u0917\u0947\u0964"',
        dont_script: '"\u092f\u0939 \u0924\u094b \u0926\u0942\u0938\u0930\u094b\u0902 \u0915\u0940 \u0924\u0941\u0932\u0928\u093e \u092e\u0947\u0902 \u092c\u0939\u0941\u0924 \u0938\u0938\u094d\u0924\u093e \u0939\u0948\u0964"',
        sub: ['\u092a\u0939\u0932\u0947 \u091a\u093f\u0902\u0924\u093e \u0938\u094d\u0935\u0940\u0915\u093e\u0930 \u0915\u0930\u0947\u0902', '\u0915\u0940\u092e\u0924 \u0915\u094b \u0928\u093f\u0935\u0947\u0936 \u0915\u0939\u0915\u0930 \u092a\u0947\u0936 \u0915\u0930\u0947\u0902', '\u0938\u093e\u092e\u093e\u091c\u093f\u0915 \u092a\u094d\u0930\u092e\u093e\u0923 \u0914\u0930 \u092a\u094d\u0930\u0936\u0902\u0938\u093e\u090f\u0901 \u0926\u093f\u0916\u093e\u090f\u0902'] },
      { title: '5. \u0935\u093f\u091c\u093f\u091f \u092c\u0941\u0915 \u0915\u0930\u0947\u0902', time: '4:00 \u2013 5:00',
        desc: '\u090f\u0915 \u0932\u0915\u094d\u0937\u094d\u092f\u0964 \u0925\u094b\u0938 \u0914\u0930 \u0938\u092e\u092f \u092c\u0924\u093e\u090f\u0902, \u0935\u093f\u091c\u093f\u091f \u092e\u093e\u0928 \u0932\u0947\u0902, \u092a\u0941\u0937\u094d\u091f\u093f \u0915\u0930\u0947\u0902\u0964',
        do_script: '"\u092e\u0948\u0902 \u0906\u092a\u0915\u093e \u092e\u0941\u092b\u094d\u0924 \u0921\u0947\u092e\u094b \u092c\u0941\u0915 \u0915\u0930 \u0926\u0942\u0902\u0964 \u0915\u094d\u092f\u093e \u0906\u092a \u0906\u091c \u0936\u093e\u092e 4 \u092c\u091c\u0947 \u092f\u093e \u0915\u0932 11 \u092c\u091c\u0947 \u0906 \u0938\u0915\u0924\u0947 \u0939\u0948\u0902?"',
        dont_script: '"\u0924\u094b \u0905\u0917\u0930 \u0915\u092d\u0940 \u0906\u0928\u093e \u0939\u094b \u0924\u094b \u092c\u0924\u093e\u090f\u0928\u0917\u093e\u0964"',
        sub: ['2 \u0935\u093f\u0936\u093f\u0937\u094d\u091f \u0938\u092e\u092f \u0935\u093f\u0915\u0932\u094d\u092a \u0926\u0947\u0902', '\u0939\u093e\u0901 \u092e\u093e\u0928 \u0915\u0930 \u091a\u0932\u0947\u0902: "\u092e\u0948\u0902 30 \u092e\u093f\u0928\u091f \u092c\u0941\u0915 \u0915\u0930 \u0930\u0939\u093e \u0939\u0942\u0902"', '\u092a\u0941\u0937\u094d\u091f\u093f\u0924 \u0938\u092e\u092f + \u0915\u093e\u0932\u094d\u092c\u0947\u0915 \u092f\u094b\u091c\u0928\u093e \u0915\u0947 \u0938\u093e\u0925 \u0938\u092e\u093e\u092a\u094d\u0924 \u0915\u0930\u0947\u0902'] },
    ];
  }
  return [
    { title: '1. Greet & Introduce', time: '0:00 \u2013 0:20',
      desc: 'Warm greeting + your name + Lakm\u00e9 Academy + confirm right person.',
      do_script: '"Hi, I\'m Deepti from <strong>Lakm\u00e9 Academy</strong>, Noida. Am I speaking to Ms. Ritu?"',
      dont_script: '"Hello, I\'m calling from Lakshmi Academy."',
      sub: ['Say "Lak-may" \u2014 not "Lakshmi"', 'Use their name immediately', 'Smile while talking'] },
      { title: '2. Discover Needs', time: '0:20 \u2013 1:30',
        desc: 'Ask 2-3 discovery questions before mentioning any course.',
        do_script: '"Are you a beginner or already doing makeup? What\'s your goal-career or personal?"',
        dont_script: '"We have basic, pro, and master courses. Which one?"',
        sub: ['Listen 60%, talk 40%', 'Qualify: experience level, goal, timeline', 'Let customer reveal their need'] },
      { title: '3. Present Solution', time: '1:30 \u2013 3:00',
        desc: 'Recommend ONE course that fits. Add value before price.',
        do_script: '"With our Pro Course, past students started earning \u20b915-25K/month within 3 months."',
        dont_script: '"The Pro Course is \u20b945,000. We also have a basic one for \u20b925,000."',
        sub: ['Value first, price second', 'Mention placement/earnings data', 'Use real student stories'] },
      { title: '4. Handle Objections', time: '3:00 \u2013 4:00',
        desc: 'Objections = buying signals. Handle with empathy + proof.',
        do_script: '"I understand. Many felt the same. The EMI is only \u20b91,500/month. You\'ll earn that back in week 1."',
        dont_script: '"It\'s actually very cheap compared to others."',
        sub: ['Acknowledge the concern first', 'Reframe price as investment', 'Use social proof testimonials'] },
      { title: '5. Book the Visit', time: '4:00 \u2013 5:00',
        desc: 'The ONE goal. Be specific, assume the visit, confirm.',
        do_script: '"Let me book your free demo. Can you come today at 4 PM or tomorrow 11 AM?"',
        dont_script: '"So, let me know if you want to visit sometime."',
        sub: ['Offer 2 specific time options', 'Assume YES: "I\'ll block 30 min for you"', 'End with confirmed time + callback plan'] },
  ];
}

/* ====== SCRIPT FIXES ====== */
function renderScriptFixes(d, lang) {
  var mistakes = d.top_mistakes.slice(0, 8);
  var html = '<div class="card"><div class="section-title">' + lang.scriptTitle + '</div>';
  html += '<p style="font-size:14px;color:#6b7280;margin-bottom:16px;">' + lang.scriptDesc + '</p><div class="mistakes-list">';
  mistakes.forEach(function(m) {
    html += '<div class="mistake-item"><div class="badge red">' + m.pct + '%</div><span>' + m.mistake + '</span></div>';
  });
  html += '</div></div>';
  html += '<div class="card"><h3 style="font-size:16px;font-weight:700;margin-bottom:12px;">' + (lang === 'hi' ? '\u092c\u093e\u0924\u091a\u0940\u0924 \u0938\u0941\u0927\u093e\u0930 \u092f\u0941\u0917\u094d\u092e' : 'Talk-Fix Pairs') + '</h3>' + buildSayPairs(currentLang).map(function(p) {
    return '<div class="say-pair"><div class="say-pair bad"><div class="label">\u274c ' + (lang === 'hi' ? '\u0917\u0932\u0924' : 'Instead of') + '</div><div class="text">' + p.bad + '</div></div><div class="say-pair good"><div class="label">\u2705 ' + (lang === 'hi' ? '\u0938\u0939\u0940' : 'Say this') + '</div><div class="text">' + p.good + '</div><div class="note">' + p.note + '</div></div></div>';
  }).join('') + '</div>';
  return html;
}

/* ====== OBJECTIONS ====== */
function renderObjections(d, lang, cont) {
  var obs = cont.objections || [
    { objection: '\u201cIt\'s too expensive.\u201d', response: '\u201cI understand. Many students felt the same. With our EMI option it\u2019s just \u20b91,500/month \u2014 you\u2019ll earn that back in week 1 of working.\u201d', tip: 'Reframe price as monthly investment, not lump sum.' },
    { objection: '\u201cI need to think about it.\u201d', response: '\u201cCompletely get it. What\u2019s the main thing you\u2019re unsure about? Let me help clear that up.\u201d', tip: 'Isolate the real objection \u2014 it\u2019s usually price or time.' },
    { objection: '\u201cI\u2019m busy right now.\u201d', response: '\u201cNo problem at all! Would tomorrow 11 AM or 4 PM work better? I\u2019ll keep it brief \u2014 10 minutes max.\u201d', tip: 'Lock a specific callback time immediately.' },
    { objection: '\u201cI\u2019ll check online.\u201d', response: '\u201cGreat idea! Though most students say visiting once makes the decision much easier. Can you come by today at 4 for a quick tour?\u201d', tip: 'Don\u2019t argue \u2014 pivot to visit.' },
    { objection: '\u201cI\u2019m already talking to other institutes.\u201d', response: '\u201cYou should! What I\u2019d suggest is visit us too so you can compare. Our placement record is one of the best.\u201d', tip: 'Welcome comparison \u2014 let your center visit win.' },
  ];
  var html = '<div class="card"><div class="section-title">' + lang.objTitle(obs.length) + '</div>';
  html += '<p style="font-size:14px;color:#6b7280;margin-bottom:16px;">' + lang.objDesc + '</p>';
  obs.forEach(function(o, i) {
    html += '<div class="objection-item"><div class="objection-header" onclick="toggleObjection(this)"><span>' + o.objection + '</span><span style="font-size:18px;">+</span></div><div class="objection-body"><div style="background:#f0fdf4;padding:10px 14px;border-radius:8px;margin:8px 0;font-size:14px;"><strong>' + (lang === 'hi' ? '\u091c\u0935\u093e\u092c' : 'Response') + ':</strong> ' + o.response + '</div><div style="font-size:12px;color:#6b7280;padding:4px 14px 8px;">\ud83d\udca1 ' + o.tip + '</div></div></div>';
  });
  html += '</div>';
  return html;
}

/* ====== ROLE PLAY ====== */
function renderRolePlay(d, lang, cont) {
  var rp = cont.roleplay || [
    { title: lang === 'hi' ? '\u092c\u094d\u0930\u093e\u0902\u0921 \u0928\u093e\u092e \u0938\u0941\u0927\u093e\u0930\u0947\u0902' : 'Fix the Brand Name', sub: lang === 'hi' ? '\u0917\u094d\u0930\u093e\u0939\u0915 \u0928\u0947 \u0917\u0932\u0924 \u0928\u093e\u092e \u0938\u0941\u0928\u093e' : 'Customer heard wrong name', agent: lang === 'hi' ? '\u0906\u092a: \u0928\u092e\u0938\u094d\u0924\u0947! \u092e\u0948\u0902 \u0932\u093e\u0915\u092e\u0947 \u0905\u0915\u093e\u0921\u092e\u0940 \u0938\u0947 \u092c\u094b\u0932 \u0930\u0939\u093e \u0939\u0942\u0902, \u0928\u0949\u092f\u0921\u093e\u0964 \u0932\u093e\u0915-\u092e\u0947, \u092c\u094d\u0930\u093e\u0902\u0921 \u0915\u0940 \u0924\u0930\u0939\u0964 \u0915\u094d\u092f\u093e \u092e\u0948\u0902 \u0936\u094d\u0930\u0940\u092e\u0924\u0940 \u0930\u093f\u0924\u0941 \u0938\u0947 \u092c\u093e\u0924 \u0915\u0930 \u0930\u0939\u093e \u0939\u0942\u0902?' : 'You: Hi! I\'m calling from <strong>Lakm\u00e9 Academy</strong>, Noida. Lak-may, like the brand. Am I speaking to Ms. Ritu?', tip: lang === 'hi' ? '\u0932\u093e\u0915-\u092e\u0947 \u0915\u094b 2\u092c\u093e\u0930 \u0915\u0939\u0947\u0902: \u092a\u0939\u0932\u0947 \u0928\u093e\u092e \u092e\u0947\u0902, \u092b\u093f\u0930 \u0938\u094d\u092a\u0937\u094d\u091f\u0940\u0915\u0930\u0923 \u092e\u0947\u0902\u0964 \u092f\u0939 \u090f\u0915 \u0938\u093e\u0926\u093e \u092c\u0926\u0932\u093e\u0935 52% \u0915\u0949\u0932\u094b\u0902 \u0915\u0940 \u0938\u092e\u0938\u094d\u092f\u093e \u0939\u0932 \u0915\u0930\u0924\u093e \u0939\u0948\u0964' : 'Say Lak-may TWICE: in the name and then clarify. This one simple fix addresses 52% of calls.' },
    { title: lang === 'hi' ? '\u091c\u0930\u0942\u0930\u0924 \u092a\u0939\u0932\u0947 \u092a\u0942\u091b\u0947\u0902' : 'Discover First', sub: lang === 'hi' ? '\u0917\u094d\u0930\u093e\u0939\u0915 \u0928\u0947 \u0915\u094b\u0930\u094d\u0938 \u0915\u0947 \u092c\u093e\u0930\u0947 \u092e\u0947\u0902 \u092a\u0942\u091b\u093e' : 'Customer asked about courses', agent: lang === 'hi' ? '\u0906\u092a: \u092c\u093f\u0932\u094d\u0915\u0941\u0932! \u092a\u0939\u0932\u0947 \u092c\u0924\u093e\u090f\u0902 \u2014 \u0915\u094d\u092f\u093e \u0906\u092a \u0928\u090f \u0939\u0948\u0902 \u092f\u093e \u092a\u0939\u0932\u0947 \u0938\u0947 \u092e\u0947\u0915\u092a \u0915\u0930\u0924\u0940 \u0939\u0948\u0902? \u0914\u0930 \u0906\u092a\u0915\u093e \u0932\u0915\u094d\u0937\u094d\u092f \u0915\u094d\u092f\u093e \u0939\u0948?' : 'You: Of course! First tell me \u2014 are you a beginner or already doing makeup? And what\u2019s your goal?', tip: lang === 'hi' ? '\u0915\u092d\u0940 \u092d\u0940 \u0938\u0940\u0927\u0947 \u0915\u094b\u0930\u094d\u0938 \u0915\u0940 \u091c\u093e\u0928\u0915\u093e\u0930\u0940 \u0926\u0947\u0928\u0947 \u0938\u0947 \u092a\u0939\u0932\u0947 \u090f\u0915 \u0938\u0935\u093e\u0932 \u092a\u0942\u091b\u0947\u0902\u0964 \u092f\u0939 \u0906\u092a\u0915\u0947 \u0938\u0941\u091d\u093e\u0935 \u0915\u094b 10\u0917\u0941\u0923\u093e \u092c\u0947\u0939\u0924\u0930 \u092c\u0928\u093e\u090f\u0917\u093e\u0964' : 'Always ask one question before giving any course info. It makes your recommendation 10x more relevant.' },
    { title: lang === 'hi' ? '\u092e\u0942\u0932\u094d\u092f \u092a\u0939\u0932\u0947, \u0915\u0940\u092e\u0924 \u092c\u093e\u0926 \u092e\u0947\u0902' : 'Value Before Price', sub: lang === 'hi' ? '\u0917\u094d\u0930\u093e\u0939\u0915 \u0928\u0947 \u092b\u0940 \u092a\u0942\u091b\u093e' : 'Customer asked about fees', agent: lang === 'hi' ? '\u0906\u092a: \u092a\u094d\u0930\u094b \u0915\u094b\u0930\u094d\u0938 \u0938\u0947 \u0939\u092e\u093e\u0930\u0947 \u091b\u093e\u0924\u094d\u0930 3 \u092e\u0939\u0940\u0928\u0947 \u092e\u0947\u0902 \u20b915-25K/\u092e\u0939\u0940\u0928\u093e \u0915\u092e\u093e\u0928\u0947 \u0932\u0917\u0924\u0947 \u0939\u0948\u0902\u0964 \u0914\u0930 EMI \u0938\u093f\u0930\u094d\u092b \u20b91,500/\u092e\u0939\u0940\u0928\u093e \u0939\u0948\u0964 \u092f\u0939 \u0916\u0930\u094d\u091a \u0928\u0939\u0940\u0902, \u0928\u093f\u0935\u0947\u0936 \u0939\u0948\u0964' : 'You: Our Pro Course students start earning \u20b915-25K/month within 3 months. The EMI is only \u20b91,500/month. This isn\u2019t an expense \u2014 it\u2019s an investment.', tip: lang === 'hi' ? '\u0915\u0940\u092e\u0924 \u092c\u0924\u093e\u0928\u0947 \u0938\u0947 \u092a\u0939\u0932\u0947 \u0939\u092e\u0947\u0936\u093e \u092a\u0939\u0932\u0947 \u092e\u0942\u0932\u094d\u092f \u092c\u0924\u093e\u090f\u0902\u0964 \u0906\u092f \u0915\u0940 \u0938\u0902\u0916\u094d\u092f\u093e \u092a\u0939\u0932\u0947, \u092b\u093f\u0930 \u0915\u0940\u092e\u0924\u0964' : 'Always lead with value before price. Earnings first, investment second.' },
  ];
  window._rpScenarios = rp;
  var html = '<div class="card"><div class="section-title">' + lang.rpTitle(rp.length) + '</div>';
  html += '<p style="font-size:14px;color:#6b7280;margin-bottom:16px;">' + lang.rpDesc + '</p><div class="roleplay-grid">';
  rp.forEach(function(s, i) {
    html += '<div class="roleplay-card" onclick="showRoleplay(' + i + ')" style="cursor:pointer;padding:14px;border-radius:10px;border:1px solid #e5e2dd;background:#fafaf9;transition:border-color .15s;"><div style="font-weight:600;font-size:14px;">' + s.title + '</div><div style="font-size:12px;color:#6b7280;margin-top:4px;">' + s.sub + '</div></div>';
  });
  html += '</div><div id="roleplay-detail" style="margin-top:16px;padding:16px;border-radius:10px;background:#fff7ed;border:1px solid #fed7aa;"><div id="rp-title" style="font-weight:700;font-size:15px;margin-bottom:8px;"></div><div id="rp-role" style="font-size:12px;color:#6b7280;margin-bottom:8px;"></div><div id="rp-agent" style="font-size:14px;background:#f0fdf4;padding:10px 14px;border-radius:8px;margin-bottom:8px;"></div><div id="rp-tip" style="font-size:13px;color:#92400e;padding:6px 0;"></div></div></div>';
  return html;
}

/* ====== CENTER TIPS ====== */
function renderCenterTips(d, lang, cont) {
  var centers = d.centers || {};
  var centerNames = Object.keys(centers);
  var html = '<div class="card"><div class="section-title">' + (lang === 'hi' ? '\u0915\u0947\u0902\u0926\u094d\u0930-\u0935\u093e\u0930 \u091c\u093e\u0928\u0915\u093e\u0930\u0940' : 'Center-wise Insights') + '</div>';
  html += '<p style="font-size:14px;color:#6b7280;margin-bottom:16px;">' + (lang === 'hi' ? '\u092a\u094d\u0930\u0924\u094d\u092f\u0947\u0915 \u0915\u0947\u0902\u0926\u094d\u0930 \u0915\u0947 \u092a\u094d\u0930\u0926\u0930\u094d\u0936\u0928 \u0915\u093e \u0935\u093f\u0936\u094d\u0932\u0947\u0937\u0923' : 'Performance breakdown by center') + '</p><div class="centers-grid">';
  centerNames.forEach(function(name) {
    var c = centers[name];
    var scoreClass = c.avg_score >= 30 ? 'good' : c.avg_score >= 20 ? 'avg' : 'bad';
    html += '<div class="center-card" style="padding:14px;border-radius:10px;background:#fafaf9;border:1px solid #e5e2dd;"><div style="font-weight:700;font-size:15px;text-transform:capitalize;">' + name.replace(/-/g, ' ') + '</div><div style="display:flex;gap:10px;margin-top:8px;flex-wrap:wrap;"><div class="badge ' + scoreClass + '">' + (lang === 'hi' ? '\u0914\u0938\u0924' : 'Avg') + ': ' + c.avg_score + '</div><div class="badge" style="background:#dbeafe;color:#1d4ed8;">' + (lang === 'hi' ? '\u0915\u0941\u0932' : 'Total') + ': ' + c.total + '</div><div class="badge" style="background:#f0fdf4;color:#15803d;">' + (lang === 'hi' ? '\u0938\u092c\u0938\u0947 \u0905\u091a\u094d\u091b\u093e' : 'Best') + ': ' + c.best + '</div><div class="badge" style="background:#fef2f2;color:#dc2626;">' + (lang === 'hi' ? '\u0938\u092c\u0938\u0947 \u0916\u0930\u093e\u092c' : 'Worst') + ': ' + c.worst + '</div></div></div>';
  });
  html += '</div></div>';
  html += '<div class="card"><h3 style="font-size:16px;font-weight:700;margin-bottom:12px;">' + (lang === 'hi' ? '\u0938\u092d\u0940 \u0915\u0947\u0902\u0926\u094d\u0930\u094b\u0902 \u0915\u0947 \u0932\u093f\u090f \u091f\u093f\u092a\u094d\u0938' : 'Tips for All Centers') + '</h3><div class="dos-list">' + cont.dos.map(function(item) { return '<div><span style="color:#22c55e;font-weight:700;flex-shrink:0;">\u2713</span> <span>' + item + '</span></div>'; }).join('') + '</div></div>';
  return html;
}

/* ====== PRESENTATION SLIDES ====== */
function buildPresoSlides(d, lang, cont) {
  var slides = [
    { title: lang.presSlides[0], content: '<div style="font-size:clamp(32px,8vw,64px);font-weight:800;text-align:center;color:#f97316;">' + d.total_calls + '</div><div style="font-size:clamp(18px,4vw,28px);text-align:center;margin-top:8px;color:#fff;">' + (lang === 'hi' ? '\u0915\u0949\u0932\u094b\u0902 \u0915\u093e \u0935\u093f\u0936\u094d\u0932\u0947\u0937\u0923' : 'Calls Analyzed') + '</div><div style="font-size:16px;text-align:center;margin-top:20px;color:rgba(255,255,255,.6);">' + (lang === 'hi' ? '3 \u0915\u0947\u0902\u0926\u094d\u0930\u094b\u0902 \u0938\u0947 \u0921\u0947\u091f\u093e' : 'Data from 3 centers') + '</div>' },
    { title: lang.presSlides[1], content: '<div style="text-align:center;"><div style="font-size:clamp(40px,10vw,72px);font-weight:800;color:' + (d.avg_score >= 60 ? '#22c55e' : d.avg_score >= 30 ? '#f97316' : '#ef4444') + ';">' + d.avg_score + '<span style="font-size:0.4em;opacity:.5;">/100</span></div><div style="font-size:clamp(16px,3vw,22px);margin-top:8px;color:#fff;">' + (lang === 'hi' ? '\u0914\u0938\u0924 \u0938\u094d\u0915\u094b\u0930' : 'Average Score') + '</div></div>' },
    { title: lang.presSlides[2], content: '<div class="dos-donts-grid"><div class="dos-box"><h3>' + lang.dosTitle(cont.dos.length) + '</h3><div class="dos-list">' + cont.dos.slice(0, 8).map(function(item, i) { return '<div><span style="color:#22c55e;font-weight:700;">' + (i+1) + '.</span> <span>' + item + '</span></div>'; }).join('') + '</div></div><div class="donts-box"><h3>' + lang.dontsTitle(cont.donts.length) + '</h3><div class="donts-list">' + cont.donts.slice(0, 8).map(function(item, i) { return '<div><span style="color:#ef4444;font-weight:700;">' + (i+1) + '.</span> <span>' + item + '</span></div>'; }).join('') + '</div></div></div>' },
    { title: lang.presSlides[3], content: '<div>' + buildCallFlow(currentLang).map(function(s) { return '<div style="margin-bottom:12px;padding:10px 14px;background:rgba(255,255,255,.06);border-radius:8px;"><div style="font-weight:600;font-size:14px;">' + s.title + ' <span style="font-weight:400;font-size:12px;opacity:.5;">' + s.time + '</span></div><div style="font-size:13px;margin-top:4px;opacity:.8;">' + s.desc + '</div></div>'; }).join('') + '</div>' },
    { title: lang.presSlides[4], content: '<div style="text-align:center;"><div style="font-size:clamp(28px,6vw,48px);font-weight:800;color:#22c55e;">' + (lang === 'hi' ? '\u092f\u093e\u0926 \u0930\u0916\u0947\u0902' : 'Remember') + '</div><div style="font-size:clamp(16px,3vw,24px);margin-top:16px;color:#fff;line-height:1.8;">' + (lang === 'hi' ? '\u0939\u0930 \u0915\u0949\u0932 \u0915\u093e \u090f\u0915 \u0932\u0915\u094d\u0937\u094d\u092f: <span style="color:#f97316;">\u0938\u0947\u0902\u091f\u0930 \u0935\u093f\u091c\u093f\u091f</span>\n\u092a\u0942\u091b\u0947\u0902 \u092a\u0939\u0932\u0947, \u092c\u0924\u093e\u090f\u0902 \u092c\u093e\u0926 \u092e\u0947\u0902\n\u092e\u0942\u0932\u094d\u092f \u092a\u0947\u0936 \u0915\u0930\u0947\u0902, \u092b\u093f\u0930 \u0915\u0940\u092e\u0924\n\u0939\u092e\u0947\u0936\u093e \u0926\u094b \u0938\u092e\u092f \u0935\u093f\u0915\u0932\u094d\u092a \u0926\u0947\u0902' : 'ONE goal per call: <span style="color:#f97316;">Book the visit</span>\nDiscover first, recommend second\nValue first, price second\nAlways offer 2 time options') + '</div></div>' },
  ];
  var presoHtml = '';
  slides.forEach(function(s, i) {
    presoHtml += '<div class="preso-slide' + (i === 0 ? ' active' : '') + '" data-slide="' + i + '"><div style="padding:' + (i === 0 ? '40px 24px' : '24px') + ';display:flex;flex-direction:column;justify-content:center;min-height:60vh;">' + (i > 0 ? '<div style="font-size:13px;font-weight:600;color:rgba(255,255,255,.4);margin-bottom:12px;text-transform:uppercase;letter-spacing:1px;">' + s.title + '</div>' : '') + '<div>' + s.content + '</div></div></div>';
  });
  document.getElementById('preso-container').innerHTML = presoHtml;
  window._presoSlides = document.querySelectorAll('.preso-slide');
  window._presoIdx = 0;
}
"""

if __name__ == "__main__":
    build_html()
