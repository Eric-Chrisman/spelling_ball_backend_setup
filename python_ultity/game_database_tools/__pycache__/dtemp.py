from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import sys

def decrypt_file(input_file, output_file, key):
    with open(input_file, "rb") as f:
        data = f.read()

    nonce = data[:12]
    ciphertext = data[12:]

    aesgcm = AESGCM(key)
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)

    with open(output_file, "wb") as f:
        f.write(plaintext)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python aes_decrypt.py <input_file> <output_file> <key_hex>")
        sys.exit(1)
    
    key = bytes.fromhex(sys.argv[3])
    decrypt_file(sys.argv[1], sys.argv[2], key)