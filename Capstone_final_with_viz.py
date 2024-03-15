# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 10:32:35 2024

@author: Kathleen
"""

#%%reset 
#%reset

#%% test

#for local use only 
# import os
    
# os.getcwd()
# os.chdir("C:\\Users\\Kathleen\\Documents\\GitCapstone\\")

#%% Get moses files
import os
datadir='en-zh.txt'
file1 = 'TED2013.en-zh_en.txt'
file2 = 'TED2013.en-zh_zh.txt'

filepath1 = os.path.join(datadir,file1)

with open(filepath1, encoding = "utf-8") as f:
    moses_en = (item.strip() for item in f.readlines())

filepath2 = os.path.join(datadir,file2)

with open(filepath2, encoding = "utf-8") as f2:
    moses_zh = (item.strip() for item in f2.readlines())

moses_dict = dict(zip(moses_zh, moses_en))

#check dictionary. 
#moses_dict['另一种情况']


#%%remove multi-sentence 

sentence_dict = {key.replace(' ',''):value for (key, value) in moses_dict.items() if '。' not in key}
#len(sentence_dict)


#%% sentence length 

import pandas as pd 
import re

zh = pd.DataFrame(sentence_dict.keys())
zh = zh.rename(columns={0 : 'zh'})

#exclude punctuation from zhong so we can count characters
punctuation_pattern = r'[^\u4e00-\u9fa50-9\s]'

def remove_punctuation(text):
    # Use regular expression to remove punctuation/special characters
    cleaned_text = re.sub(punctuation_pattern, '', text)
    return cleaned_text

# Apply the function to each string in the series
zh['zh_0'] = zh['zh'].apply(remove_punctuation)

en = pd.DataFrame(sentence_dict.values())
en = en.rename(columns={0 : 'en'})

#combine en and zh
data = pd.concat([zh, en], axis = 1)

##EXCLUDE URLS 
website = 'www.'
data = data[~data['en'].str.contains('www.')]
#data.head(10)

data['spl_en']=data['en'].str.split()
data['ct_en'] = data['spl_en'].apply(len)
data['ct_zh'] = data['zh_0'].apply(len)

pd.set_option('display.max_columns', 10)
pd.set_option('display.max_rows', 40)

#exclude outliers 
eq1 = data['ct_en'].quantile(q=.25)
eq3 = data['ct_en'].quantile(q=.75)
data['ct_en'].describe()
IQR = eq3-eq1

zq1 = data['ct_zh'].quantile(q=.25)
zq3 = data['ct_zh'].quantile(q=.75)
data['ct_zh'].describe()
IQR = zq3-zq1

# we know the low bound must be 3 because of content tags that ar 2 char. 
data_clean = data[~((data['ct_en']<3) | (data['ct_en']>eq3+1.5*IQR))]
data_clean = data_clean[~((data_clean['ct_zh']<3) | (data['ct_zh']>zq3+1.5*IQR))]

#data_clean.describe()

data_clean['diff'] = data['ct_zh']-data['ct_en']
testset = data_clean[(data_clean['diff']>25) & (data_clean['ct_en']<10)]
pd.DataFrame.to_csv(testset, 'test.csv')

#%% basic search functions

def searchterm(term): 
    examples = list()
    for sent in sentence_dict.keys(): 
        if term in sent: 
            examples.append(sent)
    return examples

# nose = searchterm('鼻子')
# nose
# searchterm('恢复听力')

def searchterm_dict(term): 
    examples = {key:value for (key, value) in sentence_dict.items() if term in key}
    return examples

#%% Count Frequency
import re

def pre_subgrams(gram, target, phrasebook):
    phrasebook.append(gram)
    for i in range(4,1,-1): 
        if len(gram) - len(target) >= i: 
            #DROP THE LAST CHARACTER AND REPEAT
            gram = gram[1:]
            phrasebook.append(gram)
    return phrasebook

def post_subgrams(gram, target, phrasebook):
    phrasebook.append(gram)
    for i in range(4,1,-1): 
        if len(gram) - len(target) >= i: 
            #DROP THE LAST CHARACTER AND REPEAT
            gram = gram[:-1]
            phrasebook.append(gram)
    return phrasebook  

def removejunk(phrasebook):
    """Remove the entire entry if it starts or ends with a junk character, aka space or punctuation. 
    We have already kept the shortened forms of all of these grams, so keeping them or shortening them now would be duplicative. 
    """
    junk = ['(', ')', ',', '.' , '。', ' ', '!', '！', '%', '，', '（', '）', '?', '？', '"', '“', '”']
    for i in range(4): 
        for phrase in phrasebook:
            if phrase[0] in junk:
                phrasebook.remove(phrase)
            elif phrase[-1] in junk: 
                phrasebook.remove(phrase)
            else:
                continue
    #removejunk(phrasebook)
    return phrasebook

# sampy = ['看起来', ' 好的儿', '! 你是我的好朋友', '女儿在哪儿', ',女儿在哪儿', '你看 ', '你看']
# result = removejunk(sampy)
# result

def getgrams(target): 
    sentences = searchterm(target)
    #print(sentences)
    phrasebook = list()
    regex_pre =re.compile(fr'(.{{1,4}}{target})')
    regex_post=re.compile(fr'({target}.{{1,4}})')
    for sent in sentences: 
        #search for phrases
        result_pre =(re.search(regex_pre, sent))
        result_post = (re.search(regex_post, sent))
        #append phrases
        if result_pre != None:
            pre_fix = result_pre.groups()[0]
            phrasebook = pre_subgrams(pre_fix, target, phrasebook)
        if result_post != None: 
           post_fix = result_post.groups()[0]
           phrasebook = post_subgrams(post_fix, target, phrasebook)
    #remove junk 
    phrasebook = removejunk(phrasebook)
        
    return phrasebook    

# listening = getgrams('听力')
# len(listening)
# listening2 = set(listening)
# len(listening2)

#128, 96

#%% Counter Test

from collections import Counter

def countgrams(target, gram_number): 
    phrasebook = getgrams(target)
    counts = Counter(phrasebook)
    return counts.most_common(gram_number)

countgrams('走路', 10)
#%% USER count grams  - DEPRECATED

# donesy = ['DONE', 'Done', 'done']
# def user_search_loop():
#     while True: 
#         target_term = input('\n Please enter a search term of no more than 4 characters, or enter "done" to end session:')
#         if target_term in donesy: 
#             print('Thank you. 谢谢。')
#             break
#         elif len(target_term) >4: 
#             print('\n Invalid search term.') 
#         else: 
#             results = countgrams(target_term)
#             print(results)

# user_search_loop()

#%% get examples 
from collections import defaultdict

#result = countgrams('台湾', 20)


def lizigroup(target, gram_number=15): 
    result = countgrams(target, gram_number)
    top = [pair[0] for pair in result]      
    lizi = defaultdict(list)
    for gram in top: 
        for key, value in sentence_dict.items():
            if gram in key:
                lizi[gram].append({key:value})
    result={a:b for a,b in result} #make the result a dictionary so that it can be combined via dictionary comprehension
    combine_results= {key: [result[key], lizi[key]] for key in lizi}
    return combine_results

#lizigroup('走路',10)
# len(result_lizi)
# type(result_lizi)

#%% for viz:top grams

def topgram2(target, gram_number=10): 
    result = countgrams(target, gram_number)
    grams = [items for items, values in result] 
    y_values = [values for items, values in result]
    return grams, y_values

#grams, y_values = topgram2('国', 20)

#%% user gets examples 


def user_lizi(target, gram_number=10, examples=5):
    result_lizi = lizigroup(target, gram_number)
    for key, value in result_lizi.items():
        st.write(f'**Phrase: {key}.**')
        st.write(f'Number of Instances: {value[0]}. Examples below:')
        for i in range(min(examples,value[0])):
            st.write(value[1][i])


#user_lizi('美', 5, 5)


#user_lizi('美国', 3)



#%% streamlit
import streamlit as st 

from streamlit_echarts import st_echarts

scatter_data = [[eng, zhong] for eng, zhong in zip(data_clean['ct_en'], data_clean['ct_zh'])]


scatter_options = {
    "title": {
      "text": 'Sentence Length in Source Data by Language',
      "subtext": 'English vs. Chinese',
      "left": 'center'
    },
    "xAxis": {'name':'English'},
    "yAxis": {'name':'Chinese'},
    "series": [
        {
            "symbolSize": 5,
            "data": scatter_data,
            "type": "scatter",
        }
    ],
    # xAxis: [
    #   makeAxis(0, 'xAxisLeft-yAxisTop', 'carbohydrate', 'middle'),
}




def app(): 
        
    st.title("语境探秘 - Context Explorer")
    st.markdown("""Improve your Chinese through grammatical examples. Enter a term to see the most common phrases containing that term in our dataset. You may also select the number of phrases and examples to return.""")
    st.markdown("""The app presently uses a database of TED talks presented in 2013, [provided by CASCAMAT](http://www.casmacat.eu/corpus/ted2013.html). 
                All data were obtained from the [Open Parallel Corpus Project](https://opus.nlpl.eu/). For More information see J. Tiedemann, 2012, [Parallel Data, Tools and Interfaces in OPUS](http://www.lrec-conf.org/proceedings/lrec2012/pdf/463_Paper.pdf).""")
    
    target = st.text_input("Search term (Max 4 characters)", '太')

    gram_number = st.number_input("Number of phrases to return (Max 20)", min_value = 1, max_value = 20)
    examples = st.number_input("Number of examples per phrase (Max 20)", min_value = 1, max_value = 20)
    
    
    user_lizi(target, gram_number, examples)
    
    grams, y_values = topgram2(target, 10)
    

    bar_options = {
      "title": {
        "text": 'Top 10 Phrases for Search Term',
        "left": 'center'
      },
        "xAxis": {  "axisLabel": {"interval": 0, "rotate": 30 } ,
        "type": 'category',
        "data": grams, 
      },
      "yAxis": {
        "type": 'value'
      },
      "series": [
        {
          "data": y_values,
          "type": 'bar'
        }
      ]
    };
    st_echarts(options=bar_options, height="500px")

    st.markdown("**The graph below shows the lengths of English sentences in the Data set compared to Chinese sentences. Outliers have been removed using the IQR method.**")
    st_echarts(options=scatter_options, height="500px")
    

    
    
    
if __name__=='__main__':
    app()
    
    
#%% viz for streamlit 


#%% USER count grams 

# donesy = ['DONE', 'Done', 'done']
# def user_search_loop():
#     while True: 
#         target = input('\n Please enter a search term of no more than 4 characters, or enter "done" to end session:')
#         if target in donesy: 
#             print('Thank you. 谢谢。')
#             break
#         elif len(target) >4: 
#             print('\n Invalid search term.') 
#         else: 
#             user_lizi(target, 5)
#             #else: 
#              #   print('\n Invalid number.')
#             #print(output)

