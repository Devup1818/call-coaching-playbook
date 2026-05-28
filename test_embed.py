import re, json

with open("/Users/deveshupadhyay/TASK CETE/master-report.html") as f:
    html = f.read()

if "window.__REPORT_DATA__ = null" in html:
    print("ERROR: Still has null placeholder")
    exit(1)

m = re.search(r"window\.__REPORT_DATA__ = '(.*?)';", html, re.DOTALL)
if not m:
    print("ERROR: Could not find __REPORT_DATA__")
    exit(1)

raw = m.group(1)
data_str = raw.replace("\\'", "'").replace('\\\\', '\\')
data = json.loads(data_str)
print(f"OK: {data['total_calls']} calls, avg {data['avg_score']}/100")
print(f"Data size: {len(raw)} chars")
