from scipy.io import loadmat
from tqdm import tqdm
import numpy as np

"""
This program implements CORAL
CORAL, which stands for Correlation Alignment Method, finds a linear transformation A of the source features that 
minimize the distance between the covariance of source and target.
"""

# Prepare data
amazon = loadmat('office-vgg/office-caltech-vgg-sumpool-amazon-fc6.mat')
caltech = loadmat('office-vgg/office-caltech-vgg-sumpool-amazon-fc6.mat')
dslr = loadmat('office-vgg/office-caltech-vgg-sumpool-amazon-fc6.mat')
webcam = loadmat('office-vgg/office-caltech-vgg-sumpool-amazon-fc6.mat')

# Run experiments
rounds = 20
Xtt = dslr['x']
Ytt = dslr['y'][0]

for _ in tqdm(range(rounds)):

	Xr = amazon['x']
	Yr = amazon['y'][0]

	# CORAL
	cov_source = np.cov(Xr) + np.eye(len(Xr))
	cov_target = np.cov(Xtt) + np.eye(len(Xtt))
