import numpy as np
import csv
from tqdm import tqdm
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler

def generate_train_testset(data, division=0.8):
	mask = np.random.rand(len(data)) < division
	return data[mask], data[~mask]

selfData = np.array(list(csv.reader(open("../Data/selfData.csv", "r"), delimiter=","))).astype("float")
nonSelfData = np.array(list(csv.reader(open("../Data/nonSelfData.csv", "r"), delimiter=","))).astype("float")

trainSelfData, testSelfData = generate_train_testset(selfData, division=0.8)
trainNonSelfData, testNonSelfdata = generate_train_testset(nonSelfData, division=0.8)

scaler = StandardScaler()
scaler.fit(np.concatenate((trainSelfData, trainNonSelfData)))
print(scaler.mean_)
print(scaler.var_)

trainSelfData = scaler.fit_transform(trainSelfData)
testSelfData = scaler.fit_transform(testSelfData)
trainNonSelfData = scaler.fit_transform(trainNonSelfData)
testNonSelfData = scaler.fit_transform(testNonSelfdata)

def test():
	r = 2.5

	detect = lambda detector, entry: np.linalg.norm(detector - entry) < r

	repertoire = np.load("../Data/repertoire.data.npy")

	TP = 0
	FP = 0
	TN = 0
	FN = 0

	for entry in tqdm(testNonSelfdata):
		#print(np.linalg.norm(repertoire[1] - entry))
		res = any([detect(detector, entry) for detector in repertoire])
		if res:
			TP += 1
		else:
			FN += 1

	print("\nTP", TP)
	print("FN", FN)


	for entry in tqdm(testSelfData):
		#print(np.linalg.norm(repertoire[1] - entry))
		res = any([detect(detector, entry) for detector in repertoire])
		if res:
			FP += 1
		else:
			TN += 1

	print("FP", FP)
	print("TN", TN)

def train():
	mu_d = lambda x, detector, r: -1 * np.linalg.norm(detector - x)**2 / (2 * r**2)

	# TODO: NORMALIZE

	num_iter = 10
	num_detec = 500
	r = 2.5
	t = 5
	eta = 1
	tau = 750

	repertoire = [(0, np.random.normal(loc=0, scale=1, size=9)) for _ in range(num_detec)]

	for i in range(num_iter):
		for j, (age, detector) in enumerate(repertoire):
			print("Iteration", i, "Detector", j)

			knn = sorted(trainSelfData, key=lambda x: np.linalg.norm(detector - x))[:20]
			nearestSelf = np.mean(knn, axis=0)
			if np.linalg.norm(detector-nearestSelf) < r:
				dir = detector - nearestSelf

				if age > t:
					repertoire[j] = (0, np.random.normal(loc=0, scale=1, size=9))
				else:
					detector += eta * dir
					repertoire[j] = (age + 1, detector)

			else:
				numerator = np.sum([mu_d(d, detector, r)*(detector - d) for a, d in repertoire], axis=0)
				demoninator = np.sum([mu_d(d, detector, r) for a, d in repertoire], axis=0)
				dir = numerator / demoninator
				detector += eta * dir
				repertoire[j] = (0, detector)

		eta = eta * np.exp(-1*i / tau)

		np.save("../Data/repertoire-cycle-{}.data".format(i), [detector for age, detector in repertoire])

if __name__ == "__main__":
	train()
	# test()