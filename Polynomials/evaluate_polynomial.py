def evaluate_polynomial(polynomial, secret_key):
    x = 1
    result = 0
    for coef in polynomial:
        result += x * coef
        x *= secret_key
    return result
