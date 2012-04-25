#-*- coding: utf-8 -*-
import igraph
import time
from multiprocessing import Pool
g = igraph.Graph(18000)

def f(i):
    #Первая оптимизация, это так сказать развёртка цикла. Добавляем сразу несколько рёбер.
    g.add_edges([(i+1,i),(i+2,i+1),(i+3,i+2),(i+4,i+3),(i+5,i+4),(i+6,i+5),(i+7,i+6),(i+8,i+7),(i+9,i+8),(i+10,i+9),(i+11,i+10),(i+12,i+11),(i+13,i+12),(i+14,i+13),(i+15,i+14),(i+16,i+15)])
    g.es[i]["weight"]=i%5
    g.es[i+1]["weight"]=i%5
    g.es[i+2]["weight"]=i%5
    g.es[i+3]["weight"]=i%5
    g.es[i+4]["weight"]=i%5
    g.es[i+5]["weight"]=i%5
    g.es[i+6]["weight"]=i%5
    g.es[i+7]["weight"]=i%5
    g.es[i+8]["weight"]=i%5
    g.es[i+9]["weight"]=i%5
    g.es[i+10]["weight"]=i%5
    g.es[i+11]["weight"]=i%5
    g.es[i+12]["weight"]=i%5
    g.es[i+13]["weight"]=i%5
    g.es[i+14]["weight"]=i%5
    g.es[i+15]["weight"]=i%5
#    print i

start = time.time()
i=0
#Вторая оптимизация создаём пул из 4-х процессов и запускаем всё асинхронно и параллельно
p = Pool(processes=4)
while i<10000:
    #print i
    p.map_async(f,[i,i+16,i+32,i+48])
    i+=64
finish = time.time()
print "Заполнение графа 10000 вершинами за: ",(finish - start)