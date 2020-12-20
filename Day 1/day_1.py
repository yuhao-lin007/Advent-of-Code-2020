from math import prod

def get_valid_entries(entries, nums_used, total_required):
    length = len(entries)
    
    if nums_used < 1 or nums_used > length:
        return

    last_indice_index = nums_used - 1
    indices = [i for i in range(nums_used)]

    checks = 0
    while True:
        #print(f"Indices: {indices} ({checks})")

        checks += 1
        # Check if numbers based on indice values totals to required value
        numbers = [entries[indice] for indice in indices]
        if sum(numbers) == total_required:
            #print(f"Checks: {checks}")
            return numbers

        indices[last_indice_index] += 1

        # Overflow to next indice(s) if required
        for i in range(nums_used-1, 0, -1):
            min_indice = max(indices[:i]) + 1
            max_indice = length - nums_used + i
            if indices[i] > max_indice:
                indices[i-1] += 1
                indices[i] = min_indice

        # Check if it has reached the end
        if indices[0] > length - nums_used:
            #print(f"Checks: {checks}")
            return

total_required = 2020

with open("input.txt", "r") as file:
    entries = [int(entry) for entry in file]

# Task 1
print("Task 1")
valid_entries = get_valid_entries(entries, 2, total_required)
print("Valid Entries:", valid_entries)
if valid_entries:
    print("Valid Entries Product:", prod(valid_entries))

print()

# Task 2
print("Task 2")
valid_entries = get_valid_entries(entries, 3, total_required)
print("Valid Entries:", valid_entries)
if valid_entries:
    print("Valid Entries Product:", prod(valid_entries))
