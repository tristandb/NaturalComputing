import random
import sys
import pickle

N = 10
R = 3
generate_nr_detectors = 100000
use_nr_detectors = 1000
test_size = -1
threshold = 0.1 #0.1 is just some magic value that I thought would work and might not be optimal.

def allsubstr(s, n):
	return [s[i:i + n] for i in range(len(s) - n + 1)]

def allsubblocks(s, n):
	return [s[i*n:(i+1)+n] for i in range(len(s)//n)]

def match(s, detector, r):
	return any([True for i in range(len(s)-r+1) if s[i:i+r] == detector[i:i+r]])

def any_match(s, detectors, r):
	return any([match(s, detector, r) for detector in detectors])

def anomaly_score(s, detectors, r):
	return len([detector for detector in detectors if match(s, detector, r)])

def generate_detectors(alphabet, train, amount, r, n):
	detectors = []
	while len(detectors) < amount:
		detector = ''.join([random.choice(alphabet) for _ in range(n)])
		if not any_match(detector, train, r):
			detectors += [detector]
		sys.stdout.write('Generating b-cells: [' + (int(50 * (len(detectors) / amount)))*'#' + \
			(50-int(50 * (len(detectors) / amount)))*' ' + '] ' + str(len(detectors)) + '/' + str(amount) + '\r')
	return detectors

def evaluate(s, detectors, r, n):
	return sum([anomaly_score(chunk, detectors, r) for chunk in allsubstr(s, n)]) / float(len(allsubstr(s, n)))

def main():
	directory = "snd-cert/"
	pad_char = '!'
	generate = False

	with open(directory + "snd-cert.alpha") as f:
		alphabet = f.read()[:-1]

	if pad_char in alphabet:
		print("Padding character should not be in alphabet. Exiting...")
		return

	with open(directory + "snd-cert.train") as f:
		train = [y for x in [allsubblocks(el, N) for el in f.read().split('\n')] for y in x]

	test = []
	for i in range(1,4):
		with open(directory + "snd-cert.{}.test".format(i)) as f:
			testdata = [sample if len(sample) >= N else sample+pad_char*(N-len(sample)) for sample in f.read().split('\n')]

		with open(directory + "snd-cert.{}.labels".format(i)) as f:
			labels = f.read().split('\n')

		test += zip(testdata, labels)

	ones = len([label for label in labels if label == '1'])
	zeroes = len([label for label in labels if label == '0'])
	print("Ones in test data: {}. Zeroes in test data: {}".format(ones, zeroes))

	if generate == True:
		detectors = generate_detectors(alphabet, train, nr_detectors, R, N)
		pickle.dump(detectors, open('detectors.dmp', 'wb'))
	else:
		print("Loading b-cells from disk...")
		detectors = pickle.load(open('detectors.dmp', 'rb'))
		print("Done.")

	detectors = random.sample(detectors, use_nr_detectors)
	if test_size != -1:
		test = random.sample(test, test_size)

	print("Evaluating {} test cases".format(len(test)))
	correct = 0
	wrong = 0
	for sample, label in test:
		#print(evaluate(sample, detectors, R, N) > 0.1, label)
		res = evaluate(sample, detectors, R, N)
		if res > threshold and label == '1':
			correct += 1
		elif res <= threshold and label == '0':
			correct += 1
		else:
			wrong += 1

		sys.stdout.write("Correct: {}\t Incorrect: {}\r".format(correct, wrong))

if __name__ == "__main__":
	main()