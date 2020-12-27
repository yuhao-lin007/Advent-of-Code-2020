"""
Credit to u/kaklarakol:
https://www.reddit.com/r/adventofcode/comments/kfeldk/2020_day_18_solutions/gh0ntoo/

I didn't use their solution directly but I compared my results to theirs and
found the expression which was messing me up on part 2.
The expression in question:
5 + 3 * 4 + (6 + 2 * (6 * 2 + 6 + 3) * 2 * 6 + (9 * 9 * 3)) + 2 + 6
"""

import operator
import re

OPERATORS = {
	"+": operator.add,
	"*": operator.mul
}


def evaluate_simple_expression_linearly(expression):
	components = expression.split()
	result = 0
	next_operator = operator.add
	for component in components:
		if component.isnumeric():
			number = int(component)
			result = next_operator(result, number)
		else:
			next_operator = OPERATORS[component]
	return result


def evaluate_simple_expression_part_2(expression):
	additions = re.findall("(?:(?:[0-9]+)* \+ [0-9]+)+", expression)
	for addition in additions:
		numbers = [int(num) for num in addition.split(" + ")]
		expression = expression.replace(addition, str(sum(numbers)), 1)
	return evaluate_simple_expression_linearly(expression)


def evaluate_expression(expression, simple_expression_parser):
	inner_brackets = re.findall("\([^()]+\)", expression)
	while len(inner_brackets) > 0:
		for exp in inner_brackets:
			simple_exp = re.sub("[()]", "", exp)
			expression = expression.replace(
				exp,
				str(evaluate_expression(simple_exp, simple_expression_parser)),
				1)
		
		inner_brackets = re.findall("\([^()]+\)", expression)
	
	return simple_expression_parser(expression)


with open("input.txt", "r") as file:
	expressions = file.read().split("\n")

# Part 1
results = []
for expression in expressions:
	result = evaluate_expression(expression, evaluate_simple_expression_linearly)
	results.append(result)
print("Part 1:", sum(results))

# Part 2
results = []
for expression in expressions:
	result = evaluate_expression(expression, evaluate_simple_expression_part_2)
	results.append(result)
print("Part 2:", sum(results))