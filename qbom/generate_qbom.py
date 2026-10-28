import json
from pathlib import Path
from datetime import datetime, timezone

BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_FILE = BASE_DIR / "reports/go-cbom.json"
OUTPUT_FILE = BASE_DIR / "reports/qbom/go-qbom.json"

# Risk assessment based on algorithm identification.
# Actual usage, key sizes, and deployment exposure are not verified.
RISK_RULES = {
    "rsa": {
        "quantum_risk": "High",
        "classical_risk": "Depends on key size",
        "quantum_readiness": "Classical",
        "recommendation": "Assess RSA usage and plan migration to appropriate post-quantum algorithms."
    },
    "aes": {
        "quantum_risk": "Depends on key size",
        "classical_risk": "Depends on key size and mode",
        "quantum_readiness": "Requires verification",
        "recommendation": "Verify AES key size and cipher mode. Prefer AES-256 with authenticated encryption."
    },
    "des": {
        "quantum_risk": "Not separately assessed",
        "classical_risk": "High",
        "quantum_readiness": "Classical",
        "recommendation": "Replace DES with an approved modern encryption algorithm."
    },
    "md5": {
        "quantum_risk": "Not separately assessed",
        "classical_risk": "High",
        "quantum_readiness": "Classical",
        "recommendation": "Replace MD5 for security-sensitive cryptographic uses."
    },
    "sha-1": {
        "quantum_risk": "Not separately assessed",
        "classical_risk": "High",
        "quantum_readiness": "Classical",
        "recommendation": "Replace SHA-1 for security-sensitive cryptographic uses."
    },
    "sha-256": {
        "quantum_risk": "Lower concern",
        "classical_risk": "Low for appropriate uses",
        "quantum_readiness": "Requires usage verification",
        "recommendation": "Review usage and required security strength."
    },
    "hmacsha": {
        "quantum_risk": "Requires verification",
        "classical_risk": "Depends on hash and key",
        "quantum_readiness": "Requires verification",
        "recommendation": "Identify the HMAC hash algorithm and key strength."
    }
}

def assess_asset(component):
    name = component.get("name", "Unknown")
    crypto = component.get("cryptoProperties", {})
    algorithm = crypto.get("algorithmProperties", {})

    rule = RISK_RULES.get(name.lower(), {
        "quantum_risk": "Unknown",
        "classical_risk": "Unknown",
        "quantum_readiness": "Unknown",
        "recommendation": "Identify the algorithm, key properties, and actual usage."
    })

    return {
        "name": name,
        "bom_ref": component.get("bom-ref"),
        "asset_type": crypto.get("assetType", "Unknown"),
        "primitive": algorithm.get("primitive", "N/A"),
        "algorithm_family": algorithm.get("algorithmFamily", "Unknown"),
        "key_size": algorithm.get("classicalSecurityLevel", "Unknown"),
        **rule,
        "assessment_basis": "Algorithm inventory only",
        "usage_verified": False
    }

def main():
    with INPUT_FILE.open(encoding="utf-8") as f:
        cbom = json.load(f)

    assets = [
        assess_asset(component)
        for component in cbom.get("components", [])
        if component.get("type") == "cryptographic-asset"
    ]

    report = {
        "report_type": "Custom QBOM-style Quantum Risk Assessment",
        "generator": "Custom Python POC using cdxgen CBOM",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_cbom": str(INPUT_FILE.relative_to(BASE_DIR)),
        "note": (
            "This is not an official cdxgen QBOM. "
            "Risk classifications are preliminary and do not confirm "
            "actual cryptographic usage or exploitable vulnerabilities."
        ),
        "summary": {
            "total_crypto_assets": len(assets),
            "high_quantum_risk": sum(
                a["quantum_risk"] == "High" for a in assets
            ),
            "high_classical_risk": sum(
                a["classical_risk"] == "High" for a in assets
            ),
            "unknown_quantum_risk": sum(
                a["quantum_risk"] == "Unknown" for a in assets
            )
        },
        "assets": assets
    }

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print("QBOM-style assessment generated successfully!")
    print(f"Output: {OUTPUT_FILE}")
    print(json.dumps(report["summary"], indent=2))

if __name__ == "__main__":
    main()
