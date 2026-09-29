"""
Correlation power analysis on the first-round S-box output of AES-128.

Leakage model: the power drawn when the device writes SubBytes(pt ^ k) is
roughly linear in the Hamming weight of that byte. For each key byte we try
all 256 guesses, predict the Hamming weight for every trace, and correlate
the prediction against every sample of the measured traces. The right guess
lines up with the real leakage at the moment the S-box output is computed
and gives a clear correlation peak; the wrong guesses don't.

    python cpa.py                 # recover the key, check it, save plots
    python cpa.py --no-plots
"""

import argparse
import os
import pickle
import warnings
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))

SBOX = np.array([
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16,
], dtype=np.uint8)

HW = np.array([bin(n).count("1") for n in range(256)], dtype=np.float64)


def load(path):
    warnings.filterwarnings("ignore", category=DeprecationWarning)  # pickle from an older numpy
    with open(path, "rb") as f:
        data = pickle.load(f)
    traces = np.asarray(data["trace_array"], dtype=np.float64)
    pts = np.asarray(data["textin_array"], dtype=np.uint8)
    cts = np.asarray(data["textout_array"], dtype=np.uint8)
    return traces, pts, cts


def correlate(traces, pt_byte):
    """Pearson correlation of every key guess against every sample.

    traces: (N, T), pt_byte: (N,)  ->  (256, T)
    """
    guesses = np.arange(256, dtype=np.uint8)
    hyp = HW[SBOX[pt_byte[None, :] ^ guesses[:, None]]]          # (256, N)
    hyp = hyp - hyp.mean(axis=1, keepdims=True)
    t = traces - traces.mean(axis=0)
    num = hyp @ t                                                 # (256, T)
    den = np.sqrt((hyp ** 2).sum(axis=1))[:, None] * np.sqrt((t ** 2).sum(axis=0))[None, :]
    with np.errstate(invalid="ignore", divide="ignore"):
        r = num / den
    return np.nan_to_num(r)


def attack(traces, pts):
    key, peaks, margins, corr_maps = [], [], [], []
    for b in range(16):
        r = np.abs(correlate(traces, pts[:, b]))
        best_per_guess = r.max(axis=1)
        order = np.argsort(best_per_guess)[::-1]
        key.append(int(order[0]))
        peaks.append(best_per_guess[order[0]])
        margins.append(best_per_guess[order[0]] - best_per_guess[order[1]])
        corr_maps.append(r)
    return key, peaks, margins, corr_maps


def traces_needed(traces, pts, key, steps):
    """Rank of the correct key byte (0 = top) as the trace count grows."""
    ranks = np.zeros((16, len(steps)), dtype=int)
    for i, n in enumerate(steps):
        for b in range(16):
            score = np.abs(correlate(traces[:n], pts[:n, b])).max(axis=1)
            ranks[b, i] = int((score > score[key[b]]).sum())
    return ranks


def aes_check(key, pt, ct):
    """Encrypt one plaintext with the recovered key and compare."""
    sys.path.insert(0, os.path.join(HERE, "..", "07-dfa"))
    from aes import AES
    c = AES(key)
    c.KeyExpansion()
    return list(c.encrypt(pt=list(int(x) for x in pt))) == [int(x) for x in ct]


def plots(traces, pts, key, corr_maps, steps, ranks, outdir):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})

    # 1. correlation over time for byte 0: every wrong guess in grey, the
    #    right one on top.
    r = corr_maps[0]
    fig, ax = plt.subplots(figsize=(9, 3.2))
    for g in range(256):
        if g != key[0]:
            ax.plot(r[g], color="#c8c8c8", lw=0.4)
    ax.plot(r[key[0]], color="#c0392b", lw=1.0, label=f"correct guess 0x{key[0]:02x}")
    ax.set_xlabel("sample")
    ax.set_ylabel("|correlation|")
    ax.set_title("Key byte 0: correlation vs. time, all 256 guesses")
    ax.legend(frameon=False, loc="upper right")
    fig.tight_layout()
    fig.savefig(os.path.join(outdir, "cpa_byte0_vs_time.png"), dpi=150)
    plt.close(fig)

    # 2. peak correlation per guess for byte 0
    fig, ax = plt.subplots(figsize=(9, 2.8))
    peak = r.max(axis=1)
    colors = ["#c0392b" if g == key[0] else "#7f8c8d" for g in range(256)]
    ax.bar(range(256), peak, color=colors, width=1.0)
    ax.set_xlim(-1, 256)
    ax.set_xlabel("key guess")
    ax.set_ylabel("max |correlation|")
    ax.set_title("Key byte 0: peak correlation for each guess")
    fig.tight_layout()
    fig.savefig(os.path.join(outdir, "cpa_byte0_guesses.png"), dpi=150)
    plt.close(fig)

    # 3. how many traces it takes
    fig, ax = plt.subplots(figsize=(9, 3.2))
    for b in range(16):
        ax.plot(steps, ranks[b], color="#34495e", alpha=0.35, lw=1)
    ax.plot(steps, ranks.mean(axis=0), color="#c0392b", lw=2, label="mean over 16 bytes")
    ax.set_xlabel("number of traces")
    ax.set_ylabel("rank of correct byte")
    ax.set_yscale("symlog", linthresh=1)
    ax.set_title("How fast the key falls out")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(os.path.join(outdir, "cpa_rank_vs_traces.png"), dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--traces", default=os.path.join(HERE, "real-traces.pkl"))
    ap.add_argument("--no-plots", action="store_true")
    args = ap.parse_args()

    traces, pts, cts = load(args.traces)
    print(f"{traces.shape[0]} traces x {traces.shape[1]} samples")

    key, peaks, margins, corr_maps = attack(traces, pts)
    print("byte  guess  peak |r|  lead over 2nd")
    for b in range(16):
        print(f"{b:4d}   0x{key[b]:02x}    {peaks[b]:.3f}     {margins[b]:.3f}")
    print("key:", bytes(key).hex())

    ok = aes_check(key, pts[0], cts[0])
    print("AES(pt[0], key) == ct[0]:", ok)

    n = traces.shape[0]
    steps = list(range(5, n + 1, 1))
    ranks = traces_needed(traces, pts, key, steps)
    first_all = next((s for i, s in enumerate(steps) if np.all(ranks[:, i:] == 0)), None)
    print("traces needed for every byte to stay at rank 0:", first_all)

    if not args.no_plots:
        plots(traces, pts, key, corr_maps, steps, ranks, HERE)
        print("plots written to", HERE)
