# Sapientia

Natural Language Processing workflow ([Cénotélie](https://cenotelie.fr/main))

## Prerequisites

[Python 3.5.10](https://www.python.org/downloads/release/python-3510/)

Sapientia is based on [SpaCy](https://spacy.io/) and [Prodigy](https://prodi.gy/) from [explosion](https://explosion.ai/). All needed librairies and packages are provided through the requirements.txt file. To install the requirements, please open a terminal and use :
 	
    pip install -r requirements.txt 
 	 

## Overview

Sapientia consists in a Natural Language Processing (NLP) workflow that uses deep learning, more specifically supervised learning in order to extract knowledge from text. It  enables to automatically :
- Extract named entities from text 
- Extract semantic relations existing between these named entities
- Provide an output as RDF triples for interoperability

Sapientia is mainly used in eCollab but is a standalone project. It can be reused in any use case where knowledge extraction from text is needed.

## Components

Sapientia is composed of : 

- a Natural Language Processing (NLP) chain
- a workflow for training NLP models
- NLP models trained specifically for the eCollab use case
- Input / Output (IO) functionalities for files manipulation
- an Optical Character Recognition (OCR) algorithm
- A knowledge extraction component 
- A language detection component

### Natural Language Processing (NLP)

The main component is a Natural Language Processing chain that is used to extract knowledge from text. 

First, a Natural Language Processing model is applied on a text. 

Then, Named Entity Recognition (NER) can be performed on the text in order to extract its named entities.   

We can also extract semantic relations existing between named entities thanks to a specific NLP component.

We also provide text preprocessing functionalities, such as a custom sentence segmentation in order to ease the NER task. 

### Language detection

As an NLP model is language-dependent, we provide a language detection component. Indeed, we need to detect the main language used in a text in order to automatically apply the appropriate NLP model.

We use [langdetect](https://pypi.org/project/langdetect/), which is a Python port of Google's [language detection](https://github.com/shuyo/language-detection) project, in order to automatically detect languages in a text.

### Training a NLP model

Standard NLP models from SpaCy ([English](https://spacy.io/models/en) or [French](https://spacy.io/models/fr)) can be used to perform named entity recognition (NER) on text.

However, for specific use cases, it is essential to train a specific NLP model. We use supervised learning to train a neural network NLP model.

In supervised learning, training data, that is annotated examples, is needed in order to generate the model.

To annotate training data, we use an annotation tool, [Prodigy](https://prodi.gy/). To annotate training data, we need :
- Data to annotate (in jsonl format)
- Labels for named entities
- Labels for relations

We provide functions to generate the annotation data in jsonl format from data files and scripts to trigger the annotation process in a dedicated web page as well as generating the NLP model. 

### NLP models for eCollab

We trained a NLP model for the eCollab project. It enables to perform NER and relation extraction on English texts.

### Parsing files 

In most cases, we need to process files instead of raw text. Therefore, we provide Input / Output (IO) functionalities for file manipulation as well as an Optical Character Recognition (OCR) algorithm to extract textual content of PDF files.

### Knowledge extraction

We also provide a knowledge extraction component for specific tasks such as requirements extraction in text.

### Knowledge representation

We use RDF, which is an interoperable format, to output named entities and relation extracted from files. 