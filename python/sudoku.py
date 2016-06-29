import math

class Sudoku(object):
	# input strings are 81 charcters long, serailized from left to right, top to bottom 
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

		def get_units(string, cell_num):
			row_num = math.floor(cell_num/9)
			col_num = cell_num % 9
			boxes = self.boxes(list(range(81)))
			for n in range(9):
				if cell_num in boxes[n]:
					box_num = n
					break
			return self.rows(string)[row_num], self.columns(string)[col_num], self.boxes(string)[box_num]

		def check_if_determined(cell_num, possibles):
			for unit in get_units(list(range(81)), cell_num):
				# ignore the cell's own possible values
				unit.remove(cell_num)
				unit_possibles = set([n for l in [possibles[u] for u in unit] for n in l])
				for p in possibles[cell_num]:
					if p not in unit_possibles:
						# the cell must have value p
						return p
			return None

		def make_guess(possibles, solution, previous_guesses):
			sort_func = lambda x: str(len(x[1])) + "-" + str(99 - possibles.count(x[1])) + "-" + str(x[0])
			guesses = sorted([(i, possibles[i]) for i in range(81) if len(possibles[i]) > 1], key=sort_func)
			previous = [g['cell_num'] for g in previous_guesses]
			i = val_index = 0
			next = guesses[i][0]

			while next in previous:
				if len(guesses[i][1]) > val_index + 1:
					val_index += 1
				elif i + 1 < len(guesses):
					val_index = 0
					i += 1
				else: # out of guesses, go back up the guessing tree one step
					print("going back one")
					possibles, solution, previous_guesses = previous_guesses[-1]['possibles'], previous_guesses[-1]['solution'], previous_guesses[-1]['history']
					return possibles, solution, previous_guesses

				next = guesses[i][0]

			guess = {
				'cell_num': guesses[i][0],
				'val': guesses[i][1][val_index],
				'possibles': possibles,
				'solution': solution,
				'history': previous_guesses
			}
			print("guessing  ", guess['cell_num'], "=", guess['val'])
			solution = solution[:i] + guess['val'] + solution[i + 1:]
			possibles[i] = guess['val']
			previous_guesses.append(guess)
		
			return possibles, solution, previous_guesses

		solution = puzzle_string
		possibles, nums = [], "123456789"

		for i in range(81):
			if solution[i] == ".":
				used = [n for u in get_units(solution, i) for n in u]
				used = set([x for y in used for x in y])
				possibles.append([n for n in nums if n not in used])
			else:
				possibles.append(solution[i]) 

		must_guess = False
		previous_guesses = []	

		while "." in solution:
			if not must_guess:
				must_guess = True
				for i in range(81):
					if solution[i] == ".":
						val = check_if_determined(i, possibles)
						if val:
							print("determined", i, "=", val)
							solution = solution[:i] + val + solution[i+1:]
							possibles[i] = val
							must_guess = False
			else:
				possibles, solution, previous_guesses =  make_guess(possibles, solution, previous_guesses)
				must_guess = False
					
		return solution

	@classmethod
	def check_solution(self, puzzle_string, solution_string):
		solution_matches_puzzle = all([puzzle_string[i] in (solution_string[i], ".") for i in range(81)])
		print(self.is_valid_solution(solution_string), solution_matches_puzzle)
		return self.is_valid_solution(solution_string) and solution_matches_puzzle

	@classmethod
	def is_valid_solution(self, solution_string):
		
		def check_unit(string):
			print (string, sum([int(i) for i in string]))
			return sum([int(i) for i in string]) == 45

		funcs = [self.rows, self.columns, self.boxes]
		checks = [all(map(lambda u: check_unit(u), f(solution_string))) for f in funcs]

		return all(checks)