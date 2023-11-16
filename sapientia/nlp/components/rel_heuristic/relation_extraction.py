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


def associate_sentences_to_named_entities(named_entities, text):
    """
    Associate sentence of the text to extracted named entities
    :param named_entities: named entities
    :param sentences: sentences of the text
    :return: named entities associated to sentence of the text from which they were recognized
    """
    sentences_to_named_entities = {}
    sentences = sentence_segmentation(text)
    for sentence in sentences:
        sentences_to_named_entities[sentence] = []
    for named_entity in named_entities:
        sentence = get_sentence_for_named_entity(named_entity, text)
        sentence_start = get_sentence_start(sentence, sentences)
        elements = sentences_to_named_entities[sentence_start]
        elements.append(named_entity)
        sentences_to_named_entities[sentence_start] = elements
    return sentences_to_named_entities


def has_more_specific_occurrence_in_triggering_text(text, triggering_text, sentence):
    """
    Check if a specific text has a longer (more specific) occurrence in triggering text that appears in the sentence
    (for exemple, if the text "composed" exists in triggering text and in the sentence, considering the text "compose")
    :param text: text
    :param triggering_text: triggering text
    :param sentence: sentence
    :return: true if the text has a more specific occurrence in triggering text that appears in the sentence, false
    otherwise
    """
    has_more_specific_occurrence = False
    for trigger in triggering_text:
        if len(trigger["text"]) > len(text):
            if trigger["text"].startswith(text) and trigger["text"] in sentence:
                text_index = sentence.find(text)
                trigger_index = sentence.find(trigger["text"])
                if text_index == trigger_index:
                    has_more_specific_occurrence = True
    return has_more_specific_occurrence




def extract_relation(relation_label, sentences, sentences_to_named_entities, source_labels, target_labels, triggering_text):
    """
    :param relation_label: relation label (name of the relations to extract)
    :param sentences: sentences of the text
    :param sentences_to_named_entities: sentence to their associated named entities
    :param source_labels: possible labels of the source named entities in the relation (can be None if no label has to be specified)
    :param target_labels: possible labels of the target named entities in the relation (can be None if no label has to be specified)
    :param triggering_text: possible texts triggering the relation associated with an indicator of the way to trigger the relation
    :return relations
    """
    if not isinstance(relation_label, str):
        raise TypeError(relation_label, " invalid relation label")
    if not isinstance(sentences_to_named_entities, dict):
        raise TypeError(sentences_to_named_entities, " couldn't associate named entities to sentences of the text")
    if source_labels is not None and not isinstance(source_labels, list):
        raise TypeError(source_labels, " invalid source labels")
    if target_labels is not None and not isinstance(target_labels, list):
        raise TypeError(target_labels, " invalid source labels")
    if triggering_text is not None and not isinstance(triggering_text, list):
        raise TypeError(triggering_text, " invalid triggering text")
    relations = []
    for sentence_index, named_entities in sentences_to_named_entities.items():
        source_named_entities = []
        target_named_entities = []
        if source_labels or target_labels:
            for named_entity in named_entities:
                if source_labels:
                    for source_label in source_labels:
                        if named_entity["label"] == source_label:
                            source_named_entities.append(named_entity)
                if target_labels:
                    for target_label in target_labels:
                        if named_entity["label"] == target_label:
                            target_named_entities.append(named_entity)
        else:
            for named_entity in named_entities:
                source_named_entities.append(named_entity)
                target_named_entities.append(named_entity)
        if triggering_text:
            sentence = sentences[sentence_index]
            has_triggering_text = False
            for trigger in triggering_text:
                text = trigger.get("text")
                if text in sentence:
                    has_triggering_text = True
            if has_triggering_text:
                text_index = 0
                for trigger in triggering_text:
                    text = trigger.get("text")
                    active = trigger.get("active")
                    if text in sentence:
                        text_index = get_sentence_start(sentence_index, sentences) + sentence.find(text)
                        has_more_specific_occurrence = has_more_specific_occurrence_in_triggering_text(text, triggering_text, sentence)
                        if not has_more_specific_occurrence:
                            if active:
                                for source_named_entity in source_named_entities:
                                    for target_name_entity in target_named_entities:
                                        if source_named_entity["start_char"] < text_index < target_name_entity["start_char"]:
                                            if source_named_entity != target_name_entity:
                                                relation = relation_label + "(" + source_named_entity["text"].lower() + "," + target_name_entity["text"].lower() + ")"
                                                if relation not in relations:
                                                    relations.append(relation)
                            else:
                                for source_named_entity in source_named_entities:
                                    for target_name_entity in target_named_entities:
                                        if target_name_entity["start_char"] < text_index < source_named_entity["start_char"]:
                                            if source_named_entity != target_name_entity:
                                                relation = relation_label + "(" + source_named_entity["text"].lower() + "," + target_name_entity["text"].lower() + ")"
                                                if relation not in relations:
                                                    relations.append(relation)
        else:
            for target_name_entity in target_named_entities:
                source_entity = None
                for source_named_entity in source_named_entities:
                    if target_name_entity["start_char"] > source_named_entity["start_char"]:
                        if source_entity is not None:
                            if source_named_entity["start_char"] > source_entity["start_char"]:
                                source_entity = source_named_entity
                        else:
                            source_entity = source_named_entity
                if source_entity is not None and source_entity != target_name_entity:
                    relation = relation_label + "(" + source_entity["text"].lower() + "," + target_name_entity["text"].lower() + ")"
                    if relation not in relations:
                        relations.append(relation)
    return relations


def create_new_relations_from_existing_relations(relations, first_relation_label, first_named_entity_position, second_relation_label, second_named_entity_position, new_relation_label):
    """
    Create relations from existing relations with transitivity property
    :param relations: relations
    :param first_relation_label: first relation label used to create new relations
    :param first_named_entity_position: named entity position to use in the first relation in order to create the new relation (can be "left" or "right")
    :param second_relation_label: second relation label used to create new relations
    :param second_named_entity_position: named entity position to use in the second relation in order to create the new relation (can be "left" or "right")
    :param new_relation_label: new relation label
    """
    new_relations = []
    for relation in relations:
        if relation.split("(")[0] == first_relation_label:
            left_entity = relation.split("(")[1].split(",")[0].removesuffix(")")
            right_entity = relation.split("(")[1].split(",")[1].removesuffix(")")
            first_entity = left_entity
            common_entity = right_entity
            if first_named_entity_position == "right":
                first_entity = right_entity
                common_entity = left_entity
            for rel in relations:
                if rel.split("(")[0] == second_relation_label:
                    possible_common_entity = rel.split("(")[1].split(",")[1].removesuffix(")")
                    if second_named_entity_position == "right":
                        possible_common_entity = rel.split("(")[1].split(",")[0].removesuffix(")")
                    if possible_common_entity == common_entity:
                        if second_named_entity_position == "left":
                            second_entity = rel.split("(")[1].split(",")[0].removesuffix(")")
                        else:
                            second_entity = rel.split("(")[1].split(",")[1].removesuffix(")")
                        new_relation = new_relation_label + "(" + first_entity + "," + second_entity + ")"
                        if new_relation not in new_relations:
                            new_relations.append(new_relation)
    return new_relations
