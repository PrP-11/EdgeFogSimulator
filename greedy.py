# QAP problem
# 2-opt heuristic

from copy import copy, deepcopy
from random import randint
import math
# import constants
import re
import sys
import os
import time

def cost(matching, d, f):
	total = 0
	size = len(matching)
	for i in range(0, size):
		for j in range(0, size):
			if i != j:
				x = get(matching[i], matching[j], f) * get(i, j, d)
				total = total + x
	return total

def get(first, second, array):
	return array[ int(math.sqrt(len(array))) * first + second]

def iteration(m, d, f):
	best_matching = []
	best_matching = copy(m)
	best_path = cost(m, d, f)
	size = len(m)
	i = 0
	#print m
	for i in range(0, size-1):
		for j in range(i+1, size):
			posI = m.index(i)
			posJ = m.index(j)
			m[posI] = j
			m[posJ] = i
			current_path = cost(m, d, f)
			if(current_path < best_path):
				best_matching = copy(m)
				best_path = current_path
	print ('final solution: ', best_matching)
	print ('final cost: ', best_path)

def get_minor(list, n):
	for i in range(0, n):
		if i not in list:
			return i
	return None

# greedy algorithm to generate initial solution
def initial_solution(distance, flow):
	n = int(math.sqrt(len(distance)))
	best_cost_final = 0
	m_x = []

	for q in range(0, n):
		m = [q]
		m2 = [q]
		j = 0
		while j < n-1:
			k = get_minor(m, n)
			m.append(k)
			m2 = copy(m)
			best_cost = cost(m, distance, flow)
			if j == 0:
				best_cost_final = best_cost
			for i in range(0, n):
				if i not in m:
					m2[len(m2)-1] = i
					c = cost(m2, distance, flow)
					if c < best_cost:
						m[len(m)-1] = i
						best_cost = c
			j = j + 1

		if best_cost < best_cost_final:
			best_cost_final = best_cost
			m_final = copy(m)

		m_x.append(m)

	# check the best greedy initial solution, considering solutions starting with 0, 1, 2 .. n
	b_array = copy(m_x[0])
	b_cost = cost(b_array, distance, flow)

	for i in range(1, n):
		cus = cost(m_x[i], distance, flow)
		if cus < b_cost:
			b_cost = cus
			b_array = copy(m_x[i])

	print ('initial solution: ', b_array)
	print ('initial cost: ', b_cost)

	return b_array


#################

filepath = "Files/"+ sys.argv[1]
totalNodes = sys.argv[1]

with open(filepath+"/device_conn") as f:
    device_conn = [[int(num) for num in line.split()] for line in f]

with open(filepath+"/device_proc") as f:
    for line in f:
        device_proc = [int(i) for i in line.split()]

with open(filepath+"/job_conn") as f:
    job_conn = [[int(num) for num in line.split()] for line in f]

with open(filepath+"/job_size") as f:
    for line in f:
        job_size = [int(i) for i in line.split()]

start_time = time.time()
from itertools import chain
distance = list(chain.from_iterable(device_conn))
flow = list(chain.from_iterable(job_conn))
# read_file()
initial_matching = initial_solution(distance, flow)
iteration(initial_matching, distance, flow)
print("Time Taken", time.time()-start_time)
# print(distance)
