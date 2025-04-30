import random
from app.colors import bcolors

_l = 127
_h = 128

def set_key_range(l, h):
    global _l, _h
    _l = l
    _h = h

def generate_polynomial(keys):
    polynomial = [1]  # Start with 1

    for key in keys:
        temp = polynomial.copy()
        polynomial.insert(0, 0)
        for i in range(len(temp)):
            temp[i] *= key
        for i in range(len(temp)):
            polynomial[i] -= temp[i]

    group_key = random.randint(2**_l, 2**_h)
    print(f"{bcolors.BOLD}{bcolors.OKGREEN}Group key: {group_key}{bcolors.ENDC}")
    polynomial[0] += group_key
    return polynomial

def gen_intergroup_polynomial(degree):
    return [random.randint(2**_l, 2**_h) for _ in range(degree + 1)]
