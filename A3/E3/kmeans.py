"""
Select K points as initial centroids.
repeat
    Form K clusters by assigning each point to its closest centroid.
    Recompute the centroid of each cluster.
until Centroids do not change.
"""
import random

import pandas

def main():
    data = pandas.read_csv('iris.csv', header=-1)

if __name__ == '__main__':
    main()





