# AES S-box: table vs. composite field

- `table/aes_sbox.v`: the S-box as a 256-way `case`.
- `composite/`: the S-box computed as GF(2⁸) inverse + affine map, with the inverse done in GF((2⁴)²):

  ```
  x ──transform──▶ (h, l) in GF(2⁴)²
      d = λ·h² ⊕ l·(h ⊕ l)          squarer, scaling_op, mult_4, xor_mod
      d⁻¹                           inverse (16-entry table)
      (h·d⁻¹, (h ⊕ l)·d⁻¹)          mult_4 ×2
  ──inverse_transform──▶ A_mult ──⊕ 0x63──▶ S(x)
  ```

- `tb/sbox_equiv_tb.v` runs all 256 inputs through both and fails on any disagreement (it passes).
- `synth/` holds one Yosys script per (design, target). `reports/` has the logs I got with Yosys 0.66.

| Target | Table | Composite |
|---|---|---|
| ROM kept as memory | 2048 bits | 64 bits |
| Generic gates (`abc -g`) | 634 | 177 |
| 4-input LUTs | 270 | 73 |
| Nangate 45nm | 442.1 µm² | 235.1 µm² |
| Xilinx 7-series, flattened | 32 LUT6, 16 MUXF7, 8 MUXF8 | same |
| Xilinx 7-series, hierarchical | – | 87 LUTs, 24 MUXF7, 12 MUXF8 |

The composite field wins wherever the basic cell is small (standard cells, 4-LUTs). On 6-LUTs it wins nothing: flattened, it's just an 8-input function, and Yosys lands on the same mapping as the table.

The composite version also matters beyond area. Its internals are small linear and non-linear pieces with clear boundaries, and that's what masking schemes against power analysis are built on. A 256-entry ROM gives you nothing to work with.
