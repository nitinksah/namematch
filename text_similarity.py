# Python imports
from fuzzywuzzy import fuzz
import numpy as np
import re

# Local imports
from preprocess.text_preprocessing import ProcessText
from preprocess.text_preprocessing import get_soundex, findSubsets, stringExpander, removeMatchedWord

# Accessing the process_text as an object
process_text = ProcessText()

# String expander
string_expander = stringExpander()

digit_mapping = {
    "1": "a",
    "2": "b",
    "3": "c",
    "4": "d",
    "5": "e",
    "6": "f",
    "7": "g",
    "8": "h",
    "9": "i",
    "0": "j",
}


class similarText:
    def __init__(self, query_string, search_text):
        self.lenEqual = True if len(query_string[0].split(" ")) == len(search_text[0].split(" ")) else False

        if len(query_string[0].split(" ")) == len(search_text[0].split(" ")):
            if len(query_string[0]) < len(search_text[0]):
                query_string[0], search_text[0] = search_text[0], query_string[0]

        self.similar_trademark = []
        self.query_string = query_string

        self.coded_string = []
        self.subset_len = []

        self.idx = 0
        for self.idx in range(len(self.query_string)):
            self.query_string[self.idx] = self.digit2Char(self.query_string[self.idx])
            sl, cs = self.getCodedString(self.query_string[self.idx])

            self.coded_string.append(cs)
            self.subset_len.append(sl)

        self.search_text = search_text

    @staticmethod
    def sortedSentence(Sentence):
        # Splitting the Sentence into words
        words = Sentence.split(" ")
        # Sorting the words
        words.sort()
        # Making new Sentence by
        # joining the sorted words
        newSentence = " ".join(words)
        # Return newSentence
        return newSentence

    @staticmethod
    def getCodedString(trademark):
        trademark = trademark.strip()
        token_text = trademark.split(" ")

        coded_sentence = []
        for token in token_text:
            if token == "":
                continue
            coded_sentence.append(get_soundex(token))
        return len(token_text), "_".join(coded_sentence)

    def getSearchQuerySubset(self, tokenize_sentence, q_idx):
        index_sequence = np.arange(0, len(tokenize_sentence))

        subset_pair_len = self.subset_len[q_idx]
        tokenize_sentence = self.sortedSentence(" ".join(tokenize_sentence))
        query_string = self.sortedSentence(self.query_string[self.idx])

        if tokenize_sentence == query_string:
            subset_pair_len = self.subset_len[q_idx]

        elif len(tokenize_sentence.split(" ")) == len(self.query_string[self.idx].split(" ")) and len(
                tokenize_sentence.split(" ")) > 1:
            tokenize_sentence = self.sortedSentence(tokenize_sentence)
            query_string = self.sortedSentence(query_string)

            if self.getCodedString(tokenize_sentence) == self.getCodedString(query_string):
                self.query_string[self.idx] = tokenize_sentence
                subset_pair_len = self.subset_len[q_idx]
            else:
                """
                new updated changes
                """
                query_string, tokenize_sentence = removeMatchedWord(query_string, tokenize_sentence)
                if len(tokenize_sentence.split(" ")) == len(query_string.split(" ")):
                    self.query_string[self.idx] = query_string
                    subset_pair_len = self.subset_len[q_idx]
                else:
                    subset_pair_len = self.subset_len[q_idx] - 1

        tokenize_sentence = tokenize_sentence.split(" ")

        ind_subsets = findSubsets(index_sequence, subset_pair_len)
        string_subsets = []
        for inx_subset in ind_subsets:
            string_subset = []
            for idx in inx_subset:
                string_subset.append(tokenize_sentence[idx])

            string_subset = " ".join(string_subset)
            string_subsets.append(string_subset)

        return string_subsets

    @staticmethod
    def index(sub_str, str):
        # All occurrences of substring in string
        res = [i.start() for i in re.finditer(sub_str.lower(), str.lower())]

        return len(res)

    @staticmethod
    def digit2Char(sentence):
        x = list(sentence)
        for idx, key in enumerate(digit_mapping):
            try:
                digit_idx = x.index(key)
            except:
                continue
            x[digit_idx] = digit_mapping[key]

        x = "".join(x)
        return x

    def checkSimilarity(self, string_subsets, q_idx):
        remove_duplication = []
        for subset in string_subsets:
            if " ".join(sorted(subset.split(" "))) in remove_duplication:
                continue
            else:
                remove_duplication.append(" ".join(sorted(subset.split(" "))))
        string_subsets = remove_duplication

        coded_sentence = []
        self.query_string[self.idx] = self.sortedSentence(self.query_string[self.idx])
        for sentence in string_subsets:
            query_string = string_expander(sentence, self.query_string[self.idx])
            sentence = self.sortedSentence(sentence)
            _, coded_string = self.getCodedString(query_string)

            sentence = self.digit2Char(sentence)

            _, code = self.getCodedString(sentence)

            code_split = code.split("_")
            query_split = coded_string.split("_")

            dict_ = {}
            percentage_ratio = []

            split_sentence = sentence.split(" ")
            split_query_string = query_string.split(" ")

            # swapping
            if len(code_split) > len(query_split):
                code_split, query_split = query_split, code_split
                split_sentence, split_query_string = split_query_string, split_sentence

            while "" in split_sentence:
                split_sentence.remove("")
            while "" in split_query_string:
                split_query_string.remove("")

            for idx in range(len(code_split)):
                word_ratio = []
                for idx1 in range(len(query_split)):
                    ratio = fuzz.ratio(code_split[idx], query_split[idx1])
                    string_ratio = fuzz.ratio(split_sentence[idx], split_query_string[idx1])

                    if "-".join(sorted([split_sentence[idx], split_query_string[idx1]])) in dict_:
                        break
                    else:
                        dict_["-".join(sorted([split_sentence[idx], split_query_string[idx1]]))] = 1
                    print(split_sentence[idx], "/", split_query_string[idx1])
                    print(ratio, "/", string_ratio)
                    if string_ratio > 75:
                        word_ratio.append(ratio)
                    else:
                        word_ratio.append(string_ratio)
                if len(word_ratio) != 0:
                    percentage_ratio.append(max(word_ratio))

            if len(percentage_ratio) != 0:
                print(percentage_ratio)
                avg_ratio = np.mean(percentage_ratio)
                if avg_ratio > 50:
                    if self.index(self.query_string[self.idx], sentence) > 0:
                        coded_sentence.append(100)
                coded_sentence.append(avg_ratio)
            else:
                print("ERROR: numpy mean on empty list")
                continue
        return coded_sentence

    @staticmethod
    def checkThreshold(coded_sentence):
        min_ = min(coded_sentence)
        max_ = len([score for score in coded_sentence if score > 59])
        if coded_sentence.count(min_) > max_:  # len(coded_sentence) / 2:
            return np.mean(coded_sentence)
        return coded_sentence[np.argmax(coded_sentence)]

    def trademark_report(self):

        global thresh
        for wordmark in self.search_text:

            tokenize_sentence = wordmark.split(" ")
            for q_idx in range(len(self.subset_len)):
                string_subsets = self.getSearchQuerySubset(tokenize_sentence, q_idx)
                for string_subset in string_subsets:
                    if type(string_subset) == str:
                        string_subsets = list(set(string_subsets))
                coded_sentence = self.checkSimilarity(string_subsets, q_idx)

                thresh = self.checkThreshold(coded_sentence)

        return thresh

