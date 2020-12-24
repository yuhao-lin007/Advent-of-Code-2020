from pprint import pprint
import math

with open("input.txt", "r") as file:
	lines = file.read().split()
	departure_time = int(lines[0])
	bus_ids = lines[1].split(",")
	working_bus_ids = [int(n) for n in bus_ids if n != "x"]

# Part 1
bus_time_waited = [(i, i - departure_time % i) for i in working_bus_ids]
closest_bus = min(bus_time_waited, key=lambda b: b[1])
print("Part 1:", math.prod(closest_bus))

# Part 2 - Used hints (found out the "Chinese Remainder Theorem" was required and researched it)

# All bus IDs are prime so all pairs of IDs will have a GCD of 1
# Therefore, the Chinese Remainder Theorem will work
def chinese_remainder_theorem(bus_ids):
	# If you're confused I would recommend watching this video:
	# https://youtu.be/zIFehsBHB8o

	# Create a dictionary of the following format:
	# key: bus_id
	# value: array containing various info
	# array[0] is timestamp offset
	# Equations used for array[1] onwards:
	# x ≅ b (mod n)
	# N is the product of all the 'n's (n₁ * n₂ * n₃...)
	# Nᵢ = N/nᵢ (i.e. the product of all the 'n's excluding nᵢ)
	# xᵢ ≅ (1/Nᵢ) (mod n) (i.e. modular inverse of Nᵢ mod n)
	# array[1] is the remainder (bᵢ)
	# array[2] is Niᵢ
	# array[3] is xᵢ

	# Only adds array[0]
	bus_id_info = {int(bus_id): [i] for i, bus_id in enumerate(bus_ids) if bus_id != "x"}

	id_product = math.prod(bus_id_info)

	# Adds array[1] onwards
	x = 0
	for bus_id in bus_id_info:
		info = bus_id_info[bus_id]
		offset = info[0]

		bi = (bus_id - offset) % bus_id
		info.append(bi)

		# Using floor division here means ni will be an integer instead of a float
		# When a float is greater than 2^53 then precision issues will occur
		# ni on its own isn't greater than 2^53 (at least in the puzzle input)
		# But x is so x must be an integer (which it will be if bi, ni, and xi are all integers)
		ni = id_product // bus_id
		info.append(ni)

		c = ni % bus_id
		xi = 1
		while (c * xi) % bus_id != 1:
			xi += 1
		info.append(xi)

		x += bi * ni * xi

	t = x % id_product

	return t

print("Part 2:", chinese_remainder_theorem(bus_ids))