# cdxgen CBOM Proof of Concept

A multi-language proof of concept to evaluate cryptographic inventory generation using **cdxgen**, compare scanner output against known cryptographic operations, and produce readable JSON, HTML, and CSV reports.

The repository contains Java, Python, Go, and Node.js applications, their generated reports, reporting utilities, and a separate Hardware Bill of Materials experiment on an AWS EC2 instance.

## Contents

1. [Objective](#1-objective)
2. [POC approach and rationale](#2-poc-approach-and-rationale)
3. [Versions and scope](#3-versions-and-scope)
4. [Repository structure](#4-repository-structure)
5. [Prerequisites and installation](#5-prerequisites-and-installation)
6. [Application preparation and crypto examples](#6-application-preparation-and-crypto-examples)
7. [Generating CBOM reports](#7-generating-cbom-reports)
8. [Validating and inspecting reports](#8-validating-and-inspecting-reports)
9. [Generating HTML reports](#9-generating-html-reports)
10. [Generating CSV reports](#10-generating-csv-reports)
11. [Results and findings](#11-results-and-findings)
12. [Hardware Bill of Materials](#12-hardware-bill-of-materials)
13. [Performance measurement](#13-performance-measurement)
14. [Troubleshooting](#14-troubleshooting)
15. [CI/CD integration approach](#15-cicd-integration-approach)
16. [Limitations and next steps](#16-limitations-and-next-steps)
17. [Conclusion](#17-conclusion)
18. [References](#18-references)

## 1. Objective

The POC evaluates whether cdxgen can:

- Generate CycloneDX inventories for applications written in different languages.
- Identify cryptographic algorithms and related cryptographic material.
- Detect known crypto operations deliberately included in application source code.
- Provide evidence such as source files, line numbers, and usage information.
- Identify legacy algorithms included as controlled detection samples.
- Produce machine-readable JSON and readable HTML/CSV outputs.
- Support a repeatable workflow suitable for later CI/CD integration.

The evaluation checks both successful detections and missing detections.

A successful command or a valid JSON file does not, by itself, demonstrate complete cryptographic coverage.

### Terminology

| Term | Meaning in this POC |
|---|---|
| SBOM | Inventory of software components, including dependencies and frameworks |
| CBOM | Inventory containing cryptographic assets, potentially alongside ordinary software components |
| HBOM | Inventory of hardware and firmware visible to the collector |
| Cryptographic asset | A component with `type: "cryptographic-asset"` |
| Algorithm asset | A cryptographic asset representing an algorithm |
| Related crypto material | An asset indicator representing material such as a key or private key |
| Evidence | Information connecting a reported component to a source location or analysis method |

The CBOM files in this repository contain both software dependencies and cryptographic assets. They are not crypto-only lists.

## 2. POC approach and rationale

The investigation progressed through three stages.

### Stage 1: Baseline scans

Existing Java, Python, and Go microservices were scanned to establish an initial baseline.

The earlier POC report recorded zero cryptographic assets for those baseline scans.

This result did not establish that the applications or their dependencies contained no cryptography. It showed that the scans had not emitted supported cryptographic assets.

### Stage 2: Controlled crypto programs

Small programs containing known cryptographic operations were used to test positive detection.

This made it possible to ask:

- Does the scanner detect an algorithm that is definitely present?
- Does it preserve its mode and key length?
- Does it identify the source location?
- Does it consolidate multiple operations into one asset?
- Does detection vary by language and API?

### Stage 3: Application-level examples

The final repository contains application-level crypto examples and reports generated with cdxgen 13.4.0.

Java, Python, and Go retain the structure of the salary, attendance, and employee microservices. Node.js provides a small Express application.

| Decision | Reason |
|---|---|
| Test multiple languages | Evaluate coverage differences across language ecosystems |
| Add known crypto operations | Establish a source-level reference against which scanner output can be checked |
| Include API handlers | Demonstrate how the examples connect to application functionality |
| Isolate legacy samples | Evaluate detection of older algorithms without exposing them as normal API features |
| Preserve JSON | Retain the most detailed scanner output for analysis and automation |
| Generate HTML | Make results readable without requiring JSON inspection |
| Generate CSV | Support spreadsheet filtering and comparisons |
| Record missed detections | Document practical limitations instead of equating scan completion with completeness |
| Explore HBOM separately | Evaluate host inventory as a distinct capability |

## 3. Versions and scope

### Earlier investigation versus final repository

| Item | Earlier investigation | Final committed CBOM reports |
|---|---|---|
| cdxgen version | 12.8.7 | 13.4.0 |
| npm package | `@cyclonedx/cdxgen` | `@cdxgen/cdxgen` |
| CycloneDX specification | 1.6 | 1.7 |
| Main test scope | Baseline repositories and small controlled programs | Four applications containing crypto examples |
| Evidence location | Separate POC report | JSON, HTML, CSV, and source files in this repository |

The final Java, Python, Go, and Node.js JSON reports identify **cdxgen 13.4.0** in their metadata.

The findings below describe the committed repository snapshot at:

`f5ed8952cd1df8c181e8b9536aa10026d5814045`

### Reproduction scope

The setup and scan commands below form a reconstructed reproduction workflow.

The repository does not retain the complete original terminal history or final scan logs. Therefore:

- These commands should not be treated as an exact transcript of every historical run.
- Fresh outputs may differ because of runtime versions, dependency resolution, installed analysis helpers, environment, or scan options.
- The committed reports remain the reference for the findings documented here.
- New scans are written to `run-output/` so that committed reference reports remain available for comparison.

The earlier 12.8.7 benchmark measurements must not be treated as measurements of the final 13.4.0 application scans.

## 4. Repository structure

| Path | Purpose |
|---|---|
| `repos/java-api-cbom/` | Java salary application with crypto utilities and endpoints |
| `repos/python-api-cbom/` | Python attendance application with crypto utilities and endpoints |
| `repos/go-api-cbom/` | Go employee application with crypto utilities, tests, and endpoints |
| `repos/nodejs-api-cbom/` | Express application with crypto examples and tests |
| `reports/java-cbom.json` | Final Java CBOM |
| `reports/python-cbom.json` | Final Python CBOM |
| `reports/go-cbom.json` | Final Go CBOM |
| `reports/nodejs-cbom.json` | Final Node.js CBOM |
| `reports/*-cbom.html` | Readable application report summaries |
| `reports-csv/` | Java, Go, and Node.js component exports |
| `reports/hbom/` | Custom and collector-generated hardware reports |
| `scripts/cbom_to_html.py` | Converts CBOM JSON into HTML |
| `scripts/generate_hbom.py` | Converts filtered `lshw` inventory into JSON and HTML |

A Python CSV is not included in the reference snapshot. It can be generated using the CSV command below.

Logs, dependency directories, build outputs, and scanner caches are excluded through `.gitignore`.

## 5. Prerequisites and installation

### 5.1 Required tools

| Tool | Purpose |
|---|---|
| Linux environment | Reference POC platform was Ubuntu on AWS EC2 |
| Git | Clone the repository |
| Node.js 24 or newer | Declared runtime requirement of the upstream cdxgen 13.4.0 npm package |
| npm | Install cdxgen and Node.js dependencies |
| JDK and Maven | Prepare the Java application |
| Python 3.11 or newer | Python application and report generation |
| Python virtual environment support | Isolate Python dependencies |
| Poetry | Install dependencies from the Python project |
| Go | Prepare and test the Go application |
| `jq` | Inspect and export JSON |
| GNU `time` | Capture elapsed time and peak process memory |
| `lshw` | Optional custom hardware inventory |

The Java project declares Java 17 in `pom.xml`. The Go module declares `go 1.20`. These declarations do not establish the exact runtime versions used in the historical scans.

Source-analysis helpers may have additional runtime requirements. Check their installation and startup messages if deep analysis fails.

### 5.2 Install common Ubuntu packages

```bash
sudo apt-get update
```

```bash
sudo apt-get install -y git jq time python3 python3-venv python3-pip openjdk-17-jdk maven golang-go build-essential libpq-dev
```

Package availability and versions depend on the Ubuntu release. Verify the installed versions before continuing.

Install Node.js 24 or newer using your standard Node.js installation method.

If NVM is already installed:

```bash
nvm install 24
```

```bash
nvm use 24
```

Verify:

```bash
node --version
```

```bash
npm --version
```

### 5.3 Install cdxgen 13.4.0

cdxgen v13 uses the `@cdxgen/cdxgen` package name.

If an older global installation exists under the previous package name, remove it before installing v13 to avoid command conflicts:

```bash
npm uninstall -g @cyclonedx/cdxgen
```

Install the version associated with the final reports:

```bash
npm install -g @cdxgen/cdxgen@13.4.0
```

With NVM, global npm packages are normally installed without `sudo`.

Verify the installed command:

```bash
cdxgen --version
```

```bash
cbom --help
```

```bash
command -v cdxgen
```

```bash
npm list -g --depth=0
```

Do not omit optional dependencies when preparing a full source-analysis environment without first checking which helpers the scan needs.

### 5.4 Clone the repository

```bash
git clone https://github.com/Shivam-250298/final-poc-cdxgen.git
```

```bash
cd final-poc-cdxgen
```

Create directories for fresh outputs:

```bash
mkdir -p run-output/reports run-output/reports-csv run-output/validation logs
```

Run the remaining commands from the repository root unless a command explicitly changes directories.

For comparison against the reviewed snapshot, use a separate checkout or worktree at commit `f5ed8952cd1df8c181e8b9536aa10026d5814045`.

### 5.5 Record the environment

```bash
{ date -u; git rev-parse HEAD; node --version; npm --version; cdxgen --version; java -version; mvn -version; python3 --version; go version; } > logs/environment.txt 2>&1
```

Retain this file with the scan logs and reports.

## 6. Application preparation and crypto examples

### 6.1 Java

Application: `repos/java-api-cbom/`

Main crypto files:

- `src/main/java/com/opstree/microservice/salary/crypto/CryptoUtils.java`
- `src/main/java/com/opstree/microservice/salary/crypto/CryptoController.java`

| Operation | Implementation |
|---|---|
| Hashing | SHA-256 |
| Encryption/decryption | AES-256-GCM |
| Signing/verification | RSA-2048 with `SHA256withRSA` |
| Message authentication | HMAC-SHA256 |

The examples use Java security and cryptography APIs. The final application's `pom.xml` does not declare the Bouncy Castle dependency used in an earlier standalone experiment.

Prepare the application:

```bash
mvn -f repos/java-api-cbom/pom.xml -DskipTests package
```

This command builds the application while skipping test execution. It must not be described as a passing test run.

The complete application has infrastructure configuration inherited from the original microservice. Building or scanning it is different from successfully starting the full service with its backend dependencies.

### 6.2 Python

Application: `repos/python-api-cbom/`

Main crypto files:

- `utils/crypto_utils.py`
- `utils/legacy_crypto_samples.py`
- `router/crypto.py`

| Operation | Implementation |
|---|---|
| Hashing | SHA-256 |
| Encryption/decryption | AES-256-GCM |
| Signing/verification | RSA-2048, PKCS#1 v1.5, SHA-256 |
| Key derivation | PBKDF2-HMAC-SHA256 |
| Isolated legacy samples | MD5 and SHA-1 |

The legacy samples are not imported by the Flask API.

Create an isolated environment:

```bash
python3 -m venv repos/python-api-cbom/.venv
```

Install Poetry into that environment:

```bash
repos/python-api-cbom/.venv/bin/python -m pip install poetry
```

Install application dependencies:

```bash
(cd repos/python-api-cbom && . .venv/bin/activate && poetry install --no-root --no-interaction)
```

`--no-root` installs the dependencies without attempting to install the application as a distributable package.

If Poetry reports a mismatch between `pyproject.toml` and `poetry.lock`, resolve it deliberately and retain the resulting dependency changes with the scan evidence.

A lightweight utility check can run without starting the Flask application:

```bash
(cd repos/python-api-cbom && .venv/bin/python -c 'from utils.crypto_utils import sha256_hash,aes_demo,rsa_demo,pbkdf2_demo; assert len(sha256_hash("hello")) == 64; assert aes_demo("hello") == "hello"; assert rsa_demo("hello"); assert pbkdf2_demo("password"); print("Crypto utility checks passed")')
```

This is a suggested smoke check, not evidence of a historical full application test run.

### 6.3 Go

Application: `repos/go-api-cbom/`

Main crypto files:

- `crypto/crypto.go`
- `crypto/legacy.go`
- `crypto/crypto_test.go`
- `api/crypto.go`

| Operation | Implementation |
|---|---|
| Hashing | SHA-256 |
| Encryption/decryption | AES-256-GCM |
| Signing/verification | RSA-2048 with RSA-PSS |
| Message authentication | HMAC-SHA256 |
| Isolated legacy samples | MD5, SHA-1, DES |

The DES sample contains a fixed demonstration key. It exists for detection testing and is not exposed through a crypto API handler.

Download dependencies:

```bash
(cd repos/go-api-cbom && go mod download)
```

Run the focused crypto tests:

```bash
(cd repos/go-api-cbom && go test ./crypto -v)
```

Build the application:

```bash
(cd repos/go-api-cbom && go build ./...)
```

The repository already contains `go.mod`. Do not run `go mod init` again.

### 6.4 Node.js

Application: `repos/nodejs-api-cbom/`

Main files:

- `crypto-utils.js`
- `app.js`
- `test/crypto.test.js`

| Operation | Implementation |
|---|---|
| Hashing | SHA-256 |
| Key derivation | PBKDF2-HMAC-SHA256 |
| Encryption/decryption | AES-256-GCM |
| Signing/verification | RSA-2048 with SHA-256 |
| Message authentication | HMAC-SHA256 |

Install dependencies from the lockfile:

```bash
npm ci --prefix repos/nodejs-api-cbom
```

Run the tests:

```bash
npm test --prefix repos/nodejs-api-cbom
```

The five committed crypto tests passed during repository review.

Start the demonstration API:

```bash
npm start --prefix repos/nodejs-api-cbom
```

In another terminal:

```bash
curl http://localhost:3000/health
```

```bash
curl -X POST http://localhost:3000/hash -H 'Content-Type: application/json' -d '{"text":"hello"}'
```

The encryption endpoint returns its demonstration key with the ciphertext so that the decryption flow can be tested. This is POC behavior, not a production key-management design.

## 7. Generating CBOM reports

### 7.1 Command options

| Option | Purpose |
|---|---|
| `-t` | Select the project type |
| `--spec-version 1.7` | Request CycloneDX 1.7 output |
| `--include-crypto` | Enable supported cryptographic inventory collection |
| `--evidence` | Request supported evidence enrichment |
| `--deep` | Enable deeper analysis paths |
| `-o` | Specify the output file |

The `cbom` alias supplies crypto-oriented defaults. The examples below state the main options explicitly to make the requested behavior visible.

Flags request analysis; they do not guarantee that every algorithm, parameter, or source location will be reported.

### 7.2 Java scan

```bash
/usr/bin/time -v -o logs/java-performance.log cbom -t java --spec-version 1.7 --include-crypto --evidence --deep -o run-output/reports/java-cbom.json repos/java-api-cbom > logs/java-scan.log 2>&1
```

### 7.3 Python scan

Use the application's environment for dependency visibility:

```bash
(cd repos/python-api-cbom && . .venv/bin/activate && /usr/bin/time -v -o ../../logs/python-performance.log cbom -t python --spec-version 1.7 --include-crypto --evidence --deep -o ../../run-output/reports/python-cbom.json . > ../../logs/python-scan.log 2>&1)
```

The working directory differs from the historical paths recorded in the committed report, so source-path formatting may differ.

Virtual environments and installed package contents can affect inventory scope. Record any exclusions you add rather than treating excluded and non-excluded scans as equivalent.

### 7.4 Go scan

```bash
/usr/bin/time -v -o logs/go-performance.log cbom -t go --spec-version 1.7 --include-crypto --evidence --deep -o run-output/reports/go-cbom.json repos/go-api-cbom > logs/go-scan.log 2>&1
```

### 7.5 Node.js scan

Start with the normal JavaScript scan:

```bash
/usr/bin/time -v -o logs/nodejs-performance.log cdxgen -t js --spec-version 1.7 --include-crypto --evidence --deep -o run-output/reports/nodejs-cbom.json repos/nodejs-api-cbom > logs/nodejs-scan.log 2>&1
```

Inspect the generated crypto assets before accepting the result.

#### POC multi-type workaround

The earlier investigation used the following multi-type pattern to reach a crypto-producing analysis route:

```bash
/usr/bin/time -v -o logs/nodejs-multitype-performance.log cdxgen -t js -t crypto --spec-version 1.7 --include-crypto --evidence --deep -o run-output/reports/nodejs-multitype-cbom.json repos/nodejs-api-cbom > logs/nodejs-multitype-scan.log 2>&1
```

Treat this as a version-specific POC workaround, not as a claim that `crypto` is an officially supported project type.

The repository history confirms:

- Initial Node.js report: 68 components, zero cryptographic assets.
- Updated report: 71 components, three cryptographic assets.
- Update commit: `9fec8a660e371142981eeaa87c63f7206cc77dce`, titled “Update Node.js CBOM with multi-type crypto detection.”

The exact final historical invocation is not preserved.

### 7.6 Check completion

Immediately after a scan, inspect its exit status:

```bash
echo $?
```

Review the corresponding scan log and output file even when the exit status is zero.

A completed scan can still have incomplete detection or failed optional enrichment.

## 8. Validating and inspecting reports

The following examples inspect the committed Go report. Replace the path with a fresh report under `run-output/reports/` when validating a new scan.

### 8.1 Check JSON syntax

```bash
jq empty reports/go-cbom.json
```

### 8.2 Inspect format and tool metadata

```bash
jq '{bomFormat, specVersion, timestamp: .metadata.timestamp, tools: .metadata.tools}' reports/go-cbom.json
```

### 8.3 Count components and crypto assets

```bash
jq '{total_components: ((.components // []) | length), total_crypto_assets: ([.components[]? | select(.type == "cryptographic-asset")] | length)}' reports/go-cbom.json
```

These counts exclude the parent component under `metadata.component`.

### 8.4 List asset names

```bash
jq -r '.components[]? | select(.type == "cryptographic-asset") | .name' reports/go-cbom.json
```

### 8.5 Inspect full crypto details

```bash
jq '.components[]? | select(.type == "cryptographic-asset") | {name, cryptoProperties, properties, evidence}' reports/go-cbom.json
```

This is necessary because useful information may appear in:

- `cryptoProperties`
- Custom `properties`
- `evidence.identity`
- `evidence.occurrences`

### 8.6 Extract source-location properties

```bash
jq -r '.components[]? | select(.type == "cryptographic-asset") | .name as $name | .properties[]? | select(.name | endswith("sourceLocation")) | [$name, .value] | @tsv' reports/go-cbom.json
```

### 8.7 Summarize all application reports

```bash
for report in reports/*-cbom.json; do jq -r --arg report "$report" '[$report, .specVersion, ((.components // []) | length), ([.components[]? | select(.type == "cryptographic-asset")] | length)] | @tsv' "$report"; done
```

### 8.8 Additional structural validation

The earlier POC recorded basic JSON and field inspection. A separately documented full schema validation run is not part of the historical evidence.

For a new validation run using the v13 toolset:

```bash
cdx-validate -i reports/go-cbom.json --strict > run-output/validation/go-validation.log 2>&1
```

Review the output and exit status. Repeat for each report.

Structural validity does not establish detection completeness or confirm that the application uses cryptography securely.

## 9. Generating HTML reports

The repository includes:

`scripts/cbom_to_html.py`

It reads an existing JSON file and produces a standalone HTML summary using Python's standard library.

### Convert the committed reports

```bash
for language in java python go nodejs; do python3 scripts/cbom_to_html.py "reports/${language}-cbom.json" "run-output/reports/${language}-cbom.html"; done
```

To convert newly generated JSON, use `run-output/reports/` as the input directory as well.

### Included information

- Total component count.
- Cryptographic asset count.
- Other component count.
- CycloneDX version.
- Scanner name and version.
- BOM serial number.
- Asset names, types, OIDs, primitives, and algorithm families.
- Dependency and component inventory.

### Current limitations

The converter does not display every field in the JSON.

It currently omits:

- Source locations and occurrence evidence.
- Strength labels.
- Detailed operation information.
- Dependency relationships.
- Detailed key or certificate properties.
- Vulnerability analysis and remediation.

The HTML generation time is the conversion time, not the original scan time.

For detailed investigation, use the JSON as the primary record.

### Viewing the reports

Download an HTML file and open it in a browser.

For local HTTP viewing:

```bash
python3 -m http.server 8000 --bind 127.0.0.1 --directory reports
```

Then open:

`http://127.0.0.1:8000/go-cbom.html`

GitHub normally displays HTML source rather than rendering the report as a hosted page.

## 10. Generating CSV reports

The committed CSV files contain all components, including libraries, frameworks, and crypto assets.

### Export all components

```bash
for language in java python go nodejs; do jq -r '(["Type","Name","Version","Primitive","BOM Reference"] | @csv), (.components[]? | [.type, .name, (.version // "N/A"), (.cryptoProperties.algorithmProperties.primitive // "N/A"), .["bom-ref"]] | @csv)' "reports/${language}-cbom.json" > "run-output/reports-csv/${language}-cbom.csv"; done
```

### Export crypto assets only

```bash
jq -r '(["Name","Asset Type","Primitive","OID","BOM Reference"] | @csv), (.components[]? | select(.type == "cryptographic-asset") | [.name, (.cryptoProperties.assetType // "N/A"), (.cryptoProperties.algorithmProperties.primitive // "N/A"), (.cryptoProperties.oid // "N/A"), .["bom-ref"]] | @csv)' reports/go-cbom.json > run-output/reports-csv/go-crypto-only.csv
```

### Existing column naming

The committed exports use the header `Algorithm` for values taken from the algorithm's `primitive` field.

For example, `hash`, `mac`, and `block-cipher` describe primitive categories, not algorithm names.

The commands above use the more precise header `Primitive`. The actual asset name remains in `Name`.

`N/A` means that the selected field is absent or not applicable. It does not mean the component has no cryptographic relevance.

## 11. Results and findings

### 11.1 Final inventory summary

| Language | Total components | Other components | Crypto assets | Crypto source locations |
|---|---:|---:|---:|---|
| Java | 129 | 127 | 2 | Not recorded on the crypto assets |
| Python | 79 | 78 | 1 | Not recorded on the crypto asset |
| Go | 82 | 73 | 9 | Present |
| Node.js | 71 | 68 | 3 | Present |

All four final reports use CycloneDX 1.7 and identify cdxgen 13.4.0.

“Other components” includes ordinary libraries and frameworks. It is not a count of vulnerabilities.

### 11.2 Java

Source includes:

- SHA-256.
- AES-256-GCM.
- RSA-2048 signing and verification.
- HMAC-SHA256.

Reported crypto asset names:

- `sha-256`
- `hmacSHA`

Findings:

- SHA-256 and an HMAC-family asset are present.
- AES and RSA are absent from the final crypto component list despite being present in the source.
- The reported assets lack source-location evidence.
- The generic `hmacSHA` entry does not preserve the exact HMAC-SHA256 configuration used by the application.
- Missing source evidence limits attribution to a particular application call.

Reference: [Java JSON](reports/java-cbom.json) · [Java HTML](reports/java-cbom.html)

### 11.3 Python

Source includes:

- SHA-256.
- AES-256-GCM.
- RSA-2048 signing and verification.
- PBKDF2-HMAC-SHA256.
- Isolated MD5 and SHA-1 samples.

Reported crypto asset:

- `aes`

Findings:

- The final report contains one AES asset.
- SHA-256, RSA, PBKDF2, MD5, and SHA-1 are not represented as crypto assets.
- AES mode, key length, and source location are not recorded on the asset.
- The report includes Python dependencies and additional native/Rust-related dependency entries.
- Without source evidence, the AES entry cannot be conclusively attributed to the application's specific AES-GCM call.

Reference: [Python JSON](reports/python-cbom.json) · [Python HTML](reports/python-cbom.html)

### 11.4 Go

Reported algorithm assets:

- `aes`
- `des`
- `hmacSHA`
- `md5`
- `rsa`
- `sha-1`
- `sha-256`

Reported related-material assets:

- `key`
- `private-key`

Findings:

- The report represents all seven algorithm families included in the Go fixtures.
- The nine-asset total includes two material indicators; it does not mean nine distinct algorithms.
- Source locations connect the assets to the crypto implementation and legacy sample files.
- The report labels DES, MD5, and SHA-1 as weak through custom properties.
- The AES asset does not preserve the full AES-256-GCM configuration.
- The RSA asset does not preserve the 2048-bit key length.
- The RSA primitive is recorded as `pke`, while the demonstration uses RSA-PSS signing. Source review remains necessary to understand the operation.
- Key-material entries indicate detected material categories; they are not exported private-key values.

These are static-analysis observations. A `runtime` usage-scope property is not proof that the code was dynamically executed during scanning.

Reference: [Go JSON](reports/go-cbom.json) · [Go HTML](reports/go-cbom.html)

### 11.5 Node.js

Source includes:

- SHA-256.
- AES-256-GCM.
- RSA-2048.
- PBKDF2-HMAC-SHA256.
- HMAC-SHA256.

Reported crypto assets:

- `rsa`
- `sha-1`
- `sha-256`

Findings:

- RSA and SHA-256 have application source evidence.
- SHA-1 evidence points to dependency files under `node_modules`, including `cookie-signature` and `etag`.
- SHA-256 consolidates evidence for hashing, HMAC, key derivation, and signature operations.
- HMAC and PBKDF2 are therefore represented in usage evidence without separate named component entries.
- AES-256-GCM is absent from the final crypto inventory even though the application implements it and the AES round-trip test passes.
- RSA key length is not preserved on the crypto asset.
- Finding SHA-1 in a dependency does not, by itself, establish an exploitable vulnerability. Its purpose and execution context require review.

Reference: [Node.js JSON](reports/nodejs-cbom.json) · [Node.js HTML](reports/nodejs-cbom.html)

### 11.6 Interpretation

The results demonstrate that:

1. Software dependency discovery and cryptographic operation discovery are different capabilities.
2. Language support does not imply equal crypto coverage across languages.
3. Asset count is not the same as operation count.
4. Dependency crypto and application crypto should be distinguished.
5. Algorithm presence does not establish correct mode, key length, or secure usage.
6. A missing asset is not proof that the algorithm is absent from the application.

No controlled same-source, same-environment comparison between 12.8.7 and 13.4.0 is preserved here. Differences between the earlier and later experiments should not be attributed solely to the scanner upgrade.

## 12. Hardware Bill of Materials

HBOM exploration is separate from the application CBOM evaluation.

### 12.1 Custom `lshw` conversion

The script `scripts/generate_hbom.py` reads:

`logs/hbom-lshw.json`

It selects these hardware classes:

- Processor.
- Memory.
- Disk.
- Storage.
- Network.
- Display.
- Bus.
- Volume.

It writes:

- `reports/hbom/hbom.json`
- `reports/hbom/hbom.html`

The committed custom report contains:

| Item | Value |
|---|---|
| CycloneDX specification | 1.6 |
| Inventory entries | 18 |
| Hardware classes | 8 |
| Metadata tool name | `lshw inventory converter` |

To regenerate on a test host:

```bash
sudo apt-get install -y lshw
```

```bash
mkdir -p logs
```

```bash
sudo lshw -json > logs/hbom-lshw.json
```

```bash
python3 scripts/generate_hbom.py
```

Unlike the CBOM examples, this script writes directly to the committed report paths. Use a separate working copy when preserving the original reports.

The script hardcodes the EC2 platform, `c7i-flex.large` instance type, and virtualization description. Update those fields before using it on another host.

### 12.2 cdxgen HBOM collector

The second report identifies `cdx-hbom` as its collector.

| Item | Value |
|---|---|
| CycloneDX specification | 1.7 |
| Inventory entries | 59 |
| Device entries | 58 |
| Firmware entries | 1 |
| HTML hardware-class groups | 12 |

A documented command for a new collection is:

```bash
hbom -o run-output/reports/hbom.json
```

This is a reproduction example, not the preserved historical command.

The dedicated generator for `hbom-official.html` is not included in this repository. The application CBOM converter is not equivalent to that hardware-specific presentation.

### 12.3 Why the counts differ

The custom converter filters the raw inventory into a narrower set of entries. The collector report includes a broader representation, including PCI and firmware-related entries.

Therefore, 18 versus 59 should not be interpreted as a direct accuracy score.

Both reports describe hardware visible within the EC2 virtual machine, not the complete physical AWS host.

References: [Custom HBOM](reports/hbom/hbom.json) · [Collector HBOM](reports/hbom/hbom-official.json)

## 13. Performance measurement

The scan examples use GNU `time` to record:

- Elapsed wall-clock time.
- User CPU time.
- System CPU time.
- Maximum resident set size.
- Command exit status.

Inspect a measurement:

```bash
cat logs/go-performance.log
```

Extract key fields:

```bash
grep -E 'User time|System time|Elapsed|Maximum resident set size|Exit status' logs/go-performance.log
```

On Linux, dividing maximum resident set size in kilobytes by 1024 gives an approximate MiB value.

### Interpretation

- Elapsed time includes waiting, dependency retrieval, and analysis.
- Peak RSS is a process-memory metric, not whole-host memory consumption or a sum of all concurrent helper processes.
- User/system CPU time is not a whole-host CPU utilization percentage.
- Cold dependency downloads and warm-cache runs are not equivalent.
- Different applications are not directly comparable benchmark workloads.

Final 13.4.0 performance logs are not committed. No final-run performance values are claimed in this README.

For repeatable benchmarking, record versions, instance size, scan arguments, cache conditions, and several runs per application.

## 14. Troubleshooting

| Observation | Possible explanation | Action |
|---|---|---|
| `cdxgen` is unavailable | npm executable directory is not on `PATH` | Check `command -v cdxgen` and the active Node installation |
| Wrong cdxgen version runs | Old and new package installations coexist | Inspect global npm packages and command resolution |
| Engine compatibility error | Node.js is below the package requirement | Use a compatible Node.js runtime |
| JSON exists but crypto count is zero | Unsupported patterns, routing differences, or incomplete analysis | Inspect logs and compare against known source examples |
| Java crypto coverage is incomplete | Dependency discovery succeeded but crypto detection was partial | Check build and analyzer logs; compare each expected operation |
| Python contains only AES | Final inventory does not represent all source operations | Inspect crypto fields and evidence; do not infer complete coverage |
| Go reports more assets than algorithm families | Related key material is also counted | Separate `algorithm` from `related-crypto-material` |
| Node.js reports SHA-1 unexpectedly | Dependency code was analyzed | Read source locations before attributing it to application code |
| Node.js misses AES | Source usage did not become a final crypto component | Retain the source fixture, output, version, and logs for investigation |
| HTML lacks source locations | The converter does not render those fields | Inspect JSON or extend the converter |
| CSV contains `N/A` | The selected field is absent or inapplicable | Inspect the original component |
| Fresh counts differ | Different environment, dependencies, helper versions, or options | Compare environment records and lockfiles |
| Python full-service startup fails | Backend configuration or dependencies are unavailable | Separate crypto utility checks from full-service integration tests |
| Custom HBOM shows the wrong instance type | Script metadata is hardcoded | Update metadata before collection |
| HBOM collector returns partial data | Missing utilities or insufficient access | Inspect collector diagnostics and the resulting evidence |

## 15. CI/CD integration approach

A Jenkinsfile or equivalent automated scan pipeline is not committed in this snapshot.

A proposed integration sequence is:

1. Check out a specific application commit.
2. Prepare the required language runtime and dependencies.
3. Run focused build and crypto tests.
4. Generate the CycloneDX JSON report.
5. Validate the report.
6. Generate HTML and CSV from the same JSON.
7. Print a scan summary.
8. Archive reports, validation output, environment details, and logs.

### Example console summary

```bash
jq -r '"Total Components: \((.components // []) | length)\nTotal Crypto Assets: \([.components[]? | select(.type == "cryptographic-asset")] | length)"' run-output/reports/go-cbom.json
```

List individual assets:

```bash
jq -r '[.components[]? | select(.type == "cryptographic-asset")] | to_entries[] | "Asset \(.key + 1): \(.value.name) | Type: \(.value.cryptoProperties.assetType // "unknown")"' run-output/reports/go-cbom.json
```

### Suggested pipeline checks

- Fail on scanner execution errors or missing output.
- Fail when required structural validation fails.
- Check known-positive fixtures for expected crypto detections.
- Preserve analysis warnings and incomplete-enrichment messages.
- Apply a separately defined policy for disallowed algorithms.
- Review dependency findings in context.

A universal “crypto count must be greater than zero” rule is insufficient. Expectations should depend on the application and its known crypto usage.

Generating this inventory does not automatically provide vulnerability matching, remediation recommendations, or a production security decision.

## 16. Limitations and next steps

### Current limitations

- Detection is incomplete for several known source operations.
- Java and Python crypto entries lack source-level attribution.
- Algorithm modes and key sizes are not consistently preserved.
- Multiple operations can be consolidated into one asset.
- Dependencies contribute crypto findings.
- HTML and CSV contain only selected JSON fields.
- Original final scan commands and performance logs are not retained.
- The official HBOM HTML generator is not committed.
- No automated pipeline or repeated benchmark suite is committed.
- Inventory generation does not establish full security or compliance coverage.

### Next steps

- Add a versioned scan runner with recorded arguments and exit statuses.
- Capture runtime, scanner, and helper versions with every run.
- Keep known-positive fixtures and expected-detection assertions.
- Extend HTML reporting with source locations, operations, and evidence.
- Separate application and dependency crypto where attribution is available.
- Add Python CSV generation to the standard reporting workflow.
- Store validation results alongside each report.
- Compare scanner versions on identical source and dependency snapshots.
- Investigate missed detections with minimal reproducible examples.
- Integrate generation and reporting into CI/CD.
- Evaluate downstream vulnerability and crypto-policy analysis separately.
- Parameterize host metadata in the custom HBOM converter.

## 17. Conclusion

The POC demonstrates that cdxgen can generate useful software and cryptographic inventories across Java, Python, Go, and Node.js, with JSON outputs that can be converted into readable HTML and CSV reports.

For these fixtures, Go provided the broadest explicit algorithm coverage. Node.js provided useful application and dependency source evidence, while Java and Python showed substantial gaps between implemented operations and reported assets.

The practical outcome is a working inventory and reporting approach with documented detection boundaries.

For security assurance, remediation planning, or cryptographic migration, the generated CBOM should be reviewed against source code and supplemented with additional analysis.

## 18. References

### This repository

- [Application source](repos/)
- [CBOM reports](reports/)
- [CSV exports](reports-csv/)
- [CBOM HTML converter](scripts/cbom_to_html.py)
- [Custom HBOM converter](scripts/generate_hbom.py)

### Upstream documentation

- [cdxgen repository](https://github.com/cdxgen/cdxgen)
- [cdxgen 13.4.0 package and runtime declarations](https://github.com/cdxgen/cdxgen/blob/v13.4.0/package.json)
- [cdxgen 13.4.0 README](https://github.com/cdxgen/cdxgen/blob/v13.4.0/README.md)
- [cdxgen CLI reference](https://github.com/cdxgen/cdxgen/blob/v13.4.0/docs/CLI.md)
- [cdxgen HBOM documentation](https://github.com/cdxgen/cdxgen/blob/v13.4.0/docs/HBOM.md)
- [cdxgen validation documentation](https://github.com/cdxgen/cdxgen/blob/v13.4.0/docs/CDX_VALIDATE.md)
- [CycloneDX](https://cyclonedx.org/)
- [Node.js downloads](https://nodejs.org/en/download)
- [NVM](https://github.com/nvm-sh/nvm)

### Original microservice projects

- [Salary API](https://github.com/OT-MICROSERVICES/salary-api)
- [Attendance API](https://github.com/OT-MICROSERVICES/attendance-api)
- [Employee API](https://github.com/OT-MICROSERVICES/employee-api)

Preserve the original projects' license notices when redistributing their code.
