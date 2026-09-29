`timescale 1ns / 1ps

// Squaring in GF(2^4). Linear, so it is just a few XORs.
module squarer(input [3:0] in, output [3:0] out);

assign out[3]=(in[3]&1);
assign out[2]=(in[3]&1)^(in[1]&1);
assign out[1]=(in[2]&1);
assign out[0]=(in[2]&1)^(in[0]&1);

endmodule
