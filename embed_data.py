import json, os, glob

base_dir = os.path.dirname(__file__)
reports_dir = os.path.join(base_dir, "reports")
targets = ["master-report.html", "training.html", "index.html"]

json_files = glob.glob(os.path.join(reports_dir, "master-data-*.json"))
if not json_files:
    print("No master-data JSON files found in reports/")
    exit(1)

latest = max(json_files, key=os.path.getmtime)
print(f"Embedding: {latest}")

with open(latest) as f:
    data = json.load(f)

json_str = json.dumps(data, ensure_ascii=False)
MARKER = "__DATA_OBJECT__"

for filename in targets:
    path = os.path.join(base_dir, filename)
    if not os.path.exists(path):
        print(f"SKIP: {filename} not found")
        continue
    with open(path) as f:
        html = f.read()

    if MARKER not in html:
        print(f"ERROR: Could not find '{MARKER}' in {filename}")
        continue

    html = html.replace(MARKER, json_str)
    with open(path, "w") as f:
        f.write(html)
    print(f"Done! {filename} now has embedded data ({len(json_str)} bytes).")

print("Open training.html directly in your browser.")
