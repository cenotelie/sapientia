#!/usr/bin/env python

import re


def sentences_fixing(sentences):
    """
    Sentences fixing
    :param sentences: sentences extracted from text
    :return: correct sentences (when sentences are split, there might be errors that need fixing. For example,
    e.g. might be considered as the end of a sentence, and it should not.)
    """
    fixed_sentences = []
    eg = "e.g."
    ref = "ref"
    broken = False
    for sentence in sentences:
        if broken:
            if fixed_sentences:
                new_sentence = fixed_sentences.pop() + " " + sentence
            else:
                new_sentence = sentences[0]
            fixed_sentences.append(new_sentence)
        else:
            fixed_sentences.append(sentence)
        if sentence.endswith(eg) or sentence.endswith(ref):
            broken = True
        else:
            if broken:
                broken = False
    return fixed_sentences


def group_lists_in_sentences(sentences):
    """
    Group items from lists as single sentence
    :param sentences: sentences
    :return: sentences with grouped items from lists
    """
    grouped_sentences = []
    for sentence in sentences:
        if sentence.startswith("•") or sentence.startswith("-"):
            bullet = True
        else:
            bullet = False
        if bullet:
            if grouped_sentences:
                new_sentence = grouped_sentences.pop() + " " + sentence
                grouped_sentences.append(new_sentence)
            else:
                grouped_sentences.append(sentence)
        else:
            grouped_sentences.append(sentence)
    return grouped_sentences


def sentences_cleaning(sentences):
    """
    Sentences cleaning
    :param sentences: sentences extracted from text
    :return: cleaned sentences
    """
    while "" in sentences:
        sentences.remove("")
    while ", " in sentences:
        sentences.remove(", ")
    while "," in sentences:
        sentences.remove(",")
    cleaned_sentences = []
    for sentence in sentences:
        sent = sentence.replace("\n", "")
        sent = sent.replace("\"", "")
        sent = re.sub("Page [0-9]+ of [0-9]+", "", sent)
        sent = re.sub("CONFIDENTIAL AND PROPRIETARY DOCUMENT", "", sent)
        sent = sent.partition("CORAC GENOME - SPOILER ROTARY EMA SPECIFICATION")[0]
        sent = sent.lstrip()
        cleaned_sentences.append(sent)
    return cleaned_sentences
