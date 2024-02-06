# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 10:32:35 2024

@author: Kathleen
"""
#%reset
import opustools

opus_reader_samp = opustools.OpusRead(
    directory='Books',
    source='en',
    target='fi')

opus_reader_samp.printPairs()
type(opus_reader_samp)
len(opus_reader_samp)
opus_reader_samp.trg_annot

#%% #attempt 2 

import opustools
#set working directory 
opus_reader = opustools.OpusRead(
    directory='TED2013',
    source='en',
    target='zh', 
    maximum= '10', 
    leave_non_alignments_out = 'True'
    )

type(opus_reader.printPairs())

#%%

import opustools
#set working directory 
opus_reader = opustools.OpusRead(
    directory='QED',
    source='zh',
    target='aa', 
    maximum= '10', 
    leave_non_alignments_out = 'True'
    )

opus_reader.add_doc_ending
opus_reader.printPairs()
opus_reader.out_put_pair("14","12")

import os
os.getcwd()



#%%

# opus_reader.
# opus_reader.out_put_pair()
# opus_reader.check_lang


#%%
opustools.OpusRead()
opus_reader = opustools.OpusRead(
    directory='TED2013',
    source='en',
    target='zh', 
    maximum= '10', 
    leave_non_alignments_out = 'True', 
    write='Ted2013',
    write_mode='normal'
    )
opus_reader.printPairs()


#%% MOSES files 
#encoding must be UTF. 
# downloaded files as MOSES 
# opened files in Visual Studio and CHANGED file endings to .txt

filepath = 'C:/Users/Kathleen/Documents/GitCapstone/en-zh.txt/TED2013.en-zh_en.txt'

with open(filepath, encoding = "utf-8") as f:
    while True:
        line = f.readline()
        if not line:
            break
        print(line.strip())


filepath2 = 'C:/Users/Kathleen/Documents/GitCapstone/en-zh.txt/TED2013.en-zh_zh.txt'

#with open(filepath2, encoding = "utf-8") as f2:
#    line = f2.readline()

with open(filepath2, encoding = "utf-8") as f2:
    while True:
        line2 = f2.readline()
        if not line2:
            break
        print(line2.strip())


#%% 
#generator test

sample = ['edward', 'bella', 'jacob', 'renesmee', 'charlie']

genx = (name for name in sample)
geny = (len(name) for name in sample) 

namelen = dict(zip(genx, geny))
namelen['edward']

namelen.keys()
#%% 
filepath = 'C:/Users/Kathleen/Documents/GitCapstone/en-zh.txt/TED2013.en-zh_en.txt'

with open(filepath, encoding = "utf-8") as f:
    moses_en = (item.strip() for item in f.readlines())

filepath2 = 'C:/Users/Kathleen/Documents/GitCapstone/en-zh.txt/TED2013.en-zh_zh.txt'

with open(filepath2, encoding = "utf-8") as f2:
    moses_zh = (item.strip() for item in f2.readlines())

moses_dict = dict(zip(moses_zh, moses_en))

#%% now that I have the dictionary, I need to check it's aligned. 

import difflib

#look up an english entry based on a chinese entry we know exists. 
moses_dict['海洋是一个非常复杂的事物。']

moses_dict['另一种情况']


#a quote we _sort of_ know exists. 
#this comes from XML  -- get need to get a fuzzy match to find out how it is spaced/ punctuated in the moses file. 
test1 = "而另一种 “方位细胞” ， 我之前没有提到它 ， 它们像指南针一样 ， 都是根据你的朝向来作出反应的"
difflib.get_close_matches(test1,moses_dict.keys())

#this key finds the correct translation. 
moses_dict['而另一种“方位细胞”， 我之前没有提到它， 它们像指南针一样，都是根据你的朝向来作出反应的。'] 


test2 = '他们是每侧最边上的两位 。 这是棒球诊所的一部分 ， 在这里我们尝试 棒球联赛 ， 国务院 ， （ 它建起了外交基础 ） 在军队中的棒球运动员 ， 也就是那些能真正上战场的人 ， 之间的合作 ， 并且他们把这种诊所 开到了拉丁美洲和加勒比地区 ， 开到了洪都拉斯 ， 开到了尼加拉瓜 ， 开到了所有中美洲和加勒比的 棒球很流行国家 ， 而且它创造了安全感 '
difflib.get_close_matches(test2,moses_dict.keys())
#once we have the right spacing, we plug that back in to the dictionary to get the value. 
test2 = '他们是每侧最边上的两位。 这是棒球诊所的一部分， 在这里我们尝试 棒球联赛， 国务院， （它建起了外交基础） 在军队中的棒球运动员， 也就是那些能真正上战场的人，之间的合作， 并且他们把这种诊所 开到了拉丁美洲和加勒比地区， 开到了洪都拉斯，开到了尼加拉瓜， 开到了所有中美洲和加勒比的 棒球很流行国家， 而且它创造了安全感。'
moses_dict[test2]



#%% 

