import hashlib
import secrets


def generate_salt():
    return secrets.token_hex(16)


def hash_password(password, salt):
    return hashlib.sha256((password + salt).encode("utf-8")).hexdigest()


def verify_password(password, salt, stored_hash):
    return hash_password(password, salt) == stored_hash


def simple_encrypt(text):
    return text[::-1]


def simple_decrypt(text):
    return text[::-1]
