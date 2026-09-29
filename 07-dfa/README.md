# Differential fault analysis

Flip a random byte of the AES state at the start of round 8 and compare the faulty ciphertext with the correct one.

```
round 8  SB SR MC   one byte  ->  one full column
round 9  SB SR      one full column  ->  one byte in each column
         MC         each column: (a·f, b·f, c·f, d·f), (a,b,c,d) a column of the MixColumns matrix
round 10 SB SR ARK  ciphertext
```

For each column, guess the 4 last-round-key bytes that sit over it in the ciphertext, undo the last round for both ciphertexts, and keep the guesses whose difference has that shape for some f. Roughly 2⁸ guesses survive per pair, and a second pair cuts that down to one.

- `aes.py` is the reference AES from the course, and `dfa.ipynb` is the lab notebook. Part 1 simulates the fault and Part 2 recovers the 4 key bytes of column 0 (the tutorial code is by Sayandeep Saha).
- `dfa.py` goes further. It handles all four columns, supports any fault position, and inverts the key schedule to get the master key.

```
$ python dfa.py --trials 5
5/5 keys recovered from two faulty ciphertexts each

$ python dfa.py --test          # the notebook's test data, fault position unknown
fault at byte  0  ->  K10 = 9fb53e1f5c88f7a5bc472279312bb577
                     key = 1e1d1c1b1a191817161514131211100f
...
```

Faults at bytes 0, 5, 10 and 15 all give the same answer. ShiftRows puts those four bytes in the same column, so the fault spreads identically.

Each run takes well under a second. The whole attack needs two faulty encryptions and one clock glitch or voltage dip that corrupts a single byte, which is why real hardware checks its own computation (duplicate and compare, or parity on the state) before releasing a ciphertext.
