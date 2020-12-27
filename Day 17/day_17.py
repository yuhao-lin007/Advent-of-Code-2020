def set_element(lis, value, *indices):
	if isinstance(lis[indices[0]], list):
		set_element(lis[indices[0]], value, *indices[1:])
	else:
		lis[indices[0]] = value


def complete_copy(lis):
	"""
	Credit: https://stackoverflow.com/a/1601774/8004215
	"""
	if isinstance(lis, list):
		return list(map(complete_copy, lis))
	return lis


def get_num_dimensions(grid):
	"""
	Note: Only works for uniform arrays
	"""
	num = 0
	if isinstance(grid, list):
		num += get_num_dimensions(grid[0]) + 1
		return num
	return num 


def get_dimensional_grid(grid, num_dimensions):
	"""
	Note: num_dimensions must be less than the initial number of dimensions to
	have any effect
	"""
	num_dimensions_initial = get_num_dimensions(grid)
	if num_dimensions <= num_dimensions_initial:
		return grid
	
	for i in range(num_dimensions - num_dimensions_initial):
		grid = get_dimensional_grid([grid], num_dimensions-1)
	return grid


def make_all_inactive(grid):
	new_grid = complete_copy(grid)
	for i, item in enumerate(new_grid):
		if isinstance(item, list):
			new_grid[i] = make_all_inactive(item)
		else:
			new_grid[i] = "."
	return new_grid


def expand_grid(grid):
	new_grid = complete_copy(grid)
	
	if isinstance(new_grid[0], list):
		for i, item in enumerate(new_grid):
			new_grid[i] = expand_grid(item)

		cross_section = make_all_inactive(new_grid[0])
		new_grid.insert(0, complete_copy(cross_section))
		new_grid.append(complete_copy(cross_section))
	else:
		new_grid.insert(0, ".")
		new_grid.append(".")

	return new_grid


def get_adjacent_cubes(grid, *indices, **kwargs):
	num_dimensions = get_num_dimensions(grid)
	if len(indices) != num_dimensions:
		raise ValueError("the number of indices passed does not match the " \
						"grid's number of dimensions")

	cubes = []
	
	for i in range(-1, 2):
		index = indices[0] + i
		if index >= len(grid) or index < 0:
			continue
		cross_section = grid[index]

		if isinstance(cross_section, list):
			offset_indices = []
			if "offset_indices" in kwargs:
				offset_indices.extend(kwargs["offset_indices"])
			offset_indices.append(i)

			cubes.extend(get_adjacent_cubes(cross_section, *indices[1:], offset_indices=offset_indices))
		else:
			offset_indices = kwargs["offset_indices"] + [i]
			if all(index == 0 for index in offset_indices):
				continue
			cubes.append(cross_section)

	return cubes


def simulate_round(grid, **kwargs):
	new_grid = complete_copy(grid)
	
	for i, cross_section in enumerate(grid):
		if isinstance(cross_section, list):
			iteration_indices = []
			if "iteration_indices" in kwargs:
				iteration_indices.extend(kwargs["iteration_indices"])
			iteration_indices.append(i)

			if "original_grid" in kwargs:
				original_grid = kwargs["original_grid"]
			else:
				original_grid = grid
			if "main_grid" in kwargs:
				main_grid = kwargs["main_grid"]
			else:
				main_grid = new_grid

			cross_section = simulate_round(
				cross_section,
				iteration_indices=iteration_indices,
				original_grid=original_grid,
				main_grid=main_grid)
		else:
			iteration_indices = kwargs["iteration_indices"] + [i]

			original_grid = kwargs["original_grid"]
			main_grid = kwargs["main_grid"]
			if cross_section == "#" and get_adjacent_cubes(original_grid, *iteration_indices).count("#") not in {2, 3}:
				set_element(main_grid, ".", *iteration_indices)
			if cross_section == "." and get_adjacent_cubes(original_grid, *iteration_indices).count("#") == 3:
				set_element(main_grid, "#", *iteration_indices)

	return new_grid


def simulate_game(initial_state, rounds, dimensions):
	grid = get_dimensional_grid(initial_state, dimensions)
	for i in range(rounds):
		grid = expand_grid(grid)
		grid = simulate_round(grid)
	return grid


def count_active_cubes(grid):
	num = 0
	for cross_section in grid:
		if isinstance(cross_section, list):
			num += count_active_cubes(cross_section)
		else:
			if cross_section == "#":
				num += 1
	return num


with open("input.txt", "r") as file:
	initial_state = [list(row) for row in file.read().split()]

# Part 1
grid_3d = simulate_game(initial_state, 6, 3)
print("Part 1:", count_active_cubes(grid_3d))

# Part 2
grid_4d = simulate_game(initial_state, 6, 4)
print("Part 2:", count_active_cubes(grid_4d))