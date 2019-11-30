#!/usr/bin/env python
# coding: utf-8

# # Suggesting Algorithm and Tools to be used for the given problem (Topic)

# ### Installations
# ##### pip install nltk
# ##### pip install sklearn

# ### Preparing nltk

# In[1]:
import nltk
from nltk.tokenize import word_tokenize
import webbrowser
import nltk
nltk.download('punkt')

from spellchecker import SpellChecker

spell = SpellChecker()


# ### Importing other packages

# In[2]:


import string
from sklearn.feature_extraction.text import TfidfVectorizer


# ### Cosine similarity function

# In[3]:


stemmer = nltk.stem.porter.PorterStemmer()
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)

def stem_tokens(tokens):
    return [stemmer.stem(item) for item in tokens]

# remove punctuation, lowercase, stem
def normalize(text):
    return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))

vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words='english')

def cosine_sim(text1, text2):
    tfidf = vectorizer.fit_transform([text1, text2])
    return ((tfidf * tfidf.T).A)[0, 1]


# ### Code to load csv file 

# In[4]:


# getRows(), takes the file name and returns the list of topics from the dataset
import csv


def getRows(filename):
    topics = []
    with open(filename, mode='r', encoding='utf8', errors='ignore') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            topics.append(row["Linkname"])
            line_count += 1
        return topics

# getresult takes filename and the index of the row to be searched and 
# returns the algorithm and tools corresponding to that index 
def getresult(filename, index):
    
    with open(filename, mode='r', encoding='utf8', errors='ignore') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count == index:
                print("Search: %s" % row["Linkname"] + "\nTools: %s"% row["Link"])
                

                webbrowser.open(row["Link"])
                break
            
            line_count += 1

def compare(filename1, token):
    
    with open(filename1, mode='r', encoding='utf8', errors='ignore') as csv_file1:
        csv_reader1 = csv.DictReader(csv_file1)
        #token=str(token)
        for row in csv_reader1:
            #print(row)
            if token == row['abbr']:
               
                #print("Search: %s" % row["Linkname"] + "\nTools: %s"% row["Link"])
                fullform=row["fullform"]
                print(fullform)
                return fullform
        return token
                
def listToString(s):  
    
    # initialize an empty string 
    str1 = ""  
    
    # traverse in the string   
    for ele in s:  
        str1 += ele   
        str1 +=' '
    
    # return string   
    return str1  
        

# In[ ]:

while True:
    if __name__ == '__main__':
        print('Loading file...')
        # loading dataset.csv file
        filename = 'klsgit.csv'  # name of the file to be loaded 
        topic_list = getRows(filename)
        print("")
        tokens= input('Enter the search string: ').lower()
        
        #function to split text into word
        nltk.download('stopwords')
        input_string=word_tokenize(tokens)
        filename1='abbr.csv'
        # find those words that may be misspelled
        for i in input_string:
            index1=input_string.index(i)
            misspelled = spell.unknown([i])

            for word in misspelled:
                # Get the one `most likely` answer
                autocorrected=spell.correction(word)
                print(autocorrected)
                if autocorrected !='':
                    
                    input_string[index1]=autocorrected
                    input_string1=input_string
                    print(input_string1)
                else:
                    pass
        
        #index=input_string.index(i)
            fullform=compare(filename1,i)
            input_string[index1]=fullform
            input_string1=listToString(input_string)   
            print(input_string1)  
                        
                # Get a list of `likely` options
                #print(spell.candidates(word))

        #for i in input_string:
                    
        cosine_list = {}
        for i, x in enumerate(topic_list):
            cosine_list.update({i: cosine_sim(x, input_string1)})
            print(cosine_list)
            # x=max(cosine_list)
            # print(f"{x}yyyyyyyyyyyyyyyyyyyyyy")
            if cosine_sim(x, input_string1)==0.0:
                print("no match")
                exit
            else:

                sorted_list = sorted(cosine_list.items(), key=lambda x: x[1], reverse=True)
                print(sorted_list)
                # get the index of the top result
        for x in sorted_list[:1]:
            # print(x[0])
            i=0
            if i<=0:
                getresult(filename, x[0])  # x[0] is the index of required record in dataset.csv file
                i+=1

    # In[ ]:




