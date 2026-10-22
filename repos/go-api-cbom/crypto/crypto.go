package crypto

import (
	"crypto"
	"crypto/aes"
	"crypto/cipher"
	"crypto/hmac"
	"crypto/rand"
	"crypto/rsa"
	"crypto/sha256"
	"encoding/hex"
	"fmt"
)

// SHA-256 hashing
func SHA256Hash(text string) string {
	sum := sha256.Sum256([]byte(text))
	return hex.EncodeToString(sum[:])
}

// AES-256-GCM encryption and decryption
func AESDemo(text string) (string, error) {
	key := make([]byte, 32)
	if _, err := rand.Read(key); err != nil {
		return "", err
	}

	block, err := aes.NewCipher(key)
	if err != nil {
		return "", err
	}

	gcm, err := cipher.NewGCM(block)
	if err != nil {
		return "", err
	}

	nonce := make([]byte, gcm.NonceSize())
	if _, err := rand.Read(nonce); err != nil {
		return "", err
	}

	ciphertext := gcm.Seal(nil, nonce, []byte(text), nil)
	plaintext, err := gcm.Open(nil, nonce, ciphertext, nil)
	if err != nil {
		return "", err
	}

	return string(plaintext), nil
}

// RSA-2048 digital signature and verification
func RSADemo(text string) (bool, error) {
	privateKey, err := rsa.GenerateKey(rand.Reader, 2048)
	if err != nil {
		return false, err
	}

	digest := sha256.Sum256([]byte(text))

	signature, err := rsa.SignPSS(
		rand.Reader, privateKey, crypto.SHA256, digest[:], nil,
	)
	if err != nil {
		return false, err
	}

	err = rsa.VerifyPSS(
		&privateKey.PublicKey, crypto.SHA256, digest[:], signature, nil,
	)

	return err == nil, err
}

// HMAC-SHA256
func HMACDemo(text string) (string, error) {
	key := make([]byte, 32)
	if _, err := rand.Read(key); err != nil {
		return "", fmt.Errorf("generate HMAC key: %w", err)
	}

	mac := hmac.New(sha256.New, key)
	mac.Write([]byte(text))
	return hex.EncodeToString(mac.Sum(nil)), nil
}
