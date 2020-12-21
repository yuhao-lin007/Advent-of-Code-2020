from copy import deepcopy

# A bit overengineered but oh well

class Program:
	def __init__(self):
		self.instruction_index = 0
		self.prev_instruction_indexes = []
		self.acc_value = 0
		self.is_loop = False

	def is_infinite_loop(self, instructions, is_debug=False):
		self.instruction_index = 0
		self.prev_instruction_indexes = []
		self.acc_value = 0
		self.is_loop = False
		while not self.is_at_end(instructions):
			instruction = instructions[self.instruction_index]
			if self.instruction_index in self.prev_instruction_indexes:
				self.is_loop = True
				break
			self.prev_instruction_indexes.append(self.instruction_index)
			self.instruction_index, self.acc_value = instruction.execute(self.instruction_index, self.acc_value)
		
		if is_debug:
			print(f"Acc Value before end: {self.acc_value:<5} Is an Infinite Loop: {self.is_loop}")
		return self.is_loop
	
	def fix(self, instructions, is_debug=False):
		for i, instruction in enumerate(instructions):
			instruction_type = type(instruction)
			if instruction_type == Instruction:
				new_instruction = InstructionJmp(instruction.argument)
			elif instruction_type == InstructionJmp:
				new_instruction = Instruction(instruction.argument)
			else:
				continue
			instructions[i] = new_instruction

			if not self.is_infinite_loop(instructions):
				if is_debug:
					print("Acc Value at end of Fixed Instructions:", self.acc_value)
				return instructions

			instructions[i] = instruction

	def is_at_end(self, instructions):
		return self.instruction_index >= len(instructions)

class Instruction:
	def __init__(self, argument):
		self.argument = argument
	
	def execute(self, instruction_index, acc_value):
		return instruction_index + 1, acc_value

class InstructionAcc(Instruction):
	def execute(self, instruction_index, acc_value):
		return instruction_index + 1, acc_value + self.argument

class InstructionJmp(Instruction):
	def execute(self, instruction_index, acc_value):
		return instruction_index + self.argument, acc_value

instruction_classes = {
	"acc": InstructionAcc,
	"jmp": InstructionJmp,
}
with open("input.txt", "r") as file:
	instructions = []
	for line in file:
		components = line.split()
		operation = components[0]
		argument = int(components[1])

		instruction_class = instruction_classes.get(operation, Instruction)
		instruction = instruction_class(argument)
		instructions.append(instruction)

program = Program()

# Part 1
print("Part 1")
program.is_infinite_loop(instructions, is_debug=True)

print()

# Part 2
print("Part 2")
program.fix(instructions, is_debug=True)
