from math import ceil, log2

def get_row_number(seat, num_rows):
    lower_half_row = 0
    upper_half_row = num_rows - 1

    for character in seat[:int(log2(num_rows))]:
        if character == "F":
            upper_half_row = (upper_half_row + lower_half_row) // 2
        elif character == "B":
            lower_half_row = ceil((upper_half_row + lower_half_row) / 2)
    
    return lower_half_row

def get_column_number(seat, num_columns):
    lower_half_column = 0
    upper_half_column = num_columns - 1
    
    for character in seat[-int(log2(num_columns)):]:
        if character == "L":
            upper_half_column = (upper_half_column + lower_half_column) // 2
        elif character == "R":
            lower_half_column = ceil((upper_half_column + lower_half_column) / 2)

    return lower_half_column

with open("input.txt", "r") as file:
    seats = [seat.rstrip() for seat in file]

num_rows = 128
num_columns = 8

seat_ids = []
for seat in seats:
    row = get_row_number(seat, num_rows)
    column = get_column_number(seat, num_columns)

    seat_id = row * num_columns + column
    seat_ids.append(seat_id)

# Part 1
print("Part 1")
seat_id_max = max(seat_ids)
print("Max Seat ID:", seat_id_max)

print()

# Part 2
print("Part 2")
seat_id_min = min(seat_ids)

seat_ids_sorted = sorted(seat_ids)
for i in range(seat_id_min, seat_id_max+1):
    if i != seat_ids_sorted[i-seat_id_min]:
        print("Missing ID:", i)
        break
