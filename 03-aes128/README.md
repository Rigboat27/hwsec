# AES-128 core

An iterative encryption core. On reset it loads `plaintext ⊕ key`. After that, each clock runs one full round (SubBytes, ShiftRows, MixColumns, AddRoundKey) and derives the next round key on the fly. After round 9 the final round (no MixColumns) is combinational on the output and `done` goes high.

| File | |
|---|---|
| `aescipher.v` | top level: round counter, state and key registers |
| `rounds.v`, `rounndlast.v` | a normal round and the final round |
| `subbytes.v`, `shiftrow.v`, `mixcolumn.v` | the round steps; S-boxes come from `../02-sbox/composite` |
| `KeyGeneration.v` | one step of the key schedule, with RotWord, SubWord and Rcon |
| `AES_TB.v` | encrypts one block and compares with the Python reference |

`mixcolumn.v` was left half-done in the course template. Each output bit of `02·a ⊕ 03·b ⊕ c ⊕ d` expands into plain XORs once you write out `xtime`:

```
xtime(a) = {a6, a5, a4, a3^a7, a2^a7, a1, a0^a7, a7}
```

```
make sim-aes      # from the repo root
```

prints `ciphertext 12786e6e08af735b5504a0a5c7ca950e` and `PASS`.

Synthesis (`synth_aes.ys`) gives 7,678 Nangate cells, about 11,000 µm², with 261 flip-flops (128 state, 128 key, round counter, done). Most of the rest is XOR/XNOR. `rounds` and `rounndlast` each instantiate their own SubBytes and key schedule, so there are 40 S-boxes where 20 would do. That's the first thing I'd fix.
