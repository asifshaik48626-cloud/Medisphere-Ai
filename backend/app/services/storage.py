import hmac
import hashlib
import time
from urllib.parse import urlencode
from ..config import settings

class SecureStorageService:
    @classmethod
    def generate_presigned_url(cls, storage_key: str, expires_in: int = 3600) -> str:
        """
        Generates a secure, cryptographically signed URL that expires after a set duration.
        """
        expiry_timestamp = int(time.time()) + expires_in
        
        # Create message payload to sign
        payload = f"{storage_key}:{expiry_timestamp}"
        
        # Sign the payload using the app's secret key
        signature = hmac.new(
            settings.SECRET_KEY.encode('utf-8'),
            payload.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        # Build query parameters
        params = {
            "key": storage_key,
            "expires": expiry_timestamp,
            "signature": signature
        }
        
        # Generate final signed URL endpoint path
        return f"{settings.API_V1_STR}/documents/download-file?{urlencode(params)}"

    @classmethod
    def verify_presigned_url(cls, storage_key: str, expires: int, signature: str) -> bool:
        """
        Verifies the validity and expiration status of a signed storage key URL.
        """
        # 1. Check expiration timestamp
        if int(time.time()) > expires:
            return False
            
        # 2. Recreate signature and compare
        payload = f"{storage_key}:{expires}"
        expected_signature = hmac.new(
            settings.SECRET_KEY.encode('utf-8'),
            payload.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        # Constant time comparison to prevent timing side-channel attacks
        return hmac.compare_digest(expected_signature, signature)
