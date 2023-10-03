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
    for document in documents:
        sentence = get_sentence_for_named_entity(document, text)
    return definition_relations


def compliance_extraction():
    """

    """
    return []


def composition_extraction():
    """

    """
    return []


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
        definitions = definition_extraction(text)
        relations.extend(definitions)
    if "STANDARD" in ner_labels:
        compliances = compliance_extraction()
        relations.extend(compliances)
    if "COMPONENT" in ner_labels:
        if "SYSTEM" in ner_labels:
            compositions = composition_extraction()
            relations.extend(compositions)
        print("")
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
        print("")
        values = values_extraction()
        relations.extend(values)
        units = units_extraction()
        relations.extend(units)
    if "PROCESS" in ner_labels:
        print("")
        perform = performances_extraction()
        relations.extend(perform)
        operations = operations_extraction()
        relations.extend(operations)
    if "PHASE" in ner_labels:
        print("")
        phases = phases_extraction()
        relations.extend(phases)
    print(text)
    return relations
