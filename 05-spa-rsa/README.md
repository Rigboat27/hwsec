# Simple power analysis on RSA

`rsa.py` is left-to-right square-and-multiply. It always squares, but it multiplies only when the current exponent bit is 1. Since the private exponent `d` is what drives the loop, the sequence of operations *is* the key. On a power trace a multiply looks different from a square, so a single decryption spells out `d` as a pattern of S and SM.

The usual countermeasures remove the data-dependent branch. Square-and-multiply-always does a (dummy) multiply on every bit. The Montgomery ladder does one square and one multiply per bit and uses the bit only to decide which register gets which result.
