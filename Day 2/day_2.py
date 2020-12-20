class PasswordDatum():
    def __init__(self, password, valid_letter, number_valid_1, number_valid_2):
        self.password = password
        self.valid_letter = valid_letter
        self.number_valid_1 = number_valid_1
        self.number_valid_2 = number_valid_2

    def is_valid_old(self): # Used in Part 1
        num_valid_letter = 0
        for letter in self.password:
            if letter == self.valid_letter:
                num_valid_letter += 1
        return self.number_valid_1 <= num_valid_letter <= self.number_valid_2

    def is_valid_new(self): # Used in Part 2
        return [self.password[self.number_valid_1 - 1] == self.valid_letter,
                self.password[self.number_valid_2 - 1] == self.valid_letter] \
                .count(True) == 1

with open("input.txt", "r") as file:
    password_data = []
    for datum in file:
        datum = datum.rstrip()
        data = datum.split(" ")
        
        password = data[2]
        valid_letter = data[1].rstrip(":")
        valid_range = map(int, data[0].split("-"))
        
        password_datum = PasswordDatum(password, valid_letter, *valid_range)
        password_data.append(password_datum)

num_valid_old = 0
num_valid_new = 0
for password_datum in password_data:
    if password_datum.is_valid_old():
        num_valid_old += 1
    if password_datum.is_valid_new():
        num_valid_new += 1

# Part 1
print("Part 1")
print("Passwords Valid:", num_valid_old)

print()

# Part 2
print("Part 2")
print("Passwords Valid:", num_valid_new)

