from Cryptography_Utilities.encode import encode
from Cryptography_Utilities.encrypt import encrypt

def encrypt_polynomial(polynomial, key):
    as_string = ' '.join(str(c) for c in polynomial)
    encoded = encode(as_string)
    encrypted = encrypt(encoded, bin(key)[2:])
    return encrypted
