#!/usr/bin/env python

import csv

from sapientia.nlp.preprocessing.data_cleaning import sentences_cleaning


def requirements_extraction(sentences):
    """
    Extract requirements from sentences
    :param sentences: sentences in a text
    :return: requirements
    """
    requirements = []
    sentences = sentences_cleaning(sentences)
    for sentence in sentences:
        if ("shall" in sentence) or ("should" in sentence) or ("must" in sentence) or ("will" in sentence) \
                or ("may" in sentence):
            requirements.append(sentence)
    return requirements


def get_abbreviations(abbreviations_file):
    """
    Get abbreviations from CSV file
    :param abbreviations_file: csv file containing all abbreviations
    :return: abbreviations
    """
    with open(abbreviations_file, mode='r') as infile:
        reader = csv.reader(infile)
        abbreviations = {rows[0]: rows[1] for rows in reader}
    return abbreviations
