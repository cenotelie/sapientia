#!/usr/bin/env python

import spacy


def load_model(model):
    """
    Load Natural Language Processing (NLP) model
    :param model: NLP model (SpaCy)
    :return: Language object containing all components and data needed to process text
    """
    nlp = spacy.load(model)
    return nlp


def apply_model(nlp, text):
    """
    Apply NLP model on a text
    :param nlp: NLP chain (Language object containing all components and data needed to process text)
    :param text: text
    :return: text processed with NLP workflow (SpaCy)
    """
    doc = nlp(text)
    return doc


def tokenize(doc):
    """
    Tokenization
    :param doc: text processed through NLP model (SpaCy)
    :return: tokens
    """
    tokens = []
    for token in doc:
        tokens.append(
            {
                "text": token.text,
                "lemma": token.lemma_,
                "pos": token.pos_,
                "tag": token.tag_,
                "dep": token.dep_
            }
        )
    return tokens


def sentence_segmentation(doc):
    """
    Sentence segmentation
    :param doc: text processed through NLP model (SpaCy)
    :return: sentences in the text
    """
    sentences = []
    assert doc.has_annotation("SENT_START")
    for sent in doc.sents:
        sentences.append(sent.text)
    return sentences


def named_entity_recognition(doc):
    """
    Named entity recognition
    :param doc:  text processed through NLP model (SpaCy)
    :return: named entities
    """
    named_entities = []
    for ent in doc.ents:
        named_entities.append(
            {
                "text": ent.text,
                "start_char": ent.start_char,
                "end_char": ent.end_char,
                "label": ent.label_
            }
        )
    return named_entities


def get_vocab(nlp):
    """
    Get lexemes in vocabulary
    :param nlp: NLP chain (Language object containing all components and data needed to process text)
    :return: lexemes
    """
    return nlp.vocab


def get_vocab_length(nlp):
    """
    Get number of lexemes in vocabulary
    :param nlp: NLP chain (Language object containing all components and data needed to process text)
    :return: number of lexemes
    """
    return len(nlp.vocab)
