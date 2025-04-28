import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import os

def decrypt(encrypted_uid):
    encryption_key = b'thisismyfcdriveencryptsecretkey1'

    # Decode Base64 and split IV + encrypted data
    encrypted_uid_bytes = base64.b64decode(encrypted_uid)
    iv = encrypted_uid_bytes[:16]
    encrypted_data = encrypted_uid_bytes[16:]

    # Decrypt using AES with CBC mode
    cipher = Cipher(algorithms.AES(encryption_key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(encrypted_data) + decryptor.finalize()

    # Unpad the decrypted data
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    original_uid = unpadder.update(padded_data) + unpadder.finalize()

    return original_uid.decode('utf-8')



def encrypt(firebase_uid):
    encryption_key = b'thisismyfcdriveencryptsecretkey1'  # 32 bytes key for AES-256
    iv = os.urandom(16)  # Random 16-byte IV

    # Pad the data to AES block size (128 bits)
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(firebase_uid.encode('utf-8')) + padder.finalize()

    # Create AES cipher and encrypt
    cipher = Cipher(algorithms.AES(encryption_key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    # Prepend IV to encrypted data and encode as Base64
    combined = iv + encrypted_data
    return base64.b64encode(combined).decode('utf-8')
