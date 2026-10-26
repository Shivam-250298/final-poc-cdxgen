#!/usr/bin/env python3

import json
import sys
import html
from pathlib import Path
from datetime import datetime, timezone

def esc(value):
    if isinstance(value, (dict, list)):
        value = json.dumps(value, ensure_ascii=False)
    return html.escape(str(value if value is not None else "—"))

def generate(input_file, output_file):
    with open(input_file, encoding="utf-8") as f:
        bom = json.load(f)

    components = bom.get("components", [])
    crypto = [c for c in components if c.get("type") == "cryptographic-asset"]
    libraries = [c for c in components if c.get("type") != "cryptographic-asset"]

    metadata = bom.get("metadata", {})
    tool_names = []

    for tool in metadata.get("tools", {}).get("components", []):
        tool_names.append(f"{tool.get('name', '')} {tool.get('version', '')}".strip())

    crypto_rows = ""
    for c in crypto:
        props = c.get("cryptoProperties", {})
        algo = props.get("algorithmProperties", {})
        crypto_rows += f"""
        <tr>
            <td><strong>{esc(c.get('name'))}</strong></td>
            <td>{esc(props.get('assetType'))}</td>
            <td>{esc(props.get('oid'))}</td>
            <td>{esc(algo.get('primitive'))}</td>
            <td>{esc(algo.get('algorithmFamily'))}</td>
        </tr>"""

    if not crypto_rows:
        crypto_rows = '<tr><td colspan="5" class="empty">No cryptographic assets recorded in this CBOM.</td></tr>'

    library_rows = ""
    for c in libraries:
        library_rows += f"""
        <tr>
            <td>{esc(c.get('name'))}</td>
            <td>{esc(c.get('version'))}</td>
            <td>{esc(c.get('type'))}</td>
            <td>{esc(c.get('group'))}</td>
        </tr>"""

    if not library_rows:
        library_rows = '<tr><td colspan="4" class="empty">No other components recorded.</td></tr>'


    # CBOM_SOURCE_DETAILS_V1
    locations_file = Path(input_file).with_name("java-crypto-locations.json")
    locations = []
    if locations_file.exists():
        locations = json.loads(locations_file.read_text(encoding="utf-8"))
        if not isinstance(locations, list):
            raise ValueError("Source locations JSON must contain an array.")

    location_rows = ""
    for item in sorted(
        locations,
        key=lambda x: (
            str(x.get("file") or ""),
            x.get("line") or 0,
            x.get("column") or 0,
            str(x.get("code") or ""),
        ),
    ):
        location_rows += (
            "<tr>"
            + "".join(
                "<td>" + esc(item.get(key)) + "</td>"
                for key in ("file", "line", "column", "code", "tags")
            )
            + "</tr>"
        )
    if not location_rows:
        location_rows = (
            '<tr><td colspan="5" class="empty">'
            'No source locations supplied.</td></tr>'
        )

    location_section = f"""
<section>
<h2>Crypto Source Locations ({len(locations)} records)</h2>
<p class="meta">Source: {esc(locations_file.name)} — extracted from
the reachables analysis slices. These are source-analysis records;
they are not evidence attached to individual CBOM assets.
Multiple records can refer to the same operation.</p>
<table>
<thead><tr><th>File</th><th>Line</th><th>Column</th>
<th>Code / Operation</th><th>Scanner Tags</th></tr></thead>
<tbody>{location_rows}</tbody>
</table>
</section>
"""

    crypto_details = ""
    for component in crypto:
        crypto_details += (
            "<details><summary>" + esc(component.get("name"))
            + "</summary>"
        )
        for field in ("bom-ref", "description", "cryptoProperties",
                      "properties", "evidence"):
            value = component.get(field)
            display = (
                "Not recorded" if value is None
                else json.dumps(value, ensure_ascii=False, indent=2)
            )
            crypto_details += (
                "<h3>" + esc(field) + "</h3>"
                '<pre style="white-space:pre-wrap;overflow-wrap:anywhere">'
                + esc(display) + "</pre>"
            )
        crypto_details += "</details>"

    detail_section = (
        "<section><h2>Recorded Crypto Asset Details</h2>"
        + (crypto_details or "<p>No cryptographic assets recorded.</p>")
        + "</section>"
    )

    annotation_details = ""
    for annotation in bom.get("annotations", []) or []:
        annotation_details += (
            '<pre style="white-space:pre-wrap;overflow-wrap:anywhere">'
            + esc(json.dumps(annotation, ensure_ascii=False, indent=2))
            + "</pre>"
        )
    annotation_section = (
        "<section><h2>BOM Annotations</h2>"
        '<p class="meta">Includes document descriptions and any audit '
        'annotations recorded in this BOM. An annotation is not necessarily '
        'an audit finding. No findings does not establish security.</p>'
        + (annotation_details or "<p>No annotations recorded.</p>")
        + "</section>"
    )

    project = Path(input_file).stem.replace("-cbom", "").upper()
    generated = datetime.now(timezone.utc).strftime("%d %b %Y, %H:%M UTC")

    document = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(project)} | CBOM Report</title>
<style>
* {{ box-sizing: border-box; }}
body {{ margin: 0; background: #f3f6fb; color: #172338;
        font-family: Arial, Helvetica, sans-serif; }}
header {{ background: #14243c; color: white; padding: 34px 7%; }}
header h1 {{ margin: 0 0 8px; font-size: 29px; }}
header p {{ margin: 0; color: #c3d1e4; }}
main {{ max-width: 1200px; margin: 30px auto; padding: 0 22px; }}
.cards {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
          gap: 16px; margin-bottom: 28px; }}
.card {{ background: white; border: 1px solid #e1e7f0; border-radius: 12px;
         padding: 23px; }}
.card .value {{ font-size: 32px; font-weight: 700; color: #193e73; }}
.card .label {{ margin-top: 8px; color: #637187; font-size: 13px; }}
section {{ background: white; border: 1px solid #e1e7f0; border-radius: 12px;
           margin-bottom: 24px; padding: 24px; overflow-x: auto; }}
h2 {{ font-size: 20px; margin: 0 0 18px; }}
table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
th {{ background: #edf2f9; color: #344761; text-align: left; }}
th, td {{ padding: 12px; border-bottom: 1px solid #e7ecf3;
          overflow-wrap: anywhere; }}
tr:hover td {{ background: #f8faff; }}
.empty {{ text-align: center; color: #748095; padding: 28px; }}
.note {{ background: #f0f5fc; border-left: 4px solid #3769a5;
         padding: 15px; line-height: 1.6; font-size: 13px; }}
.meta {{ font-size: 13px; color: #56657a; line-height: 1.9; }}
footer {{ text-align: center; padding: 20px; color: #748095; font-size: 12px; }}
@media print {{
  body {{ background: white; }}
  section, .card {{ break-inside: avoid; }}
}}
</style>
</head>
<body>
<header>
    <h1>{esc(project)} — Cryptographic Bill of Materials</h1>
    <p>CycloneDX CBOM Analysis Report</p>
</header>
<main>
<div class="cards">
    <div class="card"><div class="value">{len(components)}</div>
        <div class="label">Total Components</div></div>
    <div class="card"><div class="value">{len(crypto)}</div>
        <div class="label">Cryptographic Assets</div></div>
    <div class="card"><div class="value">{len(libraries)}</div>
        <div class="label">Other Components</div></div>
    <div class="card"><div class="value">{esc(bom.get('specVersion', '—'))}</div>
        <div class="label">CycloneDX Version</div></div>
</div>

<section>
<h2>Report Information</h2>
<div class="meta">
<strong>Project:</strong> {esc(project)}<br>
<strong>BOM Format:</strong> {esc(bom.get('bomFormat'))}<br>
<strong>Serial Number:</strong> {esc(bom.get('serialNumber'))}<br>
<strong>Tool:</strong> {esc(', '.join(tool_names) or 'Not specified')}<br>
<strong>HTML Generated:</strong> {esc(generated)}
</div>
</section>

<section>
<h2>Cryptographic Assets ({len(crypto)})</h2>
<table>
<thead><tr>
<th>Algorithm / Asset</th><th>Asset Type</th><th>OID</th>
<th>Primitive</th><th>Algorithm Family</th>
</tr></thead>
<tbody>{crypto_rows}</tbody>
</table>
</section>

{location_section}
{detail_section}
{annotation_section}

<section>
<h2>Dependency and Component Inventory ({len(libraries)})</h2>
<table>
<thead><tr>
<th>Component</th><th>Version</th><th>Type</th><th>Group</th>
</tr></thead>
<tbody>{library_rows}</tbody>
</table>
</section>

<section>
<h2>Important Limitations</h2>
<div class="note">
This report displays information from the supplied CycloneDX JSON and, when available, the separate source-location JSON. Missing fields are not inferred. Source locations apply to the source revision that was scanned.
A missing cryptographic asset does not prove that the application does not use
cryptography. Detection depends on scanner coverage and successful analysis.
This report does not perform vulnerability analysis or provide remediation recommendations.
</div>
</section>
</main>
<footer>Generated from CycloneDX JSON | CBOM Proof of Concept</footer>
</body>
</html>"""

    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    Path(output_file).write_text(document, encoding="utf-8")
    print(f"Created: {output_file} | {len(components)} components | {len(crypto)} crypto assets")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Usage: python3 cbom_to_html.py input.json output.html")
    generate(sys.argv[1], sys.argv[2])
