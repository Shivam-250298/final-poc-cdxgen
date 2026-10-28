#!/usr/bin/env python3

import json
import sys
import html
from pathlib import Path
from datetime import datetime, timezone


def esc(value):
    if value is None or value == "":
        return "—"
    return html.escape(str(value))


def badge(value):
    value = str(value or "Unknown")
    lower = value.lower()

    if lower == "high":
        style = "high"
    elif lower == "low" or lower == "lower concern":
        style = "low"
    elif lower == "unknown" or "verification" in lower:
        style = "unknown"
    else:
        style = "medium"

    return f'<span class="badge {style}">{esc(value)}</span>'


def generate(input_file, output_file):
    with open(input_file, encoding="utf-8") as f:
        data = json.load(f)

    assets = data.get("assets", [])
    summary = data.get("summary", {})

    project = Path(input_file).stem.replace("-qbom", "").upper()
    generated = datetime.now(timezone.utc).strftime("%d %b %Y, %H:%M UTC")

    total = len(assets)
    high_quantum = sum(
        str(a.get("quantum_risk", "")).lower() == "high"
        for a in assets
    )
    high_classical = sum(
        str(a.get("classical_risk", "")).lower() == "high"
        for a in assets
    )
    unknown_quantum = sum(
        str(a.get("quantum_risk", "")).lower() == "unknown"
        for a in assets
    )

    rows = ""
    details = ""
    recommendations = ""
    high_risk_rows = ""

    for asset in assets:
        name = asset.get("name", "Unknown")
        quantum = asset.get("quantum_risk", "Unknown")
        classical = asset.get("classical_risk", "Unknown")
        readiness = asset.get("quantum_readiness", "Unknown")
        recommendation = asset.get("recommendation", "Not recorded")

        rows += f"""
        <tr>
            <td><strong>{esc(name)}</strong></td>
            <td>{esc(asset.get('asset_type'))}</td>
            <td>{esc(asset.get('primitive'))}</td>
            <td>{badge(quantum)}</td>
            <td>{badge(classical)}</td>
            <td>{esc(readiness)}</td>
        </tr>"""

        recommendations += f"""
        <tr>
            <td><strong>{esc(name)}</strong></td>
            <td>{esc(recommendation)}</td>
        </tr>"""

        if str(quantum).lower() == "high" or str(classical).lower() == "high":
            high_risk_rows += f"""
            <tr>
                <td><strong>{esc(name)}</strong></td>
                <td>{badge(quantum)}</td>
                <td>{badge(classical)}</td>
                <td>{esc(recommendation)}</td>
            </tr>"""

        details += f"""
        <details>
            <summary>{esc(name)}</summary>
            <div class="meta">
                <strong>Asset Type:</strong> {esc(asset.get('asset_type'))}<br>
                <strong>Primitive:</strong> {esc(asset.get('primitive'))}<br>
                <strong>Algorithm Family:</strong> {esc(asset.get('algorithm_family'))}<br>
                <strong>Key Size:</strong> {esc(asset.get('key_size'))}<br>
                <strong>Quantum Risk:</strong> {esc(quantum)}<br>
                <strong>Classical Risk:</strong> {esc(classical)}<br>
                <strong>Quantum Readiness:</strong> {esc(readiness)}<br>
                <strong>Usage Verified:</strong> {esc(asset.get('usage_verified'))}<br>
                <strong>Assessment Basis:</strong> {esc(asset.get('assessment_basis'))}<br>
                <strong>Recommendation:</strong> {esc(recommendation)}
            </div>
        </details>"""

    if not rows:
        rows = '<tr><td colspan="6" class="empty">No assets recorded.</td></tr>'

    if not high_risk_rows:
        high_risk_rows = (
            '<tr><td colspan="4" class="empty">'
            'No assets classified as High risk.</td></tr>'
        )

    document = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(project)} | Quantum Cryptography Assessment</title>

<style>
* {{ box-sizing: border-box; }}

body {{
    margin: 0;
    background: #f3f6fb;
    color: #172338;
    font-family: Arial, Helvetica, sans-serif;
}}

header {{
    background: #14243c;
    color: white;
    padding: 34px 7%;
}}

header h1 {{
    margin: 0 0 8px;
    font-size: 29px;
}}

header p {{
    margin: 0;
    color: #c3d1e4;
}}

main {{
    max-width: 1200px;
    margin: 30px auto;
    padding: 0 22px;
}}

.cards {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 16px;
    margin-bottom: 28px;
}}

.card {{
    background: white;
    border: 1px solid #e1e7f0;
    border-radius: 12px;
    padding: 23px;
}}

.card .value {{
    font-size: 32px;
    font-weight: 700;
    color: #193e73;
}}

.card .label {{
    margin-top: 8px;
    color: #637187;
    font-size: 13px;
}}

section {{
    background: white;
    border: 1px solid #e1e7f0;
    border-radius: 12px;
    margin-bottom: 24px;
    padding: 24px;
    overflow-x: auto;
}}

h2 {{
    font-size: 20px;
    margin: 0 0 18px;
}}

table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
}}

th {{
    background: #edf2f9;
    color: #344761;
    text-align: left;
}}

th, td {{
    padding: 12px;
    border-bottom: 1px solid #e7ecf3;
    overflow-wrap: anywhere;
    vertical-align: top;
}}

tr:hover td {{
    background: #f8faff;
}}

.meta {{
    font-size: 13px;
    color: #56657a;
    line-height: 1.9;
}}

.badge {{
    display: inline-block;
    padding: 5px 10px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 600;
}}

.high {{
    background: #fde8e8;
    color: #a61b1b;
}}

.medium {{
    background: #fff2d8;
    color: #986000;
}}

.low {{
    background: #e2f5e9;
    color: #176b39;
}}

.unknown {{
    background: #edf0f5;
    color: #536176;
}}

details {{
    border-bottom: 1px solid #e7ecf3;
    padding: 14px 0;
}}

summary {{
    cursor: pointer;
    font-weight: 600;
    color: #193e73;
}}

details .meta {{
    padding: 14px 0 0 12px;
}}

.note {{
    background: #f0f5fc;
    border-left: 4px solid #3769a5;
    padding: 15px;
    line-height: 1.6;
    font-size: 13px;
}}

.empty {{
    text-align: center;
    color: #748095;
    padding: 28px;
}}

footer {{
    text-align: center;
    padding: 20px;
    color: #748095;
    font-size: 12px;
}}

@media print {{
    body {{ background: white; }}
    section, .card {{ break-inside: avoid; }}
}}
</style>
</head>

<body>

<header>
    <h1>{esc(project)} — Quantum Cryptography Assessment</h1>
    <p>QBOM-style Risk Assessment | Cryptographic Inventory Analysis</p>
</header>

<main>

<div class="cards">
    <div class="card">
        <div class="value">{total}</div>
        <div class="label">Total Cryptographic Assets</div>
    </div>

    <div class="card">
        <div class="value">{high_quantum}</div>
        <div class="label">High Quantum Risk</div>
    </div>

    <div class="card">
        <div class="value">{high_classical}</div>
        <div class="label">High Classical Risk</div>
    </div>

    <div class="card">
        <div class="value">{unknown_quantum}</div>
        <div class="label">Unknown Quantum Risk</div>
    </div>
</div>

<section>
<h2>Report Information</h2>
<div class="meta">
<strong>Project:</strong> {esc(project)}<br>
<strong>Report Type:</strong> {esc(data.get('report_type'))}<br>
<strong>Source CBOM:</strong> {esc(data.get('source_cbom'))}<br>
<strong>Assessment Generator:</strong> {esc(data.get('generator'))}<br>
<strong>HTML Generated:</strong> {esc(generated)}
</div>
</section>

<section>
<h2>Quantum Risk Assessment ({total} Assets)</h2>
<table>
<thead>
<tr>
<th>Algorithm / Asset</th>
<th>Asset Type</th>
<th>Primitive</th>
<th>Quantum Risk</th>
<th>Classical Risk</th>
<th>Quantum Readiness</th>
</tr>
</thead>
<tbody>{rows}</tbody>
</table>
</section>

<section>
<h2>High-Risk Findings</h2>
<p class="meta">
Assets classified as High in either quantum or classical risk.
These are preliminary algorithm-level classifications, not confirmed vulnerabilities.
</p>
<table>
<thead>
<tr>
<th>Algorithm / Asset</th>
<th>Quantum Risk</th>
<th>Classical Risk</th>
<th>Recommended Action</th>
</tr>
</thead>
<tbody>{high_risk_rows}</tbody>
</table>
</section>

<section>
<h2>Recommendations</h2>
<table>
<thead>
<tr>
<th>Algorithm / Asset</th>
<th>Recommendation</th>
</tr>
</thead>
<tbody>{recommendations}</tbody>
</table>
</section>

<section>
<h2>Detailed Cryptographic Asset Assessment</h2>
{details}
</section>

<section>
<h2>Assessment Limitations</h2>
<div class="note">
This is a custom QBOM-style assessment generated from an existing
cryptographic inventory. It is not an official cdxgen QBOM output.
Risk classifications are based on recorded algorithm names and
available metadata.

<br><br>

Actual cryptographic usage, key sizes, implementation details,
protocol configurations, and runtime exposure have not been verified.
An identified algorithm does not necessarily indicate an exploitable
vulnerability.

<br><br>

Unknown or missing information requires further investigation.
This report should be used to prioritize verification and
post-quantum cryptography migration planning, not as proof of
application security or insecurity.
</div>
</section>

</main>

<footer>
Generated from QBOM-style JSON | Custom Quantum Cryptography Assessment
</footer>

</body>
</html>"""

    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    Path(output_file).write_text(document, encoding="utf-8")

    print(f"HTML report generated: {output_file}")
    print(f"Total assets: {total}")
    print(f"High quantum risk: {high_quantum}")
    print(f"High classical risk: {high_classical}")
    print(f"Unknown quantum risk: {unknown_quantum}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(
            "Usage: python3 generate_html.py input.json output.html"
        )

    generate(sys.argv[1], sys.argv[2])
