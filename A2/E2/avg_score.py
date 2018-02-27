from collections import defaultdict


def main():
	for name in ['snd-cert']:
		for j in range(1, 3):
			for i in range(1, 10):
				with open('syscalls/{}/10/{}.{}.labels'.format(name, name, j), 'r') as label_file, open(
						'syscalls/{}/10/scores/{}.{}.{}.txt'.format(name, name, j, i), 'r') as score_file, open(
						'syscalls/{}/10/scores/{}.{}.{}.scores'.format(name, name, j, i), 'w') as score_write_file:

					counts = defaultdict(int)
					sum = defaultdict(float)
					score_list = [float(score) for score in score_file]

					for i, label in enumerate(label_file):
						counts[label.strip()] += 1
						sum[label.strip()] += score_list[i]

					average = dict()
					for key in counts:
						average[key] = sum[key] / counts[key]

					average_int = {int(k): v for k, v in average.items()}
					print(average_int)
					for key in average_int:
						score_write_file.write(str(average_int[key]) + '\n')


if __name__ == '__main__':
	main()
