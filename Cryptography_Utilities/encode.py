from app.colors import bcolors

def encode(s):
    encoded = ''.join(format(ord(c), '07b') for c in s)
    print(f"{bcolors.OKGREEN}Encoded: {encoded}{bcolors.ENDC}")
    return encoded
