# Python imports
from itertools import groupby
import itertools
import string
import re


class RemovePunctuation:
    """
    class to remove the corresponding punctuation from the list of punctuations
    """

    def __init__(self):
        """
        :param empty: None
        """
        self.punctuation = string.punctuation

    def __call__(self, punctuations):
        """
        Apply the transformations above.
        :param punctuation: take the single punctuation(in my case '?')
        :return: transformed punctuation list, excluding the '?'
        """
        if type(punctuations) == str:
            punctuations = list(punctuations)
        for punctuation in punctuations:
            self.punctuation = self.punctuation.translate(str.maketrans('', '', punctuation))
        return self.punctuation


# Accessing the remove_punctuation object
remove_punctuation = RemovePunctuation()


class ProcessText:
    def __init__(self):
        """
        :param empty: None
        """
        pass

    @staticmethod
    def lower_casing(text):
        text_lower = text.lower()

        return text_lower

    @staticmethod
    def tokenization(text):
        # tokenize words
        text_tokens = text.split(" ")
        return text_tokens

    @staticmethod
    def remove_salutations(text):
        text = text.replace('(huf)', '').replace('(HUF)', '')
        salutations = ['mrs ', 'smt ', 'shri ', 'shree ', 'mr ', 'm/s ', 'm/s ', 's/o ', 'd/o ', 'h/o ', 'w/o ',
                       'mrs. ', 'smt. ', 'shri. ', 'shree. ', 'mr. ', 'm/s. ', 'm/s. ', 's/o. ', 'd/o. ', 'h/o. ',
                       'w/o. ']

        for salutation in salutations:
            text = text.replace(salutation, '')
        return text

    @staticmethod
    def remove_punctuation_text(text):
        """custom function to remove the punctuation"""

        res = (re.findall(r'\w+|[^\s\w]+', text))
        name = []
        for word in res:
            clean_word = word.translate(str.maketrans('', '', remove_punctuation("")))
            if clean_word != "":
                name.append(clean_word)

        return " ".join(name)

    def __call__(self, text):
        clean_text = []
        # do the lower case casting
        text_lower = self.lower_casing(text)

        # remove salutation completely
        rm_salutations = self.remove_salutations(text_lower)

        # remove all the punctuation necessary
        rm_punctuation = self.remove_punctuation_text(rm_salutations)

        # tokenization of name
        text_tokens = self.tokenization(rm_punctuation)

        for word in text_tokens:
            clean_text.append(word)

        return [i[0] for i in groupby(clean_text)]


def get_soundex(token):
    # Get the soundex code for the string
    token = token.upper()

    soundex = ""

    # first letter of input is always the first letter of soundex
    soundex += token[0]

    # create a dictionary which maps letters to respective soundex codes. Vowels and 'H', 'W' and 'Y' will be
    # represented by '.'
    dictionary = {
        "BFPV": "1",
        "CGJKQSXZ": "2",
        "DT": "3",
        "L": "4",
        "MN": "5",
        "R": "6",
        "AEIOUHWY": ".",
    }

    for char in token[1:]:
        for key in dictionary.keys():
            if char in key:
                code = dictionary[key]
                if code != soundex[-1]:
                    soundex += code

    # remove vowels and 'H', 'W' and 'Y' from soundex
    soundex = soundex.replace(".", "")

    # trim or pad to make soundex a 4-character code
    soundex = soundex[:4].ljust(4, "0")

    return soundex


def findSubsets(s, n):
    discontinues_sequence = [list(i) for i in itertools.combinations(s, n)]
    sequence = []
    for subset in discontinues_sequence:
        sequence.append(subset[::-1])

    sequence.extend(discontinues_sequence)
    return sequence


"""
EXAMPLE 1:
    subsets = [
        "divyanshu dimri",
        "dimri divyanshu",
        "jao divyanshu",
        "jao dimri",
        "divyanshu jao",
        "dimri jao",
    ]
    input_string = "divyanshu dimrijao"

EXAMPLE 2:
    subsets = [
        "dimri divyanshu",
        "rao divyanshu",
        "mathew divyanshu",
        "rao dimri",
        "mathew dimri",
        "mathew rao",
        "divyanshu dimri",
        "divyanshu rao",
        "divyanshu mathew",
        "dimri rao",
        "dimri mathew",
        "rao mathew",
    ]
    input_string = "divyanshudimri raomathew"

string_expander = stringExpander()
string_expander(subset, input_string)
"""


class stringExpander(object):
    def __call__(self, subset, input_string):
        subset = subset.split(" ")
        input_string = input_string.split(" ")

        expanded_string = None
        for idx in range(len(input_string)):
            for sub_string in subset:

                if input_string[idx].find(sub_string) != -1:
                    start_index = input_string[idx].find(sub_string)
                    end_index = len(sub_string)

                    if len(input_string[idx]) == len(sub_string):
                        continue
                    start_idx, end_idx = start_index, start_index + end_index
                    try:
                        if input_string[idx][end_idx]:
                            expanded_string = " ".join(
                                [
                                    input_string[idx][
                                        start_index : start_index + end_index
                                    ],
                                    input_string[idx][start_index + end_index :],
                                ]
                            ).strip()
                    except:
                        expanded_string = " ".join(
                            [
                                input_string[idx][
                                    start_index : start_index + end_index
                                ],
                                input_string[idx][:start_index],
                            ]
                        ).strip()

                    input_string[idx] = expanded_string

        return " ".join(input_string)


# subset = "divyanshu dimri"
# input_string = "divyanshudimri"
# string_expander = stringExpander()
# print(string_expander(subset, input_string))

"""
Time Complexity: O(2N)
Space Complexity: O(2N)

N: Word Length/ Character Length
"""


def removeMatchedWord(query_string, tokenize_sentence):

    query_string, tokenize_sentence = query_string.split(" "), tokenize_sentence.split(" ")
    duplicates = {}

    tokenization = []
    tokenization.extend(query_string)
    query_len = len(tokenization)

    tokenization.extend(tokenize_sentence)

    for idx in range(len(tokenization)):
        if tokenization[idx] in duplicates:
            duplicates[tokenization[idx]][0] += 1
            duplicates[tokenization[idx]][1].append(idx)
        else:
            duplicates[tokenization[idx]] = [1, [idx]]

    for _, key in enumerate(duplicates):
        if duplicates[key][0] > 1:
            for idx in duplicates[key][1]:
                tokenization[idx] = ""

    query_string, tokenize_sentence = tokenization[0: query_len], tokenization[query_len:]
    return " ".join(query_string), " ".join(tokenize_sentence)
