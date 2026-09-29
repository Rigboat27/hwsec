`timescale 1ns / 1ps

// Inverse in GF(2^4). Only 16 entries, so a small table is fine here.
module inverse(input [3:0]a,output reg  [3:0]c);

always @(a)
case (a)
   4'h0: c=4'h0;
   4'h1: c=4'h1;
   4'h2: c=4'h9;
   4'h3: c=4'he;
   4'h4: c=4'hd;
   4'h5: c=4'hb;
   4'h6: c=4'h7;
   4'h7: c=4'h6;
   4'h8: c=4'hf;
   4'h9: c=4'h2;
   4'ha: c=4'hc;
   4'hb: c=4'h5;
   4'hc: c=4'ha;
   4'hd: c=4'h4;
   4'he: c=4'h3;
   4'hf: c=4'h8;
endcase

endmodule
