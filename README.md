# hwsec

Work from the Summer School 2026 on hardware security at the Trust Lab at IIT Bombay

The school had two halves, and this repo follows them. In the first half I built AES in hardware: gate-level warm-up, then the S-box two different ways, then a full AES-128 core, with synthesis numbers for each. In the second half the same cipher got attacked through timing, power and faults. Seeing both sides changed how I read RTL. A design that is correct in simulation can still hand over its key to someone with an oscilloscope.

## What's here

| Folder | What it is | Result |
|---|---|---|
| [`01-accumulator`](01-accumulator) | 4-bit accumulator from hand-built half/full adders and a register | 29 cells, 48.4 µm² on Nangate 45nm |
| [`02-sbox`](02-sbox) | AES S-box as a 256-entry table vs. composite field GF((2⁴)²) | 47% less area in standard cells, identical on 6-input LUTs |
| [`03-aes128`](03-aes128) | Iterative AES-128 core, one round per clock, key schedule on the fly | Matches the software reference; ~11,000 µm² |
| [`04-timing-attack`](04-timing-attack) | Password check that exits early on the first wrong character | 10-char password in 386 queries instead of 94¹⁰ |
| [`05-spa-rsa`](05-spa-rsa) | Square-and-multiply RSA and why one power trace leaks the exponent | Lab setup |
| [`06-cpa`](06-cpa) | Correlation power analysis on 50 real AES power traces | Full 128-bit key, stable after 35 traces |
| [`07-dfa`](07-dfa) | Differential fault analysis with a single byte fault in round 8 | Full key from 2 faulty ciphertexts |

## Building it

### S-box: table vs. composite field

The S-box is the only non-linear part of AES, and it's where most of the area goes. The obvious way to build it is a lookup table. The other way is to compute the GF(2⁸) inverse directly, mapping the byte into the tower field GF((2⁴)²) so that the inverse breaks down into a few 4-bit multiplies, squarings and a 16-entry inverse. I checked both against each other on all 256 inputs, then synthesized each one five ways with Yosys:

| Target | Table | Composite |
|---|---|---|
| ROM kept as memory | 2048 bits | 64 bits (just the GF(2⁴) inverse) |
| Generic gates | 634 | 177 |
| 4-input LUTs | 270 | 73 |
| Nangate 45nm | 442.1 µm² | **235.1 µm²** |
| Xilinx 7-series, flattened | 32 LUT6 + 16 MUXF7 + 8 MUXF8 | exactly the same |

The last row surprised me. On a 7-series FPGA the S-box is just an 8-input Boolean function, and once the composite design is flattened the tools map it to the same netlist as the table. All the algebra buys nothing there. Keep the hierarchy and the composite version actually gets worse (87 LUTs). The tower-field trick pays off on ASICs and small-LUT fabrics, not on 6-LUT FPGAs.

### AES-128 core

The core in `03-aes128` runs one round per clock and computes each round key on the fly. It uses the composite S-box. The final round has its own copy of the round logic, so there are 40 S-box instances in all (16 + 4 for the key schedule, twice). Sharing them between the two is the obvious next area win. The course version left MixColumns unfinished. With it filled in, the testbench now checks the output against the Python reference instead of dumping a waveform, and it passes. Synthesized to Nangate 45nm, it comes to 7,678 cells and about 11,000 µm², 261 of which are flip-flops.

## Breaking it

- **Timing.** A string compare that stops at the first mismatch runs longer the more of your guess is right. Guess one character at a time and keep the one that runs longest, and the search goes from exponential to linear.
- **Simple power analysis.** In left-to-right square-and-multiply, the multiply only happens on 1 bits. One trace of one decryption shows the whole private exponent.
- **Correlation power analysis.** Predict the Hamming weight of the first-round S-box output under all 256 guesses for a key byte and correlate each prediction with the measured traces. The right guess peaks at |r| ≈ 0.89 at the moment the S-box output is computed, 0.18 to 0.31 clear of the best wrong guess on every byte. With 50 traces all 16 bytes come out, and the key encrypts the captured plaintext to the captured ciphertext.

  ![correlation for key byte 0](06-cpa/cpa_byte0_vs_time.png)

- **Fault analysis.** A single random byte fault at the start of round 8 spreads to exactly one byte per column by the time it reaches round 9's MixColumns. That leaves a fixed (2f, f, f, 3f)-style pattern the last round key has to satisfy. The lab version recovers 4 key bytes. I extended it to all four columns and then ran the key schedule backwards, so two faulty ciphertexts give the master key. On the course's test data it gives `1e1d1c1b1a191817161514131211100f`.

## Running things

```
make sim       # accumulator, S-box equivalence, AES core (iverilog)
make synth     # all the Yosys runs above
make attacks   # timing, CPA, DFA (python3 with numpy + matplotlib)
```

The committed synthesis reports in `02-sbox/reports` came from Yosys 0.66. An older Yosys (0.33) gives slightly different absolute areas (267.6 vs. 471.1 µm²), but the ratio stays the same.

## Notes

- The lab code in this repo was rewritten after the summer
- Several files started as course scaffolding: the Verilog templates, the lab notebooks, and the round-8 DFA tutorial by Proff. Sayandeep Saha. The CPA traces are the ones handed out in the lab.
- `libs/` has the Nangate 45nm Open Cell Library used for all the area numbers.
