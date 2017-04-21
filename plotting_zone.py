####################################
#file_name: plotting_zone.py       #
#author: Riccardo La Grassa        #
#data created: 16/11/2016          #
#data last modified:               #
#Python interpreter: 3.5.2         #
#mail: riccardo2468@gmail.com      #
####################################

import matplotlib.pyplot as plt
import numpy as np
from nltk import FreqDist


def autolabel_barh(rects):
    # attach some text labels
    for rect in rects:
        width = rect.get_width()
        plt.text(width+0.25,rect.get_y() + rect.get_height() / 2.1, '%d' % int(width), fontsize=6,fontweight='bold',
                 bbox=dict(facecolor='lime', boxstyle='round', alpha=0.25))

def autolabel_barv(rects,color_box):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2., 0.3+height, '%d' % int(height), fontsize=7, ha='center', va='bottom',bbox = dict(boxstyle='round', facecolor=color_box, alpha=0.25))


def analysis_word(w,str_title,n_fig):
    my_colors1 = [(1.0 / (1.0 + np.math.log2(x)), 0.0, x / len(w)) for x in range(1, len(w) + 1)]
    fig = plt.figure(n_fig, facecolor='white', edgecolor='k', figsize=(7, 9))
    #fig, ((ax1, ax2)) = plt.subplots(nrows=2)
    fig.suptitle(str_title)
    labelsW = [i[0] for i in w]
    valuesW = [i[1] for i in w]
    indexesW = [w for w in range(0,len(labelsW))]
    width = 1
    bar_w=plt.barh(indexesW, valuesW, width, color=my_colors1, align='center')
    plt.yticks(indexesW, labelsW, fontsize='10')
    autolabel_barh(bar_w)


def analysis_frequency(dateX,dateY,legend_labelX,legend_labelY):

    fig1 = plt.figure(1, facecolor='white', edgecolor='red', figsize=(13, 6))
    fig1.suptitle('Comparison numbers tweet')

    fdist1 = FreqDist(dateX)
    most_common1 = fdist1.most_common(len(dateX))
    most_common1.sort()
    labelsX = [i[0] for i in most_common1]
    valuesX = [i[1] for i in most_common1]

    fdist2 = FreqDist(dateY)
    most_common2 = fdist2.most_common(len(dateY))
    most_common2.sort()
    labelsY = [i[0] for i in most_common2]
    valuesY = [i[1] for i in most_common2]

    indexesX = np.arange(len(labelsX))
    width = 0.4

    my_colors = [(0.0, 0.0, x / len(labelsX)) for x in range(1, len(labelsX) + 1)]

    bar_X=plt.bar(indexesX-0.3, valuesX, width, color=my_colors, align='center', label=legend_labelX)
    autolabel_barv(bar_X,'blue')

    indexesY = np.arange(len(labelsY))
    bar_Y=plt.bar(indexesY, valuesY, width, fc=(1, 0, 0, 0.4), align='center', label=legend_labelY)
    autolabel_barv(bar_Y,'red')
    plt.xticks(indexesX, labelsX, rotation='vertical', fontsize='7')
    plt.legend(loc='upper right')

    ###########################################################################
    ###################plot frequencies####################
    fig2 = plt.figure(2, facecolor='white', edgecolor='red', figsize=(13, 5))
    fig2.suptitle('Plot tweetX frequencies of '+legend_labelX)
    plt.xticks(indexesX, labelsX, rotation='vertical', fontsize='7')
    plt.plot(indexesX, valuesX, color='b')

    fig3 = plt.figure(3, facecolor='white', edgecolor='red', figsize=(13, 5))
    fig3.suptitle('Plot tweetY frequencies of '+legend_labelY)
    plt.xticks(indexesY, labelsY, rotation='vertical', fontsize='7')
    plt.plot(indexesY, valuesY, color='r')