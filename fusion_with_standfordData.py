import os
import tweepy
from progressbar import Percentage
from progressbar import ProgressBar
from pygraphml import Graph
from pygraphml import GraphMLParser
import time




def create_abstraction_file1(name):
    try:
        l=[]
        with open(name, 'r') as f:
            for item in f:
                c=item.splitlines()
                l.append(c[0].split())
        f.close()
        return l
    except IOError:
        print('File not found!')
        exit('Exit')


#write graphml
def write_graph(g):
    parser = GraphMLParser()
    parser.write(g, "/home/nataraja/Scrivania/all_merge.graphml")

def read_graph():
    try:
        parser = GraphMLParser()
        g = parser.parse("data_set/graph_xml/huge_graph.graphml") #Huge Graph
        return g
    except Exception as e:
        print(e)
        exit()




g = Graph()
g=read_graph()
first_level = []
first_level=create_abstraction_file1("/home/nataraja/Scrivania/twitter_data")

print('List created')
p = ProgressBar(
    widgets=[Percentage()],
    min_value=0,
    max_value=len(first_level))  # a simple bar
p.start(0)
start=time.time()

for i in range(0,len(first_level)):
    p.update(i)
    for j in range(0,len(first_level[i])):
        flag=False
        for node in g.nodes():
            if first_level[i][j] == node['label']:
                flag = True
                break
        if not flag:
            g.add_node(first_level[i][j]) #if node not exist add it
p.finish()
print('node added!')

p = ProgressBar(
    widgets=[Percentage()],
    min_value=0,
    max_value=len(first_level))  # a simple bar
p.start(0)
start=time.time()

for i in range(0,len(first_level)):
    p.update(i)
    flag = False
    for edge in g.edges():
        if first_level[i][0] == edge.node1['label'] and first_level[i][1] == edge.node2['label']:
            flag = True
            break
    if not flag:
        g.add_edge_by_label(first_level[i][0], first_level[i][1])







p.finish()
print(time.time()-start)
write_graph(g)