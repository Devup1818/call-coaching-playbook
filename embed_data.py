import json, base64, glob, os

base_dir = os.path.dirname(__file__)
reports_dir = os.path.join(base_dir, "reports")
targets = ["master-report.html", "training.html"]

json_files = glob.glob(os.path.join(reports_dir, "master-data-*.json"))
if not json_files:
    print("No master-data JSON files found in reports/")
    exit(1)

latest = max(json_files, key=os.path.getmtime)
print(f"Embedding: {latest}")

with open(latest) as f:
    raw_json = f.read()

b64 = base64.b64encode(raw_json.encode()).decode()
B64_MARKER = "__B64__"

for filename in targets:
    path = os.path.join(base_dir, filename)
    if not os.path.exists(path):
        print(f"SKIP: {filename} not found")
        continue
    with open(path) as f:
        html = f.read()

    if B64_MARKER not in html:
        print(f"ERROR: Could not find '{B64_MARKER}' in {filename}")
        continue

    html = html.replace(B64_MARKER, b64)
    with open(path, "w") as f:
        f.write(html)
    print(f"Done! {filename} now has embedded data ({len(raw_json)} bytes, {len(b64)} base64).")

print("Open training.html directly in your browser.")
