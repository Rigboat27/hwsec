# rsa_hint.py

import math

# the exponent is the secret information.

def modexp(base, exponent, modulus):

    result = 1

    bits = bin(exponent)[2:]

    for bit in bits:

        # Always executed
        result = (result * result) % modulus

        # Executed only for secret bit = 1
        if bit == "1":

            result = (result * base) % modulus

    return result


def rsa_decrypt(ciphertext, d, n):

    return modexp(
        ciphertext,
        d,
        n
    )


# Example parameters
n = 3233
d = 2753

ciphertext = 855

plaintext = rsa_decrypt(
    ciphertext,
    d,
    n
)

print("Plaintext =", plaintext)