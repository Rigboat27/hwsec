`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 10.02.2020 05:16:37
// Design Name: 
// Module Name: inverter
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
