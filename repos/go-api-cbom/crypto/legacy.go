package crypto

// Legacy algorithms are isolated for CBOM detection testing.
// Do not use for security or expose through API endpoints.

import (
	"crypto/des"
	"crypto/md5"
	"crypto/sha1"
	"encoding/hex"
)

func LegacyMD5(text string) string {
	sum := md5.Sum([]byte(text))
	return hex.EncodeToString(sum[:])
}

func LegacySHA1(text string) string {
	sum := sha1.Sum([]byte(text))
	return hex.EncodeToString(sum[:])
}

func LegacyDES(text string) ([]byte, error) {
	key := []byte("12345678") // Fixed demo key; intentionally insecure
	block, err := des.NewCipher(key)
	if err != nil {
		return nil, err
	}

	input := make([]byte, 8)
	copy(input, []byte(text))
	output := make([]byte, 8)
	block.Encrypt(output, input)
	return output, nil
}
