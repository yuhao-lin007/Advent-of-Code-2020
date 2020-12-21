import re
from copy import deepcopy

with open("input.txt", "r") as file:
    lines = [re.sub(" bags?|\.| contain no other", "", line)
             for line in file.read().split("\n")]

rules = {}
for line in lines:
    rule = re.split(" contain |, ", line)
    color = rule[0]
    bag_contents_raw = rule[1:]
    
    bag_contents = []
    for b in bag_contents_raw:
        content = b.split(" ", 1)
        content[0] = int(content[0])
        
        bag_contents.append(content)

    rules[color] = bag_contents

def fill_bag(bag, rule):
	"""
    Recursively fills the bag.
    Works by replacing each reference to the bag color with the
    bag color's contents.

	Returns a dictionary containing how many of each bag there is.
    """
	num_bags = {}
	for i, content in enumerate(rule):
		content_num = content[0]
		content_color = content[1]
		content_rule = deepcopy(rules[content_color])

		if content_color in num_bags:
			num_bags[content_color] += content_num
		else:
			num_bags[content_color] = content_num

		bag[i][1] = content_rule

		inner_num_bags = fill_bag(bag[i][1], content_rule)
		for color in inner_num_bags:
			num = inner_num_bags[color]
			if color in num_bags:
				num_bags[color] += content_num * num
			else:
				num_bags[color] = content_num * num
	return num_bags

def count_total_bags(num_bags):
	total = 0
	for color in num_bags:
		num = num_bags[color]
		total += num
	return total

bags = deepcopy(rules)

total_bags_all = {}
num_bags_with_shiny_gold = 0
for color in rules:
	rule = rules[color]
	bag = bags[color]

	num_bags = fill_bag(bag, rule)
	total_bags = count_total_bags(num_bags)

	total_bags_all[color] = total_bags

	if "shiny gold" in num_bags:
		num_bags_with_shiny_gold += 1

# Part 1
print("Part 1")
print("Num Bags with Shiny Gold Bag:", num_bags_with_shiny_gold)

print()

# Part 2
print("Part 2")
color = "shiny gold"
if color in total_bags_all:
	print(f"{color:12}Total Bags: {total_bags_all[color]}")
else:
	print(color, "not found!")

print()

# Extra
print("Extra")
#print(total_bags_all) # Warning: This dictionary contains a lot of elements with the actual puzzle input

total_bags_highest_num = max(total_bags_all.values())
total_bags_highest_all = [t for t in total_bags_all.items() if t[1] == total_bags_highest_num]

for t in total_bags_highest_all:
	print(f"{t[0]} has the highest number of total bags at {total_bags_highest_num} bags!")