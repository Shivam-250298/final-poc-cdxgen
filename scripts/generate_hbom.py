#!/usr/bin/env python3

import json
import html
import uuid
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter

SOURCE = Path("logs/hbom-lshw.json")
OUTPUT = Path("reports/hbom")
OUTPUT.mkdir(parents=True, exist_ok=True)

ALLOWED_CLASSES = {
    "processor", "memory", "disk", "storage",
    "network", "display", "bus", "volume"
}

components = []

def walk(node):
    if isinstance(node, list):
        for item in node:
            walk(item)
        return

    if not isinstance(node, dict):
        return

    hardware_class = node.get("class", "")

    if hardware_class in ALLOWED_CLASSES:
        description = node.get("description", "")
        product = node.get("product", "")
        vendor = node.get("vendor", "")

        # Generic names prevent accidental publication
        # of host-specific identifiers.
        name = str(product or description or hardware_class)

        properties = [
            {
                "name": "hbom:hardwareClass",
                "value": hardware_class
            }
        ]

        if description:
            properties.append({
                "name": "hbom:description",
                "value": str(description)
            })

        if vendor:
            properties.append({
                "name": "hbom:vendor",
                "value": str(vendor)
            })

        size = node.get("size")
        if isinstance(size, (int, float)):
            properties.append({
                "name": "hbom:reportedSize",
                "value": str(size)
            })

        components.append({
            "type": "device",
            "bom-ref": f"hardware-{len(components)+1:03d}",
            "name": name,
            "properties": properties
        })

    for child in node.get("children", []):
        walk(child)


with SOURCE.open(encoding="utf-8") as f:
    inventory = json.load(f)

walk(inventory)

timestamp = datetime.now(timezone.utc).isoformat()

bom = {
    "bomFormat": "CycloneDX",
    "specVersion": "1.6",
    "serialNumber": f"urn:uuid:{uuid.uuid4()}",
    "version": 1,
    "metadata": {
        "timestamp": timestamp,
        "tools": {
            "components": [{
                "type": "application",
                "name": "lshw inventory converter"
            }]
        },
        "component": {
            "type": "platform",
            "name": "Amazon EC2 virtual machine",
            "properties": [
                {
                    "name": "hbom:instanceType",
                    "value": "c7i-flex.large"
                },
                {
                    "name": "hbom:virtualization",
                    "value": "Amazon EC2 / KVM"
                }
            ]
        }
    },
    "components": components
}

json_path = OUTPUT / "hbom.json"
json_path.write_text(
    json.dumps(bom, indent=2, ensure_ascii=False),
    encoding="utf-8"
)

counts = Counter(
    next(
        (p["value"] for p in c["properties"]
         if p["name"] == "hbom:hardwareClass"),
        "unknown"
    )
    for c in components
)

def safe(value):
    return html.escape(str(value), quote=True)

rows = []

for component in components:
    props = {
        p["name"]: p["value"]
        for p in component["properties"]
    }

    rows.append(
        "<tr>"
        f"<td>{safe(component['name'])}</td>"
        f"<td>{safe(props.get('hbom:hardwareClass', ''))}</td>"
        f"<td>{safe(props.get('hbom:vendor', '—'))}</td>"
        f"<td>{safe(props.get('hbom:description', '—'))}</td>"
        "</tr>"
    )

summary_rows = "".join(
    f"<tr><td>{safe(k)}</td><td>{v}</td></tr>"
    for k, v in sorted(counts.items())
)

page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>HBOM | Hardware Inventory Report</title>
<style>
* {{ box-sizing: border-box; }}
body {{
  margin: 0;
  font-family: Arial, sans-serif;
  background: #f3f6fb;
  color: #172338;
}}
header {{
  background: #14243c;
  color: white;
  padding: 35px 7%;
}}
header h1 {{ margin: 0 0 10px; }}
header p {{ color: #c3d1e4; }}
main {{
  max-width: 1200px;
  margin: 30px auto;
  padding: 0 20px;
}}
.cards {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 16px;
  margin-bottom: 25px;
}}
.card, section {{
  background: white;
  border: 1px solid #e1e7f0;
  border-radius: 12px;
  padding: 24px;
}}
.card strong {{
  display: block;
  font-size: 30px;
  color: #193e73;
}}
.card span {{
  color: #637187;
  font-size: 13px;
}}
section {{
  margin-bottom: 24px;
  overflow-x: auto;
}}
h2 {{ font-size: 20px; margin-top: 0; }}
table {{
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}}
th, td {{
  padding: 12px;
  border-bottom: 1px solid #e7ecf3;
  text-align: left;
  overflow-wrap: anywhere;
}}
th {{ background: #edf2f9; }}
tr:hover td {{ background: #f8faff; }}
.note {{
  background: #f0f5fc;
  padding: 15px;
  border-left: 4px solid #3769a5;
  line-height: 1.6;
}}
</style>
</head>
<body>
<header>
<h1>Hardware Bill of Materials (HBOM)</h1>
<p>Amazon EC2 — Virtual Hardware Inventory</p>
</header>
<main>
<div class="cards">
<div class="card">
<strong>{len(components)}</strong>
<span>Hardware Components</span>
</div>
<div class="card">
<strong>{len(counts)}</strong>
<span>Hardware Classes</span>
</div>
<div class="card">
<strong>1.6</strong>
<span>CycloneDX Version</span>
</div>
</div>

<section>
<h2>System Information</h2>
<p><b>Platform:</b> Amazon EC2</p>
<p><b>Instance Type:</b> c7i-flex.large</p>
<p><b>Virtualization:</b> KVM</p>
<p><b>Inventory Date:</b> {safe(timestamp)}</p>
</section>

<section>
<h2>Hardware Class Summary</h2>
<table>
<tr><th>Hardware Class</th><th>Count</th></tr>
{summary_rows}
</table>
</section>

<section>
<h2>Hardware Component Inventory</h2>
<table>
<tr>
<th>Component</th>
<th>Class</th>
<th>Vendor</th>
<th>Description</th>
</tr>
{''.join(rows)}
</table>
</section>

<section>
<h2>Scope and Limitations</h2>
<div class="note">
This report represents hardware visible inside an AWS EC2
virtual machine. It does not represent the complete physical
AWS host inventory. Scanner-generated bridge entries and
host-specific identifiers have been excluded.
This report is an inventory, not a hardware vulnerability assessment.
</div>
</section>
</main>
</body>
</html>
"""

html_path = OUTPUT / "hbom.html"
html_path.write_text(page, encoding="utf-8")

print("HBOM generation completed")
print(f"Hardware components: {len(components)}")
print(f"Hardware classes: {len(counts)}")
print(f"JSON: {json_path}")
print(f"HTML: {html_path}")
print("\nClass summary:")
for name, count in sorted(counts.items()):
    print(f"  {name}: {count}")
