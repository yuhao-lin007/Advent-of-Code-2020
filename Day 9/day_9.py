def get_valid_contiguous_set(numbers, total):
	for length in range(2, len(numbers)+1):
		for offset in range(len(numbers)-length+1):
			contiguous_set = numbers[offset:offset+length]
			if sum(contiguous_set) == total:
				return contiguous_set

with open("input.txt", "r") as file:
	numbers = list(map(int, file.read().split()))

preamble_length = 25
for i in range(len(numbers) - preamble_length):
	previous_numbers = numbers[i:i+preamble_length]
	total = numbers[i+preamble_length]
	total_valid = False
	for num1 in previous_numbers:
		for num2 in previous_numbers:
			if num1 + num2 == total:
				total_valid = True
	if not total_valid:
		invalid_total = total

# Part 1
print("Part 1")
print(invalid_total, "is an invalid total!")

print()

# Part 2
print("Part 2")
contiguous_set = get_valid_contiguous_set(numbers, invalid_total)
print("Encryption Weakness:", min(contiguous_set) + max(contiguous_set))