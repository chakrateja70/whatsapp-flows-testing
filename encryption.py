"""
WhatsApp Flows Encryption/Decryption Module
"""

import base64
import json
import logging
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

logger = logging.getLogger(__name__)


class FlowEndpointException(Exception):
    """Custom exception for Flow endpoint errors"""
    def __init__(self, status_code: int, message: str):
        super().__init__(message)
        self.status_code = status_code


def decrypt_request(body: dict, private_pem: str, passphrase: str = "") -> dict:
    """
    Decrypt WhatsApp Flow request
    
    Args:
        body: Request body containing encrypted data
        private_pem: Private key in PEM format
        passphrase: Passphrase for private key (optional)
    
    Returns:
        Dict with decrypted_body, aes_key, and initial_vector
    """
    encrypted_aes_key = body.get("encrypted_aes_key")
    encrypted_flow_data = body.get("encrypted_flow_data")
    initial_vector = body.get("initial_vector")
    
    # Load private key
    passphrase_bytes = passphrase.encode('utf-8') if passphrase else None
    private_key = serialization.load_pem_private_key(
        private_pem.encode('utf-8'),
        password=passphrase_bytes
    )
    
    # Decrypt AES key
    try:
        decrypted_aes_key = private_key.decrypt(
            base64.b64decode(encrypted_aes_key),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    except Exception as error:
        logger.error(f"Decryption error: {error}")
        raise FlowEndpointException(
            421,
            "Failed to decrypt the request. Please verify your private key."
        )
    
    # Decrypt flow data
    flow_data_buffer = base64.b64decode(encrypted_flow_data)
    initial_vector_buffer = base64.b64decode(initial_vector)
    
    TAG_LENGTH = 16
    encrypted_flow_data_body = flow_data_buffer[:-TAG_LENGTH]
    encrypted_flow_data_tag = flow_data_buffer[-TAG_LENGTH:]
    
    # Decrypt using AES-128-GCM
    cipher = Cipher(
        algorithms.AES(decrypted_aes_key),
        modes.GCM(initial_vector_buffer, encrypted_flow_data_tag)
    )
    decryptor = cipher.decryptor()
    
    decrypted_data = decryptor.update(encrypted_flow_data_body) + decryptor.finalize()
    decrypted_json_string = decrypted_data.decode('utf-8')
    
    return {
        "decrypted_body": json.loads(decrypted_json_string),
        "aes_key": decrypted_aes_key,
        "initial_vector": initial_vector_buffer
    }


def encrypt_response(response: dict, aes_key: bytes, initial_vector: bytes) -> str:
    """
    Encrypt response for WhatsApp Flow
    
    Args:
        response: Response data to encrypt
        aes_key: AES key from decrypted request
        initial_vector: Initial vector from decrypted request
    
    Returns:
        Base64 encoded encrypted response
    """
    # Flip initial vector
    flipped_iv = bytes(~b & 0xFF for b in initial_vector)
    
    # Encrypt response data using AES-128-GCM
    cipher = Cipher(
        algorithms.AES(aes_key),
        modes.GCM(flipped_iv)
    )
    encryptor = cipher.encryptor()
    
    response_json = json.dumps(response)
    encrypted_data = encryptor.update(response_json.encode('utf-8')) + encryptor.finalize()
    
    # Combine encrypted data and auth tag
    encrypted_data_with_tag = encrypted_data + encryptor.tag
    
    return base64.b64encode(encrypted_data_with_tag).decode('utf-8')
