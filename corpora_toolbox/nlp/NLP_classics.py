# -*- coding: utf-8 -*-

"""
The :mod:`corpora_toolbox.nlp.NLP_classics` implements some of the most classic functions
used for NLP analysis.

"""

# Author: Laura Hernandez-Dominguez <laura.hzdz@gmail.com>, 2018
#         Laboratoire d'ingénierie Cognitive et Sémantique (LiNCS)
#         http://lincs.etsmtl.ca
#         École de technologie supérieure (ÉTS)
#
# Free software: MIT license

from corpora_toolbox.utils.io import read_file_in_string
from math import *
import re


def divide_file_into_lines(file_with_route):
    """
    This function for separates the contents of a text file into lines, removing
    any caret returns ('\r') in the process.

    Parameters
    ----------
    file_with_route: the name of the text file with its path

    Returns
    -------
    lines: a list of all lines found in the file.
    """

    string = read_file_in_string(file_with_route)
    lines = string.replace("\r", "").split('\n')

    return lines


def __separate_sentences_for_n_grams(list_of_tags, remove_punctuation=True):
    """
    __separate_sentences_for_n_grams was created exclusively for the retrieve_n_grams function.
    It will separate (chunk) the text in sentences by using the ".".

    Parameters
    ----------
    list_of_tags: A list of tagged tuples (original word, lemma, tag) from which to extract
                   the n-grams.
    remove_punctuation: If True, it removes from the returned sentences all the punctuation marks
                   so that they are not included in the n-grams.


    Returns
    -------
    sentences: A list of sentences (lists of tagged tuples) separating with ".". The "." won't
    be included in the n-grams regardless of the value of remove_punctuation.
    """
    sentences = []

    sentence = []
    for tag_object in list_of_tags:
        if tag_object.lemma == ".":
            sentences.append(list(sentence))
            sentence = []
        else:
            if tag_object.tag.startswith("F"):
                if not remove_punctuation:
                    sentence.append(tag_object)
            else:
                sentence.append(tag_object)

    # In case the list_of_tags does not end with ".":
    if len(sentence) > 0:
        sentences.append(list(sentence))

    return sentences


def estimate_richness_stats(n_grams):
    """
    This function estimates the most used vocabulary richness measures used in text analysis.

    Parameters
    ----------
    n_grams: A Counter Object with the n_grams to use for estimating the richness stats.
             NOTE: the original measures are estimated on 1-grams.

    Returns
    -------
    richness_stats: a dictionary with the most common statistics for measuring vocabulary richness.
                keys:
                V1: hapax legomena
                V2: hapax dislegomena
                N: number of words (text size)
                V: number of different words (vocabulary size)
                Brunet: Brunet's index
                Honore: Honoré's statistics
                TTR: type token ratio
                Sichel: Sichel's formulation
                Yule: Yule measure
                Entropy: entropy of the word distribution
    """

    richness_stats = {}

    richness_stats["V1"] = 0
    richness_stats["V2"] = 0
    richness_stats["N"] = 0
    freqs = {}
    for n_gram in n_grams.keys():
        reps = n_grams[n_gram]

        if str(reps) in freqs:
            freqs[str(reps)] += 1
        else:
            freqs[str(reps)] = 1

        richness_stats["N"] += reps
        if reps <= 2:
            richness_stats["V2"] += 1
            if reps == 1:
                richness_stats["V1"] += 1

    richness_stats["V"] = len(n_grams.keys())

    if not (richness_stats["N"] == 0 or richness_stats["V"] == 0):
        richness_stats["Brunet"] = richness_stats["N"] ** richness_stats["V"] ** -0.172
    else:
        richness_stats["Brunet"] = 0

    if not richness_stats["V"] == 0 and not (1 - (richness_stats["V1"] / richness_stats["V"])) == 0:
        richness_stats["Honore"] = 100 * log(richness_stats["N"],10) / (1 - (richness_stats["V1"] / richness_stats["V"]))
    else:
        richness_stats["Honore"] = 0

    if not richness_stats["V"] == 0:
        richness_stats["TTR"] = richness_stats["V1"] / richness_stats["V"]
        richness_stats["Sichel"] = richness_stats["V2"] / richness_stats["V"]
    else:
        richness_stats["TTR"] = 0
        richness_stats["Sichel"] = 0

    addition = 0
    for i in freqs.keys():
        addition += (int(i)**2) * freqs[str(i)]

    if not richness_stats["N"] == 0:
        richness_stats["Yule"] = (((10**4)*addition)/richness_stats["N"]) - (1/richness_stats["N"])
    else:
        richness_stats["Yule"] = 0

    addition = 0
    for n_gram in n_grams.keys():
        if not richness_stats["N"] == 0:
            p = n_grams[n_gram] / richness_stats["N"]
        else:
            p = 0
        addition += p * log(p,2)
    richness_stats["Entropy"] = -1 * addition

    return richness_stats


def retrieve_n_grams(n, list_of_tags, remove_punctuation=True, lemmas=True, only_tokens=True, only_tags=False):
    """
    Retrieves the n-grams of lemmas with their tags from a list if tag objects.
    It uses the "." as a phrase delimiter.

    Parameters
    ----------
    n: the number of grams
    list_of_tags: a list of tagged objects from which to extract
                   the n-grams.
    remove_punctuation: whether to include symbols (such as commas) in the n-grams
    lemmas: Whether to include the lemmas or the original words.
                     NOTE: if only_tags = True, this option is void.
                     Example:
                        with lemmas=True: {'be': 16, 'he': 14, 'i': 11}
                        with lemmas=False: {'He': 14, 'I': 11, 'is': 10}
    only_tokens: Whether to make n-grams of lemmas/words, without the POS tags.
                    Example:
                        with only_tokens=True: {'be': 16, 'he': 14, 'i': 11}
                        with only_tokens=False: {'be/V': 16, 'he/P': 14, 'i/P': 11}
    only_tags: Whether to make n-grams of only the tags.
                    Example:
                        with only_tags=True: {'P_V': 31, 'V_P': 15, 'V_R': 11}
                        with only_tags=False: {'be/V': 16, 'he/P': 14, 'i/P': 11}

    Returns
    -------
    n_grams: a list of the n-grams:

    Example:
    -------
    For: "A B C, D E. F G H I.", after FreeLing or other tagger:
    test = [('A', 'a', 'Ta'), ('B', 'b', 'Tb'), ('C', 'c', 'Tc'), (",", ',', 'Fc'), ('D', 'd', 'Td'),
            ('E', 'e', 'Te'), ('.', '.', 'Fp'), ('F', 'f', 'Tf'), ('G', 'g', 'Tg'), ('H', 'h', 'Th'),
            ('I', 'i', 'Ti')]
    corpus_n_grams=retrieve_n_grams(n,test,remove_punctuation=True)
    print(corpus_n_grams)
        N = 1
        -----
        [('a/Ta'), ('b/Tb'), ('c/Tc'), ('d/Td'), ('e/Te'),
        ('f/Tf'), ('g/Tg'), ('h/Th'), ('i/Ti')]
    """
    n_grams=[]

    sentences = __separate_sentences_for_n_grams(list_of_tags,remove_punctuation)

    for sentence in sentences:
        if len(sentence) >= n :
            for i in range(len(sentence)-n+1):
                n_words = ""
                n_tags = ""
                for j in range(0, n):
                    if lemmas:
                        n_words += sentence[i+j].lemma
                    else:
                        n_words += sentence[i + j].original
                    n_tags += sentence[i + j].tag
                    if j < n-1:
                        n_words += "_"
                        n_tags += "_"

                if only_tags:
                    n_grams.append(n_tags)
                else:
                    if only_tokens:
                        n_grams.append(n_words)
                    else:
                        n_grams.append(n_words + "/" + n_tags)

    return n_grams


def remove_n_gram_repetitions(sentence, n, French=False):
    """
    When dealing with dialogs and other spontaneous texts, speakers tend to repeat n-grams during
    their speech, due to hesitation, retracing or emphasis (E.g. "yes, yes, yes... I know"). As
    part of the pre-processing step, it is useful to eliminate this repetitions to avoid hindering
    the performance of automatic taggers or parsers due to this phenomenon.

    Parameters
    ----------
    sentence: The sentence from which to remove the repetition of n-grams.
    n: the size of the n-gram
    French: For the specific case of French language, certain n-grams are repeated as part of the
            regular syntax (E.g. "nous nous somme leveés tôt").

    Returns
    -------
    new_sentence: the new sentence without the repetition of n-grams
    count_reps: the number of n-grams that were removed from the sentece
    """

    count_reps = 0
    new_sentence = ""

    # re.split(r'\W+') separates words by apostrophe. To avoid this, we temporarily
    # replace them by a code word: "codewordapostrophe"
    sentence = sentence.replace("\'", "codewordapostrophe")

    split_sentence = re.split(r'\W+', sentence)
    remove = [False] * len(split_sentence)

    if len(split_sentence) > n:

        position = 0
        while position < len(split_sentence) - (2*n) + 1:
            previous_n_gram = []
            next_n_gram = []
            for i in range(position, position+n):
                previous_n_gram.append(split_sentence[i])
                next_n_gram.append(split_sentence[i+n])

            if previous_n_gram == next_n_gram:
                if French:
                    if not (split_sentence[position + n].lower() == "vous" or \
                            split_sentence[position + n].lower() == "nous"):
                        for i in range(0, n):
                            remove[position + n + i] = True
                else:
                    remove[position + n] = True

            position += 1

    tokenized_sentence = re.split(r'(\W+)', sentence)

    index = 0
    for token in tokenized_sentence:
        if token == split_sentence[index]:
            if not remove[index]:
                new_sentence += token
            else:
                count_reps+=1
            index +=1
        else:
            new_sentence += token

    new_sentence = new_sentence.replace("codewordapostrophe", "\'")
    count_reps = int(count_reps/n)

    return new_sentence, count_reps



