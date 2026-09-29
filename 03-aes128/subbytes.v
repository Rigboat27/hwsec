`timescale 1ns / 1ps

module subbytes(data,sb);

input [127:0] data;
output [127:0] sb;

     sbox q0( .sboxIn(data[127:120]),.sboxOut(sb[127:120]) );
     sbox q1( .sboxIn(data[119:112]),.sboxOut(sb[119:112]) );
     sbox q2( .sboxIn(data[111:104]),.sboxOut(sb[111:104]) );
     sbox q3( .sboxIn(data[103:96]),.sboxOut(sb[103:96]) );
     
     sbox q4( .sboxIn(data[95:88]),.sboxOut(sb[95:88]) );
     sbox q5( .sboxIn(data[87:80]),.sboxOut(sb[87:80]) );
     sbox q6( .sboxIn(data[79:72]),.sboxOut(sb[79:72]) );
     sbox q7( .sboxIn(data[71:64]),.sboxOut(sb[71:64]) );
     
     sbox q8( .sboxIn(data[63:56]),.sboxOut(sb[63:56]) );
     sbox q9( .sboxIn(data[55:48]),.sboxOut(sb[55:48]) );
     sbox q10(.sboxIn(data[47:40]),.sboxOut(sb[47:40]) );
     sbox q11(.sboxIn(data[39:32]),.sboxOut(sb[39:32]) );
     
     sbox q12(.sboxIn(data[31:24]),.sboxOut(sb[31:24]) );
     sbox q13(.sboxIn(data[23:16]),.sboxOut(sb[23:16]) );
     sbox q14(.sboxIn(data[15:8]),.sboxOut(sb[15:8]) );
     sbox q16(.sboxIn(data[7:0]),.sboxOut(sb[7:0]) );
	  
endmodule
