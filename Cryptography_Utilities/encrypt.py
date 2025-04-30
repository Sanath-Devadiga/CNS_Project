from app.colors import bcolors

def encrypt(binary_string, key):
    key = (key * ((len(binary_string) // len(key)) + 1))[:len(binary_string)]
    encrypted = ''.join(str(int(b)^int(k)) for b, k in zip(binary_string, key))
    print(f"{bcolors.OKGREEN}Encrypted: {encrypted}{bcolors.ENDC}")
    return encrypted
