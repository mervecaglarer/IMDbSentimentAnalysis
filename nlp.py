import io, os
import re as re
import zipfile as zipfile
import sys
import random
import math 
import time
from functools import reduce
import csv
import json 

class Classifier(object):
    fileUrl = ""
    docListTrain={0:{},1:{}}
    docListTest={}
    def __init__(self):
        #Init train data
        with open('sentimentData.csv',encoding='UTF-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count += 1
                else:
                    document={
                        'text' : row[0]
                    }
                    if row[1] == 'positive':
                        self.docListTrain[0][line_count] = document
                    elif row[1] == 'negative':
                        self.docListTrain[1][line_count] = document
                    line_count += 1

        #Init test data
        line_count = 0
        file = open("tmp/comments.csv","r",encoding='UTF-8')
        for row in file:
            comment = row[:-1]
            comment = json.loads(comment)
            self.docListTest[list(comment.keys())[0]]={}
            self.docListTest[list(comment.keys())[0]]['text'] = list(comment.values())[0]

    def normalize(self,text):
        # Non-breaking to normal space
        NON_BREAKING = re.compile(u"\s+"), " "
        # Multiple dot
        MULTIPLE_DOT = re.compile(u"\.+"), "."
        # Sentence dots
        SENTENCE_DOT = re.compile(u"(?!\B\"\s+[^\"]*)[\.?!](?![^\"]*\s+\"\B)"), r" -d- "
        # Merge multiple spaces.
        ONE_SPACE = re.compile(r' {2,}'), ' '
        # Numbers
        NUMBERS= re.compile(r'[0-9]*[0-9]'), ' ' 
        # 2.5 -> 2.5 - asd. -> asd . 
        DOT_WITHOUT_FLOAT = re.compile("((?<![0-9])[\.])"), r' '
        # 2,5 -> 2,5 - asd, -> asd , 
        COMMA_WITHOUT_FLOAT = re.compile("((?<![0-9])[,])"), r' '
        # doesn't -> doesn't  -  'Something' -> ' Something '
        QUOTE_FOR_NOT_S = re.compile("\b(?<![n])[\'](?![t])\b"), r' '
        AFTER_QUOTE_SINGLE_S = re.compile("\s+[s]\s+"), r' '
        # Extra punctuations "!()
        NORMALIZE = re.compile("([\–])"), r'-'
        EXTRAS_PUNK = re.compile("([^\'\.\,\w\s\-\–])"), r' '

        REGEXES = [
            NON_BREAKING,
            MULTIPLE_DOT,
            NUMBERS,
            QUOTE_FOR_NOT_S,
            AFTER_QUOTE_SINGLE_S,
            SENTENCE_DOT,
            DOT_WITHOUT_FLOAT,
            COMMA_WITHOUT_FLOAT,
            NORMALIZE,
            EXTRAS_PUNK,
            ONE_SPACE
        ]
        text = text.lower()
        for regexp, subsitution in REGEXES:
            text = regexp.sub(subsitution, text)
        return text

    def tokenizer(self,text):
        normalizedText = self.normalize(text)
        tokens = normalizedText.split('-d-')
        tokens = "</s> <s>".join(tokens)
        tokens = tokens.split(' ')
        tokens[0] = "<s>"
        tokens[len(tokens)-1] = "</s>"
        return tokens

    def tokenizers(self):
        for sit, docs in self.docListTrain.items():
            self.docListTrain[sit]['all_tokens'] = []
            for key,value in docs.items():
                if key != 'all_tokens':
                    tokens = self.tokenizer(value['text'])
                    self.docListTrain[sit][key]['tokens'] = tokens
                    self.docListTrain[sit]['all_tokens'].extend(tokens)

        for idx, doc in self.docListTest.items():
            tokens = self.tokenizer(doc['text'])
            self.docListTest[idx]['tokens'] = tokens

    # Getting 2 dictionary, like {abc:1},{abc:1} return {abc:2}
    

    def modelling(self):
        def reducer(first, last):
            for item in last: 
                for item in last:
                    first[item] = first.get(item, 0) + last.get(item, 0)
            return first
        for sit, docs in self.docListTrain.items():
            a = self.docListTrain[sit]['all_tokens']
            tokensMap = map(lambda char: dict([[char, 1]]), a)
            wordFreq = reduce(reducer, tokensMap)
            totalWord = sum(list(wordFreq.values())) #count all words
            self.docListTrain[sit]['dl'] = totalWord 
            self.docListTrain[sit]['TF'] = wordFreq  # words freq for all docs of each situation 
            self.docListTrain[sit]['1-gram'] = dict()
            self.docListTrain[sit]['1-gram'].update((k, v/totalWord) for k,v in self.docListTrain[sit]['TF'].items())

    def fit(self):
        posCount=0
        negCount=0
        for key,value in self.docListTest.items():
            tokens = value['tokens']
            probs = [0 for i in self.docListTrain.keys()] # probs for situation
            for sit , properties in self.docListTrain.items(): 
                for token in tokens:
                    if token in properties['1-gram'].keys():
                        probs[int(sit)] += math.log(1/properties['1-gram'][token])
            minVal = min(probs)
            if probs.index(minVal) == 0:
                posCount +=1
            else:
                negCount +=1
        summ = posCount + negCount
        percentage = (posCount/summ) * 100
        return percentage
