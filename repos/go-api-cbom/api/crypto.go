package api

import (
	"net/http"

	cbomcrypto "employee-api/crypto"
	"github.com/gin-gonic/gin"
)

type CryptoRequest struct {
	Text string `json:"text"`
}

func CryptoHashAPI(c *gin.Context) {
	var req CryptoRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, gin.H{
		"algorithm": "SHA-256",
		"hash":      cbomcrypto.SHA256Hash(req.Text),
	})
}

func CryptoAESAPI(c *gin.Context) {
	var req CryptoRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	result, err := cbomcrypto.AESDemo(req.Text)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, gin.H{
		"algorithm":     "AES-256-GCM",
		"decryptedText": result,
	})
}

func CryptoRSAAPI(c *gin.Context) {
	var req CryptoRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	verified, err := cbomcrypto.RSADemo(req.Text)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, gin.H{
		"algorithm":         "RSA-2048",
		"signatureVerified": verified,
	})
}

func CryptoHMACAPI(c *gin.Context) {
	var req CryptoRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	result, err := cbomcrypto.HMACDemo(req.Text)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, gin.H{
		"algorithm": "HMAC-SHA256",
		"hmac":      result,
	})
}
