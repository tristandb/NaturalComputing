import numpy as np
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
from keras.models import Sequential
from keras.layers import Dense, Activation
import json
from Gecco2018.source.Python.Framework.Detectors.Sequential_wrapper import Sequential_wrapper

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

	model = Sequential_wrapper()
	model.add(Dense(100, input_dim=9))
	model.add(Activation('relu'))

	model.add(Dense(units=1))
	model.add(Activation('linear'))

	model.compile(loss='mean_squared_error', metrics=['mae', 'acc'], optimizer='rmsprop')

	X_train = train.drop(['Time', 'EVENT'], axis=1).dropna(axis=0)
	y_train = train.dropna(axis=0)['EVENT']

	X_test = test.drop(['Time', 'EVENT'], axis=1).dropna(axis=0)
	y_test = test.dropna(axis=0)['EVENT']

	model.fit(X_train, y_train, epochs=100, verbose=2, validation_data=(X_test, y_test))

	with open('model.txt', 'w') as outfile:
		json.dump(model.history, outfile)


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
