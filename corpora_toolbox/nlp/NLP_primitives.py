# -*- coding: utf-8 -*-

"""
The :mod:`corpora_toolbox.nlp.NLP_primitives` defines the basic structure of the most
used classes for NLP applications.
"""

# Author: Laura Hernandez-Dominguez <laura.hzdz@gmail.com>, 2018
#         Laboratoire d'ingénierie Cognitive et Sémantique (LiNCS)
#         http://lincs.etsmtl.ca
#         École de technologie supérieure (ÉTS)
#
# Free software: MIT license


class Tag:
    """
    A tag object will be composed of four elements:
    The original word, the lemma, the tag, and the tag certainty (probability; if available).
    """
    def __init__(self, original="", lemma="", tag="", certainty=-1):
        """Initializes the data."""
        self.original = original
        self.lemma = lemma
        self.tag = tag
        self.certainty = certainty


class Parse:
    """
    A parse object will be composed of:
    The parsing (could be a whole parsing or a fragment, such as an utterance) and
    the maximum depth of the parsing.
    """
    def __init__(self, parsing="", max_depth=-1):
        """Initializes the data."""
        self.parsing = parsing
        self.max_depth = max_depth
