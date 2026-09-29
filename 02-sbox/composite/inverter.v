`timescale 1ns / 1ps

// Inverse in GF(2^8), done in GF((2^4)^2) instead of with a 256-entry table.
// Map into the tower field, split into a high/low nibble pair, invert with
// 4-bit arithmetic, map back.
module inverter(input[7:0] inverterIn,output[7:0] inverterOut);
wire[7:0] Tout;
wire[3:0]sqrOut,sc_out,xorOut1,mulOut1,xorOut2,invOut,mulOut2,mulOut3;

transform T(inverterIn,Tout);
squarer sq(Tout[7:4],sqrOut);
scaling_op sc_op(sqrOut,sc_out);
xor_mod xor1(Tout[3:0],Tout[7:4],xorOut1);
mult_4 mul1(Tout[3:0],xorOut1,mulOut1);
xor_mod xor2(sc_out,mulOut1,xorOut2);
inverse inv(xorOut2,invOut);
mult_4 mul2(invOut,Tout[7:4],mulOut2);
mult_4 mul3(invOut,xorOut1,mulOut3);
inverse_transform invT({mulOut2,mulOut3},inverterOut);

endmodule
