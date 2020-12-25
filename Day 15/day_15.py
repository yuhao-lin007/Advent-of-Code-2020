def memory_game(numbers, final_turn):
	turn_spoken = {num: i + 1 for i, num in enumerate(numbers[:-1])}

	next_num = numbers[-1]
	for turn_num in range(len(numbers)+1, final_turn+1):
		last_turn_num = turn_num - 1
		if next_num in turn_spoken:
			spoken_num = last_turn_num - turn_spoken[next_num]
		else:
			spoken_num = 0
		turn_spoken[next_num] = last_turn_num

		next_num = spoken_num
	
	return spoken_num

with open("input.txt", "r") as file:
	numbers = [int(num) for num in file.read().split(",")]

# Part 1
print("Part 1:", memory_game(numbers, 2020))

# Part 2
print("Part 2:", memory_game(numbers, 30000000))