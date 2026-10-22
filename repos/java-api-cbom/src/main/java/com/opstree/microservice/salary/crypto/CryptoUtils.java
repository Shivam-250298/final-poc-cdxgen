package com.opstree.microservice.salary.crypto;

import java.nio.charset.StandardCharsets;
import java.security.*;
import java.util.Base64;
import javax.crypto.*;
import javax.crypto.spec.GCMParameterSpec;
import javax.crypto.spec.SecretKeySpec;

public class CryptoUtils {

    // 1. SHA-256: Generate a hash
    public static String sha256(String text) throws Exception {
        MessageDigest md = MessageDigest.getInstance("SHA-256");
        byte[] hash = md.digest(text.getBytes(StandardCharsets.UTF_8));
        return Base64.getEncoder().encodeToString(hash);
    }

    // 2. AES-256-GCM: Encrypt and decrypt data
    public static String aesDemo(String text) throws Exception {
        KeyGenerator generator = KeyGenerator.getInstance("AES");
        generator.init(256);
        SecretKey key = generator.generateKey();

        byte[] iv = new byte[12];
        new SecureRandom().nextBytes(iv);

        Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");
        cipher.init(Cipher.ENCRYPT_MODE, key, new GCMParameterSpec(128, iv));
        byte[] encrypted = cipher.doFinal(text.getBytes(StandardCharsets.UTF_8));

        cipher.init(Cipher.DECRYPT_MODE, key, new GCMParameterSpec(128, iv));
        byte[] decrypted = cipher.doFinal(encrypted);

        return new String(decrypted, StandardCharsets.UTF_8);
    }

    // 3. RSA-2048: Digital signature and verification
    public static boolean rsaDemo(String text) throws Exception {
        KeyPairGenerator generator = KeyPairGenerator.getInstance("RSA");
        generator.initialize(2048);
        KeyPair pair = generator.generateKeyPair();

        Signature signature = Signature.getInstance("SHA256withRSA");
        signature.initSign(pair.getPrivate());
        signature.update(text.getBytes(StandardCharsets.UTF_8));
        byte[] signed = signature.sign();

        signature.initVerify(pair.getPublic());
        signature.update(text.getBytes(StandardCharsets.UTF_8));

        return signature.verify(signed);
    }

    // 4. HMAC-SHA256: Message authentication
    public static String hmac(String text) throws Exception {
        KeyGenerator generator = KeyGenerator.getInstance("HmacSHA256");
        SecretKey key = generator.generateKey();

        Mac mac = Mac.getInstance("HmacSHA256");
        mac.init(key);

        return Base64.getEncoder().encodeToString(
            mac.doFinal(text.getBytes(StandardCharsets.UTF_8))
        );
    }
}
