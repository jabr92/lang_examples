from math import floor
import pdb, copy
# input strings are 81 charcters long, serailized from left to right, top to bottom 
# with periods for blank spaces and no separator for rows

def print_board(s, p):
	for x in range(0, 81, 9):
		print(s, [x  if is_determined(x) else "." for x in p[x:x+9]])
	print("")

def rows(puzzle_string):
	return [puzzle_string[x:x+9] for x in range(0, 81, 9)]

def columns(puzzle_string):
	return [puzzle_string[x::9] for x in range(9)]

def boxes(puzzle_string):
	box_start = [0, 3, 6, 27, 30, 33, 54, 57, 60]
	return [puzzle_string[b:b+3] + puzzle_string[b+9:b+12] + puzzle_string[b+18:b+21] for b in box_start]

def units_of(puzzle_string, cell_num):
	row_num = floor(cell_num/9)
	col_num = cell_num % 9
	all_boxes = boxes(list(range(81)))
	for n in range(9):
		if cell_num in all_boxes[n]:
			box_num = n
			break
	return rows(puzzle_string)[row_num], columns(puzzle_string)[col_num], boxes(puzzle_string)[box_num]

def common_cells(cell_num):
	return set(x for y in units_of(list(range(81)), cell_num) for x in y if x != cell_num)

def is_determined(val):
	return isinstance(val, str)

def set_val(possibles, cell_num, val):
	possibles[cell_num] = val
	for i in [x for x in common_cells(cell_num) if not is_determined(possibles[x])]:
		options = possibles[i]
		if val in options:
			possibles[i].remove(val)
			if len(possibles[i]) == 1:
				possibles[i] = possibles[i][0]
	return possibles

def scan_possibles(possibles):
	scan = True
	while scan:
		scan = False
		for i in [x for x in range(81) if not is_determined(possibles[x])]:
			for unit in units_of(list(range(81)), i):
				# ignore the cell's own possible values
				unit.remove(i)
				unit_possibles = set(x for y in [possibles[u] for u in unit] for x in y)
				for p in possibles[i]:
					if p not in unit_possibles:
						possibles = set_val(possibles, i, p)
						scan = True
	return possibles

def solve(puzzle_string):
	# print("solving", puzzle_string)
	possibles, nums = [], "123456789"

	for i in range(81):
		val = puzzle_string[i]
		if val == ".":
			taken = set([x for y in units_of(puzzle_string, i) for x in y])	
			possibles.append([n for n in nums if n not in taken])
		else:
			possibles.append(val)

	def has_duplicate_val(p):
		for i in [x for x in range(81) if is_determined(p[x])]:
			common_vals = [p[x] for x in common_cells(i) if is_determined(p[x])]
			if p[i] in common_vals:
				return True
		return False

	revert_points = []
	possibles = scan_possibles(possibles)
	sort_func = lambda x: str(len(x[1])) + "-" + str(99 - possibles.count(x[1])) + "-" + str(x[0])
	duplicate = False

	while not all(is_determined(x) for x in possibles) or duplicate:
		if duplicate:
			possibles = revert_points.pop()
		else:
			guess = sorted([(i, possibles[i]) for i in range(81) if not is_determined(possibles[i])], key=sort_func)[0]
			cell_num, val = guess[0], guess[1][0]
			# print("guessing  ", cell_num, "=", val)
			revert = copy.deepcopy(possibles)
			revert[cell_num].remove(val)
			if len(revert[cell_num]) == 1:
				revert = set_val(revert, cell_num, revert[cell_num][0])
			revert_points.append(revert)
			# pdb.set_trace()
			possibles = scan_possibles(set_val(possibles, cell_num, val))
		duplicate = has_duplicate_val(possibles)
					
	return "".join(possibles)

def check_solves(puzzle_string, solution_string):
	return all([puzzle_string[i] in (solution_string[i], ".") for i in range(81)])

def is_valid_solution(solution_string):
	
	def check_unit(unit):
		return set(unit) == set("123456789")

	funcs = [rows, columns, boxes]
	checks = [all(map(lambda u: check_unit(u), f(solution_string))) for f in funcs]

	return all(checks)

if __name__=="__main__":
	i = 0
	for l in [x.strip() for x in open("../sudoku_puzzles.txt").readlines()]:	
		i += 1
		solution = solve(l)
		check = check_solves(l, solution)
		valid = is_valid_solution(solution)
		print("problem", i, check, valid)
		# print_board("p:", l)
		# print_board("s:", solution)
		if not (check and valid):
			break