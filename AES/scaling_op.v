`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 10.02.2020 01:40:07
// Design Name: 
// Module Name: scaling_op
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


module scaling_op(input[3:0] in,output[3:0] out);

assign out[3]=in[0];
assign out[2]=in[3];
assign out[1]=in[2];
assign out[0]=in[0]^in[1];
endmodule
