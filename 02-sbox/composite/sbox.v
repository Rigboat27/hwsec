`timescale 1ns / 1ps

// AES S-box, composite-field version: GF(2^8) inverse followed by the
// affine map (A_mult, then XOR with 0x63).
module sbox(input[7:0] sboxIn,output[7:0] sboxOut);
wire[7:0] inverterOut,Aout;

inverter invMod(sboxIn,inverterOut);

A_mult Amod(inverterOut,Aout);

assign sboxOut[7]=Aout[7];
assign sboxOut[6]=Aout[6]^1'b1;
assign sboxOut[5]=Aout[5]^1'b1;
assign sboxOut[4]=Aout[4];
assign sboxOut[3]=Aout[3];
assign sboxOut[2]=Aout[2];
assign sboxOut[1]=Aout[1]^1'b1;
assign sboxOut[0]=Aout[0]^1'b1;

endmodule
