####################################
#file_name: similarity.py          #
#author: Riccardo La Grassa        #
#data created: 16/11/2016          #
#data last modified:               #
#Python interpreter: 3.5.2         #
#mail: riccardo2468@gmail.com      #
####################################



import re
import numpy as np
import sys
import matplotlib.pyplot as plt
import time
import math
import tweepy
import fusion_with_standfordData
import datetime
import matplotlib.dates as mdates
from click._compat import raw_input

import word_netV1 as wrd_net1
import word_netV2 as wrd_net2
import plotting_zone as plt_zone
from nltk import FreqDist

# it computes the similarity with vector model
#input: doc weighted 1 doc weighted 2 and the doc 2 aligned(for compute the scalar product)
#output:similarity of the vector model
def sim_vectorial(doc_w1,doc_align_2,doc_w2):
    scalar_product=0.0
    lenght_norm2=0.0
    lenght_norm1=0.0
    for i in zip(doc_w1,doc_align_2):
        scalar_product= scalar_product + i[0]*i[1]

    for i in doc_w1:
        lenght_norm1=lenght_norm1 + math.pow(i,2)

    for a in doc_w2:
        lenght_norm2 = lenght_norm2 + math.pow(a,2)


    if scalar_product == 0: return 0 #totally different
    else:
        return (scalar_product/((math.sqrt(lenght_norm1)) * (math.sqrt(lenght_norm2))))

#it computes the weighting scheme (tf-idf) of all list
# and it aligns the terms of the second list with the first list ( if it exist, otherwise it puts 0)
# in this way, i don't consider another structure for the words set
#input:list target X and Y
#output: doc weighted 1, doc weighted 2, doc aligned 2 seeing the first
def tf_idf(list1,list2):
    doc_mix_=[]
    gold=[]
    temp=[]
    temp_repl=[]
    not_replicated=[]
    fusion_list=[]
    fusion_list.append(list1)
    fusion_list.append(list2) #lista1 U lista2
    #frequency for each term  in doc j
    for i in range(0,len(fusion_list)):
        #set_clean_list=set(fusion_list[i]) #i create a set for each account twitter
        for j in (fusion_list[i]): # for each word of doc(set) count the occurrences inside the doc
            if not j in temp_repl: #i don't consider the same words
                temp_repl.append(j)
                #tf
                n_i=1 #of course
                fr_i=fusion_list[i].count(j)


                #idf
                if any(j in item for item in fusion_list[1-i]):
                    n_i=n_i + 1

                w= ((1 + math.log10(fr_i))) * (math.log10((1+2 / n_i))) #tf-idf
                temp.append(w)

        doc_mix_.append([w for w in temp]) #first list -> doc weight 1 second list -> doc weight 2
        temp.clear()
        not_replicated.append([w for w in temp_repl])
        temp_repl.clear()



    #Finally, i won.. Fortunately i come from C
    for item in not_replicated[0]:
        if item in not_replicated[1]:
            gold.append(doc_mix_[1][not_replicated[1].index(item)])
        else:
            gold.append(0)
    return doc_mix_[0],gold,doc_mix_[1] #this is too importat, see an explanation!


#The function computes the coefficient jaccard through the formula: |A inter B| / |AUB|->|A|+|B|-|A inter B|
#input:nothing
#output:jaccard coefficient
def jaccard_coefficient():
    #intersect=[w for w in listX_clean if w in listY_clean] #intersection #I don't use it because i don't considerer  the word frequency
    intersect=set(listX_clean).intersection(set(listY_clean))
    jaccard=len(intersect)/(len(listX_clean)+len(listY_clean)-len(intersect))
    return jaccard



#I clean the list X through a procedure mixed of grammarFile as a reference and expression regular for alienating the useless words
#input:set tweet of target X
#output: set Clean tweet of target X
def clean_text(original_list):
    list_splitted=[]
    list_clean=[]
    for i in original_list:
        list_splitted.append(i.split())

    #grammar file. i will erase all the useless words
    grammarlist=[]
    try:
        with open('data_set/grammarList', 'r') as f:
            grammarlist.append(f.read().splitlines())


    except IOError:
        print('file not found!')
        exit()


    for i in range(0, len(list_splitted)):


        for j in range(0, len(list_splitted[i])):

            if not re.search('https?|RT|[^A-Za-z]|amp|[ah|ha]+', list_splitted[i][j]):
                list_splitted[i][j]=re.sub('•|‘|"|”|!|“|,|:|&|;|/|\+|\?|…|[.]+|-|–|—|→|\(|\)', '', list_splitted[i][j].lower()) #i clean the text from link replytweet and @tag
                if not (len(list_splitted[i][j]) < 4 ):
                    if not (any(list_splitted[i][j].lower() in s for s in grammarlist)):
                        list_clean.append(list_splitted[i][j].lower())

    f.close()
    return list_clean



#it converts the target's name string into numerical id
#input: string targets
#return: names id if it exist! otherwise exit()
def get_user_information(source1, source2):
    while True:
        try:
            user1 = api.get_user(source1)
            user2 = api.get_user(source2)

            s1 = {'name': user1.name,
                 'screen_name': user1.screen_name,
                 'id': user1.id,
                 'friends_count': user1.friends_count,
                 'followers_count': user1.followers_count,
                 'followers_ids': user1.followers_ids()}

            s2 = {'name': user2.name,
                  'screen_name': user2.screen_name,
                  'id': user2.id,
                  'friends_count': user2.friends_count,
                  'followers_count': user2.followers_count,
                  'followers_ids': user2.followers_ids()}

            return s1['id'], s2['id']
        except tweepy.TweepError as e:
            if ('88' in e.reason):
                print('Too many requests, Wait: 15 min...\n')
                time.sleep(60 * 15) #because i exceeded the requests
            else:
                print(e.reason)
                exit()



#Final the summary contain the computational result#
#input:nothing
#output:file_name
def generate_summary_file():
    try:
        with open('data_set/Summary with '+str(len(list_tweetX))+' post with targets X: '+str(sys.argv[1])+' Y: '+str(sys.argv[2]), 'w') as f:
            f.write('')
            f.write('--Number of tweet postX and Number of tweet postY--\n')
            f.write(str(len(list_tweetX))+'-'+str(len(list_tweetY))+'\n\n')
            f.write('--Comparison similarity--\n')
            f.write('Jaccard: '+str(jaccard_value)+'\n'+'Vector model: '+str(similarity_vectorial)+'\n'+
                    'Vector Model with WordnetV2: ' + str(similarity_vectorial_w2)+'\n')
            f.write('Time Vector model: '+str(time_vector_model)+'\n'+'Time with WordnetV2: '+str(time_vector_model_wrdnetV2)+'\n'+
                    'Time with Jaccard: '+str(time_jaccard)+'\n')
            f.write('The top 40 most commons words of the targetX:\n\n'+str(most_common1)+'\n\n')
            f.write('The top 40 most commons words of the targetY:\n\n' + str(most_common2) + '\n\n')
            f.close()


    except IOError:
        print('Error to generate a summary file!')
        exit()



#####################
#Error Control main #
#####################
if(len(sys.argv) != 3):
    print('Error Missing parameters! You try to write --help \n')
    exit()

if(sys.argv[1]=='--help'):
    print('****'*10)
    print('namefile.py parameter\n\nparameters = sourceX sourceY \'@\' \nfor example nomefile.py michiokaku russelcrowe')
    exit()


# enter the corresponding information from your Twitter application ( these are my access credential):
CONSUMER_KEY = 'NM4xHHBwm7fiBQjf0X4QfdN8X'
CONSUMER_SECRET = 'u6pnGad8o11sNhLiY77voEbAUawHejgGiVgxKBwPFVKLyLyRbD'
ACCESS_KEY = '251060755-lUeE2kxqXjMfL5hLqzmo4EuyuWo4wYmqcihTEU0o'
ACCESS_SECRET = 'sUCSFY1PkPkVxVD5P96EixYzCjJnUapeXmzyJ8HQ1UW2s'
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify=True) #This is a standard  of the server twitter, probably to prevent too many requests by bot

source1, source2 = get_user_information(str(sys.argv[1]), str(sys.argv[2])) #i get data target from shell
list_tweetX=[]
list_tweetY=[]
time_tweetX=[]
time_tweetY=[]

#Get tweet post from target X and Y
for page in tweepy.Cursor(api.user_timeline, id=source1).pages(40):
    for item in page:
        time_tweetX.append(item.created_at)#i get the data creation of all post, i will use it after
        list_tweetX.append(item.text)

for page in tweepy.Cursor(api.user_timeline, id=source2).pages(40):
    for item in page:
        time_tweetY.append(item.created_at)
        list_tweetY.append(item.text)


listX_clean=clean_text(list_tweetX)
listY_clean=clean_text(list_tweetY)


print('Comparison of Similarity')
start = time.time()
jaccard_value=jaccard_coefficient()
time_jaccard=time.time()-start
print('Similarity Jaccard coefficient: ',jaccard_value,'Time: ',time_jaccard)


start = time.time()
doc_weight1,doc_weight2,not_replicated=tf_idf(listX_clean,listY_clean)
similarity_vectorial=sim_vectorial(doc_weight1,doc_weight2,not_replicated)
time_vector_model=time.time()-start
print('Similarity vector model: ',similarity_vectorial,'Time: ',time_vector_model)


''''
#i call the python file (word_netV1.py) for the comparison between the model vector and the model vector with wordnet
start = time.time()
doc_weight1,doc_align_2,doc_weight2=wrd_net1.tf_idf(listX_clean,listY_clean)
similarity_vectorial_w1=wrd_net1.sim_vectorial(doc_weight1,doc_align_2,doc_weight2)
time_vector_model_wrdnet1=time.time()-start
print('Similarity vector model with WordnetV1(old version) ',similarity_vectorial_w1,'Time:',time_vector_model_wrdnet1)
'''

#i call the python file (word_netV2.py) for a comparison between the model vector and the model vector with wordnetV2
start = time.time()
doc_weight1,doc_align_2,doc_weight2=fusion_with_standfordData.tf_idf(listX_clean, listY_clean)
similarity_vectorial_w2=fusion_with_standfordData.sim_vectorial(doc_weight1, doc_align_2, doc_weight2)
time_vector_model_wrdnetV2=time.time()-start
print('Similarity vector model with WordnetV2 ',similarity_vectorial_w2,'Time:',time_vector_model_wrdnetV2)


fdist1=FreqDist(listX_clean)
fdist2=FreqDist(listY_clean)
most_common1=fdist1.most_common(40)
most_common2=fdist2.most_common(40)

#I call the module for plotting. You see the plotting_zone.py
plt_zone.analysis_frequency([w.date() for w in time_tweetX], [w.date() for w in time_tweetY], str(sys.argv[1]), str(sys.argv[2])) # i set the date without hours minutes and seconds
plt_zone.analysis_word(most_common1, 'Words Frequency analysis of '+str(sys.argv[1]), 4)
plt_zone.analysis_word(most_common2, 'Words Frequency analysis of '+str(sys.argv[2]), 5)
plt.show()


#if you want, you can create a summary file containing some results such as computation time, similarity of the various models
reply = raw_input("Do you want to generate a text file index? Y/N: ")
if (reply.lower() == 'y'): generate_summary_file()
#else bye bye.. see you!

