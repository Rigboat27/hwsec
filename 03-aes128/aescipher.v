`timescale 1ns / 1ps

module aescipher(clk,datain,key,dataout,reset,done);
    input clk,reset;
    input [127:0] datain;
    input [127:0] key;
    output[127:0] dataout;
    output done;
    reg [3:0] round;
    reg [127:0] rin,lst_round_data,lst_round_key,key_in;
    wire [127:0] rout,keyout;
	reg done;
	always @(posedge clk)
	   begin
           if(reset)
            begin
               round<=4'd0;
            end
           else if(done==1'b0)
               round<=round+1;
           else 
               round<=round;
       end
	
	always @(posedge clk)
	   begin
	       if(reset)
	           begin
	               rin<=datain^key;
	               key_in<=key;
	               done<=1'b0;
	           end
	       else if(round==4'd8)
	           begin
                   rin<=rout;
                   key_in<=keyout;
	               done<=1'b1;
	           end
	       else if(round==4'd9)
	           begin
                   rin<=rin;
                   key_in<=key_in;
	               done<=1'b1;
	           end
	       else
	           begin
	               rin<=rout;
	               key_in<=keyout;
	           end
	   end   
	 
    rounds r(.rc(round),.data(rin),.keyin(key_in),.keyout(keyout),.rndout(rout));
    rounndlast lstRound(.rc(round),.rin(rin),.keylastin(key_in),.fout(dataout));
    
endmodule
