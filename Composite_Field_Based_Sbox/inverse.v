`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 10.02.2020 01:20:49
// Design Name: 
// Module Name: inverse
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


module inverse(input [3:0]a,output reg  [3:0]c);

always @(a)
case (a)
   4'h00: c=4'h0;
   4'h01: c=4'h1;
   4'h02: c=4'h9;
   4'h03: c=4'he;
   4'h04: c=4'hd;
   4'h05: c=4'hb;
   4'h06: c=4'h7;
   4'h07: c=4'h6;
   4'h08: c=4'hf;
   4'h09: c=4'h2;
   4'h0a: c=4'hc;
   4'h0b: c=4'h5;
   4'h0c: c=4'ha;
   4'h0d: c=4'h4;
   4'h0e: c=4'h3;
   4'h0f: c=4'h8;
endcase

endmodule
