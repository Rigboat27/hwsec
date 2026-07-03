`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 10.02.2020 01:11:01
// Design Name: 
// Module Name: squarer
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


module squarer(input [3:0] in, output [3:0] out);

assign out[3]=(in[3]&1);
assign out[2]=(in[3]&1)^(in[1]&1);
assign out[1]=(in[2]&1);
assign out[0]=(in[2]&1)^(in[0]&1);



endmodule