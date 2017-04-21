####################################
#file_name: word_netV2.py          #
#author: Riccardo La Grassa        #
#data created: 16/11/2016          #
#data last modified:               #
#Python interpreter: 3.5.2         #
#mail: riccardo2468@gmail.com      #
####################################

from nltk.corpus import wordnet
import math
from progressbar import AnimatedMarker
from progressbar import Percentage
from progressbar import ProgressBar

#it computes the similarity of the vector model with wordnet
#input: doc weighted 1 doc weighted 2 and the doc 2 aligned(for compute the scalar product)
#output:similarity of the vector model
def sim_vectorial(doc_w1,doc_align_2,doc_w2):
    scalar_product=0.
    lenght_norm2=0.
    lenght_norm1=0.
    for i in zip(doc_w1,doc_align_2):
        scalar_product= scalar_product + round(i[0]*i[1],2)

    for i in doc_w1:
        lenght_norm1=lenght_norm1 + round(math.pow(i,2),2)

    for a in doc_w2:
        lenght_norm2 = lenght_norm2 + round(math.pow(a,2),2)



    if scalar_product == 0.: return 0 #totally different
    else:
        return (scalar_product/round((( round(math.sqrt(lenght_norm1),2)) * ( round(math.sqrt(lenght_norm2),2))),2))

#I find n_i of IDF smooth --> log2((1 + 2 / n_i))
#input:term and other set
#output:True or False
def sim_word_net(j, z1):
    wordFromList1 = wordnet.synsets(j)

    for word2 in z1:
        if word2 == j: return True
    for word2 in z1:
            wordFromList1 = wordnet.synsets(j)
            if wordFromList1:
                wordFromList2 = wordnet.synsets(word2)
                if wordFromList2:
                    s = wordFromList1[0].wup_similarity(wordFromList2[0])
                    if s != None and s > 0.90:
                        return True #so, the term exists in this document( or it's a synonyms )
    return False

#for the word frequency
def sim_word_net_for_fr(j, z1):
    count_fr = 0
    for word2 in z1:
            if word2 == j:  count_fr = count_fr + 1
            else:
                wordFromList1 = wordnet.synsets(j)
                if wordFromList1:
                    wordFromList2 = wordnet.synsets(word2)
                    if wordFromList2:
                        s = wordFromList1[0].wup_similarity(wordFromList2[0])
                        if s != None and s > 0.90:
                            count_fr = count_fr + 1

    if count_fr > 0:
        return count_fr
    else:
        return 1

#I see the repl_list, and i verify if the new word is in the list ( term by term or a possible synonym)
#if the correspondence between the new word and an element of the repli_list is more than 0.90, i don't insert
#the weighted term for representation of doc, because i had already inserted the word ( or its synonym ) in the list.
#you see the tf_if function from line 112 to line 127
def scan(j,repl_list):
    if not repl_list: return True

    for word2 in repl_list:
            if word2 == j:  return False

    for word2 in repl_list:
        wordFromList1 = wordnet.synsets(j)
        if wordFromList1:
            wordFromList2 = wordnet.synsets(word2)
            if wordFromList2:
                s = wordFromList1[0].wup_similarity(wordFromList2[0])
                if s != None and s > 0.90:
                    return False
    return True

#
#it computes the weighting scheme (tf-idf) of all lists. The difference with vector model: I don't consider only the same terms
#but also their synonyms. It's configured with 0.90 of similarity between the term considered and the all terms of the other list
#or between the term considered in the same list with all list terms for the computation  of TF Schema. You see the functions or read
#the document for a better explanation.
#input:list target X and Y
#output: doc weighted 1, doc weighted 2, doc aligned 2 seeing the first
def tf_idf(list1, list2):
    j_bar=0
    doc_mix = []
    gold = []
    temp = []
    temp_repl=[]
    fusion_list = []
    not_replicated=[]
    fusion_list.append(list1.copy())
    fusion_list.append(list2.copy())  # lista1 U lista2

    # frequency for each term  in doc j
    for i in range(0, len(fusion_list)):
        p = ProgressBar(widgets=['Working TF-IDF doc '+str(i), ':', Percentage(), ' ', AnimatedMarker(markers='←↖↑↗→↘↓↙')],
                        min_value=0,
                        max_value=len(fusion_list[i]))#a simple bar
        p.start(0)

        for j in (fusion_list[i]):  # for each word of doc(set) count the occurrences inside the doc
            if scan(j, temp_repl):
                temp_repl.append(j)
                p.update(j_bar)
                # tf
                n_i = 1 #of course

                fr_i = sim_word_net_for_fr(j, fusion_list[i])

                # idf
                if (sim_word_net(j, fusion_list[1 - i])):  # look at the opposite list!
                    # return True? --> it means that it is a very similar  word
                    n_i = n_i + 1
                w = round((1 + round(math.log10(fr_i), 2)) * (round(math.log10(1+2/n_i), 2)),2)  # tf-idf
                temp.append(w)
            j_bar=j_bar+1
        j_bar=0
        doc_mix.append(temp.copy())  # first list -> doc weight 1 second list -> doc weight 2
        temp.clear()
        not_replicated.append(temp_repl.copy())
        temp_repl.clear()
        p.finish()

    p = ProgressBar(
        widgets=['Working the best pair synonymous-term:', Percentage(), ' ', AnimatedMarker(markers='←↖↑↗→↘↓↙')],
        min_value=0, max_value=len(list1))
    p.start(0)
    #this is very important for the alignment of the terms doc 2 with doc 1
    #(because, i will compute the weighted doc1 and 2 through the scalar product)
    for word1 in not_replicated[0]:
        t=0.
        flag=False
        p.update(j_bar)
        if word1 in not_replicated[1]:
            gold.append(doc_mix[1][not_replicated[1].index(word1)])
            flag=True

        if not flag:
            for word2 in not_replicated[1]:
                wordFromList1 = wordnet.synsets(word1)
                if wordFromList1:
                    wordFromList2 = wordnet.synsets(word2)
                    if wordFromList2:
                        s = wordFromList1[0].wup_similarity(wordFromList2[0])
                        if s != None and s > t:
                            t = s
                            save_for_index = word2

            if (t > 0.90):
                gold.append(doc_mix[1][not_replicated[1].index(save_for_index)])
            else:
                gold.append(0.0)



        j_bar=j_bar+1
    p.finish()
    return doc_mix[0], gold, doc_mix[1]
