from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

def encrypt_aes_256(data, key):
    """Encrypts data using AES-256."""
    if len(key) != 32:
        raise ValueError("Key must be 256 bits (32 bytes) long.")

    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return iv + cipher.encrypt(pad(data, AES.block_size))

def decrypt_aes_256(data, key):
    """Decrypts data using AES-256."""
    if len(key) != 32:
        raise ValueError("Key must be 256 bits (32 bytes) long.")

    iv = data[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(data[AES.block_size:]), AES.block_size)

