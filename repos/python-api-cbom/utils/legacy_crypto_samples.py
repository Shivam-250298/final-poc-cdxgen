"""Legacy cryptography samples for CBOM detection only.

Not imported by the Flask API. Never use these for security.
"""
import hashlib


def legacy_md5(text):
    return hashlib.md5(text.encode()).hexdigest()


def legacy_sha1(text):
    return hashlib.sha1(text.encode()).hexdigest()
