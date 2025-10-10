from datetime import datetime, timedelta, timezone
from typing import Any, Dict

import jwt

# TODO : Move these to environment variables
JWT_SECRET = "mysecretkey"
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_MINUTES = 60


class JWTService:
    """Service for encoding and decoding JWT tokens."""

    def __init__(self, secret: str = JWT_SECRET, algorithm: str = JWT_ALGORITHM):
        self.secret = secret
        self.algorithm = algorithm

    def encode(self, payload: Dict[str, Any]) -> str:
        """Create a signed JWT token with an expiration time."""
        exp = datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRATION_MINUTES)
        payload_with_exp = {**payload, "exp": exp}
        token = jwt.encode(payload_with_exp, self.secret, algorithm=self.algorithm)
        return token

    def decode(self, token: str) -> Dict[str, Any]:
        """Decode and verify a JWT token."""
        try:
            decoded = jwt.decode(token, self.secret, algorithms=[self.algorithm])
            return decoded
        except jwt.ExpiredSignatureError:
            return {"error": "Token has expired"}
        except jwt.InvalidTokenError:
            return {"error": "Invalid token"}
