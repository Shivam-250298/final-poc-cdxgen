from flask import Blueprint, request, jsonify
from utils.crypto_utils import (
    sha256_hash, aes_demo, rsa_demo, pbkdf2_demo
)

crypto_route = Blueprint("crypto", __name__)


@crypto_route.post("/hash")
def hash_api():
    text = request.get_json(silent=True) or {}
    return jsonify({
        "algorithm": "SHA-256",
        "hash": sha256_hash(str(text.get("text", "")))
    })


@crypto_route.post("/aes")
def aes_api():
    data = request.get_json(silent=True) or {}
    return jsonify({
        "algorithm": "AES-256-GCM",
        "decryptedText": aes_demo(str(data.get("text", "")))
    })


@crypto_route.post("/rsa")
def rsa_api():
    data = request.get_json(silent=True) or {}
    return jsonify({
        "algorithm": "RSA-2048",
        "signatureVerified": rsa_demo(str(data.get("text", "")))
    })


@crypto_route.post("/pbkdf2")
def pbkdf2_api():
    data = request.get_json(silent=True) or {}
    return jsonify({
        "algorithm": "PBKDF2-SHA256",
        "derivedKey": pbkdf2_demo(str(data.get("password", "")))
    })
