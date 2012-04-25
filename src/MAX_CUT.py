import random
users = [[1, 2, 9, 1, 8, 3, 4],
		 [2, 1,10, 3, 7, 2, 1],
		 [9,10, 1, 7, 4, 3, 1],
		 [1, 3, 7, 1, 6, 1, 7],
		 [8, 7, 4, 6, 1, 1, 9],
		 [3, 2, 3, 1, 1, 1, 2],
		 [4, 1, 1, 7, 9, 2, 1]]
#number of users
NUMBER = 7

#find weight of cut
def Cut_weight():
	weight = 0
	for i in range(NUMBER):
		for j in range(i):
			if users[i][i] != users[j][j]:
				weight = weight + users[i][j]
	return weight
#find difference between internal and external edges 
def Find_sum(index):
	i = 0
	sum = 0
	for i in range(NUMBER):
		sum = sum + users[index][i]*users[i][i]*users[index][index]
		i = i + 1
	sum = sum - users[index][index]
	return sum

#simple random method
def Random_CUT():
	for i in range(NUMBER):
		r = random.random()*2
		if r<1:
			users[i][i] = 1
		else:
			users[i][i] = -1

#find vertex and change its group
def Max_CUT():
	while 1:
		max_sum = 0
		index_to_change = 0
		for i in range(NUMBER):
			sum = Find_sum(i)
			if sum > max_sum:
				max_sum = sum
				index_to_change = i
		if max_sum == 0:
			break
		users[index_to_change][index_to_change] = (-1)*users[index_to_change][index_to_change]
	
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