from copy import deepcopy

TILE_FLOOR = "."
TILE_SEAT_EMPTY = "L"
TILE_SEAT_OCCUPIED = "#"

VISION_BLOCK_TILES = [
	TILE_SEAT_EMPTY,
	TILE_SEAT_OCCUPIED,
	]


class SimulationInfo:
	def __init__(self, final_layout, num_rounds):
		self.final_layout = final_layout
		self.num_rounds = num_rounds


class RoundInfo:
	def __init__(self, final_layout, num_changes):
		self.final_layout = final_layout
		self.num_changes = num_changes


def display_layout(layout):
	for row in layout:
		print("  ".join(row))


def simulate_seats(layout, simulation_function):
	layout = deepcopy(layout)
	rounds = 0
	changes = None
	changes_old = None
	while changes != changes_old or changes == None:
		changes_old = changes
		round_info = simulation_function(layout)
		layout = round_info.final_layout
		changes = round_info.num_changes
		rounds += 1
	
	return SimulationInfo(layout, rounds)


def simulate_round_part_1(layout):
	changes = 0
	new_layout = deepcopy(layout)

	for i, row in enumerate(layout):
		for j, tile in enumerate(row):
			if tile == TILE_SEAT_EMPTY and len(get_adjacent_tiles(layout, i, j, TILE_SEAT_OCCUPIED)) == 0:
				new_layout[i][j] = TILE_SEAT_OCCUPIED
				changes += 1
			elif tile == TILE_SEAT_OCCUPIED and len(get_adjacent_tiles(layout, i, j, TILE_SEAT_OCCUPIED)) >= 4:
				new_layout[i][j] = TILE_SEAT_EMPTY
				changes += 1
	
	return RoundInfo(new_layout, changes)


def get_adjacent_tiles(layout, row_index, column_index, tile):
	num_rows = len(layout)
	num_columns = len(layout[0])
	seats = []

	for offset_x in range(-1, 2):
		for offset_y in range(-1, 2):
			x = row_index + offset_x
			y = column_index + offset_y
			if (offset_x == offset_y == 0 or
					x >= num_rows or x < 0 or
					y >= num_columns or y < 0):
				continue

			if layout[x][y] == tile:
				seats.append((x, y))
	
	return seats


def get_num_tiles(layout, tile):
	num = 0
	for row in layout:
		for seat in row:
			if seat == tile:
				num += 1
	return num


def simulate_round_part_2(layout):
	changes = 0
	new_layout = deepcopy(layout)

	for i, row in enumerate(layout):
		for j, tile in enumerate(row):
			if tile == TILE_SEAT_EMPTY and len(get_visible_tiles(layout, i, j, TILE_SEAT_OCCUPIED, VISION_BLOCK_TILES)) == 0:
				new_layout[i][j] = TILE_SEAT_OCCUPIED
				changes += 1
			elif tile == TILE_SEAT_OCCUPIED and len(get_visible_tiles(layout, i, j, TILE_SEAT_OCCUPIED, VISION_BLOCK_TILES)) >= 5:
				new_layout[i][j] = TILE_SEAT_EMPTY
				changes += 1

	return RoundInfo(new_layout, changes)


def get_visible_tiles(layout, row_index, column_index, tile_wanted, block_tiles):
	num_rows = len(layout)
	num_columns = len(layout[0])

	visible_tiles = []

	for offset_x in range(-1, 2):
		for offset_y in range(-1, 2):
			x = row_index + offset_x
			y = column_index + offset_y
			if (offset_x == offset_y == 0 or
					x >= num_rows or x < 0 or
					y >= num_columns or y < 0):
				continue
			
			while True:
				tile = layout[x][y]
				if tile == tile_wanted:
					visible_tiles.append((x, y))
				if (tile in block_tiles or
						x + offset_x >= num_rows or x + offset_x < 0 or
						y + offset_y >= num_columns or y + offset_y < 0):
					break
				x += offset_x
				y += offset_y
	
	return visible_tiles


with open("input.txt", "r") as file:
	layout = [list(row) for row in file.read().split()]

# Part 1
simulation_info = simulate_seats(layout, simulate_round_part_1)
new_layout = simulation_info.final_layout
rounds = simulation_info.num_rounds
print(f"Part 1: Rounds: {rounds:<5} Num Occupied Seats: {get_num_tiles(new_layout, TILE_SEAT_OCCUPIED)}")

# Part 2
simulation_info = simulate_seats(layout, simulate_round_part_2)
new_layout = simulation_info.final_layout
rounds = simulation_info.num_rounds
print(f"Part 2: Rounds: {rounds:<5} Num Occupied Seats: {get_num_tiles(new_layout, TILE_SEAT_OCCUPIED)}")