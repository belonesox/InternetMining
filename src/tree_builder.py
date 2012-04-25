import pickle, os, copy

users = []
matrix = [] 
THRESHOLD = 50

def init_matrix(size):
    lil_matrix = [0]*size
    for i in xrange(size):
        matrix.append(copy.copy(lil_matrix))

def load_users_data(number):
    pickle_file = open("../data/marks/"+str(number),'r')
    ret = pickle.load(pickle_file)
    pickle_file.close()
    return ret

def prepare_data(data):
    titles = set([i[0] for i in data])
    movie_map={}
    for movie in data:
        title, mark = movie
        movie_map[title] = mark
    return titles, movie_map

def calculate_difference(first_bundle, second_bundle):
    first_titles, first_map = first_bundle
    second_titles, second_map = second_bundle
    common_titles = first_titles & second_titles
    n = float(len(common_titles))
    distance = 0
    for movie in common_titles:
        distance += abs(first_map[movie]-second_map[movie])
    if distance!=0: distance /= n 
    return n, distance

def recover_users():
    global users
    if not os.path.exists("../data/marks/users_proceeded"): return
    pickle_file = open("../data/marks/users_proceeded",'r')
    users = pickle.load(pickle_file)
    pickle_file.close()
    

def dump_matrix():
    global matrix
    pickle_file = open("../data/tree_matrix",'w')
    pickle.dump(matrix, pickle_file)
    pickle_file.close()
    
    
def delete_bad_users():
    global users
    recover_users()
    new_users = []
    for user in users:
        try: data = prepare_data(load_users_data(user))
        except: continue
        if len(data[0])<THRESHOLD: continue
        new_users.append(user)
    users = new_users
    print len(users)
    pickle_file = open("../data/marks/users_proceeded_fixed", 'w')
    pickle.dump(users, pickle_file)
    pickle_file.close()

def start():
    recover_users()
    init_matrix(len(users))
    for first_user in xrange(len(users)):
        try: first_data = prepare_data(load_users_data(users[first_user]))
        except:
            print "bad user"
            continue
        if len(first_data[0])<THRESHOLD: continue
        print first_user
        for second_user in xrange(len(users)):
            if first_user <= second_user: continue
            try:
                second_data = prepare_data(load_users_data(users[second_user]))
                if len(second_data[0])<THRESHOLD: continue
                matrix[first_user][second_user] = calculate_difference(first_data, second_data)
            except: print "bad user"
    dump_matrix()
    

start()