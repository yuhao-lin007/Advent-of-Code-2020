from pprint import pprint
import re
from math import log2

def apply_mask_part_1(mask, value):
	binary = list(bin(value)[2:].zfill(36))
	for i, m in enumerate(mask):
		if m != "X":
			binary[i] = m
	return int("".join(binary), 2)

def apply_mask_part_2(mask, address):
	new_addresses = []
	binary = list(bin(address)[2:].zfill(36))
	floating_indexes = []
	for i, m in enumerate(mask):
		if m == "1":
			binary[i] = "1"
		elif m == "X":
			binary[i] = "X"
			floating_indexes.append(i)
	
	# A bit marked as "X" is known as a floating bit.
	# This means that it can be either 0 or 1.
	# Therefore, if an address contains an "X" then there
	# will be multiple addresses.
	# The total combinations is 2 to the power of the
	# number of floating bits.

	# We can then iterate through each binary representation
	# of the bits (e.g. 000, 001, 010) and substitute them
	# into the floating bit indexes.
	
	num_addresses = 2 ** len(floating_indexes)
	bits_used = int(log2(num_addresses))
	for i in range(num_addresses):
		alternate_bits = bin(i)[2:].zfill(bits_used)
		for j, b in enumerate(alternate_bits):
			binary_index = floating_indexes[j]
			binary[binary_index] = b
		new_addresses.append(int("".join(binary), 2))

	return new_addresses

with open("input.txt", "r") as file:
	lines = file.read().split("\n")

# Part 1
memory = {}
for line in lines:
	contents = line.split(" = ")
	if contents[0] == "mask":
	 	mask = contents[1]
	elif "mem" in contents[0]:
		address = int(re.sub("[a-z\[\]]", "", contents[0]))
		value = int(contents[1])
		new_value = apply_mask_part_1(mask, value)
		memory[address] = new_value

value_sum = sum([memory[a] for a in memory])
print("Part 1:", value_sum)

# Part 2
memory = {}
for line in lines:
	contents = line.split(" = ")
	if contents[0] == "mask":
	 	mask = contents[1]
	elif "mem" in contents[0]:
		initial_address = int(re.sub("[a-z\[\]]", "", contents[0]))
		value = int(contents[1])
		new_addresses = apply_mask_part_2(mask, initial_address)
		for address in new_addresses:
			memory[address] = value

value_sum = sum([memory[a] for a in memory])
print("Part 2:", value_sum)