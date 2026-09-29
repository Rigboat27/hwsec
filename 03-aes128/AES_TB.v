`timescale 1ns / 1ps

// Encrypts one block and compares against a software reference
// (07-dfa/aes.py gives the same ciphertext for this key/plaintext).
module AES_TB;

    reg clk, reset;
    reg  [127:0] datain;
    reg  [127:0] key;
    wire [127:0] dataout;
    wire done;

    localparam [127:0] EXPECTED = 128'h12786e6e08af735b5504a0a5c7ca950e;

    aescipher tb(.clk(clk), .reset(reset), .datain(datain), .key(key),
                 .dataout(dataout), .done(done));

    initial begin
        $dumpfile("wave.vcd");
        $dumpvars(0, AES_TB);
    end

    initial clk = 1'b0;
    always #10 clk = ~clk;

    initial begin
        datain = 128'hbfdd0c7cb42a5cc3556c0f6d8a846265;
        key    = 128'h3b8285629eb97c8e4f026087bb7cd55e;
        reset  = 1'b1;
        #30 reset = 1'b0;
    end

    initial begin
        wait (done === 1'b1);
        @(negedge clk);
        $display("ciphertext %h", dataout);
        if (dataout === EXPECTED)
            $display("PASS");
        else
            $display("FAIL: expected %h", EXPECTED);
        $finish;
    end

    initial begin
        #2000 $display("FAIL: timed out waiting for done");
        $finish;
    end
endmodule
