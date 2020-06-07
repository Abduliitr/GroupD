## Basic feature extraction using text data
# Number of words
# Number of characters
# Average word length
# Number of stopwords
# Number of special characters
# Number of numerics
# Number of uppercase words

import pandas as pd
from nltk.corpus import stopwords
stop = stopwords.words('english')

## to increase the display width and display it on the same line
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

## function to calculate the average-word-length in a sentence
def avg_word(sentence):
    words = str(sentence).split()
    return (sum(len(word) for word in words)/len(words))

## to read the csv file
train = pd.read_csv('../Inputs/hotelData.csv', low_memory=False)

## to calculate the word-Count in the comments
train['word_Count'] = train['Comment'].apply(lambda x: len(str(x).split(" ")))

## to calculate the char-count in the comments
train['char_Count'] = train['Comment'].str.len() #this will also include blank spaces

## to calculate the average word length of the sentence
train['avg_word']   = train['Comment'].apply(lambda x: avg_word(x))

## to count the stopwords # Some examples of stop words are: "a," "and," "but," "how," "or," and "what."
train['stopwords']  = train['Comment'].apply(lambda x: len([x for x in str(x).split() if x in stop])) 

## to count the number of special characters starting with hashtags.
train['hashtags']   = train['Comment'].apply(lambda x: len([x for x in str(x).split() if x.startswith('#')]))

## to count the number of numerics
train['numerics']   = train['Comment'].apply(lambda x: len([x for x in str(x).split() if x.isdigit()]))

## to count the number of Uppercase words
train['upper']      = train['Comment'].apply(lambda x: len([x for x in str(x).split() if x.isupper()]))

## to print the array of all the pre-processes...
print(train[['Comment','word_Count','char_Count','avg_word','stopwords','hashtags','numerics','upper']])

train.to_csv('./Outputs/output-main1-hotelData.csv')