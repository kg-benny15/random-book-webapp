"""
Password hashing utilities for user authentication.

Uses bcrypt algorithm via Passlib for secure password storage.
"""

from passlib.context import CryptContext

# Bcrypt hashing context with 12 rounds (default)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    """
    Hash a plain text password using bcrypt.

    Args:
        plain_password: The password to hash (string)

    Returns:
        A bcrypt hash string (e.g., '$2b$12$...')

    Example:
        >>> hashed = hash_password("MySecret123")
        >>> print(hashed)
        '$2b$12$KxJk8L9kD5kF6sE2rV3uO...'
    """
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hash_password: str) -> bool:
    """
    Verify a plain password against a bcrypt hash.

    Args:
        plain_password: The password to check (string)
        hash_password: The stored bcrypt hash (string)

    Returns:
        True if the password matches, False otherwise

    Example:
        >>> is_valid = verify_password("MySecret123", stored_hash)
        >>> print(is_valid)
        True
    """
    return pwd_context.verify(plain_password, hash_password)
