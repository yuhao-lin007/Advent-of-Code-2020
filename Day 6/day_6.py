def get_group_questions_answered(group): # Used in Part 1
    questions_answered = []
    for person in group:
        for question in person:
            if question not in questions_answered:
                questions_answered.append(question)
    return questions_answered

def get_group_questions_everyone_answered(group): # Used in Part 2
    questions_answered = {}
    for person in group:
        for question in person:
            if question in questions_answered:
                questions_answered[question] += 1
            else:
                questions_answered[question] = 1

    num_people = len(group)
    return [q for q in questions_answered
            if questions_answered[q] == num_people]

with open("input.txt", "r") as file:
    groups = list(map(lambda g: g.split("\n"),
                      file.read().split("\n\n")))

# Part 1
print("Part 1")
total_questions_answered = 0
for group in groups:
    questions_answered = get_group_questions_answered(group)
    total_questions_answered += len(questions_answered)

print("Total Different Questions Answered:", total_questions_answered)

print()

# Part 2
print("Part 2")
total_questions_everyone_answered = 0
for group in groups:
    questions_everyone_answered = get_group_questions_everyone_answered(group)
    total_questions_everyone_answered += len(questions_everyone_answered)

print("Total Questions Everyone Answered:", total_questions_everyone_answered)
