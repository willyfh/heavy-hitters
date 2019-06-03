"""
__author__  = Willy Fitra Hendria
"""

from collections import Counter
import timeit

def misra_gries(data, n, m, tau):
	""" for reference:
	https://en.wikipedia.org/wiki/Misra%E2%80%93Gries_summary
	"""
	count = Counter()
	phi = tau/m
	k = m/(tau-1)
	for d in data:
		d = int(d.rstrip('\n'))
		if len(count)< k-1 or d in count:
			count[d] += 1
		else:
			for key in list(count.keys()):
				count[key] -= 1
				if count[key] == 0:
					del count[key]
	return count
		
def lossy_counting(data, m, epsilon):
	""" for reference:
	https://en.wikipedia.org/wiki/Lossy_Count_Algorithm
	"""
	count = Counter()
	bucket_ids = {}
	current_bucket_id = 1
	i = 0
	w = int(1/epsilon)
	phi = tau/m
	assert epsilon >=0 and epsilon <= phi, "epsilon must be bigger than 0 and smaller than phi"
	# processing
	for d in data:
		d = int(d.rstrip('\n'))
		i += 1
		if d in count:
			count[d] += 1
		else:
			count[d] = 1
			bucket_ids[d] = current_bucket_id - 1
		if i % w ==0:
			for key in list(count.keys()):
				if count[key] == 1:
					del count[key]
					del bucket_ids[key]
				else:
					count[key] -= 1	
			current_bucket_id += 1
	# output
	for key in list(count.keys()):
		if count[key] < (phi - epsilon) * m:
			del count[key]
	return count

def brute_force(data):
	""" brute force algorithm for comparison
	"""
	count = Counter()
	for d in data:
		d = int(d.rstrip('\n'))
		count[d] += 1
	return count

def get_frequent_items(hash_table, m, tau):
	""" to get exact frequent items after doing brute force 
	"""
	phi = tau/m
	frequent_items = {}
	for key in list(hash_table.keys()):
		if hash_table[key]/m >= phi:
			frequent_items[key] = hash_table[key]
	return frequent_items


def evaluate(exact_freqs, est_freqs, flag):
	""" to evaluate heavy hitters
	"""
	sum = 0
	m = 0
	max = -1
	for key in exact_freqs.keys():
		diff = abs(exact_freqs[key] - est_freqs[key])
		sum += diff
		if flag : # evaluation metric #1
			if exact_freqs[key] > 0:
				m += 1
		else: # evaluation metric #2
			m += 1
		if max < diff:
			max = diff
	q1 = sum/m
	q2 = max
	print("q1 = ",q1)
	print("q2 = ",q2)

def read_file(file):
	data = open(file, 'r')
	n = int(data.readline())
	m = int(data.readline())
	tau = int(data.readline())
	return n,m,tau,data
	
	
"""
File should have following format:
n m τ a1 a2 a3 . . . am

where n defines the universe, m the number of items ai
in the stream, and τ is an absolute frequency threshold (i.e. φ = τ /m).
"""
filename = "data_stream.txt"

print("\nreading file...")
n,m,tau,data = read_file(filename)
print("n = ",n)
print("m = ",m)
print("tau = ",tau)

epsilon_lossy_counting = float(input("\ninput epsilon (lossy counting) between interval 0 - phi ("+str(tau/m)+"):"))
assert epsilon_lossy_counting >= 0 and epsilon_lossy_counting <= tau/m, "epsilon must be bigger than 0 and smaller than phi"

print("\n-------------------")
print("brute force...")
print("-------------------")
start = timeit.default_timer()
count = brute_force(data)
exact_frequent_items = get_frequent_items(count, m, tau)
stop = timeit.default_timer()
print("Exact Frequent Items:")
print(exact_frequent_items)
print("\nTime: ", stop - start)  

print("\n-------------------")
print("misra gries...")
print("-------------------")
data.seek(0)
start = timeit.default_timer()
frequent_items = misra_gries(data, n, m, tau)
stop = timeit.default_timer()
print("Frequent Items:")
print(frequent_items)
print("\nTime: ", stop - start)
print("\nFirst evaluation....")
evaluate(count, frequent_items, True)
print("\nSecond evaluation....")
evaluate(exact_frequent_items, frequent_items, False)

print("\n-------------------")
print("lossy counting...")
print("-------------------")
data.seek(0)
start = timeit.default_timer()
frequent_items = lossy_counting(data, m, epsilon_lossy_counting)
stop = timeit.default_timer()
print("Frequent Items:")
print(frequent_items)
print("\nTime: ", stop - start)
print("\nFirst evaluation....")
evaluate(count, frequent_items, True)
print("\nSecond evaluation....")
evaluate(exact_frequent_items, frequent_items, False)
