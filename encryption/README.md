README.md

# Example usage:
key = get_random_bytes(32)  # Generate a random 512-bit key


"""
The message to be encrypted and decrypted.
"""
message = b"This is a secret message."

"""
Encrypts the given message using the provided 512-bit AES key.

Parameters:
- `message`: The message to be encrypted, as bytes.
- `key`: The 512-bit encryption key, as bytes.

Returns:
The encrypted message as bytes.
"""
encrypted_message = encrypt_aes_256(message, key)
decrypted_message = decrypt_aes_256(encrypted_message, key)

print("Original message:", message)
print("Encrypted message:", encrypted_message)
print("Decrypted message:", decrypted_message)
