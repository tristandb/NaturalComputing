import numpy as np
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
import json

from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier

cols_to_norm = ["Tp", "Cl", 'pH', 'Redox', 'Leit', 'Trueb', 'Cl_2', 'Fm', 'Fm_2']

pandas2ri.activate()



def main():
	"""
	Train for 100 epochs
	:return:
	"""
	data = load_dataset()
	data = normalize_data(data, cols_to_norm)
	train, test = generate_train_testset(data)

	X_train = train.drop(['Time', 'EVENT'], axis=1).dropna(axis=0)
	y_train = train.dropna(axis=0)['EVENT']

	X_test = test.drop(['Time', 'EVENT'], axis=1).dropna(axis=0)
	y_test = test.dropna(axis=0)['EVENT']

	model = XGBClassifier()
	model.fit(X_train, y_train)

	print(model)

	y_pred = model.predict(X_test)
	predictions = [round(value) for value in y_pred]

	accuracy = accuracy_score(y_test, predictions)
	print("Accuracy: %.2f%%" % (accuracy * 100.0))



def normalize_data(data, cols_to_norm):
	data[cols_to_norm] = data[cols_to_norm].apply(lambda x: (x - x.min()) / (x.max() - x.min()))
	return data


def generate_train_testset(data, division=0.8):
	mask = np.random.rand(len(data)) < 0.8
	return data[mask], data[~mask]


def load_dataset(filename='../Data/waterDataTraining.RDS'):
	readRDS = robjects.r['readRDS']
	df = readRDS(filename)
	return pandas2ri.ri2py(df)


if __name__ == "__main__":
	main()