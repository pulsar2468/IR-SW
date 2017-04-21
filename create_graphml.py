import os
import sys
import tweepy
from pygraphml import Graph
from pygraphml import GraphMLParser



#write graphml
def write_graph(g):
    parser = GraphMLParser()
    parser.write(g, "data_set/graph_xml/graph_out.graphml")


'''
def get_user_information(node):


    try:
        api.get_user(node)
        return

    except tweepy.TweepError as e:
        if ('88' in e.reason):
            print('Wait: 15 min\n')
            time.sleep(60 * 15)
        else:
            print('Name not exist! You try with another name\n')
            exit()

'''

def create_abstraction_file(name):
    try:
        l=[]
        with open(name, 'r') as f:
            for item in f:
                l.append(item.splitlines())
        f.close()
        return l
    except IOError:
        print('File not found!')
        exit('Exit')



# enter the corresponding information from yougrr Twitter application:
CONSUMER_KEY = 'NM4xHHBwm7fiBQjf0X4QfdN8X'  # keep the quotes, replace this with your consumer key
CONSUMER_SECRET = 'u6pnGad8o11sNhLiY77voEbAUawHejgGiVgxKBwPFVKLyLyRbD'  # keep the quotes, replace this with your consumer secret key
ACCESS_KEY = '251060755-lUeE2kxqXjMfL5hLqzmo4EuyuWo4wYmqcihTEU0o'  # keep the quotes, replace this with your access token
ACCESS_SECRET = 'sUCSFY1PkPkVxVD5P96EixYzCjJnUapeXmzyJ8HQ1UW2s'  # keep the quotes, replace this with your access token secret
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify=True)

#get_name_account = sys.argv[1]

g = Graph()
first_level=[]

#It's read all file.text from path below and it creates a unified graph
for (root, dirnames, files) in os.walk("data_set/graph_format_text"):
    for file in files:
        if file.endswith(".text"):
            first_level.extend(create_abstraction_file('data_set/graph_format_text/'+file))


#Create graphml from file create before
c=first_level[0][0].split(':')

for i in range(0,len(first_level)):
    c=first_level[i][0].split(':')
    split_children = c[1].replace('[', '').replace(']', '').replace(',', '')
    resplit = split_children.split()

    flag=False
    for node in g.nodes():
        if c[0] == node['label']:
            flag = True
            break
    if not flag:
        g.add_node(c[0]) #if node does not exist add it

    for i in range(0, len(resplit)):
        flag=False
        for node in g.nodes():
            if resplit[i] == node['label']:
                flag=True
                break
        if not flag:
            g.add_node(resplit[i]) #add node (in this case i see its children)

        flag = False
        for edge in g.edges():
            if resplit[i] == edge.node2['label'] and c[0] == edge.node1['label']:
                flag = True
                break
        if not flag:
            g.add_edge_by_label(c[0], resplit[i])  # add edge (if it does not exist!)




write_graph(g)
