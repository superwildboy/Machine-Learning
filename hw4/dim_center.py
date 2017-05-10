# ML 2017 hw4 problem 3.
# Estimation of Intrinsic Dimension
# Return Centers

import math
import numpy as np
import csv
from sys import argv
from sklearn.cluster import KMeans
from gen import *

SAVE = 1

# [d]dimension  [it]iteration
def find_centers(d, it):

	centers = np.zeros(d)	
	for i in range(it):
		var = []
		for d in range(1, 61):
			print("\riteration %d, dimension: %d  " % (i+1, d), end="", flush=True)
			N = np.random.randint(1e4, 1e5)
			layer_dims = [np.random.randint(60, 80), 100]
			data = gen_data(d, layer_dims, N)
			var.append( data.std() )
		centers += np.array(var)
	print("")
	
	centers /= it
	centers = centers.reshape(-1, 1)
	return centers

def output_result(dim):
	
	logdim = []
	for i, d in enumerate(dim):
		ln_d = math.log(d+1)
		logdim.append( [i, ln_d] )

	with open(argv[2], 'w') as f:
		w = csv.writer(f)
		w.writerow(['SetId', 'LogDim'])
		w.writerows(logdim)


# argv: [1]data.npz [2]dim_result.csv
def main():
	
	print("load data.npz...")
	data = np.load(argv[1])

	V = []
	if '--load-V' in argv:
		print("load variance...")
		V = np.load('V.npy')
	else:
		for i in range(200):
			print("\rcompute variance...%d" % (i+1), end="", flush=True)
			S = data[repr(i)]
			V.append( S.std() )
		print("")
		V = np.array(V)
		if SAVE:
			np.save('V.npy', V)

	centers = []
	if '--load-C' in argv:
		print("load centers...")
		centers = np.load('C.npy')
	else:
		print("compute centers...")
		centers = find_centers(60, 100)
		if SAVE: 
			np.save('C.npy', centers)

	print("sort centers of variances...") 
	centers.sort(axis=0)

	print("find closest center...")
	result = []
	for v in V:
		result.append( np.argmin( abs(centers - v)) )

	print("output result...")
	output_result(result)


if __name__ == '__main__':
	main()
