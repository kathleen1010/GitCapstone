# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 10:32:35 2024

@author: Kathleen
"""

#%%reset 
#%reset

#%% test space 

#generator test

sample = ['edward', 'bella', 'jacob', 'renesmee', 'charlie']

genx = (name for name in sample)
geny = (len(name) for name in sample) 

namelen = dict(zip(genx, geny))
namelen['edward']

namelen.keys()

twice = {key:val*2 for (key,val) in namelen.items()}
twice

twice = {key:val*2 for (key,val) in namelen.items() if 'c' not in key}
twice
#%% Import moses
filepath = 'C:/Users/Kathleen/Documents/GitCapstone/en-zh.txt/TED2013.en-zh_en.txt'

with open(filepath, encoding = "utf-8") as f:
    moses_en = (item.strip() for item in f.readlines())

filepath2 = 'C:/Users/Kathleen/Documents/GitCapstone/en-zh.txt/TED2013.en-zh_zh.txt'

with open(filepath2, encoding = "utf-8") as f2:
    moses_zh = (item.strip() for item in f2.readlines())

moses_dict = dict(zip(moses_zh, moses_en))

#%% check dictionary. 

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


#%%remove multi-sentence 

sentence_dict = {key:value for (key, value) in moses_dict.items() if '。' not in key}

#%% search 

def searchterm(term): 
    examples = list()
    for sent in sentence_dict.keys(): 
        if term in sent: 
            examples.append(sent)
    return examples

nose = searchterm('鼻子')


def searchterm_dict(term): 
    examples = {key:value for (key, value) in sentence_dict.items() if term in key}
    return examples

nose_dict = searchterm_dict('鼻子')
nose_dict

#%% input search 
def user_searchterm(): 
    target_term = input('Please enter a search term of no more than two characters:')
    if len(target_term) >2: 
        print('Invalid search term.') 
    else: 
        results = searchterm(target_term)
    return results
user_searchterm()
