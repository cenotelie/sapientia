#!/usr/bin/env python

from langdetect import detect, DetectorFactory

DetectorFactory.seed = 0


def detect_language(text):
    """
    Detect main language used in a text
    :param text: text
    :return: main language used in a text
    """
    return detect(text)
