`timescale 1ns / 1ps

// General multiplier in GF(2^4).
module mult_4(input[3:0] in1,input[3:0] in2,output[3:0] out);
assign out[3]=(in1[3]&in2[0])^(in1[2]&in2[1])^(in1[1]&in2[2])^(in1[0]&in2[3])^(in1[3]&in2[3]);
assign out[2]=(in1[2]&in2[0])^(in1[1]&in2[1])^(in1[0]&in2[2])^(in1[3]&in2[3])^(in1[3]&in2[2])^(in1[2]&in2[3]);
assign out[1]=(in1[1]&in2[0])^(in1[0]&in2[1])^(in1[3]&in2[2])^(in1[2]&in2[3])^(in1[3]&in2[1])^(in1[2]&in2[2])^(in1[1]&in2[3]);
assign out[0]=(in1[0]&in2[0])^(in1[3]&in2[1])^(in1[2]&in2[2])^(in1[1]&in2[3]);
endmodule
