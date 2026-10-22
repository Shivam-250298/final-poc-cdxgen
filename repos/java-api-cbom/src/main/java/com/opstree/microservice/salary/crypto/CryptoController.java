package com.opstree.microservice.salary.crypto;

import org.springframework.web.bind.annotation.*;
import java.util.Map;

@RestController
@RequestMapping("/crypto")
public class CryptoController {

    @PostMapping("/hash")
    public Map<String, Object> hash(@RequestParam String text) throws Exception {
        return Map.of(
            "algorithm", "SHA-256",
            "hash", CryptoUtils.sha256(text)
        );
    }

    @PostMapping("/aes")
    public Map<String, Object> aes(@RequestParam String text) throws Exception {
        return Map.of(
            "algorithm", "AES-256-GCM",
            "decryptedText", CryptoUtils.aesDemo(text)
        );
    }

    @PostMapping("/rsa")
    public Map<String, Object> rsa(@RequestParam String text) throws Exception {
        return Map.of(
            "algorithm", "RSA-2048",
            "signatureVerified", CryptoUtils.rsaDemo(text)
        );
    }

    @PostMapping("/hmac")
    public Map<String, Object> hmac(@RequestParam String text) throws Exception {
        return Map.of(
            "algorithm", "HMAC-SHA256",
            "hmac", CryptoUtils.hmac(text)
        );
    }
}
