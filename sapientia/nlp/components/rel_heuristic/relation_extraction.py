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


def approval_extraction(named_entities, text):
    """
    APPROVAL relation extraction (heuristic method)
    :param named_entities: named entities
    :param text: text
    :return: approval relations
    """
    # TODO :
    # - multiple sentence patterns (one approval and other things, multiple approvals)
    # - eventually, more complex word patterns
    approvals = []
    roles = []
    for named_entity in named_entities:
        if named_entity["label"] == "ROLE":
            roles.append(named_entity)
    sentences = sentence_segmentation(text)
    for role in roles:
        sentence = get_sentence_for_named_entity(role, text)
        sentence_start = get_sentence_start(sentence, sentences)
        sentence_end = get_sentence_end(sentence, sentence_start)
        if "validate" or "approve" in sentence:
        # TODO :  sentences -> named entities : would be way easier / more efficient / less costly ?
            for named_entity in named_entities:
                if (named_entity["label"] == "DOCUMENT" or named_entity["label"] == "STANDARD" or
                        named_entity["label"] == "CRITERIA" or named_entity["label"] == "UNIT" or
                        named_entity["label"] == "PHASE"):
                    if is_in_sentence(named_entity, sentence_start, sentence_end):
                        if role["start_char"] < named_entity["start_char"]:
                            approval_index = 0
                            if "approve" in sentence:
                                approval_index = get_sentence_start(sentence, sentences) + sentence.find("approve")
                            if "validate" in sentence:
                                approval_index = get_sentence_start(sentence, sentences) + sentence.find("validate")
                        if role["start_char"] < approval_index < named_entity["start_char"]:
                            approval = "APPROVAL(" + role["text"].lower() + "," + named_entity["text"].lower() + ")"
                        if approval not in approvals:
                            approvals.append(approval)
    return approvals


def rejection_extraction(named_entities, text):
    """
    REJECTION relation extraction (heuristic method)
    :param named_entities: named entities
    :param text: text
    :return: rejection relations
    """
    # TODO
    rejection = []
    return rejection


def definition_extraction(named_entities, text):
    """
    DEFINED_BY relation extraction (heuristic method)
    :param named_entities: named entities
    :param text: text
    :return: defined by relations
    """
    # TODO :
    #  - multiple "define" occurrences in the text
    #  - more complex word patterns
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
                    if document["start_char"] > named_entity["start_char"] and "define" in sentence:
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
    # TODO :
    #  - multiple "complies" occurrences in the text
    #  - more complex word patterns
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
    # TODO :
    #  - multiple "composed" occurrences in the text
    #  - more complex word patterns
    composition_relations = []
    components = []
    systems = []
    hardware = []
    for named_entity in named_entities:
        if named_entity["label"] == "COMPONENT":
            components.append(named_entity)
        else:
            if named_entity["label"] == "SYSTEM":
                systems.append(named_entity)
            else:
                if named_entity["label"] == "HARDWARE":
                    hardware.append(named_entity)
    sentences = sentence_segmentation(text)
    sentences_to_components_systems_and_hardware = {}
    for sentence in sentences:
        sentences_to_components_systems_and_hardware[sentence] = []
    if components:
        for component in components:
            sentence = get_sentence_for_named_entity(component, text)
            sentence_start = get_sentence_start(sentence, sentences)
            elements = sentences_to_components_systems_and_hardware[sentence_start]
            elements.append(component)
            sentences_to_components_systems_and_hardware[sentence_start] = elements
    if systems:
        for system in systems:
            sentence = get_sentence_for_named_entity(system, text)
            sentence_start = get_sentence_start(sentence, sentences)
            elements = sentences_to_components_systems_and_hardware[sentence_start]
            elements.append(system)
            sentences_to_components_systems_and_hardware[sentence_start] = elements
    if hardware:
        for element in hardware:
            sentence = get_sentence_for_named_entity(element, text)
            sentence_start = get_sentence_start(sentence, sentences)
            elements = sentences_to_components_systems_and_hardware[sentence_start]
            elements.append(element)
            sentences_to_components_systems_and_hardware[sentence_start] = elements
    for index, named_entities in sentences_to_components_systems_and_hardware.items():
        sentence = sentences[index]
        if "composed" in sentence:
            composed_index = get_sentence_start(sentence, sentences) + sentence.find("composed")
            composite = None
            constituents = []
            for named_entity in named_entities:
                if composite is None:
                    composite = named_entity
                else:
                    if composite["start_char"] < named_entity["start_char"] < composed_index:
                        composite = named_entity
                    else:
                        if composite["start_char"] > composed_index:
                            composite = named_entity
            for named_entity in named_entities:
                if named_entity["start_char"] > composed_index:
                    constituents.append(named_entity)
            for constituent in constituents:
                composition = ("COMPOSED_BY(" + composite["text"].lower() + "," + constituent["text"].lower() + ")")
                composition_relations.append(composition)
        else:
            if "compose" in sentence:
                compose_index = 0
                if "compose" in sentence:
                    compose_index = get_sentence_start(sentence, sentences) + sentence.find("compose")
                composite = None
                constituents = []
                for named_entity in named_entities:
                    if composite is None:
                        composite = named_entity
                    else:
                        if compose_index < composite["start_char"] < named_entity["start_char"]:
                            composite = named_entity
                        else:
                            if compose_index > composite["start_char"]:
                                composite = named_entity
                for named_entity in named_entities:
                    if named_entity["start_char"] < compose_index:
                        constituents.append(named_entity)
                for constituent in constituents:
                    composition = ("COMPOSED_BY(" + composite["text"].lower() + "," + constituent["text"].lower() + ")")
                    composition_relations.append(composition)
    return composition_relations


def communication_extraction(named_entities, text):
    """
    COMMUNICATION relation extraction (heuristic method)
    :param named_entities: named entities
    :param text: text
    :return: communicate relations
    """
    # TODO
    return []


def controls_extraction(named_entities, text):
    """

    """
    # TODO
    return []


def connections_extraction(named_entities, text):
    """

    """
    # TODO
    return []


def alternative_labels_extraction(named_entities):
    """

    """
    # TODO
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
        approval = approval_extraction(named_entities, text)
        relations.extend(approval)
        rejection = rejection_extraction(named_entities, text)
        relations.extend(rejection)
    if "DOCUMENT" in ner_labels:
        definitions = definition_extraction(named_entities, text)
        relations.extend(definitions)
    if "STANDARD" or "CRITERIA" in ner_labels:
        print("IN COMPLIANCE")
        compliance = compliance_extraction(named_entities, text)
        relations.extend(compliance)
    if "COMPONENT" in ner_labels:
        if "SYSTEM" in ner_labels:
            compositions = composition_extraction(named_entities, text)
            relations.extend(compositions)
        communications = communication_extraction(named_entities, text)
        relations.extend(communications)
        controls = controls_extraction(named_entities, text)
        relations.extend(controls)
        connections = connections_extraction(named_entities, text)
        relations.extend(connections)
        alternative_labels = alternative_labels_extraction(named_entities)
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
