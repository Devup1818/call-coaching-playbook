#!/usr/bin/env python3
"""Build the complete training.html with Hindi/English language selector."""
import os

BASE = os.path.dirname(os.path.abspath(__file__))

# ============================================================
# CSS
# ============================================================
CSS = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>Call Coaching Playbook — Lakmé Academy</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: 'Inter', -apple-system, system-ui, sans-serif;
    background: #f8f6f3;
    color: #1a1a2e;
    line-height: 1.6;
    font-size: 15px;
  }
  .hero {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
    color: #fff;
    padding: 40px 16px 32px;
    text-align: center;
    position: relative;
  }
  .lang-selector {
    position: absolute;
    top: 16px;
    right: 16px;
    display: flex;
    gap: 2px;
    background: rgba(255,255,255,.1);
    border-radius: 8px;
    padding: 3px;
  }
  .lang-selector button {
    padding: 6px 14px;
    border-radius: 6px;
    border: none;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    transition: all .15s;
    background: transparent;
    color: rgba(255,255,255,.5);
  }
  .lang-selector button.active {
    background: #f97316;
    color: #fff;
  }
  @media (max-width: 480px) {
    .lang-selector { top: 10px; right: 10px; }
    .lang-selector button { padding: 4px 10px; font-size: 11px; }
  }
  .hero h1 { font-size: clamp(22px, 6vw, 44px); font-weight: 800; letter-spacing: -.03em; }
  .hero h1 span { color: #f97316; }
  .hero p { margin-top: 6px; color: rgba(255,255,255,.5); font-size: clamp(12px, 3vw, 15px); }
  .hero .meta { margin-top: 14px; display: flex; justify-content: center; gap: 12px; flex-wrap: wrap; }
  .hero .meta-item { padding: 6px 12px; border-radius: 8px; background: rgba(255,255,255,.06); }
  .hero .meta-item .num { font-size: clamp(18px, 4vw, 28px); font-weight: 800; }
  .hero .meta-item .lbl { font-size: 10px; text-transform: uppercase; letter-spacing: .5px; opacity: .6; }
  .hero .meta-item.good .num { color: #22c55e; }
  .hero .meta-item.bad .num { color: #ef4444; }
  .hero .meta-item.avg .num { color: #f59e0b; }
  .hero .share-bar {
    margin-top: 16px;
    display: flex; justify-content: center; gap: 8px; flex-wrap: wrap;
  }
  .hero .share-bar button, .hero .share-bar a {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 8px 16px; border-radius: 8px; border: 1px solid rgba(255,255,255,.15);
    background: rgba(255,255,255,.08); color: #fff; font-size: 13px; font-weight: 500;
    cursor: pointer; text-decoration: none; transition: background .15s;
  }
  .hero .share-bar button:hover, .hero .share-bar a:hover { background: rgba(255,255,255,.18); }
  .share-tip {
    margin-top: 8px; font-size: 11px; color: rgba(255,255,255,.35);
  }
  .container { max-width: 1100px; margin: 0 auto; padding: 24px 12px; }
  .tab-bar {
    display: flex; gap: 3px; margin-bottom: 20px;
    background: #e2e0db; padding: 4px; border-radius: 10px;
    flex-wrap: wrap; overflow-x: auto; -webkit-overflow-scrolling: touch;
  }
  .tab {
    padding: 7px 12px; border-radius: 7px; font-size: clamp(11px, 2.5vw, 13px); font-weight: 500;
    cursor: pointer; transition: all .15s; border: none; background: none; color: #6b7280;
    white-space: nowrap;
  }
  .tab.active { background: #fff; box-shadow: 0 1px 4px rgba(0,0,0,.08); color: #1a1a2e; font-weight: 600; }
  .tab-page { display: none; }
  .tab-page.active { display: block; }
  .section-title { font-size: clamp(17px, 4vw, 22px); font-weight: 700; margin-bottom: 12px; }
  .card {
    background: #fff; border-radius: 14px; padding: clamp(16px, 4vw, 28px);
    margin-bottom: 20px; box-shadow: 0 1px 4px rgba(0,0,0,.05);
  }
  .dos-donts-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
  @media (max-width: 640px) { .dos-donts-grid { grid-template-columns: 1fr; } }
  .dos-box, .donts-box { border-radius: 10px; padding: 14px; }
  .dos-box { background: #f0fdf4; border: 1px solid #bbf7d0; }
  .donts-box { background: #fef2f2; border: 1px solid #fecaca; }
  .dos-box h3, .donts-box h3 { font-size: 14px; font-weight: 700; margin-bottom: 8px; }
  .dos-box h3 { color: #15803d; }
  .donts-box h3 { color: #dc2626; }
  .dos-list, .donts-list { font-size: 14px; }
  .dos-list > div { padding: 7px 0; border-bottom: 1px solid rgba(0,0,0,.04); display: flex; align-items: flex-start; gap: 6px; }
  .donts-list > div { padding: 7px 0; border-bottom: 1px solid rgba(0,0,0,.04); display: flex; align-items: flex-start; gap: 6px; }
  .badge {
    display: inline-block; padding: 2px 8px; border-radius: 20px;
    font-size: 11px; font-weight: 600; white-space: nowrap; flex-shrink: 0;
  }
  .badge.green { background: #bbf7d0; color: #15803d; }
  .badge.red { background: #fecaca; color: #dc2626; }
  .badge.orange { background: #fed7aa; color: #c2410c; }
  .badge.blue { background: #dbeafe; color: #1d4ed8; }
  .say-this-grid { display: grid; gap: 10px; margin-top: 16px; }
  .say-pair {
    display: grid; grid-template-columns: 1fr 1fr; gap: 10px; padding: 12px;
    border-radius: 10px; background: #fafaf9; border: 1px solid #e5e2dd;
  }
  @media (max-width: 640px) { .say-pair { grid-template-columns: 1fr; } }
  .say-pair .label { font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: .3px; margin-bottom: 4px; }
  .say-pair .text { font-size: 13px; line-height: 1.5; }
  .say-pair .note { font-size: 12px; color: #6b7280; margin-top: 4px; padding: 6px 8px; background: #fffbeb; border-radius: 6px; }
  .say-pair .bad { color: #dc2626; }
  .say-pair .good { color: #15803d; }
  .say-pair.bad { border-left: 3px solid #ef4444; }
  .say-pair.good { border-left: 3px solid #22c55e; }
  .golden-rules { margin-top: 20px; }
  .golden-rules h3 { font-size: 16px; font-weight: 700; margin-bottom: 12px; color: #1e293b; }
  .golden-rule {
    display: flex; gap: 10px; padding: 10px 12px; margin-bottom: 8px;
    background: #f8fafc; border-radius: 8px; border-left: 3px solid #f97316;
    font-size: 14px; align-items: flex-start;
  }
  .golden-rule .num {
    flex-shrink: 0; width: 24px; height: 24px; border-radius: 50%;
    background: #f97316; color: #fff; font-size: 12px; font-weight: 700;
    display: flex; align-items: center; justify-content: center;
  }
  .flow-step {
    display: flex; gap: 12px; padding: 14px; margin-bottom: 12px;
    background: #fafaf9; border-radius: 10px; border: 1px solid #e5e2dd;
  }
  .step-num {
    flex-shrink: 0; width: 32px; height: 32px; border-radius: 50%;
    background: #1e293b; color: #fff; font-size: 14px; font-weight: 700;
    display: flex; align-items: center; justify-content: center;
  }
  .step-title { font-size: 14px; font-weight: 700; margin-bottom: 4px; }
  .step-desc { font-size: 13px; color: #6b7280; margin-bottom: 6px; }
  .step-do { font-size: 13px; color: #15803d; margin-bottom: 3px; }
  .step-dont { font-size: 13px; color: #dc2626; }
  .step-sub-points { margin-top: 6px; padding-left: 16px; font-size: 12px; color: #6b7280; }
  .step-sub-points li { margin-bottom: 3px; }
  .script-compare { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
  @media (max-width: 640px) { .script-compare { grid-template-columns: 1fr; } }
  .script-box { padding: 12px; border-radius: 8px; font-size: 13px; line-height: 1.6; }
  .script-box.before { background: #fef2f2; border: 1px solid #fecaca; }
  .script-box.after { background: #f0fdf4; border: 1px solid #bbf7d0; }
  .script-box .label { font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: .3px; margin-bottom: 6px; }
  .script-box.before .label { color: #dc2626; }
  .script-box.after .label { color: #15803d; }
  .highlight-bad { background: #fecaca; padding: 1px 4px; border-radius: 3px; }
  .highlight-good { background: #bbf7d0; padding: 1px 4px; border-radius: 3px; }
  .objection-card { margin-bottom: 10px; border-radius: 10px; overflow: hidden; border: 1px solid #e5e2dd; }
  .objection-header {
    padding: 12px 14px; background: #fafaf9; cursor: pointer;
    display: flex; justify-content: space-between; align-items: center;
    font-weight: 600; font-size: 14px; user-select: none; -webkit-tap-highlight-color: transparent;
  }
  .objection-header .arrow { transition: transform .2s; font-size: 12px; }
  .objection-header.open .arrow { transform: rotate(180deg); }
  .objection-body { display: none; padding: 14px; background: #fff; border-top: 1px solid #e5e2dd; }
  .objection-body.open { display: block; }
  .objection-body .bad { color: #dc2626; font-size: 13px; }
  .objection-body .good { color: #15803d; font-size: 13px; }
  .roleplay-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 10px; margin-bottom: 16px; }
  .roleplay-card {
    padding: 14px 10px; text-align: center; border-radius: 10px;
    border: 2px solid #e5e2dd; cursor: pointer; transition: all .15s;
    background: #fff; -webkit-tap-highlight-color: transparent;
  }
  .roleplay-card:hover { border-color: #f97316; }
  .roleplay-card .emoji { font-size: 28px; margin-bottom: 6px; }
  .roleplay-card .title { font-size: 13px; font-weight: 600; }
  .roleplay-card .sub { font-size: 11px; color: #6b7280; }
  .roleplay-detail { display: none; padding: 16px; background: #fafaf9; border-radius: 10px; border: 1px solid #e5e2dd; }
  .roleplay-detail.open { display: block; }
  .roleplay-detail h4 { font-size: 16px; font-weight: 700; margin-bottom: 4px; }
  .roleplay-detail .role { font-size: 13px; color: #6b7280; margin-bottom: 10px; }
  .roleplay-detail .script { padding: 12px; background: #fff; border-radius: 8px; font-size: 13px; line-height: 1.7; border: 1px solid #e5e2dd; }
  .roleplay-detail .tip { margin-top: 10px; padding: 10px; background: #fffbeb; border-radius: 8px; font-size: 13px; color: #92400e; }
  .center-tips { display: grid; gap: 14px; }
  .center-tip-card { background: #fff; border-radius: 10px; padding: 16px; border: 1px solid #e5e2dd; border-top: 4px solid; }
  .center-tip-card .name { font-size: 16px; font-weight: 700; margin-bottom: 4px; }
  .center-tip-card .stat { font-size: 13px; color: #6b7280; margin-bottom: 10px; }
  .center-tip-card .tip-list { font-size: 13px; }
  .center-tip-card .tip-list ol { padding-left: 18px; color: #6b7280; }
  .center-tip-card .tip-list ol li { margin-bottom: 3px; }
  .footer { text-align: center; padding: 24px 12px; font-size: 12px; color: #9ca3af; }
  #loading { text-align: center; padding: 60px 20px; }
  #loading .icon { font-size: 48px; margin-bottom: 12px; }
  #loading h2 { font-size: 20px; margin-bottom: 8px; }
  #loading p { color: #6b7280; font-size: 14px; }
  #loading code { background: #e5e2dd; padding: 2px 6px; border-radius: 4px; font-size: 13px; }
  .empty-state { text-align: center; padding: 60px 20px; color: #6b7280; }
  .preso-overlay {
    position: fixed; top: 0; left: 0; width: 100%; height: 100%;
    background: #0f172a; color: #fff; z-index: 9999;
    display: none; flex-direction: column; overflow: hidden;
    font-size: clamp(16px, 3vw, 22px);
  }
  .preso-overlay.active { display: flex; }
  .preso-slide {
    flex: 1; display: flex; flex-direction: column;
    justify-content: center; align-items: center;
    padding: 40px 24px; text-align: center; overflow-y: auto;
  }
  .preso-slide .slide-num { position: absolute; top: 16px; right: 20px; font-size: 14px; color: rgba(255,255,255,.3); }
  .preso-slide .slide-icon { font-size: clamp(40px, 10vw, 72px); margin-bottom: 16px; }
  .preso-slide .slide-title { font-size: clamp(20px, 5vw, 36px); font-weight: 800; margin-bottom: 12px; }
  .preso-slide .slide-sub { font-size: clamp(14px, 3vw, 20px); color: rgba(255,255,255,.6); margin-bottom: 20px; }
  .preso-slide .slide-body { font-size: clamp(14px, 2.5vw, 18px); max-width: 700px; line-height: 1.7; color: rgba(255,255,255,.8); }
  .preso-slide .slide-body strong { color: #f97316; }
  .preso-controls {
    display: flex; justify-content: center; gap: 16px; padding: 16px;
    background: rgba(0,0,0,.3);
  }
  .preso-controls button {
    padding: 10px 24px; border-radius: 8px; border: none;
    font-size: 14px; font-weight: 600; cursor: pointer;
    background: rgba(255,255,255,.1); color: #fff; transition: background .15s;
  }
  .preso-controls button:hover { background: rgba(255,255,255,.2); }
  .preso-controls button.primary { background: #f97316; color: #fff; }
  .preso-controls button.primary:hover { background: #ea580c; }
  @media (max-width: 640px) {
    .preso-slide { padding: 24px 16px; }
    .preso-controls { gap: 8px; }
    .preso-controls button { padding: 8px 14px; font-size: 12px; }
    .tab-bar { flex-wrap: nowrap; -webkit-overflow-scrolling: touch; }
  }
</style>
</head>
<body>
"""

# ============================================================
# HTML TEMPLATE
# ============================================================
HTML_BODY = r"""
<div class="hero">
  <div class="lang-selector">
    <button id="lang-en" class="active" onclick="changeLang('en')">EN</button>
    <button id="lang-hi" onclick="changeLang('hi')">हिन्दी</button>
  </div>
  <h1>Call Coaching <span>Playbook</span></h1>
  <p id="hero-sub">Loading training data...</p>
  <div class="meta" id="hero-meta"></div>
  <div class="share-bar">
    <button onclick="window.print()">🖨 <span id="btn-print">Print / Save PDF</span></button>
    <button onclick="openPresentation()">🎬 <span id="btn-preso">Presentation Mode</span></button>
    <a href="#" onclick="shareFile(event)">📤 <span id="btn-share">Share This File</span></a>
  </div>
  <div class="share-tip" id="share-tip">💡 This file works offline. Share the .html file via WhatsApp, Email, or Drive.</div>
</div>

<div class="container" id="app">
  <div class="empty-state" id="loading">
    <div class="icon">⏳</div>
    <h2 id="loading-title">Loading training data...</h2>
    <p id="loading-sub">Run <code>python3 analyze_calls.py --master</code> first.</p>
  </div>
</div>

<div class="footer" id="footer-text">Lakmé Academy &middot; Call Coaching Playbook &middot; Open on any phone, tablet, or laptop</div>

<div class="preso-overlay" id="preso-overlay">
  <div class="preso-slide" id="preso-slide">
    <div class="slide-num" id="preso-num"></div>
    <div class="slide-icon" id="preso-icon"></div>
    <div class="slide-title" id="preso-title"></div>
    <div class="slide-sub" id="preso-sub"></div>
    <div class="slide-body" id="preso-body"></div>
  </div>
  <div class="preso-controls">
    <button id="preso-prev" onclick="presoPrev()">◀ <span id="btn-prev">Previous</span></button>
    <button class="primary" id="preso-next" onclick="presoNext()"><span id="btn-next">Next</span> ▶</button>
    <button id="preso-exit" onclick="closePresentation()">✕ <span id="btn-exit">Exit</span></button>
  </div>
</div>

<script>
window.__REPORT_DATA__ = null;
var currentLang = localStorage.getItem('trainingLang') || 'en';

function t(key) {
  var lang = langData[currentLang] || langData.en;
  var val = lang[key];
  return typeof val === 'function' ? val : (val || key);
}

function changeLang(lang) {
  currentLang = lang;
  localStorage.setItem('trainingLang', lang);
  document.getElementById('lang-en').className = lang === 'en' ? 'active' : '';
  document.getElementById('lang-hi').className = lang === 'hi' ? 'active' : '';
  // Re-render with stored data
  var data = window._reportData;
  if (data) renderAndShow(data);
}

function shareFile(e) {
  e.preventDefault();
  var msg = currentLang === 'hi'
    ? 'शेयर करने के लिए:\n\n1. training.html फ़ाइल ढूंढें\n2. WhatsApp, Email, या Drive से शेयर करें\n3. कोई भी अपने फ़ोन ब्राउज़र में खोल सकता है\n\nबिना इंटरनेट के काम करता है।'
    : 'To share:\n\n1. Find this file: training.html\n2. Share via WhatsApp, Email, or Google Drive\n3. Anyone can open in their phone browser\n\nWorks offline. No app needed.';
  alert(msg);
}
"""

# ============================================================
# Build the complete HTML
# ============================================================
def build():
    html_path = os.path.join(BASE, "training.html")
    with open(html_path, "w") as f:
        f.write(CSS)
        f.write(HTML_BODY)
        # Write the JS translations and content
        f.write(JS_CODE())
        f.write("""</script>\n</body>\n</html>""")
    print(f"Written: {html_path}")
    size = os.path.getsize(html_path)
    print(f"Size: {size/1024:.0f} KB")

if __name__ == "__main__":
    build()