# https://towardsdatascience.com/nlp-101-word2vec-skip-gram-and-cbow-93512ee24314
# https://en.wikipedia.org/wiki/Word2vec
# https://stackabuse.com/implementing-word2vec-with-gensim-library-in-python/

from gensim.models import Word2Vec
from gensim.models import KeyedVectors
from gensim.test.utils import common_texts
import nltk
from nltk.corpus import stopwords

import os
import re
import json

def flatten(input_array):
  result_array = []
  
  for element in input_array:
    if isinstance(element, str):
      if element != '':
        result_array.append(element)
    elif isinstance(element, list):
      result_array += flatten(element)
  
  return result_array

def list_files(paths):
  pwd = os.getcwd()
  files = []
  for path in paths:
    os.chdir(path)
    cwd = os.getcwd()
    for file in os.listdir('.'):
      files.append(cwd + '/' + file)
    os.chdir(pwd)

  return files

def read_data():
  years = [2017, 2018, 2019, 2020]
  months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

  paths = ["processed_data/{}/{}/".format(year, month) for year in years for month in months]
  files = list_files(paths)
  
  abstracts = []
  for file in files:
    with open(file, 'r') as f:
      data = f.read()
      parsed_data = json.loads(data)
      abstracts.append(parsed_data['abstract'])

  return abstracts
  # corpus_of_text = ""
  # for abstract in abstracts:
  #   corpus_of_text += abstract
  
  # return corpus_of_text

def run():
  # text = read_data()
  # text = text.lower()
  # text = re.sub('[^a-zA-Z]', ' ', text)
  # text = re.sub(r'\s+', ' ', text)
  # sentences = nltk.sent_tokenize(text)
  # words = [nltk.word_tokenize(sentence) for sentence in sentences]

  text = read_data()
  text = [sentence for sentence in text if sentence != None] # remove NoneType - maybe some files are empty?
  text = [sentence.lower() for sentence in text]
  text = [re.sub('[^a-zA-Z]', ' ', sentence) for sentence in text]
  text = [re.sub(r'\s+', ' ', sentence) for sentence in text]
  sentences = [nltk.word_tokenize(sentence) for sentence in text]

  # for i in range(len(words)):
  #   words[i] = [w for w in words[i] if w not in stopwords.words('english')]

  print('Processed', len(sentences), 'sentences')

  # model = Word2Vec(words, min_count = 1)
  model = Word2Vec(sentences, min_count = 1)
  print(model.wv.most_similar('tree'))
  # vocabulary = model.wv.vocab

  # word_vectors = model.wv
  # word_vectors.save('wordvectors')

  # word2vec.save('model')

run()
# model = Word2Vec.load('output.model')
# wv = KeyedVectors.load('wordvectors', mmap = 'r')
# vector = wv['computer']
# wv.most_similar('word')

# ----
# sg = 1 to change algorithm to skip=gram, otherwise it will be continuous bag of words (cbow)
# workers = Int, set number of workers
# sentences = list of sentences (headlines)
# model = Word2Vec(words, size = 100)
# word_vectors = model.wv
# del model
# ----

# model = Word2Vec([['my', 'word', 'johnny', 'boy'], ['word', 'cool', 'breeze']], min_count = 1)
# print(model.wv.most_similar('word'))
