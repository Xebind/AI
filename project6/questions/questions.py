# -*- coding: utf-8 -*-
import nltk
import os
import sys
import string
import math

#nltk.download("stopwords")

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """

    mydict = {}
    # We access the files in our corpus
    for file in os.listdir(directory):
        with open(os.path.join(directory, file), 'r', encoding="utf8") as myfile:
            data = myfile.read()
            mydict[file] = data

    return mydict


# SOLVE ENCODING - DECODING ISSUES
# ENCODE : Turns STRING to BYTES
# DECODE : Turns BYTES to STRING
# Tokenize only works with strings, but we cant print certain characters for some reason so we encode them.
def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """

    document = document.lower()
    # Hay algun caracter del dictionary que no deja imprimir bien
    #print(f"{document}")
    mylist = nltk.word_tokenize(document)
    #for word in mylist:
    #    print(f"{word}")


    # We remove punctuation and stopwords. Probably must hard code some others not included in lists
    for punctuation in mylist.copy():
        if punctuation in string.punctuation:
            mylist.remove(punctuation)
    #print(f"{mylist}")

    for stopword in mylist.copy():
        if stopword in nltk.corpus.stopwords.words("english"):
            mylist.remove(stopword)


    #for word in mylist:
        #print(f"{word.encode('utf-8')}")

    #print(f"{mylist}")
    #print(f"{mylist}")
    return mylist


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """

    # We keep track of all our words in all files
    words = set()
    for filename in documents:
        words.update(documents[filename])

    # We count in how many files each word is in and calculate idf
    idfs = {}
    for word in words:
        suma = sum(word in documents[filename] for filename in documents)
        idf = math.log(len(documents) / suma)
        # in order to print this you will have to encode utf-8 as there are weird chars
        idfs[word] = idf

    #print(f"{idfs}")
    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """

    # We create a dictionary to keep track of each file's tf-idf
    topfiles = dict.fromkeys(files)
    for file in topfiles:
        topfiles[file] = 0
    for word in query:
        for file in files:
            tf = files[file].count(word)
            #suma = sum(word in words for words in files[file])
            topfiles[file] = topfiles[file] + tf * idfs[word]

    # We order our dictionary according to values
    topfiles = {k: v for k, v in sorted(topfiles.items(), key=lambda item:item[1], reverse = True)}

    # We take the first N terms of our sorted dict, taking only the key in the list we will return
    mylist = []
    for i in range(FILE_MATCHES):
        mylist.append(list(topfiles.keys())[i])

    return mylist


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """


    # We create a dict that keeps track of "matching word measure" and "query term density" for each sentence
    topsentences = dict.fromkeys(sentences)
    for sentence in topsentences:
        topsentences[sentence] = [0, 0]

    # We determine the matching word measure for each sentence

    for sentence in sentences:
        wordcounter = 0
        sentencelength = 0
        for word in query:
            if word in sentences[sentence]:
                topsentences[sentence][0] = topsentences[sentence][0] + idfs[word]
                wordcounter = wordcounter + 1
        for item in sentences[sentence]:
            sentencelength = sentencelength + 1
        # just in case
        if sentencelength != 0:
            topsentences[sentence][1] = wordcounter / sentencelength

    # We order our dictionary according to values
    topsentences = {k: v for k, v in sorted(topsentences.items(), key=lambda item: item[1], reverse = True)}
    #for sentence in topsentences:
        #print(f" matching word measure:{topsentences[sentence][0]}, query term density:{topsentences[sentence][1]}")

    #print(f"{query}")
    #print(f" matching word measure:{topsentences[next(iter(topsentences))][0]}, query term density:{topsentences[next(iter(topsentences))][1]}")

    mylist = []
    for i in range(SENTENCE_MATCHES):
        mylist.append(list(topsentences.keys())[i].encode('utf-8'))

    return mylist

if __name__ == "__main__":
    main()
