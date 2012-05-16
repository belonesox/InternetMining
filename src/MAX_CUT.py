# -*- coding: utf-8 -*-
import random
users = [[1, 2, 9, 1, 8, 3, 4],
		 [2, 1,10, 3, 7, 2, 1],
		 [9,10, 1, 7, 4, 3, 1],
		 [1, 3, 7, 1, 6, 1, 7],
		 [8, 7, 4, 6, 1, 1, 9],
		 [3, 2, 3, 1, 1, 1, 2],
		 [4, 1, 1, 7, 9, 2, 1]]

# Нужно использовать в numpy http://numpy.scipy.org/
# Есть нативная сериализация
# http://thsant.blogspot.com/2007/11/saving-numpy-arrays-which-is-fastest.html         
         
#number of users
NUMBER = 7
# Глобальные переменные SUCKS

# Посмотрите http://www.python.org/dev/peps/pep-0008/

def Cut_weight():
	"""
	find weight of cut
	"""
	weight = 0
	for i in xrange(NUMBER):
		for j in xrange(i):
			if users[i][i] != users[j][j]:
				weight = weight + users[i][j]
	return weight

   
#find difference between internal and external edges 
def irrelevant_metric(index):
	"""
	index — индекс пользователя
	
	Возращает разность суммы antisimilarity с однокластерниками 
	минус антисимилярити с врагами.
	"""
	sum = 0
	for i in xrange(NUMBER):
		sum += users[index][i] * users[i][i] * users[index][index]
	sum = sum - users[index][index]
	return sum

#simple random method
def Random_CUT():
	for i in xrange(NUMBER):
		r = random.random() * 2
		if r < 1:
			users[i][i] = 1
		else:
			users[i][i] = -1

#find vertex and change its group
def Max_CUT():
	while 1:
		max_sum = 0
		index_to_change = 0
		for i in xrange(NUMBER):
			sum = irrelevant_metric(i)
			if sum > max_sum:
				max_sum = sum
				index_to_change = i
		if max_sum == 0:
			break
		users[index_to_change][index_to_change] *= -1
	
Max_CUT()

#Random_CUT()
print("First group:")
for i in range(NUMBER):
	if users[i][i]==1:
		print(i)
print("Second group:")
for i in range(NUMBER):
	if users[i][i]== -1:
		print(i)
print "Cut weight =", Cut_weight()