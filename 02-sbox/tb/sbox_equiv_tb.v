`timescale 1ns / 1ps

// Runs all 256 inputs through both S-boxes and counts disagreements.
module sbox_equiv_tb;
    reg  [7:0] x;
    wire [7:0] y_table, y_composite;
    integer i, bad;

    aes_sbox table_sbox(.in(x), .out(y_table));
    sbox     comp_sbox(.sboxIn(x), .sboxOut(y_composite));

    initial begin
        bad = 0;
        for (i = 0; i < 256; i = i + 1) begin
            x = i;
            #1;
            if (y_table !== y_composite) begin
                $display("mismatch at %02h: table %02h, composite %02h", x, y_table, y_composite);
                bad = bad + 1;
            end
        end
        if (bad == 0) $display("PASS: table and composite S-boxes agree on all 256 inputs");
        else          $display("FAIL: %0d mismatches", bad);
        $finish;
    end
endmodule
