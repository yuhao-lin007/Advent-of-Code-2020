import math


def is_value_following_rule(rule, value):
	return any(value in valid_range for valid_range in rule)


def get_invalid_values(ticket):
	invalid_values = []
	for value in ticket:
		value_valid = False
		for valid_ranges in field_ranges.values():
			if is_value_following_rule(valid_ranges, value):
				value_valid = True
		if not value_valid:
			invalid_values.append(value)
	return invalid_values


def is_ticket_following_rule(rule, ticket):
	for value in ticket:
		if not is_value_following_rule(rule, value):
			return False
	return True


def remove_from_2d_list(lis, value):
    for l in lis:
        if value in l:
            l.remove(value)


def get_field_positions(valid_tickets):
	field_positions = {}

	# Essentially "rotates" the tickets 90 degrees.
	# Tuple number i will contain index i of every ticket list.
	# E.g.
	# [[3, 9, 18], [15, 1, 5], [5, 14, 9]]
	# Becomes:
	# [(3, 15, 5), (9, 1, 14), (18, 5, 9)]
	ticket_columns = list(zip(*valid_tickets))

	possible_field_positions = {field: [] for field in field_ranges.keys()}

	# Populate the possible_field_positions dictionary.
	# We first check what rules each columns abide by.
	# Then we add this list of every possible position (based on the rules it
	# abides by) to possible_field_positions.
	for i, column in enumerate(ticket_columns):
		for field, valid_ranges in field_ranges.items():
			if is_ticket_following_rule(valid_ranges, column):
				possible_field_positions[field].append(i)

	# Eliminates each possible field position.
	# If there is only one possible position (i.e. the length of the list is 1)
	# then that must be the correct position for the field.
	# And since fields can't have multiple positions we can eliminate the
	# position from every possible positions list.
	while len(field_positions) != num_fields:
		for field, possible_positions in possible_field_positions.items():
			if len(possible_positions) == 1:
				position = possible_positions[0]
				field_positions[field] = position
				remove_from_2d_list(possible_field_positions.values(), position)

	return field_positions


with open("input.txt", "r") as file:
	sections = file.read().split("\n\n")

# Parse the input.
field_ranges = {}
ticket_rules_raw = sections[0].split("\n")
num_fields = len(ticket_rules_raw)
for rule_raw in ticket_rules_raw:
	components = rule_raw.split(": ")
	field = components[0]
	ranges_raw = components[1].split(" or ")
	
	ranges = []
	for range_raw in ranges_raw:
		boundaries = range_raw.split("-")
		lower_bound = int(boundaries[0])
		upper_bound = int(boundaries[1])
		# One added to the upper bound as the range function is exclusive
		# while the input range is inclusive.
		ranges.append(range(lower_bound, upper_bound+1))
	
	field_ranges[field] = ranges

main_ticket = [int(num) for num in sections[1].split("\n")[1].split(",")]

nearby_tickets = []
nearby_tickets_raw = sections[2].split("\n")
for t in nearby_tickets_raw[1:]:
	nearby_tickets.append([int(n) for n in t.split(",")])

# Part 1
valid_tickets = []
invalid_values_all = []
for ticket in nearby_tickets:
	invalid_values = get_invalid_values(ticket)
	invalid_values_all.extend(invalid_values)
	if not len(invalid_values):
		valid_tickets.append(ticket)

print("Part 1:", sum(invalid_values_all))

# Part 2
field_positions = get_field_positions(valid_tickets)

main_ticket_values = {field: main_ticket[pos] for field, pos in field_positions.items()}

departure_values = []
for field, value in main_ticket_values.items():
	if field.startswith("departure"):
		departure_values.append(value)

print("Part 2:", math.prod(departure_values))