"""
    Author: Cade Wormington
    Class: CS 540
    Lecture: 
"""

import os
import math

# create_vocabulary() reads all of the words of text files in training_directory and creates a vocabulary from them.
# training_directory is the base directory of the labels and their text files.
# cutoff is the threshold for the amount of times a word must appear to be added to the vocabulary.
def create_vocabulary(training_directory, cutoff):
    # vocabDict is a dictionary that contains each word found as keys and the count of how many times 
    # they appear as the values.
    vocabDict = {}

    # This for loop first finds the label directories in the training_directory. It then iterates through
    # the text files in each label directory to get the words from each file. It then counts the amount of 
    # times it sees a word.
    for dir in os.scandir(training_directory):
        for textFile in os.scandir(dir):
            with open(textFile, encoding="utf8") as text:
                for line in text:
                    wordType = line.rstrip()
                    
                    if wordType in vocabDict:
                        vocabDict[wordType] += 1
                    else:
                        vocabDict[wordType] = 1

    # vocabList is the vocabulary list that will be returned.
    vocabList = []

    # This for loop goes through each word in vocabDict and only adds the ones that pass the count cutoff to
    # vocabList.
    for word in vocabDict:
        if vocabDict[word] >= cutoff:
            vocabList.append(word)

    # vocabList is sorted before it is returned.
    vocabList.sort()

    return vocabList

# create_bow uses a vocabulary list to create a bag-of-words dictionary of a file.
# vocab is the vocabulary list for create_bow() to use.
# filepath is the path to the file that create_bow() should create a bag-of-words from.
def create_bow(vocab, filepath):
    # bowDict is the dictionary object that will be added to and eventually returned.
    bowDict = {}
    
    # The function opens a file and iterates through it line by line. If a word is in the vocabulary,
    # its value is incremented in the dictionary. If a word is not, the value for the dictionary key None
    # is incremented.
    with open(filepath, encoding="utf8") as textFile:
        for line in textFile:
            word = line.rstrip()
            if word in vocab:
                if word in bowDict:
                    bowDict[word] += 1
                else:
                    bowDict[word] = 1
            else:
                if None in bowDict:
                    bowDict[None] += 1
                else:
                    bowDict[None] = 1
    
    return bowDict

# load_training_data() uses a vocabulary to create a bag-of-words for each text file in the given label directories.
# vocab is the vocabulary to use.
# directory is the directory that contains directories of labels and their text files.
def load_training_data(vocab, directory):
    # dictList is the list of dictionaries that will be returned.
    dictList = []

    # This for loop iterates through each label directory and creates a bag-of-words for each file.
    # The labels and bags are both kept in a dictionary that is appended to dictList.
    for dir in os.scandir(directory):
        for textFile in os.scandir(dir):
            dictList.append({'label': dir.name, 'bow': create_bow(vocab, textFile.path)})

    return dictList

# prior() gets the prior probability of a file being a label and returns it as a log probability.
# training_data is the list of dictionaries containing a label and bag-of-words for each file.
# label_list is the list of labels to get the probabilities for.
def prior(training_data, label_list):
    # priorProbs is the dictionary that contains labels as keys and their log probabilities as values.
    priorProbs = {}

    # This for loop counts the amount of files that fall under each label and obtains the count / total files.
    # The count / total files is used as the probability that a file falls under that label.
    for label in label_list:
        count = 0
        for trainDict in training_data:
            if trainDict['label'] == label:
                count += 1
        priorProbs[label] = math.log(count/len(training_data))

    return priorProbs 

# p_word_given_label() returns a dictionary of vocab words and their log probabilities of appearing given a label.
# vocab is the vocabulary to use.
# training_data is the list of dictionaries containing a label and bag-of-words for each file.
# label is the given label used in calculating conditional probability. 
def p_word_given_label(vocab, training_data, label):
    # All words in the vocabulary are added to wordCounts as keys.
    # All of the values in wordCounts are set to 0 initially.
    wordCounts = {}
    for word in vocab:
        wordCounts[word] = 0
    
    # None is added to wordCounts since it does not exist in the vocabulary.
    wordCounts[None] = 0

    # numWords keeps track of the total amount of words that are in a label's files.
    numWords = 0

    # This for loop goes through each item in training_data that matches the specified label.
    # If the label matches, the counts of the words in each file are added to their respective values in
    # wordCounts.
    # This also increases numWords to count words.
    for trainDict in training_data:
        if trainDict['label'] == label:
            for wordFromBag in trainDict['bow']:
                wordCounts[wordFromBag] += trainDict['bow'][wordFromBag]
                numWords += trainDict['bow'][wordFromBag]

    # wordProbs is a dictionary where keys are words in the vocabulary and values are log probabilities.
    wordProbs = {}

    # Log probabilities are computed for each word in the vocabulary. Add-1 smoothing is used.
    # Probabilities are calculated as (countOfWord + 1) / (sizeOfVocab + numWords). The log of this value is then taken.
    for countedWord in wordCounts:
        wordProbs[countedWord] = math.log((wordCounts[countedWord] + 1) / (len(wordCounts) + numWords))

    return wordProbs

# train() uses the previous set of functions to compile a training model for a corpus and returns it.
# training_directory is the base directory of the labels and their text files.
# cutoff is the threshold for the amount of times a word must appear to be added to the vocabulary.
def train(training_directory, cutoff):
    # voc is the vocabulary created from the given training_directory and cutoff.
    voc = create_vocabulary(training_directory, cutoff)

    # t is the training data gathered from each file in the training_directory.
    t = load_training_data(voc, training_directory)

    # The two above variables are used in conjunction with the helper methods to create
    # a training model. This model is returned.
    return {
        'vocabulary': voc,
        'log prior': prior(t, ['2016', '2020']),
        'log p(w|y=2016)':p_word_given_label(voc, t, '2016'),
        'log p(w|y=2020)':p_word_given_label(voc, t, '2020')
    }

# classify() uses a given model to predict whether a given file will be from 2016 or 2020.
# model is the training model used for prediction.
# filepath is the path to the file that we want to run a prediction on.
def classify(model, filepath):
    # The initial probabilities are set to the prior log probabilities of being a 2016 or 2020 file respectively.
    prob2016 = model['log prior']['2016']
    prob2020 = model['log prior']['2020']

    # fileBow is a bag-of-words created using the model's vocabulary and the given file's content
    fileBow = create_bow(model['vocabulary'], filepath)

    # The log probabilities are each added with the log probabilities of vocabulary words that are 
    # found in the given file.
    for fileWord in fileBow:
        prob2016 += (model['log p(w|y=2016)'][fileWord] * fileBow[fileWord])
        prob2020 += (model['log p(w|y=2020)'][fileWord] * fileBow[fileWord])

    # A prediction (2016 or 2020) is selected based on the resulting log probabilities.
    selected = None
    if prob2016 > prob2020:
        selected = '2016'
    else:
        selected = '2020'

    # A dictionary specifying our model's prediction and the log probabilities of a file being from 2016 or 2020
    # are added to a dictionary and returned.
    retDict = {
        'predicted y': selected,
        'log p(y=2016|x)': prob2016,
        'log p(y=2020|x)': prob2020
    }

    return retDict
