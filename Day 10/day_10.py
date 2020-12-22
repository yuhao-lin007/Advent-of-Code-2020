"""
Used the following people's solutions for Part 2 as that's where I got stuck:
u/silverben10 (https://www.reddit.com/r/adventofcode/comments/ka8z8x/2020_day_10_solutions/gf9mvrh/)
Derk-Jan Karrenbeld (https://dev.to/sleeplessbyte/comment/194fe)
u/rawlexander (https://www.reddit.com/r/adventofcode/comments/ka8z8x/2020_day_10_solutions/ggmm6av/, https://youtu.be/KzTBz--x47E)
"""

def get_possible_next_adapters(adapters, rating):
	next_adapters = []
	for adapter in adapters:
		diff = adapter - rating
		if 1 <= diff <= 3:
			next_adapters.append(adapter)
	return next_adapters

def does_every_list_end_with(lis, element):
	for l in lis:
		if l[-1] != element:
			return False
	return True

def get_possible_chains(adapters): # UNUSED: Too inefficient for puzzle input but works with 2 shorter inputs
	adapters_left = adapters.copy()
	adapters_left.append(device_rating)
	
	possible_chains = [[OUTLET_RATING]]
	possible_chains_adapters_left = [adapters_left]

	while not does_every_list_end_with(possible_chains, device_rating):
		for i, chain in enumerate(possible_chains.copy()):
			if chain[-1] == device_rating:
				continue

			adapters_left = possible_chains_adapters_left[i]
			possible_next_adapters = get_possible_next_adapters(adapters_left, chain[-1])

			for j, possible_adapter in enumerate(possible_next_adapters):
				chain_new = chain.copy()
				adapters_left_new = adapters_left.copy()

				chain_new.append(possible_adapter)
				adapters_left_new.remove(possible_adapter)

				if j > 0:
					possible_chains.append(chain_new)
					possible_chains_adapters_left.append(adapters_left_new)
				else:
					possible_chains[i] = chain_new
					possible_chains_adapters_left[i] = adapters_left_new
	return possible_chains

OUTLET_RATING = 0

with open("input.txt", "r") as file:
	adapters = [int(line) for line in file.read().split()]

device_rating = max(adapters) + 3
joltages = adapters + [OUTLET_RATING, device_rating]

# Construct chain using every joltage in ascending order to minimize joltage differences
chain = sorted(joltages)

# Calculate differences between joltages
differences = [chain[i] - chain[i-1] for i in range(1, len(chain))]

# Part 1
print("Part 1:", differences.count(1) * differences.count(3))

# Part 2
num_chains = {0: 1}
for jolt in chain[1:]:
    # Each joltage route is equal to the sum of the number of routes to the previous three joltages
    # Some joltages aren't in the list of adaptors so their number of routes is 0
	num_chains[jolt] = num_chains.get(jolt-1, 0) + num_chains.get(jolt-2, 0) + num_chains.get(jolt-3, 0)

print("Part 2:", num_chains[device_rating])

# Initial Part 2 Solution - Too inefficient for puzzle input
# possible_chains = get_possible_chains(adapters)
# print("Part 2:", len(possible_chains)) # If you have an infinite amount of time this is will work! (I think)