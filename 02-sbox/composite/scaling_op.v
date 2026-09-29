`timescale 1ns / 1ps

// Multiplication by the constant lambda of the tower-field polynomial.
module scaling_op(input[3:0] in,output[3:0] out);

assign out[3]=in[0];
assign out[2]=in[3];
assign out[1]=in[2];
assign out[0]=in[0]^in[1];
endmodule
