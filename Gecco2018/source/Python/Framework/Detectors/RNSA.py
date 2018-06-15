import numpy as np
import csv
import random
from tqdm import tqdm

from sklearn.preprocessing import StandardScaler

random.seed(42)
np.random.seed(43)

def generate_train_testset(data, division=0.8):
	mask = np.random.rand(len(data)) < division
	return data[mask], data[~mask]

selfData = np.array(list(csv.reader(open("../Data/selfData.csv", "r"), delimiter=","))).astype("float")
nonSelfData = np.array(list(csv.reader(open("../Data/nonSelfData.csv", "r"), delimiter=","))).astype("float")

trainSelfData, testSelfData = generate_train_testset(selfData, division=0.8)
trainNonSelfData, testNonSelfdata = generate_train_testset(nonSelfData, division=0.8)

scaler = StandardScaler()
scaler.fit(np.concatenate((trainSelfData, trainNonSelfData)))

trainSelfData = scaler.fit_transform(trainSelfData)
testSelfData = scaler.fit_transform(testSelfData)
trainNonSelfData = scaler.fit_transform(trainNonSelfData)
testNonSelfData = scaler.fit_transform(testNonSelfdata)


def test(repertoire):
	r = 2.5

	detect = lambda detector, entry: np.linalg.norm(detector - entry) < r

	print("Testing Detectors \n")

	repertoire = np.load("../Data/simple-repertoire.data.npy")

	TP = 0
	FP = 0
	TN = 0
	FN = 0

	for entry in tqdm(testNonSelfdata):
		# print(np.linalg.norm(repertoire[1] - entry))
		res = any([detect(detector, entry) for detector in repertoire])
		if res:
			TP += 1
		else:
			FN += 1

	print("\nTP", TP)
	print("FN", FN)

	for entry in tqdm(testSelfData):
		# print(np.linalg.norm(repertoire[1] - entry))
		res = any([detect(detector, entry) for detector in repertoire])
		if res:
			FP += 1
		else:
			TN += 1

	print("\nFP", FP)
	print("TN", TN)


def train(trainSelfData):
	detectors_num = 10
	repertoire = []
	radius = 2.5

	print("Generating Detectors \n")

	pbar = tqdm(total=detectors_num)

	while len(repertoire) < detectors_num:
		# Randomly generate a candidate detector d_new.
		detector = np.random.normal(loc=0, scale=1, size=9)

		distances = sorted(trainSelfData, key=lambda x: np.linalg.norm(detector - x))

		if  np.linalg.norm(detector - distances[0]) > radius:
			repertoire.append(detector)
			pbar.update(1)

	np.save("../Data/simple-repertoire.data", repertoire)

	return repertoire

if __name__ == '__main__':
	repertoire = train(trainSelfData)
	test(repertoire)
