from re import match

with open("input.txt", "r") as file:
    data = [data.split() for data in file.read().split("\n\n")]
    
    passport_data = []
    for datum in data:
        passport_datum = {}
        for key_value in datum:
            key_value = key_value.split(":")
            key = key_value[0]
            value = key_value[1]

            passport_datum[key] = value
        passport_data.append(passport_datum)

required_fields = {"byr": lambda y: match("\d{4}", y) and 1920 <= int(y) <= 2002,
                   "iyr": lambda y: match("\d{4}", y) and 2010 <= int(y) <= 2020,
                   "eyr": lambda y: match("\d{4}", y) and 2020 <= int(y) <= 2030,
                   "hgt": lambda h: match("\d+(cm|in)", h) and \
                   ((h[-2:] == "cm" and 150 <= int(h[:-2]) <= 193) or \
                    (h[-2:] == "in" and 59 <= int(h[:-2]) <= 76)),
                   "hcl": lambda c: match("#[0-9a-f]{6}", c),
                   "ecl": lambda c: match("amb|blu|brn|gry|grn|hzl|oth", c),
                   "pid": lambda i: match("^\d{9}$", i)}

num_valid_1 = 0
num_valid_2 = 0
for datum in passport_data:
    valid_1 = True
    valid_2 = True
    for field in required_fields:
        validity_check = required_fields[field]
        if field not in datum:
            valid_1 = False
        elif not validity_check(datum[field]):
            valid_2 = False
    
    if valid_1:
        num_valid_1 += 1
        if valid_2:
            num_valid_2 += 1

# Part 1
print("Part 1")
print("Num Valid:", num_valid_1)

print()

# Part 2
print("Part 2")
print("Num Valid:", num_valid_2)
