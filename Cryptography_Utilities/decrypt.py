from app.colors import bcolors

def decrypt(binary_string, key):
    key = (key * ((len(binary_string) // len(key)) + 1))[:len(binary_string)]
    decrypted = ''.join(str(int(b)^int(k)) for b, k in zip(binary_string, key))
    print(f"{bcolors.OKGREEN}Decrypted: {decrypted}{bcolors.ENDC}")
    return decrypted
