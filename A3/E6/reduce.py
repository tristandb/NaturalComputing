import numpy as np

flatten = lambda l: [item for sublist in l for item in sublist]


def check(sudoku):
	rows = [sudoku[(i * 9):(i * 9) + 9] for i in range(9)]
	columns = [[sudoku[i + j * 9] for j in range(9)] for i in range(9)]
	blocks = [flatten(
		[[[[sudoku[i * 3 + j * 27 + x + y * 9] for x in range(3)] for y in range(3)] for i in range(3)] for j in
		 range(3)][x][y]) for x in range(3) for y in range(3)]

	if 0 in sudoku:
		return False

	for row in rows:
		if len(row) != len(list(set(row))):
			return False
	for column in columns:
		if len(column) != len(list(set(column))):
			return False
	for block in blocks:
		if len(block) != len(list(set(block))):
			return False

	return True

def simplify(sudoku):
	changed = True
	while changed:
		if check(sudoku):
			break

		rows = [sudoku[(i * 9):(i * 9) + 9] for i in range(9)]
		columns = [[sudoku[i + j * 9] for j in range(9)] for i in range(9)]
		blocks = [flatten(
			[[[[sudoku[i * 3 + j * 27 + x + y * 9] for x in range(3)] for y in range(3)] for i in range(3)] for j in
			 range(3)][x][y]) for x in range(3) for y in range(3)]

		antgrid = [[x for x in range(1, 10)] if cell == 0 else [cell] for cell in sudoku]

		for i in range(81):
			if len(antgrid[i]) == 1:
				continue

			invalid_digits = []
			for digit in antgrid[i]:
				if digit in rows[i // 9] or \
								digit in columns[i % 9] or \
								digit in blocks[((i % 9) // 3) + 3 * ((i // 9) // 3)]:
					invalid_digits += [digit]

			for digit in invalid_digits:
				antgrid[i].remove(digit)

		new_sudoku = [antgrid[i][0] if len(antgrid[i]) == 1 else 0 for i in range(81)]
		changed = not np.any(new_sudoku == sudoku)
		sudoku = new_sudoku

	return sudoku
