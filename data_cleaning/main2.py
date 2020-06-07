## Basic Text Pre-processing of text data
# Lower casing
# Punctuation removal
# Stopwords removal
# Frequent words removal
# Rare words removal
# Spelling correction
# Tokenization
# Stemming
# Lemmatization

import pandas as pd
from nltk.corpus import stopwords
stop = stopwords.words('english')

from textblob import TextBlob, Word

from nltk.stem import PorterStemmer
st = PorterStemmer()

## to increase the display width and display it on the same line
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

## to read the csv file
train = pd.read_csv('../Inputs/hotelData.csv', low_memory=False)

## to convert the comments to lower-case
train['Comment'] = train['Comment'].apply(lambda x: " ".join(x.lower() for x in str(x).split()))

## to remove punctuations
train['Comment'] = train['Comment'].str.replace('[^\w\s]','')

## Common word removal
freq = pd.Series(' '.join(train['Comment']).split()).value_counts()[:10]
# print(freq)
freq = list(freq.index)
train['Comment'] = train['Comment'].apply(lambda x: " ".join(x for x in str(x).split() if x not in freq))

## Rare words removal
freq = pd.Series(' '.join(train['Comment']).split()).value_counts()[-10:]
# print(freq)
freq = list(freq.index)
train['Comment'] = train['Comment'].apply(lambda x: " ".join(x for x in str(x).split() if x not in freq))

## Removal of Stop words
train['Comment'] = train['Comment'].apply(lambda x: " ".join(x for x in str(x).split() if x not in stop))

## Spelling Correction
# train['Comment'].apply(lambda x: str(TextBlob(x).correct()))
#------------------ IT TAKES A LOT OF TIME TO THESE CORRECTIONS, HENCE HERE IT IS APPLIED TO ONLY FIRST 5 ROWS!

## Tokenization - used the textblob library to first transform our tweets into a blob and then converted them into a series of words.
# TextBlob(train['Comment'][1]).words
# print(TextBlob(train['Comment'][1]).words)

## Stemming - the removal of suffices, like “ing”, “ly”, “s”, etc. by a simple rule-based approach.
# train['Comment'][:5].apply(lambda x: " ".join([st.stem(word) for word in str(x).split()])) # Preferring Lemmatization over Stemming

## Lemmatization
# a more effective option than stemming because it converts the word into its root word, rather than just stripping the suffices
# It makes use of the vocabulary and does a morphological analysis to obtain the root word
# Therefore, we usually prefer using lemmatization over stemming.-----------------------------------------
train['Comment'] = train['Comment'].apply(lambda x: " ".join([Word(word).lemmatize() for word in str(x).split()]))

print(train['Comment'].head())

train.to_csv('./Outputs/output-main2-hotelData.csv')