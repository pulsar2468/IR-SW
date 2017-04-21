import sys
import time
import tweepy
from pygraphml import Graph
from pygraphml import GraphMLParser


####################################
#file_name: find_it.py             #
#author: Riccardo La Grassa        #
#data created: 25/11/2016          #
#data last modified: 19/12/2016    #
#Python interpreter: 3.5.2         #
#mail: riccardo2468@gmail.com      #
####################################


def bfs_search(root,id_target):
    l=[]
    visited=[]
    l.append(root)
    visited.append(root)
    l.append('flag')
    depth=1
    start=time.time()
    while len(l) > 1:
        x = l.pop(0)
        if x != 'flag':
            for child in g.children(x):
                if (child['label'] == id_target):
                    print('Target FOUND!\nName: ', sys.argv[2])
                    print('Depth: ',depth,'\nTime: ',time.time() - start)
                    return
                if not (child in visited):#I don't consider the visited nodes
                    l.append(child)
                    visited.append(child)
        else:
            depth += 1
            l.append('flag') #set a frontier
    print('Not Found')



def get_user_information(node):
    try:
        user = api.get_user(node)
        d = {'name': user.name,
         'screen_name': user.screen_name,
         'id': user.id,
         'friends_count': user.friends_count,
         'followers_count': user.followers_count,
         'followers_ids': user.followers_ids()}
        return d['id']

    except tweepy.TweepError as e:
            print(e.reason)
            exit()



def read_graph():
    try:
        parser = GraphMLParser()
        g=parser.parse("data_set/graph_xml/graph_out.graphml") #Small Graph
        #g = parser.parse("/home/nataraja/Scrivania/data_set/graph_xml/huge_graph.graphml") #Huge Graph
        return g
    except Exception as e:
        print(e)
        exit()




#Error Control
#****************************************************
if(len(sys.argv) != 3):
    print('Error Missing parameters! You try to write --help \n')
    exit()

if(sys.argv[1]=='--help'):
    print('****'*10)
    print('namefile.py root + target namefile\n\nparameters = Target Twitter without \'@\' \nfor example nomefile.py OSHO DalaiLama')
    exit()

# enter the corresponding information from yougrr Twitter application:
CONSUMER_KEY = 'NM4xHHBwm7fiBQjf0X4QfdN8X'  # keep the quotes, replace this with your consumer key
CONSUMER_SECRET = 'u6pnGad8o11sNhLiY77voEbAUawHejgGiVgxKBwPFVKLyLyRbD'  # keep the quotes, replace this with your consumer secret key
ACCESS_KEY = '251060755-lUeE2kxqXjMfL5hLqzmo4EuyuWo4wYmqcihTEU0o'  # keep the quotes, replace this with your access token
ACCESS_SECRET = 'sUCSFY1PkPkVxVD5P96EixYzCjJnUapeXmzyJ8HQ1UW2s'  # keep the quotes, replace this with your access token secret
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify=True)

target_parameter=str(get_user_information(sys.argv[2]))
rootToId=str(get_user_information(sys.argv[1]))

g=Graph()
g=read_graph()
for i in g.nodes():
    if i['label'] == rootToId:
        root=i #i set up the root
        break
print('Root:\n',root)
bfs_search(root,target_parameter)