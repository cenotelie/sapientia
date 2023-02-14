#!/usr/bin/env python

from sapientia.io.io import load_files, create_file, append_file
from sapientia.ocr.ocr import parse
from sapientia.nlp.preprocessing.data_cleaning import sentences_cleaning, sentences_fixing, group_lists_in_sentences
from sapientia.knowledge.knowledge_extraction import requirements_extraction


def create_training_data(source_dir, target_file):
    """
    Create training data
    :param source_dir: source directory
    :param target_file: target training data file
    :return: None
    """
    files = load_files(source_dir)
    create_file(target_file)
    for file in files:
        content = parse(file)
        sentences = content.split(". ")
        sentences = sentences_fixing(sentences)
        sentences = group_lists_in_sentences(sentences)
        sentences = sentences_cleaning(sentences)
        requirements = requirements_extraction(sentences)
        for requirement in requirements:
            training_data = "{ \"text\":" + "\"" + str(requirement) + "\"}\n"
            append_file(target_file, training_data)
