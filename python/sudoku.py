import math

class Sudoku(object):
	# input strings are all 81 numerals long, serailized from left to right, top to bottom 
	# with periods for blank spaces and no separator for rows

	def rows(string):
		return [string[x:x+9] for x in range(0, 81, 9)]

	def columns(string):
		return [string[x::9] for x in range(9)]

	def boxes(string):
		box_start = [0, 3, 6, 27, 30, 33, 54, 57, 60]
		return [string[b:b+3] + string[b+9:b+12] + string[b+18:b+21] for b in box_start]

	@classmethod
	def solve(self, puzzle_string):

		# a unit refers to a row, column, or box

		def unit_nums(i):
			row_num = math.floor(i/9)
			col_num = i % 9
			boxes = self.boxes(list(range(81)))
			for n in range(9):
				if i in boxes[n]:
					box_num = n
					break
			return row_num, col_num, box_num

		def get_units(string, i):
			row, column, box = unit_nums(i)
			return self.rows(string)[row], self.columns(string)[column], self.boxes(string)[box]

		def check_if_determined(i, possibles):
			for unit in get_units(list(range(81)), i):
				# ignore the cell's own possible values
				unit.remove(i)
				unit_possibles = set([n for l in [possibles[u] for u in unit] for n in l])
				for p in possibles[i]:
					if p not in unit_possibles:
						# the cell must have value p
						return p
			return None

		def make_guess(possibles, solution, previous_guesses):
			sort_func = lambda x: str(len(x[1])) + "-" + str(99 - possibles.count(x[1])) + "-" + str(x[0])
			guesses = sorted([(i, possibles[i]) for i in range(81) if len(possibles[i]) > 1], key=sort_func)
			i = j = 0
			next = (guesses[i][0][j], guesses[i][1])
			while next in [(g.n, g.i) for g in previous_guesses]:
				if len(guesses[i][0]) > j + 1:
					j += 1
				else:
					j = 0
					i += 1
				next = (guesses[i][0][j], guesses[i][1])

			
			guess = {
				'i': 
				'n':
				'possibles': possibles,
				'solution': solution
			}
			solution = solution[:i] + n + solution[i+1:]
			possibles[i] = n
			previous_guesses.append(guess)
			return possibles, solution, previous_guesses


		solution = puzzle_string
		possibles, nums = [], "123456789"

		for i in range(81):
			if solution[i] == ".":
				taken = [n for u in get_units(solution, i) for n in u]
				taken = set([x for y in taken for x in y])
				possibles.append([n for n in nums if n not in taken])
			else:
				possibles.append(solution[i]) 

		must_guess = False
		previous_guesses = []	

		while "." in solution:(guesses[i][0][j], guesses[i][1])
			if not must_guess:
				must_guess = True
				for i in range(81):
					if solution[i] == ".":
						check = check_if_determined(i, possibles)
						if check:
							print("determined", i, check)
							solution = solution[:i] + check + solution[i+1:]
							possibles[i] = check
							must_guess = False
			else:
				possibles, solution, previous_guesses = make_guess(possibles, solution, previous_guesses)				
				


		return solution

	@classmethod
	def check_solution(self, puzzle_string, solution_string):
		solution_matches_puzzle = all([puzzle_string[i] in (solution_string[i], ".") for i in range(81)])
		return self.is_valid_solution(solution_string) and solution_matches_puzzle

	@classmethod
	def is_valid_solution(self, solution_string):
		
		def check_unit(string):
			return sum([int(i) for i in string]) == 45

		funcs = [self.rows, self.columns, self.boxes]
		checks = [all(map(lambda u: check_unit(u), f(solution_string))) for f in funcs]

		return all(checks)