from cryptography.fernet import Fernet
from django.conf import settings

key = settings.ENCRYPTION_KEY.encode()
cipher_suite = Fernet(key)


def encrypt_message(message):
    """Encrypt a message."""
    return cipher_suite.encrypt(message.encode()).decode()

def decrypt_message(message):
    """Decrypt a message."""
    return cipher_suite.decrypt(message.encode()).decode()


def encrypt_data(message):
    """Encrypt a message."""
    return cipher_suite.encrypt(message)

def decrypt_data(message):
    """Decrypt a message."""
    return cipher_suite.decrypt(message)