from math import floor
from copy import deepcopy

# input strings are 81 charcters long, serailized from left to right, top to bottom 
# with periods for blank spaces and no separator for rows

# the solution state is stored as a list where
# unknown cells are a list of possible values and known cells are a single character
is_determined = lambda val: isinstance(val, str)
all_cell_nums = list(range(81))
flatten_list = lambda l: [x for y in l for x in y]

# p can be either a puzzle/solution string or solution state
def rows(p):
	return [p[x:x+9] for x in range(0, 81, 9)]

def columns(p):
	return [p[x::9] for x in range(9)]

def boxes(p):
	box_start = [0, 3, 6, 27, 30, 33, 54, 57, 60]
	return [p[b:b+3] + p[b+9:b+12] + p[b+18:b+21] for b in box_start]

def units_of(p, cell_num):
	row_num = floor(cell_num/9)
	col_num = cell_num % 9
	box_num = floor(col_num/3) + 3*floor(row_num/3)
	return rows(p)[row_num], columns(p)[col_num], boxes(p)[box_num]

def common_cells(cell_num):
	return set(x for x in flatten_list(units_of(all_cell_nums, cell_num)) if x != cell_num)

def set_val(possibles, cell_num, val):
	possibles[cell_num] = val
	for i in [x for x in common_cells(cell_num) if not is_determined(possibles[x])]:
		options = possibles[i]
		if val in options:
			possibles[i].remove(val)
			if len(possibles[i]) == 1:
				possibles[i] = possibles[i][0]
	return possibles

def has_duplicate_val(possibles):
	for i in [x for x in all_cell_nums if is_determined(possibles[x])]:
		common_vals = [possibles[x] for x in common_cells(i) if is_determined(possibles[x])]
		if possibles[i] in common_vals:
			return True
	return False

def scan_possibles(possibles):
	scan = True
	while scan:
		scan = False
		for i in [x for x in all_cell_nums if not is_determined(possibles[x])]:
			for unit in units_of(all_cell_nums, i):
				# ignore the cell's own possible values
				unit.remove(i)
				unit_possibles = set(flatten_list([possibles[u] for u in unit]))
				for p in possibles[i]:
					if p not in unit_possibles:
						possibles = set_val(possibles, i, p)
						scan = True
	return possibles

def solve(puzzle_string):
	possibles, nums = [], "123456789"

	for i in all_cell_nums:
		val = puzzle_string[i]
		if val == ".":
			taken = set(flatten_list(units_of(puzzle_string, i)))	
			possibles.append([n for n in nums if n not in taken])
		else:
			possibles.append(val)

	revert_points = []
	possibles = scan_possibles(possibles)
	duplicate = False

	# when making a guess, do so for the lowest-number cell with the fewest possible values
	# which occur the most in all cells on the board
	sort_func = lambda x: str(len(x[1])) + "-" + str(99 - possibles.count(x[1])) + "-" + str(x[0])

	while not all(is_determined(x) for x in possibles) or duplicate:
		if duplicate:
			possibles = revert_points.pop()
		else:
			guess = sorted([(i, possibles[i]) for i in all_cell_nums if not is_determined(possibles[i])], key=sort_func)[0]
			cell_num, val = guess[0], guess[1][0]
			revert = deepcopy(possibles)
			revert[cell_num].remove(val)
			if len(revert[cell_num]) == 1:
				revert = set_val(revert, cell_num, revert[cell_num][0])
			revert_points.append(revert)
			possibles = scan_possibles(set_val(possibles, cell_num, val))
			
		duplicate = has_duplicate_val(possibles)
					
	return "".join(possibles)

def check_solves(puzzle_string, solution_string):
	return all([puzzle_string[i] in (solution_string[i], ".") for i in all_cell_nums])

def is_valid_solution(solution_string):

	funcs = [rows, columns, boxes]
	check_unit = lambda unit: set(unit) == set("123456789")
	checks = [all(map(check_unit, f(solution_string))) for f in funcs]
	return all(checks)

if __name__=="__main__":
	i = 0
	for l in [x.strip() for x in open("../sudoku_puzzles.txt").readlines()]:	
		i += 1
		solution = solve(l)
		check = check_solves(l, solution)
		valid = is_valid_solution(solution)
		print("problem #", i, check, valid)