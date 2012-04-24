import pickle, os, copy , igraph
from multiprocessing import Pool

users = []
graph = igraph.Graph()
edgeCount = 0
edges = []
THRESHOLD = 50

def init_graph(size):
    global graph
    graph = igraph.add_verties(size-1)

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
    

def dump_graph():
    global graph
    graph.write_graphml("../data/tree_graph.graphml")
    
def add_edge(first,second,data):
    global edgeCount
    global edges
    global graph
    n,diff = data
    edges.append((first,second,n,diff))
    #Пишем только тогда, когда накопиться 16 рёбер для записи. Ускорении за счёт развёртки цикла.
    if len(edges) == 16:
        first1, second1, third1 ,fouth1 = edges[0]
        first2, second2, third2 ,fouth2 = edges[1]
        first3, second3, third3 ,fouth3 = edges[2]
        first4, second4, third4 ,fouth4 = edges[3]
        first5, second5, third5 ,fouth5 = edges[4]
        first6, second6, third6 ,fouth6 = edges[5]
        first7, second7, third7 ,fouth7 = edges[6]
        first8, second8, third8 ,fouth8 = edges[7]
        first9, second9, third9 ,fouth9 = edges[8]
        first10, second10, third10 ,fouth10 = edges[9]
        first11, second11, third11 ,fouth11 = edges[10]
        first12, second12, third12 ,fouth12 = edges[11]
        first13, second13, third13 ,fouth13 = edges[12]
        first14, second14, third14 ,fouth14 = edges[13]
        first15, second15, third15 ,fouth15 = edges[14]
        first16, second16, third16 ,fouth16 = edges[15]
        graph.add_edges([(first1,second1), (first2,second2) , (first3,second3), (first4,second4), (first5,second5), (first6,second6), (first7,second7), (first8,second8), (first9,second9) , (first10,second10), (first11,second11), (first12,second12), (first13,second13), (first14,second14), (first15,second15), (first16,second16)])
        graph.es[edgeCount]["weight"] = fouth1
        graph.es[edgeCount]["n"] = third1
        graph.es[edgeCount+1]["weight"] = fouth2
        graph.es[edgeCount+1]["n"] = third2
        graph.es[edgeCount+2]["weight"] = fouth3
        graph.es[edgeCount+2]["n"] = third3
        graph.es[edgeCount+3]["weight"] = fouth4
        graph.es[edgeCount+3]["n"] = third4
        graph.es[edgeCount+4]["weight"] = fouth5
        graph.es[edgeCount+4]["n"] = third5
        graph.es[edgeCount+5]["weight"] = fouth6
        graph.es[edgeCount+5]["n"] = third6
        graph.es[edgeCount+6]["weight"] = fouth7
        graph.es[edgeCount+6]["n"] = third7
        graph.es[edgeCount+7]["weight"] = fouth8
        graph.es[edgeCount+7]["n"] = third8
        graph.es[edgeCount+8]["weight"] = fouth9
        graph.es[edgeCount+8]["n"] = third9
        graph.es[edgeCount+9]["weight"] = fouth10
        graph.es[edgeCount+9]["n"] = third10
        graph.es[edgeCount+10]["weight"] = fouth11
        graph.es[edgeCount+10]["n"] = third11
        graph.es[edgeCount+11]["weight"] = fouth12
        graph.es[edgeCount+11]["n"] = third12
        graph.es[edgeCount+12]["weight"] = fouth13
        graph.es[edgeCount+12]["n"] = third13
        graph.es[edgeCount+13]["weight"] = fouth14
        graph.es[edgeCount+13]["n"] = third14
        graph.es[edgeCount+14]["weight"] = fouth15
        graph.es[edgeCount+14]["n"] = third15
        graph.es[edgeCount+15]["weight"] = fouth16
        graph.es[edgeCount+15]["n"] = third16
        graph.es[edgeCount+16]["weight"] = fouth1
        graph.es[edgeCount+16]["n"] = third1
        edgeCount +=16
        edge = []
             
def compare_users(first_user,second_user):
    if first_user <= second_user: continue
    try:
        second_data = prepare_data(load_users_data(users[second_user]))
        if len(second_data[0])<THRESHOLD: continue
        add_edge(first_user,second_user,calculate_difference(first_data, second_data)
        except: print "bad user"
        
def push_last_edges():
    global edges
    global graph
    global edgeCount    
    while len(edges) > 0:
        first,second,n,diff = edges.pop()
        graph.add_edges((first,second))
        graph.es[edgeCount]["weight"] = diff
        graph.es[edgeCount]["n"] = n
        edgeCount += 1
        
def start():
    recover_users()
    init_graph(len(users))
    for first_user in xrange(len(users)):
        try: first_data = prepare_data(load_users_data(users[first_user]))
        except:
            print "bad user"
            continue
        if len(first_data[0])<THRESHOLD: continue
        print first_user
        p = Pool(processes=4)
        second_user = 0
        while < len(users)):
            if second_user+3 < len(users):
                # Если это не последние 3 пользователя, то обрабатываем их параллельно 
                p.map_async(compare_users,[(first_user,second_user),(first_user,second_user+1),(first_user,second_user+2),(first_user,second_user+3)])
                second_user += 4
                continue
            compare_users(first_user,second_user)
            second_user += 1
    #Поскольку записываем только по 16 рёбер, могут остаться недозаписанные рёбра
    push_last_edges()    
    dump_graph()
            
start()