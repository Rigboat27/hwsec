`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 09.02.2020 19:33:04
// Design Name: 
// Module Name: transform
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module transform(input [7:0] in, output [7:0] out);

assign out[7]=(in[7]&1)^(in[5] &1);
assign out[6]=(in[7]&1)^(in[5] &1)^(in[3]&1)^(in[2]&1);
assign out[5]=(in[7]&1)^(in[6] &1)^(in[4]&1)^(in[1]&1);
assign out[4]=(in[6]&1)^(in[5]&1)^(in[4]&1);
assign out[3]=(in[7]&1)^(in[6]&1)^(in[2]&1)^(in[1]&1);
assign out[2]=(in[6]&1)^(in[4]&1)^(in[1]&1);
assign out[1]=(in[3]&1)^(in[1]&1);
assign out[0]=(in[7]&1)^(in[6]&1)^(in[4]&1)^(in[3]&1)^(in[2]&1)^(in[0]&1);



endmodule
