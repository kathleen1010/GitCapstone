# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 10:32:35 2024

@author: Kathleen
"""

#%%reset 
#%reset

#%% test
#%% Import moses
filepath = 'C:/Users/Kathleen/Documents/GitCapstone/en-zh.txt/TED2013.en-zh_en.txt'

with open(filepath, encoding = "utf-8") as f:
    moses_en = (item.strip() for item in f.readlines())

filepath2 = 'C:/Users/Kathleen/Documents/GitCapstone/en-zh.txt/TED2013.en-zh_zh.txt'

with open(filepath2, encoding = "utf-8") as f2:
    moses_zh = (item.strip() for item in f2.readlines())

moses_dict = dict(zip(moses_zh, moses_en))

#check dictionary. 
#moses_dict['另一种情况']

#%%remove multi-sentence 

sentence_dict = {key.replace(' ',''):value for (key, value) in moses_dict.items() if '。' not in key}
#len(sentence_dict)
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
    junk = ['(', ')', ',', '.' , '。', ' ', '!', '！', '%', '，', '（', '）']
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

#countgrams('美国', 10)
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

#%% user gets examples 
import streamlit as st 

def user_lizi(target, gram_number=10, examples=5):
    result_lizi = lizigroup(target, gram_number)
    for key, value in result_lizi.items():
        st.write(f'**Phrase: {key}.**')
        st.write(f'Number of Instances: {value[0]}. Examples below:')
        for i in range(examples):
            try:
                st.write(value[1][i])
            except IndexError:
                st.write('No more examples found / 没有例子了。')


#user_lizi('美', 5, 5)


#user_lizi('美国', 3)


#%%FOR STREAMLIT 

import streamlit as st 

def app(): 
        
    st.title("找例子机 - Example Finder App")
    st.markdown("""Improve your Chinese through grammatical examples. Enter a term to see the most common phrases containing that term in our dataset. You may also select the number of phrases and examples to return.""")
    st.markdown("""The app presently uses a database of TED talks presented in 2013, [provided by CASCAMAT](http://www.casmacat.eu/corpus/ted2013.html). 
                All data were obtained from the [Open Parallel Corpus Project](https://opus.nlpl.eu/). For More information see J. Tiedemann, 2012, [Parallel Data, Tools and Interfaces in OPUS](http://www.lrec-conf.org/proceedings/lrec2012/pdf/463_Paper.pdf).""")
    
    target = st.text_input("Search term (Max 4 characters)", '太')

    gram_number = st.number_input("Number of phrases to return (Max 20)", min_value = 1, max_value = 20)
    examples = st.number_input("Number of examples per phrase (Max 20)", min_value = 1, max_value = 20)
    
    user_lizi(target, gram_number, examples)
    

if __name__=='__main__':
    app()

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

