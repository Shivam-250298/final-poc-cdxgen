# QBOM POC — Cryptographic Inventory & Quantum Readiness Assessment

## 1. Overview

This POC explores how to identify cryptographic assets in application source code and assess their potential risks, including quantum computing threats.

We used **cdxgen** to generate a Cryptography Bill of Materials (CBOM), developed custom Python scripts for quantum risk assessment, and generated JSON and HTML reports.

We also explored **TraceBOM** to understand whether runtime tracing provides additional cryptographic evidence.

### Objective

- Identify cryptographic algorithms used in applications.
- Generate a CBOM using cdxgen.
- Assess classical and quantum-related risks.
- Generate readable JSON and HTML assessment reports.
- Explore runtime cryptographic visibility using TraceBOM.
- Understand detection limitations across programming languages.

### Technologies Used

| Component | Purpose |
|---|---|
| cdxgen | Generate CBOM |
| CycloneDX | Standard BOM format |
| Python | Custom quantum risk assessment |
| JSON | Machine-readable report |
| HTML | Human-readable report |
| TraceBOM | Runtime component and cryptographic tracing |
| GitHub | Store POC scripts and reports |

**Environment:** Ubuntu EC2

**cdxgen version:** 13.5.0 for the final Go and Node.js tests.

---

## 2. Understanding CBOM and QBOM

### 2.1 What is CBOM?

**CBOM — Cryptography Bill of Materials**

A CBOM provides an inventory of cryptographic assets identified within software.

Examples include:

- Encryption algorithms: AES, DES, RSA
- Hash algorithms: MD5, SHA-1, SHA-256
- Message authentication algorithms: HMAC
- Cryptographic keys and related assets

CBOM helps answer:

- Which cryptographic algorithms are present?
- Which algorithms might be outdated?
- Which cryptographic assets require security review?

### 2.2 What is QBOM?

In this POC, **QBOM refers to a custom quantum-readiness assessment built using CBOM data**.

It evaluates detected cryptographic algorithms and provides:

- Classical security risk
- Quantum-related risk
- Quantum readiness information
- Recommendations
- Summary of findings

**Important:** Our QBOM implementation is custom. It is not a native QBOM generation feature of cdxgen.

### 2.3 CBOM vs QBOM

| CBOM | Custom QBOM Assessment |
|---|---|
| Identifies cryptographic assets | Evaluates detected assets |
| Provides algorithm inventory | Provides risk classification |
| Generated using cdxgen | Generated using Python |
| CycloneDX JSON | Custom JSON and HTML |
| Focuses on identification | Focuses on security and quantum readiness |

---

## 3. Official cdxgen Documentation

Official repository:

https://github.com/cdxgen/cdxgen

### What cdxgen Officially Supports

cdxgen supports generating CycloneDX BOMs, including cryptographic asset information.

Relevant capabilities include:

- CBOM generation
- Cryptographic algorithm identification
- Source-code and dependency analysis
- Evidence collection
- Deep scanning
- CycloneDX JSON output

Example command:

```bash
cdxgen -t js -t crypto --include-crypto --deep --evidence -o cbom.json .
```

### Important Clarification

The cdxgen functionality explored here does **not provide a dedicated native QBOM generator**.

Our approach is:

```text
Application Source Code
        |
        v
      cdxgen
        |
        v
    CBOM JSON
        |
        v
 Custom Python Assessment
        |
        v
   QBOM-style JSON
        |
        v
     HTML Report
```

The quantum risk assessment is implemented through our custom Python logic.

### Official References

- Repository: https://github.com/cdxgen/cdxgen
- CLI documentation: https://github.com/cdxgen/cdxgen/blob/master/docs/CLI.md
- Advanced documentation: https://github.com/cdxgen/cdxgen/blob/master/docs/ADVANCED.md
- TraceBOM documentation: https://github.com/cdxgen/cdxgen/blob/master/docs/TRACEBOM.md
- CycloneDX: https://cyclonedx.org/

---

## 4. POC Implementation

We explored CBOM generation and custom QBOM assessment for applications written in:

1. Go
2. Java
3. Node.js

The implementation contains two main Python scripts.

### 4.1 `generate_qbom.py`

Purpose:

- Read the CBOM JSON.
- Extract cryptographic assets.
- Identify algorithms.
- Apply predefined risk classifications.
- Generate a custom QBOM-style JSON report.

The output includes:

| Field | Description |
|---|---|
| Algorithm | Detected cryptographic asset |
| Primitive | Cryptographic operation category |
| Algorithm Family | Algorithm classification |
| Key Size | Key information, when available |
| Quantum Risk | Potential quantum-related concern |
| Classical Risk | Conventional security concern |
| Quantum Readiness | Assessment classification |
| Recommendation | Suggested action |
| Usage Verified | Whether actual usage was confirmed |

Risk classifications are based on predefined custom rules.

They are not generated automatically by cdxgen.

### 4.2 `generate_html.py`

Purpose:

Convert the custom QBOM JSON into a readable HTML report.

The HTML report includes:

- Assessment summary
- Total cryptographic assets
- Quantum risk counts
- Classical risk counts
- Algorithm findings
- Recommendations
- Individual asset details
- Assessment limitations

---

## 5. Go QBOM POC

### 5.1 Cryptographic Assets Detected

Using cdxgen, we identified **9 cryptographic assets**.

| Algorithm | Category | Security Observation |
|---|---|---|
| AES | Symmetric encryption | Security depends on key size and configuration |
| DES | Symmetric encryption | Obsolete encryption algorithm |
| HMAC-SHA | Message authentication | Requires algorithm and key verification |
| Key | Cryptographic key | Insufficient information for classification |
| MD5 | Hash | Cryptographically broken for collision resistance |
| Private Key | Cryptographic key | Algorithm and key details require verification |
| RSA | Asymmetric encryption | Vulnerable to sufficiently capable quantum attacks |
| SHA-1 | Hash | Weak collision resistance |
| SHA-256 | Hash | Generally acceptable for appropriate uses |

### 5.2 QBOM Assessment Results

| Metric | Result |
|---|---|
| Total Cryptographic Assets | 9 |
| High Quantum Risk | 1 |
| High Classical Risk | 3 |
| Unknown Quantum Risk | 2 |

**High Quantum Risk**

- RSA

**High Classical Risk**

- DES
- MD5
- SHA-1

**Unknown Quantum Risk**

- Key
- Private Key

These findings represent algorithm-level assessments.

They do not establish whether every detected asset is actively used.

### 5.3 Generated Reports

```text
qbom/
├── go-qbom.json
└── go-qbom.html
```

---

## 6. Java CBOM and QBOM Exploration

We tested Java applications using multiple cdxgen versions.

### 6.1 Java Demo Application

Project:

```text
repos/cdxgen-test/backend/
```

The application contains cryptographic operations involving:

- DES encryption
- SHA-1 hashing
- Hardcoded DES key
- ECB encryption mode

### 6.2 Observations

Earlier cdxgen versions, including 12.8.6 and 12.8.7, detected DES in our Java tests.

However, the cdxgen 13.5.0 scans of the small Java demo produced:

```text
0 components
0 cryptographic assets
```

We also tested scanning the compiled Java classes.

The result remained zero components.

**Conclusion:** Cryptographic detection varied across tested cdxgen versions and project structures.

Zero detected assets does not mean the application contains no cryptographic operations.

### 6.3 Java Microservice Assessment

A separate Java microservice CBOM contained:

| Algorithm | Result |
|---|---|
| HMAC-SHA | Detected |
| SHA-256 | Detected |

A custom QBOM JSON was generated using this existing CBOM.

Summary:

```text
Total Assets: 2
High Quantum Risk: 0
Unknown Quantum Risk: 0
```

This assessment is separate from the Java demo application.

---

## 7. Node.js QBOM POC

### 7.1 Project

```text
repos/cdxgen-test/frontend/
```

Project structure:

```text
frontend/
├── server.js
└── public/
    ├── app.js
    ├── index.html
    └── styles.css
```

### 7.2 Cryptographic Operations in Source Code

Source inspection identified:

| Algorithm / Operation | Observation |
|---|---|
| MD5 | Weak hashing |
| AES-128-ECB | ECB mode and static encryption key |
| Math.random() | Non-cryptographic randomness for token generation |

These findings were identified through source-code inspection.

### 7.3 Generate CBOM

```bash
cd ~/final/repos/cdxgen-test/frontend
```

```bash
cdxgen -t js -t crypto --include-crypto --deep --evidence -o ~/final/reports/qbom/nodejs-test-cbom.json .
```

### 7.4 Verify Detected Assets

```bash
cd ~/final
```

```bash
jq -r '.components[]? | select(.type == "cryptographic-asset") | [.name, .cryptoProperties.algorithmProperties.primitive // "N/A"] | @tsv' reports/qbom/nodejs-test-cbom.json
```

Actual output:

```text
md5    hash
```

**Result:** cdxgen 13.5.0 detected only MD5.

AES-128-ECB and Math.random() were present in the source code but were not reported as cryptographic assets by this scan.

### 7.5 Generate Node.js QBOM JSON

The existing Python generator was reused with the Node.js input and output paths.

```bash
cd ~/final
```

```bash
sed -e 's|reports/go-cbom.json|reports/qbom/nodejs-test-cbom.json|' -e 's|reports/qbom/go-qbom.json|reports/qbom/nodejs-test-qbom.json|' scripts/qbom/generate_qbom.py > scripts/qbom/generate_nodejs_qbom.py
```

```bash
python3 scripts/qbom/generate_nodejs_qbom.py
```

### 7.6 Generate HTML

```bash
python3 scripts/qbom/generate_html.py reports/qbom/nodejs-test-qbom.json reports/qbom/nodejs-test-qbom.html
```

### 7.7 Results

| Metric | Result |
|---|---|
| Total Cryptographic Assets | 1 |
| Detected Algorithm | MD5 |
| High Quantum Risk | 0 |
| High Classical Risk | 1 |
| Unknown Quantum Risk | 0 |

Generated files:

```text
nodejs-test-qbom.json
nodejs-test-qbom.html
```

Both files were copied into the GitHub repository's `qbom/` directory and committed locally.

Commit:

```text
248e0fc
```

---

## 8. TraceBOM Exploration

### 8.1 What is TraceBOM?

TraceBOM is a cdxgen capability for collecting information about components observed during application execution.

Unlike static CBOM analysis, TraceBOM focuses on runtime evidence.

It can help identify:

- Runtime libraries
- Dynamically loaded components
- Runtime dependencies
- Cryptographic activity, where supported and observable
- TLS-related information, where supported

### 8.2 Why We Tested TraceBOM

We wanted to determine whether runtime tracing could identify additional cryptographic information that the static CBOM scan missed.

Specifically:

- MD5 execution
- AES-128-ECB execution
- Runtime cryptographic libraries

### 8.3 Test Setup

The Node.js application depends on a Java API.

Java API:

```text
127.0.0.1:8081
```

Node.js application:

```text
127.0.0.1:3000
```

The cryptographic operations in `server.js` execute after the Node.js application successfully receives dashboard data from the Java API.

### 8.4 Start Java API

```bash
cd ~/final/repos/cdxgen-test/backend
```

```bash
nohup java -cp build demo.crypto.CryptoDemoServer > ~/final/logs/java-trace-test.log 2>&1 &
```

Verify:

```bash
curl -sS http://127.0.0.1:8081/api/health
```

Observed output:

```json
{
  "status": "ok",
  "service": "northstar-java-api"
}
```

### 8.5 Run TraceBOM

```bash
cd ~/final
```

```bash
timeout 35s tracebom \
  --cmd "sh -c 'node server.js & PID=\$!; sleep 3; curl -s --max-time 5 http://127.0.0.1:3000/api/dashboard >/dev/null; kill \$PID; wait \$PID 2>/dev/null'" \
  --working-dir ~/final/repos/cdxgen-test/frontend \
  --crypto-probe-mode operations \
  --allow-listen 127.0.0.1:3000 \
  --allow-loopback \
  --disable-network=false \
  --timeout 20000 \
  --output ~/final/reports/qbom/nodejs-trace-bom.json
```

### 8.6 Issues Encountered

**Issue 1 — Permission Denied**

TraceBOM initially failed with:

```text
EACCES
```

Cause:

The `safer-exec-rt` binary did not have execute permission.

Fix applied:

```bash
sudo chmod 755 /usr/lib/node_modules/@cdxgen/cdxgen/node_modules/@cdxgen/safer-exec-linux-amd64/bin/safer-exec-rt
```

**Issue 2 — Tracing Warnings**

The successful scan still reported:

- eBPF tracing permission limitations
- User namespace isolation unavailable
- cgroup resource limits unavailable

These limitations may affect runtime tracing completeness.

### 8.7 Actual TraceBOM Results

TraceBOM generated a runtime BOM containing:

```text
39 runtime components
```

Three crypto-related libraries were observed:

| Library | Description |
|---|---|
| libssl.so.3 | OpenSSL TLS/SSL library |
| libcrypto.so.3 | OpenSSL cryptographic library |
| libk5crypto.so.3 | Kerberos cryptographic library |

However:

```text
Cryptographic Assets: 0
Verified MD5 Operations: 0
Verified AES Operations: 0
```

The scan did not provide evidence confirming the execution of individual MD5 or AES operations.

### 8.8 CBOM vs TraceBOM Results

| Finding | CBOM | TraceBOM |
|---|---|---|
| MD5 | Detected | Not verified |
| AES-128-ECB | Not detected | Not verified |
| Crypto-related runtime libraries | Not established | 3 observed |
| Runtime components | Not measured | 39 |
| Quantum risk assessment | Custom Python logic | Not provided |

### 8.9 Conclusion

TraceBOM provided additional visibility into runtime libraries.

However, it did not identify additional cryptographic algorithms or confirm specific MD5/AES operations during our test.

Therefore, TraceBOM is currently considered an **optional enhancement** rather than a requirement for our QBOM POC.

---

## 9. Report Structure

Our custom QBOM JSON and HTML reports contain the following information.

### Assessment Summary

| Field | Description |
|---|---|
| Total Crypto Assets | Number of detected cryptographic assets |
| High Quantum Risk | Assets classified as high quantum risk |
| High Classical Risk | Assets classified as high classical risk |
| Unknown Quantum Risk | Assets requiring additional information |

### Asset Details

Each asset can include:

```text
Algorithm Name
Primitive
Algorithm Family
Key Size
Quantum Risk
Classical Risk
Quantum Readiness
Recommendation
Assessment Basis
Usage Verification
```

**Note:** Key-size information must be based on actual key-size evidence. A classical security level must not be treated as the key size.

### TraceBOM Enhancement

If runtime evidence is included in future reports, it should appear in a separate section:

```text
Runtime Components
Observed Crypto Libraries
Verified Crypto Operations
Runtime Evidence Status
Tracing Limitations
```

Runtime library observations must not be presented as verified algorithm execution.

---

## 10. GitHub Repository Structure

The POC repository contains a dedicated `qbom/` directory.

```text
qbom/
├── generate_qbom.py
├── generate_html.py
├── go-qbom.json
├── go-qbom.html
├── nodejs-test-qbom.json
├── nodejs-test-qbom.html
└── README.md
```

The README is intended to document the POC implementation and findings.

### Push Reports to GitHub

Example:

```bash
cd ~/final
```

```bash
cp reports/qbom/nodejs-test-qbom.json reports/qbom/nodejs-test-qbom.html qbom/
```

```bash
git add qbom/nodejs-test-qbom.json qbom/nodejs-test-qbom.html
```

```bash
git commit -m "Add Node.js QBOM JSON and HTML reports"
```

```bash
git push origin main
```

Use specific file paths when staging to avoid committing unrelated local changes.

---

## 11. Key Findings

| Area | Finding |
|---|---|
| CBOM Generation | Successfully generated cryptographic inventories |
| Go | 9 cryptographic assets detected |
| Node.js | MD5 detected |
| Java | Detection varied across tested versions and projects |
| QBOM | Custom Python-based assessment implemented |
| JSON Reporting | Successfully generated |
| HTML Reporting | Successfully generated |
| TraceBOM | 39 runtime components observed |
| Runtime Crypto Libraries | 3 libraries observed |
| Runtime Crypto Operations | Not verified |
| Quantum Risk | RSA identified as a high-risk algorithm in the Go assessment |

### Important Limitations

1. cdxgen may not identify every cryptographic operation present in source code.
2. Detection results can vary across languages, versions, and project structures.
3. Cryptographic inventory does not prove runtime execution.
4. Quantum risk depends on the algorithm, configuration, and usage context.
5. Our QBOM risk classifications are custom and require validation before production use.
6. TraceBOM may require additional system permissions to capture operation-level evidence.
7. The reports are not a complete application security assessment.

---

## 12. Recommended Approach

For the current POC:

```text
Source Code
     |
     v
cdxgen CBOM
     |
     v
Cryptographic Asset Inventory
     |
     v
Custom Quantum Risk Assessment
     |
     v
QBOM JSON
     |
     v
QBOM HTML Report
```

### Future Enhancements

- Improve cryptographic detection across Java, Node.js, Python, and Go.
- Validate risk classification against recognized cryptographic guidance.
- Improve key-size and algorithm-configuration analysis.
- Add verified runtime evidence where TraceBOM supports it.
- Include source-code findings separately from CBOM detections.
- Automate the complete workflow in CI/CD pipelines.

---

## 13. Final Conclusion

The POC successfully demonstrated how to use **cdxgen CBOM data as the foundation for a custom quantum-readiness assessment**.

We generated JSON and HTML reports, evaluated cryptographic findings across Go, Java, and Node.js, and explored TraceBOM for runtime visibility.

**Primary implementation:** cdxgen CBOM + custom Python risk assessment.

**Optional enhancement:** TraceBOM for runtime evidence.

**Current status:** POC completed for Go and Node.js QBOM reporting. Java detection requires further improvement, and TraceBOM operation-level verification remains unconfirmed.
