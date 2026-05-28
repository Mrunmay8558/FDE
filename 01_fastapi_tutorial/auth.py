"""
Authentication helper documentation:

JWT, or JSON Web Token, is a compact token format used to safely share user
identity and permission data between a client and an API. After login, the API
can create a JWT and the client can send it with later requests to prove who it is.

Passlib is a Python password-hashing library. It helps convert plain passwords
into secure hashes and later verifies login passwords against those stored hashes.

CryptContext is Passlib's configuration object. It defines which password-hashing
algorithm is used, such as bcrypt, and gives helper methods for hashing and verifying passwords.

The JWT algorithm tells PyJWT how to sign and verify the token. The same algorithm
must be used when creating the token and when decoding it later.
"""

# time is used to calculate and verify token expiry timestamps.
import time

# jwt comes from PyJWT and is used to create and decode JSON Web Tokens.
import jwt

# os reads environment variables for the JWT secret and algorithm.
import os

# CryptContext manages password hashing and verification settings.
from passlib.context import CryptContext

# FastAPI exception/status helpers can be used when auth checks need to return HTTP errors.
from fastapi import HTTPException, status

# Password hashing configuration. bcrypt is a secure algorithm for storing passwords.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Secret key used to sign JWT tokens. It should come from an environment variable.
JWT_SECRET = os.environ.get("secret")

# Algorithm used by PyJWT when signing and decoding JWT tokens.
JWT_ALGORITHM = os.environ.get("algorithm")

# Default permission level used when a specific access level is not provided elsewhere.
DEFAULT_ACCESS_LEVEL = "WRITE"


def signJWT(
    id: str,
    email: str,
    expiry_duration: int,
):
    # Build the token payload with user identity, role, email, and expiry time.
    payload = {
        "id": id,
        "email": email,
        "expires": time.time() + expiry_duration,
    }

    # Sign and return the JWT string using the configured secret and algorithm.
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def encodePayload(payload):
    # Encode any custom payload as a signed JWT.
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decodeJWT(token: str):
    try:
        # Decode the token and verify that the token expiry timestamp is still valid.
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except Exception:
        # Invalid, expired, or malformed tokens are treated as unauthenticated.
        return None


def verify_hash_password(plain_password, hashed_password):
    # Compare a plain password with a stored hashed password.
    return pwd_context.verify(plain_password, hashed_password)


def encrypt_password(password):
    # Hash a plain password before storing it.
    return pwd_context.hash(password)
