N = 6
R = 3
nr_detectors = 100000

def allsubstr(s, n):
	if len(s) < n:
		return []
	return [s[i:i + n] for i in range(len(s) - n + 1)]

def match(s, detector, r):
	#Returns whether there is an r-contiguous match of <s> on <detector>
	pass

def anomaly_score(s, detectors):
	#Returns the number of detectors that <s> matches with.
	pass

def generate_detectors(alphabet, train, amount):
	#Randomly generate <amount> detectors using <alphabet> 
	#while discarding detectors that match on elements in <train>
	pass

def evaluate(s, detectors):
	return sum([anomaly_score(chunk, detectors) for chunk in allsubstr(s, N)]) / len(allsubstr(s, N))

def main():
	directory = "snd-cert/"

	with open(directory + "snd-cert.alpha") as f:
		alphabet = f.read()[:-1]

	with open(directory + "snd-cert.train") as f:
		train = [y for x in [allsubstr(el, N) for el in f.read().split('\n')] for y in x]

	test = []
	for i in range(1,4):
		with open(directory + "snd-cert.{}.test".format(i)) as f:
			testdata = f.read().split('\n')
		with open(directory + "snd-cert.{}.labels".format(i)) as f:
			labels = f.read().split('\n')
		test += zip(testdata, labels)

	detectors = generate_detectors(alphabet, train, nr_detectors)

	for sample, label in test:
		print(evaluate(sample, detectors), label)

if __name__ == "__main__":
	main()