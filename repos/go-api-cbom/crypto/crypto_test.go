package crypto

import "testing"

func TestCryptoAlgorithms(t *testing.T) {
	text := "CBOM-POC-Test"

	if SHA256Hash(text) == "" {
		t.Fatal("SHA-256 failed")
	}

	decrypted, err := AESDemo(text)
	if err != nil || decrypted != text {
		t.Fatal("AES-256-GCM failed:", err)
	}

	verified, err := RSADemo(text)
	if err != nil || !verified {
		t.Fatal("RSA-2048 failed:", err)
	}

	mac, err := HMACDemo(text)
	if err != nil || mac == "" {
		t.Fatal("HMAC-SHA256 failed:", err)
	}

	if LegacyMD5(text) == "" || LegacySHA1(text) == "" {
		t.Fatal("Legacy hash test failed")
	}

	if _, err := LegacyDES(text); err != nil {
		t.Fatal("Legacy DES failed:", err)
	}
}
