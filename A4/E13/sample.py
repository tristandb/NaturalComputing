from collections import Counter

from sklearn.utils import resample
import matplotlib.pyplot as plt
import numpy as np
from tqdm import trange

def duplicates(array):
	counts = Counter(array)
	return len(counts.values()) - sum(counts.values())

def main():
	means = []
	for i in trange(1, 100):
		mean = []
		for _ in range(1000):
			x = np.arange(0, i)
			sample = resample(x, n_samples=i)
			mean.append(-1 * (((duplicates(sample))) / i))

		means.append(np.mean(mean))

	axes = plt.gca()
	axes.set_ylim([0, 1])
	plt.plot(means)
	plt.xlabel("Bootstrap size N")
	plt.ylabel("Out-of-bag size")
	plt.title("Left-out sample size versus bootstrap sample size")
	plt.savefig("bootstrap.png")
	plt.show()
if __name__ == '__main__':
	main()
