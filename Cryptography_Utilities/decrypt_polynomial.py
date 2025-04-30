from Cryptography_Utilities.decrypt import decrypt
from Cryptography_Utilities.decode import decode

def decrypt_polynomial(encrypted_string, key):
    decrypted = decrypt(encrypted_string, bin(key)[2:])
    decoded = decode(decrypted)
    return [int(x) for x in decoded.strip().split()]
