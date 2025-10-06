"""
Cryptographic utilities for ShadowRecon v1.0
"""

import hashlib
import base64

class CryptoUtils:
    @staticmethod
    def md5_hash(text: str) -> str:
        return hashlib.md5(text.encode()).hexdigest()

    @staticmethod
    def sha256_hash(text: str) -> str:
        return hashlib.sha256(text.encode()).hexdigest()

    @staticmethod
    def base64_encode(text: str) -> str:
        return base64.b64encode(text.encode()).decode()

    @staticmethod
    def base64_decode(encoded: str) -> str:
        try:
            return base64.b64decode(encoded).decode()
        except:
            return ""
