import math, pdb
# input strings are 81 charcters long, serailized from left to right, top to bottom 
# with periods for blank spaces and no separator for rows

def rows(puzzle_string):
	return [puzzle_string[x:x+9] for x in range(0, 81, 9)]

def columns(puzzle_string):
	return [puzzle_string[x::9] for x in range(9)]

def boxes(puzzle_string):
	box_start = [0, 3, 6, 27, 30, 33, 54, 57, 60]
	return [puzzle_string[b:b+3] + puzzle_string[b+9:b+12] + puzzle_string[b+18:b+21] for b in box_start]

def get_units(puzzle_string, cell_num):
	row_num = math.floor(cell_num/9)
	col_num = cell_num % 9
	all_boxes = boxes(list(range(81)))
	for n in range(9):
		if cell_num in all_boxes[n]:
			box_num = n
			break
	return rows(puzzle_string)[row_num], columns(puzzle_string)[col_num], boxes(puzzle_string)[box_num]

def unit_cells(cell_num):
	return get_units(list(range(81)), cell_num)

def all_unit_cells(cell_num):
	return set([x for y in unit_cells(cell_num) for x in y])

def is_determined(x):
	return isinstance(x, str)

def set_val(possibles, cell_num, val):
	for i in all_unit_cells(cell_num):
		if i != cell_num and val in possibles[i]:
			if not is_determined(possibles[i]):
				possibles[i].remove(val)
				if len(possibles[i]) == 1:
					possibles[i] = possibles[i][0]
			else:
				print("cant set", cell_num, "=", val, ":", i, "=", possibles[i])
				return False
	possibles[cell_num] = val
	return possibles

def check_if_determined(cell_num, possibles):
	units = unit_cells(cell_num)
	all_unit_vals = set([possibles[x] for x in all_unit_cells(cell_num) if isinstance(possibles[x], str)])
	for unit in units:
		# ignore the cell's own possible values
		unit.remove(cell_num)
		unit_possibles = set([x for y in [possibles[u] for u in unit] for x in y])
		for p in possibles[cell_num]:
			if p not in unit_possibles and p not in all_unit_vals:
				# the cell must have value p
				return p
	return None

def make_guess(possibles, previous_guesses):

	sort_func = lambda x: str(len(x[1])) + "-" + str(99 - possibles.count(x[1])) + "-" + str(x[0])
	guesses = sorted([(i, possibles[i]) for i in range(81) if not is_determined(possibles[i])], key=sort_func)

	if guesses:
		guess = guesses[0]
		cell_num = guess[0]
		val = guess[1][0]
		revert = possibles
		if len(revert[cell_num]) > 2:
			revert[cell_num].remove(val)
		else: 
			revert = set_val(revert, cell_num, val)
		guess = {
			'cell_num': cell_num,
			'val': val,
			'revert': revert
		}
		print("guessing  ", cell_num, "=", val)
		
		possibles = set_val(possibles, cell_num, val)
		if not possibles:
			return revert_guess(previous_guesses)
		previous_guesses.append(guess)
		return possibles, previous_guesses
	else:
		return revert_guess(previous_guesses)

def revert_guess(previous_guesses):
	print("going back one")
	last_guess = previous_guesses.pop()
	possibles = last_guess['revert']
	return possibles, previous_guesses

class Sudoku(object):

	@classmethod
	def solve(self, puzzle_string):
		print("solving", puzzle_string)
		possibles, nums = [], "123456789"

		for i in range(81):
			if puzzle_string[i] == ".":
				used = set([x for y in get_units(puzzle_string, i) for x in y])	
				possibles.append([n for n in nums if n not in used])
			else:
				possibles.append(puzzle_string[i]) 

		must_guess = False
		previous_guesses = []	

		while not all(is_determined(x) for x in possibles):
			print([] in possibles, possibles)
			if not must_guess:
				must_guess = True
				for i in [x for x in range(81) if not is_determined(possibles[x])]:
					val = check_if_determined(i, possibles)
					if val:
						print("determined", i, "=", val)
						possibles = set_val(possibles, i, val)
						must_guess = False
			else:
				possibles, previous_guesses =  make_guess(possibles, previous_guesses)
				must_guess = False
					
		return "".join(possibles)

	@classmethod
	def check_solution(self, puzzle_string, solution_string):
		solution_matches_puzzle = all([puzzle_string[i] in (solution_string[i], ".") for i in range(81)])
		return self.is_valid_solution(solution_string) and solution_matches_puzzle

	@classmethod
	def is_valid_solution(self, solution_string):
		
		def check_unit(unit):
			return set(unit) == set("123456789")

		funcs = [rows, columns, boxes]
		checks = [all(map(lambda u: check_unit(u), f(solution_string))) for f in funcs]

		return all(checks)

if __name__=="__main__":
	import sys
	i = solved = unsolved = 0
	for l in [x.strip() for x in open("../sudoku_puzzles.txt").readlines()]:	
		i+=1
		solution = Sudoku.solve(l)
		check = Sudoku.check_solution(l, solution)
		valid = Sudoku.is_valid_solution(solution)
		if not check:
			sys.exit()
		print(i, check, valid)
