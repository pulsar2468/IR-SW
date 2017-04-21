import re
import math
import tweepy
from nltk import FreqDist
from nltk.corpus import wordnet


#for classifierV1
def taxonomy(cluster_name):
    hyponyms_first_level = []
    hyponyms_second_level = []
    hyponyms_thirt_level = []
    hyponyms_fourth_level = []
    tree_hyponyms = []
    tree_final = []
    for r in cluster_name:
        label_cluster = wordnet.synsets(r)

    ########################################################
    # In this section, i create a structure (tree style) of hyponyms until fourth depth level. In this way
    # I improved the probability to find the most frequent words of the target X in the 'cluster' label considered
    # every structure contains only values of the its hyponyms
        for w in range(0, len(label_cluster)):
            x = label_cluster[w].hyponyms()
            if x:
                hyponyms_first_level.extend(label_cluster[w].hyponyms())

        for i in range(0, len(hyponyms_first_level)):
            x = hyponyms_first_level[i].hyponyms()
            if x:
                hyponyms_second_level.extend(x)

        for i in range(0, len(hyponyms_second_level)):
            x = hyponyms_second_level[i].hyponyms()
            if x:
                hyponyms_thirt_level.extend(x)

        for i in range(0, len(hyponyms_thirt_level)):
            x = hyponyms_thirt_level[i].hyponyms()
            if x:
                hyponyms_fourth_level.extend(x)

        tree_hyponyms.extend(hyponyms_first_level)
        tree_hyponyms.extend(hyponyms_second_level)
        tree_hyponyms.extend(hyponyms_thirt_level)
        tree_hyponyms.extend(hyponyms_fourth_level)

        tree_final.append([w for w in tree_hyponyms])
        tree_hyponyms.clear()
        hyponyms_first_level.clear()
        hyponyms_second_level.clear()
        hyponyms_thirt_level.clear()
        hyponyms_fourth_level.clear()
    return tree_final


def findToTreeHyponyms(listX,tree_hyponyms):

    for a in listX:
        word_without_label = wordnet.synsets(a[0])
        for z in word_without_label:
            for i in range(0,len(tree_hyponyms)):
                    if (word_without_label):
                        #s=z.wup_similarity(tree_hyponyms[i]) #Otherwise, return similarity, if it's very high and break cycle!
                        if z == tree_hyponyms[i]:
                            return 1,z

    return 0,0


def main_classifierV1(user_nameX,user_nameY,most_common1,most_common2,tree_hyponyms):
    cluster_label=[('music'),('physics'),('orientalism'),('philosophy'),('astronomy'),('art'),('history'),('politics')]

    print('ClassifierV1')
    print(user_nameX)
    for i in range(0,len(cluster_label)):
        result,hit=findToTreeHyponyms(most_common1,tree_hyponyms[i])
        if(result):
            print('Interest: ',cluster_label[i])

    print(user_nameY)
    for i in range(0, len(cluster_label)):
        result, hit = findToTreeHyponyms(most_common2,tree_hyponyms[i])
        if (result):
            print('Interest: ', cluster_label[i])
    print('\n')


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


def get_data(source1,source2):
    # enter the corresponding information from your Twitter application ( these are my access credential):
    CONSUMER_KEY = 'NM4xHHBwm7fiBQjf0X4QfdN8X'
    CONSUMER_SECRET = 'u6pnGad8o11sNhLiY77voEbAUawHejgGiVgxKBwPFVKLyLyRbD'
    ACCESS_KEY = '251060755-lUeE2kxqXjMfL5hLqzmo4EuyuWo4wYmqcihTEU0o'
    ACCESS_SECRET = 'sUCSFY1PkPkVxVD5P96EixYzCjJnUapeXmzyJ8HQ1UW2s'
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)  # This is a standard  of the server twitter, probably to prevent too many requests by bot

    list_tweetX = []
    list_tweetY = []

    # Get tweet post from target X and Y
    for page in tweepy.Cursor(api.user_timeline, id=source1).pages():
        for item in page:
            list_tweetX.append(item.text)

    for page in tweepy.Cursor(api.user_timeline, id=source2).pages():
        for item in page:
            list_tweetY.append(item.text)

    return list_tweetX,list_tweetY


def sim_word_net(j, z1):
    for i in z1:
        if (j == i): return True #so, the term exists in this document( or it's a synonym )
    return False


#it computes the weighted schema of the documents not labeled
def tf_idf(list1,clusters):
    temp=[]
    temp_repl=[]

    #doc1 weighted
    for i in list1:
        if not i in temp_repl: #i don't consider the same words
                temp_repl.append(i)

                #tf
                n_i=1 #of course
                fr_i=list1.count(i)


            #idf
        for z in range(0,len(clusters)):
            if (sim_word_net(i,clusters[z])):
                n_i=n_i + 1

        w= ((1 + math.log10(fr_i))) * (math.log10((1 + 2 / n_i))) #tf-idf
        temp.append(w)


    return temp

#weighted schema for the set documents, and alignment of all document set and doc not labeled
def tf_idf_cluster(cluster_cluster,clusters_weighted,not_replicated):

    temp = []
    temp_repl = []

    # doc1 weighted
    for i in range(0,len(cluster_cluster)):
        for j in range(0, len(cluster_cluster[i])):
            if not cluster_cluster[i][j] in temp_repl:  # i don't consider the same words
                temp_repl.append(cluster_cluster[i][j])

                # tf
                n_i = 1  # of course
                fr_i = cluster_cluster[i].count(cluster_cluster[i][j])


            # idf
                for z in range(0, len(cluster_cluster)):
                     if (sim_word_net(i, cluster_cluster[z])):
                         n_i = n_i + 1

                w = ((1 + math.log10(fr_i))) * (math.log10((1 + 2 / n_i)))  # tf-idf
                temp.append(w)

        clusters_weighted.append([w for w in temp])
        temp.clear()
        not_replicated.append([w for w in temp_repl])
        temp_repl.clear()


def alignment_doc_clusters(list_target,clusters_weighted,not_replicated,gold):
    silver = []
    for itemI in range(0,len(not_replicated)):
        for itemJ in range(0,len(not_replicated[itemI])):
            if not_replicated[itemI][itemJ] in list_target:
                silver.append(clusters_weighted[itemI][not_replicated[itemI].index(not_replicated[itemI][itemJ])])
            else:
                silver.append(0)
        gold.append([w for w in silver])
        silver.clear()


#cleaning of the text
def clean_text(original_list):
    list_splitted=[]
    list_clean=[]
    for i in original_list:
        list_splitted.append(i.split())

    #grammar file. i will erase all useless words
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


#This function gets data from files. The files are labeled  by humans and it represents the reference model
#new files not labeled will be labeled following the reference model. In this way, the algorithm of classification will become
#an algorithm supervisioned.
def get_cluster(name_cluster):
    try:
        l = []
        with open('data_set/category/'+name_cluster, 'r') as f:
            for item in f:
                l.extend(item.split())
        return l
        f.close()
    except IOError:
        print('File not found!')
        exit('Exit')


def get_twitter_data():
    try:
        l = []
        with open('data_set/top_users', 'r') as f:
            for item in f:
                l.extend(item.splitlines())
        f.close()
        return l
    except IOError:
        print('File not found!')
        exit('Exit')



def main_area():
    cluster_label = [('music'), ('physics'), ('orientalism'), ('philosophy'), ('astronomy'), ('art'), ('history'),
                     ('politics')]
    cluster_cluster = []
    clusters_weighted = []
    not_replicated = []
    print('Loading')
    tree_hyponyms=taxonomy(cluster_label)
    print('- Taxonomy clusters created')

    for i in cluster_label:
        cluster_list = get_cluster(i)
        cluster_clean = clean_text(cluster_list)
        cluster_cluster.append(cluster_clean)
    print('- Clusters cleaned')

    tf_idf_cluster(cluster_cluster, clusters_weighted, not_replicated)  # only one!
    print('- TF-IDF for clusters done')

    l = get_twitter_data()#get list users.. only name
    print('- Target data loaded\n')

    i = 0
    while (i < len(l) - 1):
        list_tweetX, list_tweetY = get_data(l[i], l[i + 1])
        listX_clean = clean_text(list_tweetX)
        listY_clean = clean_text(list_tweetY)
        fdist1 = FreqDist(listX_clean)
        fdist2 = FreqDist(listY_clean)
        most_common1 = fdist1.most_common()  # I delete the useless special symbols such as smile, etc...
        most_common2 = fdist2.most_common()
        most_common1.reverse()
        most_common2.reverse()
        main_classifierV2(l[i], l[i + 1], listX_clean, listY_clean,cluster_cluster, clusters_weighted, not_replicated,cluster_label)
        main_classifierV1(l[i], l[i + 1], most_common1[:40], most_common2[:40],tree_hyponyms)
        i += 2


def main_classifierV2(userX,userY,listX_clean,listY_clean,cluster_cluster,clusters_weighted,not_replicated,cluster_label):
    listSimX = []
    listSimY = []
    gold = []

    #doc weighted
    doc_weight1=tf_idf(listX_clean,cluster_cluster)
    doc_weight2=tf_idf(listY_clean,cluster_cluster)

    alignment_doc_clusters(listX_clean,clusters_weighted,not_replicated,gold)


    for i in range(0,len(gold)):
        listSimX.append(sim_vectorial(doc_weight1,gold[i],clusters_weighted[i]))

    gold.clear()
    alignment_doc_clusters(listY_clean, clusters_weighted, not_replicated, gold)

    for i in range(0, len(gold)):
        listSimY.append(sim_vectorial(doc_weight2, gold[i], clusters_weighted[i]))

    print('ClassifierV2')
    print(userX,' ',(listSimX),' ',cluster_label[listSimX.index(max(listSimX))])
    print(userY, ' ', (listSimY), ' ', cluster_label[listSimY.index(max(listSimY))],'\n')




main_area()










