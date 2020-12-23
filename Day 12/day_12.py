from math import radians, cos, sin, pi
from copy import deepcopy


class Instruction:
	def __init__(self, operator, arg):
		self.operator = operator
		self.arg = arg
	
	def __str__(self):
		return self.operator + str(self.arg)


class Vector2:
	def __init__(self, x, y):
		self.x = x
		self.y = y
	
	def __str__(self):
		return f"({self.x}, {self.y})"
	
	def __add__(self, other):
		return Vector2(self.x + other.x, self.y + other.y)
	
	def __mul__(self, other):
		if isinstance(other, int):
			return Vector2(self.x * other, self.y * other)
		else:
			raise NotImplementedError
	
	def __rmul__(self, other):
		if isinstance(other, int):
			return Vector2(self.x * other, self.y * other)
		else:
			raise NotImplementedError
	
	def rotate(self, degrees, origin):
		"""
		Returns a new vector rotated clockwise by the specified angle in degrees about the specified origin.
		Based on the equations from: https://matthew-brett.github.io/teaching/rotation_2d.html
		"""
		x1 = self.x - origin.x
		y1 = self.y - origin.y
		
		# Negative degrees because rotation is clockwise
		rad = radians(-degrees)
		
		c = cos(rad)
		s = sin(rad)
		
		# Rounding due to darn pi precision issues
		x2 = round(c * x1 - s * y1, 5)
		y2 = round(s * x1 + c * y1, 5)
		
		x3 = x2 + origin.x
		y3 = y2 + origin.y
		return Vector2(x3, y3)
	
	def dist_manhat(self, vec2):
		return abs(self.x + vec2.x) + abs(self.y + vec2.y)


ORIGIN = Vector2(0, 0)
WAYPOINT_START_POS = Vector2(10, 1)

DIRECTIONS = {
	"N": Vector2(0, 1),
	"E": Vector2(1, 0),
	"S": Vector2(0, -1),
	"W": Vector2(-1, 0),
}

ROTATIONS = {
	"R": 1,
	"L": -1,
}


with open("input.txt", "r") as file:
	instructions = [Instruction(l[0], int(l[1:])) for l in file.read().split()]

# Part 1
position = deepcopy(ORIGIN)
direction = Vector2(1, 0)

for ins in instructions:
	op = ins.operator
	arg = ins.arg
	if op in DIRECTIONS:
		position += DIRECTIONS[op] * arg
	elif op in ROTATIONS:
		direction = direction.rotate(ROTATIONS[op] * arg, ORIGIN)
	elif op == "F":
	 	position += direction * arg

print("Part 1:", position.dist_manhat(ORIGIN))

# Part 2
position = deepcopy(ORIGIN)
waypoint_pos_rel = deepcopy(WAYPOINT_START_POS)

for ins in instructions:
	op = ins.operator
	arg = ins.arg
	if op in DIRECTIONS:
		velocity = DIRECTIONS[op] * arg
		waypoint_pos_rel += velocity
	elif op in ROTATIONS:
		waypoint_pos_rel = waypoint_pos_rel.rotate(ROTATIONS[op] * arg, ORIGIN)
	elif op == "F":
		velocity = waypoint_pos_rel * arg
		position += velocity

print("Part 2:", position.dist_manhat(ORIGIN))