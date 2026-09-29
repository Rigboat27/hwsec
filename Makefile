# make sim     - run all three RTL testbenches (needs iverilog)
# make synth   - rerun the S-box and accumulator synthesis (needs yosys)
# make attacks - run the timing, CPA and DFA scripts (needs python3, numpy, matplotlib)

BUILD := build
SBOX  := $(wildcard 02-sbox/composite/*.v)
AES   := $(filter-out 03-aes128/AES_TB.v,$(wildcard 03-aes128/*.v))
ACC   := $(addprefix 01-accumulator/,accumulator.v adder_struct.v dff.v half_addr.v full_addr.v)

.PHONY: all sim sim-acc sim-sbox sim-aes synth attacks clean

all: sim

sim: sim-acc sim-sbox sim-aes

$(BUILD):
	mkdir -p $@

sim-acc: | $(BUILD)
	iverilog -o $(BUILD)/acc 01-accumulator/test.v $(ACC)
	cd $(BUILD) && vvp -n acc

sim-sbox: | $(BUILD)
	iverilog -o $(BUILD)/sbox 02-sbox/tb/sbox_equiv_tb.v 02-sbox/table/aes_sbox.v $(SBOX)
	vvp -n $(BUILD)/sbox

sim-aes: | $(BUILD)
	iverilog -o $(BUILD)/aes 03-aes128/AES_TB.v $(AES) $(SBOX)
	cd $(BUILD) && vvp -n aes

synth:
	cd 01-accumulator && yosys -q -s synth_accumulator.ys -l ../$(BUILD)/accumulator.log
	cd 02-sbox/synth && for f in *.ys; do yosys -q -s $$f -l ../../$(BUILD)/$${f%.ys}.log; done
	cd 03-aes128 && yosys -q -s synth_aes.ys -l ../$(BUILD)/aes.log
	@grep -H "Chip area" $(BUILD)/*.log

attacks:
	python3 04-timing-attack/attack.py
	python3 06-cpa/cpa.py
	python3 07-dfa/dfa.py --trials 5
	python3 07-dfa/dfa.py --test

clean:
	rm -rf $(BUILD) 01-accumulator/accumulator_nangate45.v 04-timing-attack/password.txt
