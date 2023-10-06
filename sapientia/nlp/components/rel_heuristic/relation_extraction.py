#!/usr/bin/env python

def extract_sentences_beginning_positions(text):
    """
    Extract sentences beginning positions from a text
    (used to extract sentences containing specific named entities)
    :param text: text
    :return:
    """
    sentences_beginning_pos = []
    pos = 0
    dot = False
    end_of_sentence = False
    for word in text:
        if word == ".":
            dot = True
        if dot:
            if word != ".":
                end_of_sentence = True
            if end_of_sentence:
                sentences_beginning_pos.append(pos)
                dot = False
                end_of_sentence = False
        pos += 1
    return sentences_beginning_pos


def sentence_segmentation(text):
    """
    Sentence segmentation
    :param text: text
    :return: sentences
    """
    sentences = {}
    sentences_and_beginning_positions = extract_sentences_beginning_positions(text)
    previous_pos = 0
    for pos in sentences_and_beginning_positions:
        sentences[previous_pos] = text[previous_pos:pos]
        previous_pos = pos
    # last sentence
    sentences[previous_pos] = text[previous_pos:len(text)]
    return sentences


def get_named_entity_beginning_position(named_entity):
    """
    Get named entity beginning position in the text
    :param named_entity: named entity
    :return: named entity beginning position
    """
    return named_entity["start_char"]


def get_sentence_for_named_entity(named_entity, text):
    """
    Get sentence from which named entity has been extracted
    :param named_entity: named entity
    :param text: text
    :return: sentence
    """
    if not isinstance(named_entity, dict):
        raise TypeError(named_entity, " is not a named entity")
    keys = named_entity.keys()
    if "start_char" not in keys or "end_char" not in keys or "label" not in keys or "text" not in keys:
        raise TypeError(named_entity, " is not a named entity")
    named_entity_beginning_position = get_named_entity_beginning_position(named_entity)
    sentences = sentence_segmentation(text)
    sentence_beginning = 0
    for beginning_position in sentences.keys():
        if named_entity_beginning_position > beginning_position > sentence_beginning:
            sentence_beginning = beginning_position
    return sentences[sentence_beginning]


def get_sentence_start(sentence, sentences):
    """
    Get sentence start character index
    :param sentence: sentence
    :param sentences: sentences of the text (dict associating start characters and sentences)
    :return: sentence start
    """
    sentence_start = 0
    if not isinstance(sentences, dict):
        raise TypeError(sentences, " invalid sentences")
    for start, s in sentences.items():
        if s == sentence:
            sentence_start = start
    return sentence_start


def get_sentence_end(sentence, sentence_start):
    """
    Get sentence end character
    :param sentence: sentence
    :param sentence_start: sentence start character index
    :return: sentence end
    """
    return sentence_start + len(sentence)


def is_in_sentence(named_entity, sentence_start, sentence_end):
    """
    Check if a named entity is in a sentence
    :param named_entity: named entity
    :param sentence_start: sentence start
    :param sentence_end: sentence end
    :return: boolean, true if named entity is in the sentence, false otherwise
    """
    if not isinstance(named_entity, dict):
        raise TypeError(named_entity, " invalid named entity")
    if "start_char" not in named_entity.keys():
        raise TypeError(named_entity, " invalid named entity")
    return sentence_start < named_entity["start_char"] < sentence_end


def get_ner_labels(named_entities):
    """
    Get named entities labels from named entities
    :param named_entities: named entities
    :return: labels
    """
    ner_labels = []
    for named_entity in named_entities:
        if named_entity["label"] not in ner_labels:
            ner_labels.append(named_entity["label"])
    return ner_labels


def collaboration_extraction(named_entities):
    """
    COLLABORATION relation extraction (heuristic method)
    :param named_entities: named entities
    :return: collaborations
    """
    collaborations = []
    roles = 0
    for named_entity in named_entities:
        if named_entity["label"] == "ROLE":
            roles += 1
    if roles > 1:
        previous_role = ""
        for named_entity in named_entities:
            if named_entity["label"] == "ROLE":
                if previous_role == "":
                    previous_role = named_entity["text"].lower()
                else:
                    if previous_role != named_entity["text"].lower():
                        collaborations.append("COLLABORATION(" + previous_role.lower() + "," +
                                              named_entity["text"].lower() + ")")
                        previous_role = named_entity["text"].lower()
    return collaborations


def responsibilities_extraction(named_entities):
    """
    RESPONSIBLE relation extraction (heuristic method)
    :param named_entities: named entities
    :return: responsibilities
    """
    responsibilities = []
    seen_role = False
    role_entity = ""
    for named_entity in named_entities:
        if seen_role:
            if named_entity["label"] == "DOCUMENT" or named_entity["label"] == "COMPONENT" or \
                    named_entity["label"] == "SYSTEM" or named_entity["label"] == "HARDWARE":
                responsibilities.append("RESPONSIBLE(" + role_entity.lower() + "," + named_entity["text"].lower() + ")")
            seen_role = False
            role_entity = ""
        if named_entity["label"] == "ROLE":
            seen_role = True
            role_entity = named_entity["text"].lower()
    return responsibilities


def provided_extraction(relations):
    """
    PROVIDED relation extraction (heuristic method)
    :param relations: extracted relations
    :return: provided relations
    """
    provided_relations = []
    for relation in relations:
        if relation.split("(")[0] == "RESPONSIBLE":
            provider = relation.split("(")[1].split(",")[0].removesuffix(")")
            to_provide = relation.split("(")[1].split(",")[1].removesuffix(")")
            for rel in relations:
                if rel.split("(")[0] == "COLLABORATION" and rel.split("(")[1].split(",")[0].removesuffix(
                        ")") == provider:
                    provided = rel.split("(")[1].split(",")[1].removesuffix(")")
                    provided_relation = "PROVIDED(" + to_provide + "," + provided + ")"
                    if provided_relation not in provided_relations:
                        provided_relations.append("PROVIDED(" + to_provide + "," + provided + ")")
    return provided_relations


def definition_extraction(named_entities, text):
    """
    DEFINED_BY relation extraction (heuristic method)
    :param named_entities: named entities
    :param text: text
    :return: defined by relations
    """
    definition_relations = []
    documents = []
    for named_entity in named_entities:
        if named_entity["label"] == "DOCUMENT":
            documents.append(named_entity)
    sentences = sentence_segmentation(text)
    for document in documents:
        sentence = get_sentence_for_named_entity(document, text)
        sentence_start = get_sentence_start(sentence, sentences)
        sentence_end = get_sentence_end(sentence, sentence_start)
        for named_entity in named_entities:
            if named_entity["label"] == "STANDARD" or named_entity["label"] == "PROCESS":
                if is_in_sentence(named_entity, sentence_start, sentence_end):
                    is_definition = False
                    if named_entity["start_char"] < document["start_char"] and "defined" in sentence:
                        # Text example : "the requirements are defined in the document"
                        # Text example : "the purchaser will provide a document in which the requirement are defined"
                        # Text example : "the purchaser has defined the requirements in the document"
                        is_definition = True
                    if document["start_char"] > named_entity["start_char"] and ("define" or "defines") in sentence:
                        define_index = get_sentence_start(sentence, sentences) + sentence.find("define")
                        if document["start_char"] < define_index < named_entity["start_char"] or \
                                define_index < named_entity["start_char"] < document["start_char"]:
                            # Text example : "The document defines the requirements"
                            # Text example : "The supplier shall define requirements in the document"
                            is_definition = True
                    if is_definition:
                        definition = "DEFINED_BY(" + named_entity["text"].lower() + "," + document["text"].lower() + ")"
                        if definition not in definition_relations:
                            definition_relations.append(definition)
    return definition_relations


def compliance_extraction(named_entities, text):
    """
    COMPLY_WITH relation extraction (heuristic method)
    :param named_entities: named entities
    :param text: text
    :return: comply with relations
    """
    compliance_relations = []
    standards_and_criteria = []
    for named_entity in named_entities:
        if named_entity["label"] == "STANDARD" or named_entity["label"] == "CRITERIA":
            standards_and_criteria.append(named_entity)
    sentences = sentence_segmentation(text)
    for standard_and_criteria in standards_and_criteria:
        sentence = get_sentence_for_named_entity(standard_and_criteria, text)
        sentence_start = get_sentence_start(sentence, sentences)
        sentence_end = get_sentence_end(sentence, sentence_start)
        for named_entity in named_entities:
            if named_entity["label"] == "DOCUMENT" or named_entity["label"] == "ROLE" or named_entity["label"] == "ORG":
                if is_in_sentence(named_entity, sentence_start, sentence_end):
                    is_compliance = False
                    if named_entity["start_char"] < standard_and_criteria["start_char"] and ("comply" in sentence or
                                                                                             "complies" in sentence):
                        compliance_index = 0
                        if "comply" in sentence:
                            compliance_index = get_sentence_start(sentence, sentences) + sentence.find("comply")
                        if "complies" in sentence:
                            compliance_index = get_sentence_start(sentence, sentences) + sentence.find("complies")
                        if named_entity["start_char"] < compliance_index < standard_and_criteria["start_char"]:
                            is_compliance = True
                        # Text example : "the purchaser complies with the requirements defined in the document"
                    if is_compliance:
                        compliance = ("COMPLY_WITH(" + named_entity["text"].lower() + "," +
                                      standard_and_criteria["text"].lower() + ")")
                        if compliance not in compliance_relations:
                            compliance_relations.append(compliance)
    return compliance_relations


def composition_extraction(named_entities, text):
    """
    COMPOSED_BY relation extraction (heuristic method)
    :param named_entities: named entities
    :param text: text
    :return: composed by relations
    """
    composition_relations = []
    return composition_relations


def communication_extraction():
    """

    """
    return []


def controls_extraction():
    """

    """
    return []


def connections_extraction():
    """

    """
    return []


def alternative_labels_extraction():
    """

    """
    return []


def features_extraction():
    """

    """
    return []


def conditions_extraction():
    """

    """
    return []


def values_extraction():
    """

    """
    return []


def units_extraction():
    """

    """
    return []


def performances_extraction():
    """

    """
    return []


def operations_extraction():
    """

    """
    return []


def phases_extraction():
    """

    """
    return []


def relations_extraction_heuristic(named_entities, text):
    """
    Relation extraction (heuristic method)
    :param named_entities: named entities
    :param text: text
    :return: relations
    """
    relations = []
    ner_labels = get_ner_labels(named_entities)
    if "ROLE" in ner_labels:
        collaborations = collaboration_extraction(named_entities)
        responsibilities = responsibilities_extraction(named_entities)
        relations = collaborations + responsibilities
        provided = provided_extraction(relations)
        relations.extend(provided)
    if "DOCUMENT" in ner_labels:
        definitions = definition_extraction(named_entities, text)
        relations.extend(definitions)
    if "STANDARD" or "CRITERIA" in ner_labels:
        print("IN COMPLIANCE")
        compliance = compliance_extraction(named_entities, text)
        relations.extend(compliance)
    if "COMPONENT" in ner_labels:
        if "SYSTEM" in ner_labels:
            compositions = composition_extraction()
            relations.extend(compositions)
        communications = communication_extraction()
        relations.extend(communications)
        controls = controls_extraction()
        relations.extend(controls)
        connections = connections_extraction()
        relations.extend(connections)
        alternative_labels = alternative_labels_extraction()
        relations.extend(alternative_labels)
        if "PARAMETER" in ner_labels:
            features = features_extraction()
            relations.extend(features)
    if "CONDITION" in ner_labels:
        conditions = conditions_extraction()
        relations.extend(conditions)
    if "UNIT" in ner_labels:
        values = values_extraction()
        relations.extend(values)
        units = units_extraction()
        relations.extend(units)
    if "PROCESS" in ner_labels:
        perform = performances_extraction()
        relations.extend(perform)
        operations = operations_extraction()
        relations.extend(operations)
    if "PHASE" in ner_labels:
        phases = phases_extraction()
        relations.extend(phases)
    return relations
