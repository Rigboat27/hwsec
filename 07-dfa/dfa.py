"""
Differential fault analysis of AES-128 with a single-byte fault at the input
of round 8.

The course notebook recovers 4 bytes of the last round key. This script
does all four columns, so two faulty/correct ciphertext pairs are enough to
pin down the whole 10th round key, and from there the master key by running
the key schedule backwards.

How the fault spreads (fault injected before SubBytes of round 8):

    round 8   SB, SR, MC  -> one full column of the state is corrupted
    round 9   SB, SR      -> each column now has exactly one corrupted byte
              MC          -> each column's difference is (a*f, b*f, c*f, d*f)
                             where (a, b, c, d) is a column of the MixColumns
                             matrix and f is an unknown non-zero byte
    round 10  SB, SR, ARK -> ciphertext

So for each round-9 column we guess the four last-round-key bytes that sit
over it in the ciphertext, peel off the last round, and keep the guesses
whose differences have that (a*f, b*f, c*f, d*f) shape for some f. About
2^8 guesses survive per pair; intersecting two pairs usually leaves one.

Run it:
    python dfa.py            # simulated faults on a random key, checks itself
    python dfa.py --test     # the "different key" test data from the notebook
"""

import argparse
import random
import sys
from itertools import product

from aes import AES, intarraytohexstring


cipher_ref = AES()
SBOX = cipher_ref.sbox
INV_SBOX = cipher_ref.sbox_inv
RCON = cipher_ref.Rcon


def xtime(x):
    return ((x << 1) & 0xff) ^ (0x1b if x & 0x80 else 0)


def gmul(x, c):
    return {1: x, 2: xtime(x), 3: xtime(x) ^ x}[c]


# MixColumns matrix. A single corrupted byte in row r of a column comes out
# of MixColumns multiplied by column r of this matrix.
MC = [[2, 3, 1, 1],
      [1, 2, 3, 1],
      [1, 1, 2, 3],
      [3, 1, 1, 2]]


def column_patterns(fault_byte):
    """For each round-9 column c, return [(ciphertext index, coefficient)] x4.

    fault_byte uses the same indexing as aes.py: index = 4*col + row.
    """
    r0, c0 = fault_byte % 4, fault_byte // 4
    c1 = (c0 - r0) % 4                    # column hit by round-8 MixColumns
    patterns = []
    for c in range(4):
        r_fault = (c1 - c) % 4            # the one bad row in round-9 column c
        coefs = [MC[row][r_fault] for row in range(4)]
        # round-10 ShiftRows moves (row, c) to (row, c - row)
        positions = [4 * ((c - row) % 4) + row for row in range(4)]
        patterns.append(list(zip(positions, coefs)))
    return patterns


def column_candidates(ct, ft, pattern):
    """All 4-byte key guesses for one column consistent with one fault pair."""
    # For every key byte guess, the difference just before round-10 SubBytes.
    diffs = []
    for pos, _ in pattern:
        diffs.append([INV_SBOX[ct[pos] ^ k] ^ INV_SBOX[ft[pos] ^ k] for k in range(256)])

    # Index guesses by the difference they produce so we can look them up.
    by_diff = []
    for d in diffs:
        table = {}
        for k, v in enumerate(d):
            table.setdefault(v, []).append(k)
        by_diff.append(table)

    found = set()
    for f in range(1, 256):
        lists = [by_diff[i].get(gmul(f, coef), []) for i, (_, coef) in enumerate(pattern)]
        if all(lists):
            found.update(product(*lists))
    return found


def recover_last_round_key(pairs, fault_byte=0):
    """pairs: list of (correct_ct, faulty_ct) as 16-int lists.

    Returns (key or None, list of candidate counts per column).
    """
    k10 = [None] * 16
    counts = []
    for pattern in column_patterns(fault_byte):
        survivors = None
        for ct, ft in pairs:
            cands = column_candidates(ct, ft, pattern)
            survivors = cands if survivors is None else survivors & cands
        counts.append(len(survivors))
        if len(survivors) != 1:
            return None, counts
        for (pos, _), k in zip(pattern, next(iter(survivors))):
            k10[pos] = k
    return k10, counts


def invert_key_schedule(k10):
    """Walk the AES-128 key schedule backwards from round key 10 to the key."""
    w = [None] * 44
    for i in range(4):
        w[40 + i] = k10[4 * i:4 * i + 4]
    for i in range(43, 3, -1):
        prev = w[i - 1]
        if i % 4 == 0:
            t = prev[1:] + prev[:1]
            t = [SBOX[b] for b in t]
            t[0] ^= RCON[i // 4]
        else:
            t = prev
        w[i - 4] = [a ^ b for a, b in zip(w[i], t)]
    return [b for word in w[:4] for b in word]


def encrypt_with_fault(cipher, pt, inj_round=8, byte_loc=0, fault=None):
    """Same as cipher.encrypt, but XORs a byte into the state at inj_round."""
    for i in range(4):
        for j in range(4):
            cipher.state[j][i] = pt[i * 4 + j]
    cipher.AddRoundKey(0)
    for rnd in range(1, cipher.Nr):
        if rnd == inj_round:
            f = fault if fault is not None else random.randint(1, 255)
            cipher.state[byte_loc % 4][byte_loc // 4] ^= f
        cipher.SubBytes()
        cipher.ShiftRows()
        cipher.MixColumns()
        cipher.AddRoundKey(rnd)
    cipher.SubBytes()
    cipher.ShiftRows()
    cipher.AddRoundKey(cipher.Nr)
    return [cipher.state[j][i] for i in range(4) for j in range(4)]


def simulate(seed=None, n_pairs=2, byte_loc=0):
    rng = random.Random(seed)
    key = [rng.randrange(256) for _ in range(16)]
    cipher = AES(key)
    cipher.KeyExpansion()

    random.seed(seed)
    pairs = []
    for _ in range(n_pairs):
        pt = [rng.randrange(256) for _ in range(16)]
        correct = list(cipher.encrypt(pt=pt))
        faulty = encrypt_with_fault(cipher, pt, byte_loc=byte_loc)
        pairs.append((correct, faulty))

    k10, counts = recover_last_round_key(pairs, byte_loc)
    print("key            :", intarraytohexstring(key))
    print("true K10       :", intarraytohexstring(cipher.get_lastroundkey()))
    if k10 is None:
        print("no unique key; survivors per column:", counts)
        return False
    master = invert_key_schedule(k10)
    print("recovered K10  :", intarraytohexstring(k10))
    print("recovered key  :", intarraytohexstring(master))
    ok = master == key
    print("match          :", ok)
    return ok


# Test data given at the end of the notebook (a different, unknown key).
TEST_PAIRS = [
    ([4, 119, 58, 121, 224, 234, 189, 82, 89, 94, 133, 164, 41, 175, 134, 125],
     [6, 186, 203, 88, 173, 164, 25, 146, 227, 135, 220, 209, 225, 95, 105, 160]),
    ([44, 76, 39, 50, 119, 245, 58, 239, 122, 105, 143, 48, 61, 45, 163, 83],
     [73, 218, 83, 175, 31, 242, 179, 213, 156, 205, 8, 163, 12, 31, 154, 225]),
]


def solve_test_data():
    # The fault position isn't given, so try all 16 and keep the ones that
    # leave exactly one key standing.
    for byte_loc in range(16):
        k10, counts = recover_last_round_key(TEST_PAIRS, byte_loc)
        if k10 is not None:
            print(f"fault at byte {byte_loc:2d}  ->  K10 = {intarraytohexstring(k10)}")
            print(f"                     key = {intarraytohexstring(invert_key_schedule(k10))}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--test", action="store_true", help="solve the notebook's test data")
    ap.add_argument("--trials", type=int, default=1, help="simulated runs with random keys")
    ap.add_argument("--byte", type=int, default=0, help="fault location (0-15)")
    args = ap.parse_args()

    if args.test:
        solve_test_data()
        sys.exit(0)

    wins = 0
    for t in range(args.trials):
        wins += simulate(seed=t, byte_loc=args.byte)
        print()
    print(f"{wins}/{args.trials} keys recovered from two faulty ciphertexts each")
