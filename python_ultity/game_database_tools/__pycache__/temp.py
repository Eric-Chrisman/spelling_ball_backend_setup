from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
import sys

def encrypt_file(input_file, output_file, key):
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)

    with open(input_file, "rb") as f:
        plaintext = f.read()

    cipertext = aesgcm.encrypt(nonce, plaintext, None)

    with open(output_file, "wb") as f:
        f.write(nonce + cipertext)
    
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python aes_encrypt.py <input_file> < output_file>")
        sys.exit(1)
    
    key = AESGCM.generate_key(bit_length=256)
    print("Encryption key (save this!):", key.hex())

    encrypt_file(sys.argv[1], sys.argv[2], key)