#!/usr/bin/env python

import tika
from tika import parser

tika.TikaClientOnly = True  # server mode (Apache Tika)
tika_server = 'http://localhost:9998/'  # server address (Apache Tika)


def parse(file):
    """
    Parse a file and extract its textual content (Apache Tika)
    :param file: file path
    :return: parsed content of the file
    """
    parsed = parser.from_file(file)
    return parsed["content"]
