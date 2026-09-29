"""
Recover the password from timing_oracle() one character at a time.

The oracle compares the guess against the stored password and bails out at
the first mismatch. The "timing" it returns is how far it got before
bailing, which is exactly what a real early-exit strcmp leaks through
execution time. So:

  * a guess whose first k characters are right runs for at least k steps,
  * and the one right character at position k makes it run longer than k.

That turns a |charset|^L brute force into at most |charset| * L queries.

    python attack.py                # uses password.txt, creates a demo one if missing
"""

import os
import string
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)  # the oracle opens password.txt relative to cwd

from timing_oracle import timing_oracle

CHARSET = string.ascii_letters + string.digits + string.punctuation


def recover(oracle=timing_oracle, charset=CHARSET, max_len=64):
    known = ""
    queries = 0
    while len(known) < max_len:
        k = len(known)
        for c in charset:
            ok, t = oracle(known + c)
            queries += 1
            if ok:
                return known + c, queries
            if t > k:          # got past position k, so c is right
                known += c
                break
        else:
            raise RuntimeError(f"no character in the charset fits position {k}")
    raise RuntimeError("gave up: password longer than max_len")


if __name__ == "__main__":
    if not os.path.exists("password.txt"):
        with open("password.txt", "w") as f:
            f.write("tru5t_L4b!")
        print("no password.txt found, wrote a demo one")

    with open("password.txt") as f:
        secret_len = len(f.readline())

    pw, q = recover()
    brute = len(CHARSET) ** secret_len
    print(f"password : {pw}")
    print(f"queries  : {q}")
    print(f"brute    : {len(CHARSET)}^{secret_len} = {brute:.2e} guesses in the worst case")
    sys.exit(0 if timing_oracle(pw)[0] else 1)
