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

#I find n_i of IDF smooth --> log2((1 + 2 / n_i))
#input:term and other set
#output:True or False
def sim_word_net(j, z1):
    silver = []
    wordFromList1 = wordnet.synsets(j)
    for z in wordFromList1:
        for i in range(0, len(z1)):
            wordFromList2 = wordnet.synsets(z1[i])
            for j in range(0, len(wordFromList2)):
                if wordFromList1 and wordFromList2:
                    s = z.wup_similarity(wordFromList2[j])
                    if s != None:
                        if s > 0.9:
                            return True  # so, the term exists in this document( or it's a synonyms )
    return False

#for the word frequency
def sim_word_net_for_fr(j, z1):
    silver = []
    count_fr = 0
    wordFromList1 = wordnet.synsets(j)
    for word2 in z1:
        wordFromList2 = wordnet.synsets(word2)
        for j in wordFromList2:
            if wordFromList1 and wordFromList2:
                s = wordFromList1[0].wup_similarity(j)
                if s != None and s > 0.9:
                    count_fr = count_fr + 1
                    break
    if count_fr > 0:
        return count_fr
    else:
        return 1




#I see the repl_list, and i verify if the new word is in the list ( term by term or a possible synonyms)
#if the correspondence between new word and a element of the repli_list is more than 0.85, i don't insert
#the weight term for rappresentation of doc, because i had already insert the word ( or your synonyms ) in the list.
#you see the tf_if function at line 112 to line 127
def scan(j,repl_list):
    if not repl_list: return True

    wordFromList1 = wordnet.synsets(j)

    for z in wordFromList1:
            for i in range(0,len(repl_list)):
                wordFromList2 = wordnet.synsets(repl_list[i])
                for j in range(0,len(wordFromList2)):
                    if wordFromList1 and wordFromList2:
                        s = z.wup_similarity(wordFromList2[j])
                        if s!=None:
                            if s >0.9:
                                return False


    return True


#it computes the weighting scheme (tf-idf) of all lists. The difference with vector model: I don't consider only same terms
#but also your synonyms. It's configured with 0.85 of similarity between the term considered and the all terms of the other list
#or between the term considered in same list with all your list terms for the computation  of TF Schema. You see the functions or read
#the document for a better explanation.
#input:list target X and Y
#output: doc weighted 1, doc weighted 2, doc aligned 2 seeing the first
def tf_idf(list1, list2):
    j_bar=0
    silver = []
    doc_mix_ = []
    gold = []
    temp = []
    temp_repl=[]
    fusion_list = []
    not_replicated=[]
    fusion_list.append(list1)
    fusion_list.append(list2)  # lista1 U lista2

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
                if (sim_word_net(j, fusion_list[1 - i])):  # look opposite list!
                    # return True? --> it means that is very similary as word
                    n_i = n_i + 1
                w = (1 + math.log10(fr_i)) * (math.log10((1+2 / n_i)))  # tf-idf
                temp.append(w)
            j_bar=j_bar+1
        j_bar=0
        doc_mix_.append([w for w in temp])  # first list -> doc weight 1 second list -> doc weight 2
        temp.clear()
        not_replicated.append([w for w in temp_repl])
        temp_repl.clear()
        p.finish()

    p = ProgressBar(
        widgets=['Working the best pair synonymous-term:', Percentage(), ' ', AnimatedMarker(markers='←↖↑↗→↘↓↙')],
        min_value=0, max_value=len(list1))
    p.start(0)
    #this is very important for the align of the terms doc 2 with doc 1
    #(because, i will compute the weighted doc1 and 2 through the scalar product)
    for word1 in not_replicated[0]:
        t=0
        p.update(j_bar)
        wordFromList1 = wordnet.synsets(word1)
        for z in wordFromList1:
            for word2 in not_replicated[1]:
                wordFromList2 = wordnet.synsets(word2)
                if wordFromList1 and wordFromList2:
                    s = z.wup_similarity(wordFromList2[0])
                    if s != None:
                        if s>t:
                            t=s
                            save_for_index=word2

        if t > 0.9:
            gold.append(doc_mix_[1][not_replicated[1].index(save_for_index)])
        else:
            gold.append(0.0)
        j_bar=j_bar+1
    p.finish()
    return doc_mix_[0], gold, doc_mix_[1]
