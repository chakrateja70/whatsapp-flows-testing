"""
RSA Key Pair Generator for WhatsApp Flows

Usage:
    python key_generator.py <passphrase>

This script generates a public and private key pair for WhatsApp Flows encryption.
Copy the private key to your .env file and upload the public key to WhatsApp.
"""

import sys
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


def generate_key_pair(passphrase: str):
    """Generate RSA key pair with passphrase protection"""
    
    # Generate private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    
    # Serialize private key with encryption
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.BestAvailableEncryption(passphrase.encode('utf-8'))
    )
    
    # Generate public key
    public_key = private_key.public_key()
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    return private_pem.decode('utf-8'), public_pem.decode('utf-8')


def main():
    if len(sys.argv) < 2:
        print("❌ Error: Passphrase is required")
        print("\nUsage: python key_generator.py <passphrase>")
        print("Example: python key_generator.py MySecurePassphrase123")
        sys.exit(1)
    
    passphrase = sys.argv[1]
    
    try:
        private_key, public_key = generate_key_pair(passphrase)
        
        print("✅ Successfully created your public private key pair!")
        print("\n" + "=" * 80)
        print("COPY PASSPHRASE & PRIVATE KEY BELOW TO .env FILE")
        print("=" * 80)
        print(f'PASSPHRASE="{passphrase}"')
        print()
        print(f'PRIVATE_KEY="{private_key}"')
        print("=" * 80)
        print("COPY PASSPHRASE & PRIVATE KEY ABOVE TO .env FILE")
        print("=" * 80)
        print()
        print("=" * 80)
        print("COPY PUBLIC KEY BELOW AND UPLOAD TO WHATSAPP")
        print("=" * 80)
        print(public_key)
        print("=" * 80)
        print("COPY PUBLIC KEY ABOVE AND UPLOAD TO WHATSAPP")
        print("=" * 80)
        
    except Exception as error:
        print(f"❌ Error while creating key pair: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
