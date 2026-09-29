`timescale 1ns / 1ps

module dff(input clk,input rst,input[4:0] in,output reg[4:0] out);
always@(posedge clk)
    begin
        if(rst)
            out<=5'd0;
        else
            out<=in;
    end
endmodule
