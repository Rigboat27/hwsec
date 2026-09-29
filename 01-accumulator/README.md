# Accumulator

The first exercise. It's a 4-bit input added into a 5-bit running total every clock. Nothing in it is behavioural: the adder is a ripple-carry chain of `half_addr`/`full_addr` modules built from primitive gates, feeding a 5-bit register with synchronous reset. (`adder.v` is the one-line `+` version, kept for comparison.)

```
iverilog -o acc test.v accumulator.v adder_struct.v dff.v half_addr.v full_addr.v && vvp acc
yosys -s synth_accumulator.ys
```

Mapped to Nangate 45nm it comes to 29 cells, 5 of them flip-flops, for 48.4 µm². Tiny, but it was the first time I followed a design all the way from RTL to a cell count.
