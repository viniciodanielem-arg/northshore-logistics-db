import hashlib
import secrets


def generate_salt():
    return secrets.token_hex(16)


def hash_password(password, salt):
    return hashlib.sha256((password + salt).encode("utf-8")).hexdigest()


def verify_password(password, salt, stored_hash):
    return hash_password(password, salt) == stored_hash

SECRET_KEY = "northshore_secure_key_2026"


def generate_encryption_key():
    return hashlib.sha256(SECRET_KEY.encode()).digest()


def simple_encrypt(text):
    if not text:
        return ""

    key = generate_encryption_key()
    encrypted_chars = []

    for i, char in enumerate(text):
        key_char = key[i % len(key)]
        encrypted_char = chr(ord(char) ^ key_char)
        encrypted_chars.append(encrypted_char)

    encrypted_string = "".join(encrypted_chars)
    return encrypted_string.encode("utf-8").hex()


def simple_decrypt(encrypted_text):
    if not encrypted_text:
        return ""

    key = generate_encryption_key()

    decoded = bytes.fromhex(encrypted_text).decode("utf-8")

    decrypted_chars = []

    for i, char in enumerate(decoded):
        key_char = key[i % len(key)]
        decrypted_char = chr(ord(char) ^ key_char)
        decrypted_chars.append(decrypted_char)

    return "".join(decrypted_chars)
