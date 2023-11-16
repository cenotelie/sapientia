import unittest

from sapientia.nlp.nlp import load_model, apply_model, named_entity_recognition
from sapientia.nlp.components.rel_heuristic.relation_extraction import (extract_sentences_beginning_positions,
                                                                        sentence_segmentation,
                                                                        get_named_entity_beginning_position,
                                                                        get_sentence_for_named_entity,
                                                                        get_sentence_start, get_sentence_end,
                                                                        is_in_sentence,
                                                                        associate_sentences_to_named_entities,
                                                                        extract_relation,
                                                                        create_new_relations_from_existing_relations,
                                                                        has_more_specific_occurrence_in_triggering_text)


class TestRelationExtraction(unittest.TestCase):
    def test_extract_sentences_beginning_positions(self):
        text = ("The supplier provides the ECU. Under supplier request, the Purchaser will provide documents identified "
                "in this section except the external standards available on the market")
        sentences_beginning_positions = extract_sentences_beginning_positions(text)
        print(sentences_beginning_positions)
        self.assertEqual(sentences_beginning_positions, [30])

    def test_sentence_segmentation(self):
        text = "Test 1. Test 2. Test 3. Test 45... Test 125"
        sentences_beginning_positions = extract_sentences_beginning_positions(text)
        sentences = sentence_segmentation(text)
        print(sentences_beginning_positions)
        print(sentences)
        self.assertEqual(sentences, {0: 'Test 1.', 7: ' Test 2.', 15: ' Test 3.', 23: ' Test 45...', 34: ' Test 125'})

    def test_get_named_entity_beginning_position(self):
        model = "assets/ner_collins_en"
        text = ("The supplier provides the ECU. Under supplier request, the Purchaser will provide documents "
                "identified in this section except the external standards available on the market")
        nlp = load_model(model)
        doc = apply_model(nlp, text)
        named_entities = named_entity_recognition(doc)
        print("\"", named_entities[0]["text"], "\"", "beginning position :", named_entities[0]["start_char"])
        self.assertEqual(get_named_entity_beginning_position(named_entities[0]), 4)

    def test_get_sentence_for_named_entity(self):
        model = "assets/ner_collins_en"
        text = ("The supplier provides the ECU. Under supplier request, the Purchaser will provide documents "
                "identified in this section except the external standards available on the market")
        nlp = load_model(model)
        doc = apply_model(nlp, text)
        named_entities = named_entity_recognition(doc)
        sentence = get_sentence_for_named_entity(named_entities[1], text)
        self.assertEqual(sentence, "The supplier provides the ECU.")
        sentence = get_sentence_for_named_entity(named_entities[2], text)
        self.assertEqual(sentence, " Under supplier request, the Purchaser will provide documents identified in this "
                                   "section except the external standards available on the market")

    def test_get_sentence_start(self):
        text = "Test 1. Test 2. Test 3. Test 45... Test 125"
        sentences = sentence_segmentation(text)
        self.assertEqual(get_sentence_start("Test 1.", sentences), 0)
        self.assertEqual(get_sentence_start(" Test 2.", sentences), 7)
        self.assertEqual(get_sentence_start(" Test 3.", sentences), 15)
        self.assertEqual(get_sentence_start(" Test 45...", sentences), 23)
        self.assertEqual(get_sentence_start(" Test 125", sentences), 34)

    def test_get_sentence_end(self):
        self.assertEqual(get_sentence_end("Test 1.", 0), 7)
        self.assertEqual(get_sentence_end(" Test 2.", 7), 15)
        self.assertEqual(get_sentence_end(" Test 3.", 15), 23)
        self.assertEqual(get_sentence_end(" Test 45...", 23), 34)
        self.assertEqual(get_sentence_end(" Test 125", 34), 43)

    def test_is_in_sentence(self):
        model = "assets/ner_collins_en"
        text = ("The supplier provides the ECU. Under supplier request, the Purchaser will provide documents "
                "identified in this section except the external standards available on the market")
        nlp = load_model(model)
        doc = apply_model(nlp, text)
        named_entities = named_entity_recognition(doc)
        sentences = sentence_segmentation(text)
        first_sentence_start = get_sentence_start(sentences[0], sentences)
        first_sentence_end = get_sentence_end(sentences[0], first_sentence_start)
        second_sentence_start = get_sentence_start(sentences[30], sentences)
        second_sentence_end = get_sentence_end(sentences[30], second_sentence_start)
        self.assertEqual(is_in_sentence(named_entities[0], first_sentence_start, first_sentence_end), True)
        self.assertEqual(is_in_sentence(named_entities[0], second_sentence_start, second_sentence_end), False)

    def test_associate_sentences_to_named_entities(self):
        model = "assets/ner_collins_en"
        text = ("The supplier provides the ECU. Under supplier request, the Purchaser will provide documents "
                "identified in this section except the external standards available on the market")
        nlp = load_model(model)
        doc = apply_model(nlp, text)
        named_entities = named_entity_recognition(doc)
        sentences_to_named_entities = associate_sentences_to_named_entities(named_entities, text)
        self.assertEqual(len(sentences_to_named_entities), 2)

    def test_has_more_specific_occurrence(self):
        sentence = "The Purchaser has defined requirements in the document."
        text = "define"
        triggering_text = [
            {"text": "define", "active": True},
            {"text": "defined", "active": False}
        ]
        has_more_specific_occurrence = has_more_specific_occurrence_in_triggering_text(text, triggering_text, sentence)
        self.assertEqual(has_more_specific_occurrence, True)

    def test_collaboration_extraction(self):
        model = "assets/ner_collins_en"
        text = ("The supplier provides the ECU. Under supplier request, the Purchaser will provide documents "
                "identified in this section except the external standards available on the market")
        nlp = load_model(model)
        doc = apply_model(nlp, text)
        named_entities = named_entity_recognition(doc)
        sentences = sentence_segmentation(text)
        sentences_to_named_entities = associate_sentences_to_named_entities(named_entities, text)
        source_labels = ["ROLE"]
        target_labels = ["ROLE"]
        triggering_text = []
        collaborations = extract_relation("COLLABORATION", sentences, sentences_to_named_entities, source_labels, target_labels, triggering_text)
        self.assertEqual(collaborations, ["COLLABORATION(supplier,purchaser)"])

    def test_responsibilities_extraction(self):
        model = "assets/ner_collins_en"
        text = ("The supplier provides the ECU. Under supplier request, the Purchaser will provide documents "
                "identified in this section except the external standards available on the market")
        nlp = load_model(model)
        doc = apply_model(nlp, text)
        named_entities = named_entity_recognition(doc)
        sentences = sentence_segmentation(text)
        sentences_to_named_entities = associate_sentences_to_named_entities(named_entities, text)
        source_labels = ["ROLE"]
        target_labels = ["COMPONENT", "SYSTEM", "HARDWARE", "DOCUMENT"]
        triggering_text = []
        responsibilities = extract_relation("RESPONSIBLE", sentences, sentences_to_named_entities, source_labels,
                                   target_labels, triggering_text)
        self.assertEqual(responsibilities, ["RESPONSIBLE(supplier,ecu)", "RESPONSIBLE(purchaser,documents)"])

    def test_provided_relations(self):
        model = "assets/ner_collins_en"
        text = ("The supplier provides the ECU. Under supplier request, the Purchaser will provide documents "
                "identified in this section except the external standards available on the market")
        nlp = load_model(model)
        doc = apply_model(nlp, text)
        named_entities = named_entity_recognition(doc)
        sentences = sentence_segmentation(text)
        sentences_to_named_entities = associate_sentences_to_named_entities(named_entities, text)
        # collaborations extraction
        source_labels = ["ROLE"]
        target_labels = ["ROLE"]
        triggering_text = []
        collaborations = extract_relation("COLLABORATION", sentences, sentences_to_named_entities, source_labels,
                                          target_labels, triggering_text)
        # responsabilities extraction
        source_labels = ["ROLE"]
        target_labels = ["COMPONENT", "SYSTEM", "HARDWARE", "DOCUMENT"]
        triggering_text = []
        responsibilities = extract_relation("RESPONSIBLE", sentences, sentences_to_named_entities, source_labels,
                                            target_labels, triggering_text)
        relations = collaborations + responsibilities
        provided = create_new_relations_from_existing_relations(relations,
                                                                "RESPONSIBLE",
                                                                "right",
                                                                "COLLABORATION",
                                                                "right",
                                                                "PROVIDED")
        print("new PROVIDED relations created : ", provided)


    def test_approval_extraction(self):
        model = "assets/ner_collins_en"
        text = ("The supplier will validate documents provided by the purchaser in accordance to appropriate criteria")
        nlp = load_model(model)
        doc = apply_model(nlp, text)
        named_entities = named_entity_recognition(doc)
        print(named_entities)
        sentences = sentence_segmentation(text)
        sentences_to_named_entities = associate_sentences_to_named_entities(named_entities, text)
        source_labels = ["ROLE"]
        target_labels = ["COMPONENT", "SYSTEM", "HARDWARE", "DOCUMENT", "STANDARD", "CRITERIA", "PROCESS", "UNIT", "PHASE"]
        triggering_text = [
            {"text": "approve", "active": True},
            {"text": "validate", "active": True}
        ]
        approval = extract_relation("APPROVAL", sentences, sentences_to_named_entities, source_labels, target_labels, triggering_text)
        self.assertEqual(approval, ['APPROVAL(supplier,documents)'])


    def test_rejection_extraction(self):
        model = "assets/ner_collins_en"
        text = ("The supplier will reject documents provided by the purchaser if they do not fulfill all requirements defined in the chapter")
        nlp = load_model(model)
        doc = apply_model(nlp, text)
        named_entities = named_entity_recognition(doc)
        print(named_entities)
        sentences = sentence_segmentation(text)
        sentences_to_named_entities = associate_sentences_to_named_entities(named_entities, text)
        source_labels = ["ROLE"]
        target_labels = ["COMPONENT", "SYSTEM", "HARDWARE", "DOCUMENT", "STANDARD", "CRITERIA", "PROCESS", "UNIT",
                         "PHASE"]
        triggering_text = [
            {"text": "reject", "active": True},
            {"text": "invalidate", "active": True}
        ]
        rejection = extract_relation("REJECTION", sentences, sentences_to_named_entities, source_labels, target_labels,
                               triggering_text)
        self.assertEqual(rejection, ['REJECTION(supplier,documents)', 'REJECTION(supplier,requirements)'])


    def test_definition_extraction(self):
        model = "assets/ner_collins_en"
        text = "The requirements are defined in the document."
        nlp = load_model(model)
        doc = apply_model(nlp, text)
        named_entities = named_entity_recognition(doc)
        sentences = sentence_segmentation(text)
        sentences_to_named_entities = associate_sentences_to_named_entities(named_entities, text)
        source_labels = ["STANDARD", "PROCESS"]
        target_labels = ["DOCUMENT"]
        triggering_text = [
            {"text": "define", "active": False},
            {"text": "defined", "active": True}
        ]
        definitions = extract_relation("DEFINED_BY", sentences, sentences_to_named_entities, source_labels, target_labels,
                               triggering_text)
        self.assertEqual(definitions, ['DEFINED_BY(requirements,document)'])

    def test_compliance_extraction(self):
        model = "assets/ner_collins_en"
        text = "The Supplier will comply with the requirements defined in the document."
        nlp = load_model(model)
        doc = apply_model(nlp, text)
        named_entities = named_entity_recognition(doc)
        sentences = sentence_segmentation(text)
        sentences_to_named_entities = associate_sentences_to_named_entities(named_entities, text)
        source_labels = ["DOCUMENT", "ROLE", "ORG"]
        target_labels = ["STANDARD", "CRITERIA"]
        triggering_text = [
            {"text": "comply", "active": True},
            {"text": "complies", "active": True}
        ]
        compliance = extract_relation("COMPLY_WITH", sentences, sentences_to_named_entities, source_labels, target_labels,
                               triggering_text)
        self.assertEqual(compliance, ['COMPLY_WITH(supplier,requirements)'])


    def test_composition_extraction(self):
        model = "assets/ner_collins_en"
        text = "The A380 is composed by a left wing, a right wing and different systems."
        nlp = load_model(model)
        doc = apply_model(nlp, text)
        named_entities = named_entity_recognition(doc)
        print(named_entities)
        sentences = sentence_segmentation(text)
        sentences_to_named_entities = associate_sentences_to_named_entities(named_entities, text)
        source_labels = ["COMPONENT", "SYSTEM", "HARDWARE"]
        target_labels = ["COMPONENT", "SYSTEM", "HARDWARE"]
        triggering_text = [
            {"text": "compose", "active": False},
            {"text": "composed", "active": True}
        ]
        composition = extract_relation("COMPOSED_BY", sentences, sentences_to_named_entities, source_labels,
                                       target_labels,
                                       triggering_text)
        self.assertEqual(composition, ['COMPOSED_BY(a380,left wing)', 'COMPOSED_BY(a380,right wing)', 'COMPOSED_BY(a380,different systems)'])
        text = "The left wing composes the A380."
        doc = apply_model(nlp, text)
        named_entities = named_entity_recognition(doc)
        print(named_entities)
        sentences = sentence_segmentation(text)
        sentences_to_named_entities = associate_sentences_to_named_entities(named_entities, text)
        source_labels = ["COMPONENT", "SYSTEM", "HARDWARE"]
        target_labels = ["COMPONENT", "SYSTEM", "HARDWARE"]
        triggering_text = [
            {"text": "compose", "active": False},
            {"text": "composed", "active": True}
        ]
        composition = extract_relation("COMPOSED_BY", sentences, sentences_to_named_entities, source_labels, target_labels,
                               triggering_text)
        self.assertEqual(composition, ['COMPOSED_BY(a380,left wing)'])


    def test_communication_extraction(self):
        model = "assets/ner_collins_en"
        text = "The ECU send messages to the A380 and the LRI"
        nlp = load_model(model)
        doc = apply_model(nlp, text)
        named_entities = named_entity_recognition(doc)
        print(named_entities)
        sentences = sentence_segmentation(text)
        sentences_to_named_entities = associate_sentences_to_named_entities(named_entities, text)
        source_labels = ["COMPONENT", "SYSTEM", "HARDWARE"]
        target_labels = ["COMPONENT", "SYSTEM", "HARDWARE"]
        triggering_text = [
            {"text": "communicate", "active": True},
            {"text": "sends message", "active": True},
            {"text": "send message", "active": True},
            {"text": "send messages", "active": True}
        ]
        communications = extract_relation("COMMUNICATE_WITH", sentences, sentences_to_named_entities, source_labels,
                                       target_labels,
                                       triggering_text)
        self.assertEqual(communications, ['COMMUNICATE_WITH(ecu,a380)', 'COMMUNICATE_WITH(ecu,lri)'])
