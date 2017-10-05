"""
create inverted index

Author: Bei-Chen Li
"""
import pickle
import re
import os

path = os.path.dirname(os.path.abspath(__file__)) + '/shakespeare_collection'


class Indexer(object):
    def __init__(self, path):

        self.path = path
        self.doc_id_dict = {}
        self.id = 0
        self.create_doc_id()

    def create_doc_id(self):
        """
        assign an id to each txt file
        storage documents id
        """
        for root, dirs, files in os.walk(self.path):
            for name in files:
                self.doc_id_dict[self.id] = os.path.join(root, name)
                self.id += 1
        with open("doc_id.pkl", "wb") as out_file:
            pickle.dump(self.doc_id_dict, out_file)

    def separate_words(self, doc_id):
        """
        split the file to get a list of words
        :param doc_id: file's id
        :return: a list of tuples like (word, doc_id)
        """
        with open(self.doc_id_dict[doc_id], "rt") as in_file:
            text = in_file.read()
        splitter = re.compile('\\W*')
        return [(s.lower(), doc_id) for s in splitter.split(text) if s != '']

    def create_inverted_index(self):
        """
        create inverted index and save the the dictionary and the postings lists in 'inverted_index.pkl'
        """
        words_list = []
        for doc_id in range(self.id):
            words_list += self.separate_words(doc_id)
        words_set = sorted(set(words_list))
        word = Word(words_set[0][0])
        dictionary = dict()
        dictionary[word.get_word()] = word
        for t in words_set:
            if t[0] == word.get_word():
                word.add(t[1])
            else:
                word = Word(t[0])
                word.add(t[1])
                dictionary[word.get_word()] = word
        with open("inverted_index.pkl", "wb") as out_file:
            pickle.dump(dictionary, out_file)


class Word(object):
    """
    information of a word in dictionary
    """
    def __init__(self, word):
        self.word = word

        # the number of documents which contain each term, which is here also the length of self.index
        self.frequency = 0

        # inverted index
        self.index = []

    def add(self, doc_id):
        """
        append a doc_id to the inverted index list
        """
        self.frequency += 1
        self.index.append(doc_id)

    def get_word(self):
        return self.word

    def get_index(self):
        return self.index

    def get_frequency(self):
        return self.frequency
