`timescale 1ns / 1ps

module AES_TB;

	// Inputs
	reg clk,reset;
    reg [127:0] datain;
    reg [127:0] key;
	// Outputs
    wire [127:0] dataout;
    wire done;
	// Instantiate the Unit Under Test (tb)
	aescipher tb(.clk(clk),.reset(reset),.datain(datain),.key(key),.dataout(dataout),.done(done));
    
    
	initial begin
	    $dumpfile("wave.vcd");
	    $dumpvars(0, AES_TB);
	end

    initial 
        begin
            clk<=1'b0;
        end
	initial begin
		// Initialize Inputs
		   datain<=128'hbfdd0c7cb42a5cc3556c0f6d8a846265;
		   key<= 128'h3b8285629eb97c8e4f026087bb7cd55e;
		   reset=1'b1;		   
		   //$dumpoff;
           #30 reset=1'b0;


	end 
	always
    #10 clk=~clk;
endmodule

