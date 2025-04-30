from app.colors import bcolors

def decode(binary):
    decoded = ''.join(chr(int(binary[i:i+7], 2)) for i in range(0, len(binary), 7))
    print(f"{bcolors.OKGREEN}Decoded: {decoded}{bcolors.ENDC}")
    return decoded
