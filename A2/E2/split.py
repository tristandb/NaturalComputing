N = 10
K = 10  # Shift size


def build_substrings(line, size):
	result = []
	if size <= len(line):
		result.extend([line[:size]])
		result.extend(build_substrings(line[size:], size))
	elif line:
		result.extend([line])

	return result


def main():
	for name in ['snd-cert', 'snd-unm']:
		directory = 'syscalls/{}/'.format(name)
		# Generate a sliding window of N over the training dataset
		with open(directory + '{}.train'.format(name)) as train_file:
			train = []
			for train_line in train_file:
				train_line = train_line.strip()
				train += build_substrings(train_line, N)
			train_file.close()

		# Save the generated training dataset to file
		with open(directory + '{}/{}.train'.format(N, name), 'w') as train_save_file:
			for train_line in train:
				train_save_file.write(train_line + '\n')
			train_save_file.close()

		# Loop all three files
		for i in range(3):
			# Generate a slinding window of N over the test dataset
			with open(directory + '{}.{}.test'.format(name, i + 1)) as test_file, open(
							directory + '{}.{}.labels'.format(name, i + 1)) as labels_file, open(
							directory + '{}/{}.{}.test'.format(N, name, i + 1), 'w') as test_save_file, open(
							directory + '{}/{}.{}.labels'.format(N, name, i + 1), 'w') as labels_save_file:
				test = []
				labels = []
				for i, (test_line, labels_line) in enumerate(zip(test_file, labels_file)):
					test_line = test_line.strip()
					test_substrings = build_substrings(test_line, N)
					if len(test_substrings[-1]) == N:
						for chunk in test_substrings:
							test_save_file.write(chunk + '\n')
							labels_save_file.write(str(i) + '\n')
					else:
						test_substrings[-1] = test_substrings[-1] + "-"  * (N - len(test_substrings[-1]))
						for chunk in test_substrings:
							test_save_file.write(chunk + '\n')
							labels_save_file.write(str(i) + '\n')

				test_file.close()
				labels_file.close()
				test_save_file.close()
				labels_save_file.close()


if __name__ == '__main__':
	main()
