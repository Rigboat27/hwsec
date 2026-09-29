`timescale 1ns / 1ps

module half_addr(input in1,input in2,output out,output cout);
xor g1(out,in1,in2);
and g2(cout,in1,in2);
endmodule
