import numpy as np
import csv
import random
from tqdm import tqdm

from sklearn.preprocessing import MinMaxScaler

random.seed(42)
np.random.seed(43)

def generate_train_testset(data, division=0.8):
	mask = np.random.rand(len(data)) < division
	return data[mask], data[~mask]

selfData = np.array(list(csv.reader(open("../Data/selfData.csv", "r"), delimiter=","))).astype("float")
nonSelfData = np.array(list(csv.reader(open("../Data/nonSelfData.csv", "r"), delimiter=","))).astype("float")

trainSelfData, testSelfData = generate_train_testset(selfData, division=0.8)
trainNonSelfData, testNonSelfdata = generate_train_testset(nonSelfData, division=0.8)

scaler = MinMaxScaler()
scaler.fit(np.concatenate((trainSelfData, trainNonSelfData)))

trainSelfData = scaler.fit_transform(trainSelfData)
testSelfData = scaler.fit_transform(testSelfData)
trainNonSelfData = scaler.fit_transform(trainNonSelfData)
testNonSelfData = scaler.fit_transform(testNonSelfdata)

np.set_printoptions(threshold=np.nan)

np.set_printoptions(suppress=True)

print(np.amax(trainNonSelfData))
print(np.amin(testSelfData))
tqdm.monitor_interval = 0

radius = 0.4

def printtofile():
	np.set_printoptions(suppress=True)
	two = np.ones((len(testNonSelfData), 1)) * 2
	zero = np.zeros((len(testSelfData), 1))
	c = np.hstack((testNonSelfData, two))
	d = np.hstack((testSelfData, zero))
	concatted = np.concatenate((c, d))

	a = [9, len(concatted)]

	print(len(concatted))
	print(len(trainSelfData))

	np.savetxt('test.txt', concatted, fmt='%f %f %f %f %f %f %f %f %f %i')

	np.savetxt('train.txt', trainSelfData, fmt='%f')

def test():

	detect = lambda detector, entry: np.linalg.norm(detector - entry) < radius

	print("Testing Detectors \n")

	repertoire = np.load("../Data/simple-repertoire.data.npy")

	print(repertoire)

	TP = 0
	FP = 0
	TN = 0
	FN = 0

	for entry in tqdm(trainNonSelfData):
		# print(np.linalg.norm(repertoire[1] - entry))
		res = any([detect(detector, entry) for detector in repertoire])
		if res:
			TP += 1
		else:
			FN += 1

	print("\nTP", TP)
	print("FN", FN)

	for entry in tqdm(trainSelfData):
		res = any([detect(detector, entry) for detector in repertoire])
		if res:
			FP += 1
		else:
			TN += 1

	print("\nFP", FP)
	print("TN", TN)

def mu(x, d):
	power = -1 * ((np.linalg.norm((d - x)) ** 2)/(2*radius**2))
	return np.exp(power)

def train(data):
	repertoire = []

	data = np.array(data)

	print("Generating Detectors \n")


	num_iter = 15
	num_detectors = 1000

	eta = 1.0
	eta_orig = 1.0

	tau = 1.0

	t_maxage = 5

	# Generate a random population of detectors
	detectors = [np.random.uniform(low=0.0, high=1.0, size=9) for _ in range(num_detectors)]
	detector_ages = np.zeros(num_detectors)

	pbar = tqdm(total=num_detectors * num_iter)


	for j in range(num_iter):
		for i, detector in enumerate(detectors):
			distances = np.array([np.linalg.norm(detector - x) for x in data])

			nearcells = data[distances.argsort()[::-1]][:20]

			nearestself = np.mean(nearcells, axis = 0)

			if np.linalg.norm(detector - nearestself) < radius:
				dir = detector - nearestself
				if detector_ages[i] > t_maxage:
					detector_ages[i] = 0
					detectors[i] = np.random.uniform(low=0.0, high=1.0, size=9)
				else:
					detector_ages[i] += 1
					detectors[i] = detector + eta * dir
			else:
				detector_ages[i] = 0
				numerator = np.sum([mu(da, detector) * (detector - da) for da in detectors])
				denominator = np.sum([mu(da, detector) for da in detectors])
				dir = numerator / denominator
				detectors[i] = detector + eta * dir

			pbar.update(1)

		eta = eta_orig * np.exp(-j/tau)

	print(detectors)

	np.save("../Data/simple-repertoire.data", detectors)
	return detectors


if __name__ == '__main__':
	# printtofile()
	repertoire = train(trainSelfData)
	test()
	pass