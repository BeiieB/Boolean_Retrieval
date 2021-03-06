import os
import pickle
from crawler import Crawler
from indexer import Indexer
from indexer import Word

path = os.path.dirname(os.path.abspath(__file__))


class Query(object):
    def __init__(self, doc_dict_length):
        """
        doc_dict_length: length of doc_dict
        dictionary: word dictionary
        """
        self.doc_dict_length = doc_dict_length
        with open("inverted_index.pkl", "rb") as in_file:
            self.dictionary = pickle.load(in_file)

    def get_doc_list(self, s):
        """
        get inverted index by given string, possibly including OR, NOT
        :return: list of inverted index
        """
        if 'AND' in s:
            return self.intersect([st.strip() for st in s.split('AND')])
        if 'NOT'in s:
            return self.complement_list(self.dictionary[s.replace('NOT ', '').lower()].get_index())
        return self.dictionary[s.lower()].get_index()

    def intersect_list(self, list1, list2):
        """
        two lists' intersection. Algorithm in section 1.3 figure 1-6
        :param list1: inverted index of word1
        :param list2: inverted index of word2
        :return:list
        """
        res = []
        p1 = p2 = 0
        while p1 != len(list1) and p2 != len(list2):
            if list1[p1] == list2[p2]:
                res.append(list1[p1])
                p1 += 1
                p2 += 1
            elif list1[p1] < list2[p2]:
                p1 += 1
            else:
                p2 += 1

        return res

    def union_list(self, list1, list2):
        """
        two lists' union
        :param list1: inverted index of word1
        :param list2: inverted index of word2
        :return:merged list
        """
        return sorted(list1+list2)

    def complement_list(self, alist):
        """
        NOT query
        :param alist: inverted index
        :return: [all index - index in list]
        """
        return list(set(range(self.doc_dict_length)) - set(alist))

    def intersect(self, words):
        """
        AND query. Algorithm in section 1.3 figure 1-7
        :param words: a list of words
        :return: intersection of all words' inverted index
        """
        if len(words) == 1:
            return self.get_doc_list(words[0])
        # words = sorted(words, key=lambda x: self.dictionary[x].get_frequency())
        res = self.get_doc_list(words[0])
        words = words[1:]
        while len(words) != 0:
            res = self.intersect_list(res, self.get_doc_list(words[0]))
            words = words[1:]

        return res

    def union(self, words):
        """
        OR query
        :param words: a list of words
        :return: union of all words' inverted index
        """
        if len(words) == 1:
            return self.get_doc_list(words[0])
        # words = sorted(words, key=lambda x: self.dictionary[x].get_frequency())
        res = self.get_doc_list(words[0])
        words = words[1:]
        while len(words) != 0:
            res = self.union_list(res, self.get_doc_list(words[0]))
            words = words[1:]

        return res


def main():
    with open("doc_id.pkl", "rb") as in_file:
        doc_dictionary = pickle.load(in_file)
    q = Query(len(doc_dictionary))
    while True:
        inp = input("Input words, separated by AND OR NOT, print q to exit:")
        if inp == 'q':
            return
        try:
            res = q.union([s.strip() for s in inp.split('OR')])
            print("result of '" + inp + "':")
            for r in res:
                print(doc_dictionary[r].replace(path+'/shakespeare_collection', ''))
            print()
        except KeyError:
            print("wrong input!")


if __name__ == "__main__":
    while True:
        c = input("do you want to crawl Shakespeare's Collected Works? y/n: ")
        if c == 'y':
            print("Downloading from Internet...")
            crawler = Crawler(path)
            crawler.crawl()
            indexer = Indexer(path)
            indexer.create_inverted_index()
            main()
            break
        elif c == 'n':
            if not os.path.exists(path + '/shakespeare_collection'):
                print("no Shakespeare's Collected Works!")
                continue
            if not os.path.exists(path + '/inverted_index.pkl'):
                print("no index file, creating index...")
                indexer = Indexer(path)
                indexer.create_inverted_index()
            main()
            break
        else:
            print("wrong input!")
