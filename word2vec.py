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
  # years = [x for x in range(1970, 2020+1)]
  years = [x for x in range(2019, 2020+1)]
  months = [x for x in range(1, 12+1)]

  paths = ["processed_data/{}/{}/".format(year, month) for year in years for month in months]
  files = list_files(paths)
  print('Detected', len(files), 'files')
  
  abstracts = []
  for file in files:
    with open(file, 'r') as f:
      data = f.read()
      parsed_data = json.loads(data)
      if parsed_data['abstract'] != None:
        abstracts.append(parsed_data['abstract'])

  return abstracts
  # corpus_of_text = ""
  # for abstract in abstracts:
  #   corpus_of_text += abstract
  
  # return corpus_of_text

def load():
  model = Word2Vec.load('model.data')
  wv = KeyedVectors.load('word_vectors.data', mmap = 'r')

  return model, wv
  # vector = wv['computer']
  # print(wv.most_similar('construction'))

def generate_dictionary():
  words = dict()
  words[0] = "commerce, market, construction, engineering, machinery, transportation, service".split(', ')
  words[1] = "media, telecommunication, telephony, movie, program, communication".split(', ')
  words[2] = "car, motorcycle, commerce, market, hotel, restaurant, fabric, clothes, utility, domestic, travel, recreation".split(', ')
  words[3] = "agriculture, livestock, food, drink, commerce, market, cleaning".split(', ')
  words[4] = "property, residence, house, pension, insurance".split(', ')
  words[5] = "packing, wood, paper, material, mining, chemical, steel".split(', ')
  words[6] = "oil, gas, fuel, biofuel".split(', ')
  words[7] = "health, commerce, market, medicine, drug, hospital, diagnosis".split(', ')
  words[8] = "computer, program, service, technology, information, software".split(', ')
  words[9] = "water, sanitation, sewer, electricity, energy, gas, utility".split(', ')

  return words

def similarities(wv, keywords):
  dictionary = dict()

  for key in keywords:
    dictionary[key] = flatten([list_similar_words(wv, word) for word in keywords[key]])

  with open('dictionary.json', 'w') as file:
    file.write(json.dumps(dictionary, indent = 2))
    

def list_similar_words(wv, word):
  similar_words = wv.most_similar(word)

  return [pair[0] for pair in similar_words] 

def run():
  # text = read_data()
  # text = text.lower()
  # text = re.sub('[^a-zA-Z]', ' ', text)
  # text = re.sub(r'\s+', ' ', text)
  # sentences = nltk.sent_tokenize(text)
  # words = [nltk.word_tokenize(sentence) for sentence in sentences]

  # text = read_data()
  # print('Finished reading data')

  # text = [sentence for sentence in text if sentence != None] # remove NoneType - maybe some files are empty?
  # print('Finished removing empty sentences')

  # text = [sentence.lower() for sentence in text]
  # print('Finished lowering sentences')
  
  # text = [re.sub('[^a-zA-Z]', ' ', sentence) for sentence in text]
  # print('Finished regex parsing 1')
  
  # text = [re.sub(r'\s+', ' ', sentence) for sentence in text]
  # print('Finished regex parsing 2')
  
  # sentences = [nltk.word_tokenize(sentence) for sentence in text]
  # print('Finished tokenization')

  # for i in range(len(words)):
  #   words[i] = [w for w in words[i] if w not in stopwords.words('english')]

  sentences = []
  years = [x for x in range(2011, 2020+1)]
  
  for year in years:
    file = open('parsed_data/parsed_{}.data'.format(str(year)), 'r')
    sentences.append(file.read().splitlines())

  sentences = flatten(sentences)
  print('Read', len(sentences), 'sentences')

  sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
  print('Finished tokenization')

  print('Training model')
  model = Word2Vec(sentences, min_count = 1)
  print('Model trained, saving model and word vectors')

  word_vectors = model.wv

  word_vectors.save('word_vectors.data')
  model.save('model.data')

# run()

keywords = generate_dictionary()
_, wv = load()
similarities(wv, keywords)


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
