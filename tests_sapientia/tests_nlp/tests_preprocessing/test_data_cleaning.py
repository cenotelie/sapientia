import unittest

from sapientia.nlp.preprocessing.data_cleaning import sentences_fixing, group_lists_in_sentences, sentences_cleaning


class TestDataCleaning(unittest.TestCase):

    def test_sentences_fixing(self):
        sentences = ["This is a sentence e.g.", "cut in half.", "This is another sentence", "Take this sentence",
                     "This is the last sentence and it is e.g.", "also cut in half",
                     "this is the beginning of a list :", "• first item", "• second item"]
        fixed_sentences = sentences_fixing(sentences)
        print(fixed_sentences)
        self.assertEqual(True, True)

    def test_group_lists_in_sentences(self):
        sentences = ["This is a sentence e.g.", "cut in half.", "This is another sentence", "Take this sentence",
                     "This is the last sentence and it is e.g.", "also cut in half",
                     "this is the beginning of a list :", "• first item", "• second item"]
        grouped_sentences = group_lists_in_sentences(sentences)
        print(grouped_sentences)
        self.assertEqual(True, True)

    def test_grouped_lists(self):
        sample_airbus = "Airbus is currently engaged in a R&T effort to prepare for the Primary Flight Control " \
                        "Actuation the Electromechanical Actuator (EMA) and the centralized actuation electronic " \
                        "(APMU) technologies. The studies objectives are:" \
                        "- The demonstration of EMA technology maturity," \
                        "- The electrical actuators reliability improvement," \
                        "- The system weight saving," \
                        "- The electrical actuators cost reduction." \
                        "- The power management optimisation of flight control actuation," \
                        "The All-Electric Aircraft is a major target for the next generation of aircraft to lower " \
                        "consumption of non-propulsive power and thus fuel burn. To remove hydraulic circuits, pumps " \
                        "and reservoirs, EMA technology is promising but need to be optimized to meet the aircraft " \
                        "manufacturer requirements (performances, lifetime, reliability, weight, space envelop, " \
                        "cost,…). The WP7 GENOME objectives are to bring APMU and EMA family (Linear and Rotary) to " \
                        "the maturity TRL6. This document is associated to the Deliverable Number WP7.1.2a2 of the " \
                        "GENOME project. Nota: This technical specification is achieved on the basis of All Electric " \
                        "Aircraft type NSA and applicable For the A320 demonstration platform:" \
                        "o The specific requirements are defined in this technical specification and identified by " \
                        "(*) Italic," \
                        "o The ECU functions shall be integrated inside the APMU. Impacts on requirements are " \
                        "clarified in ACTUATION 2015 specifications “Power Drive Electronics Module Technical" \
                        "Specification” ref. 2015-AI-F-DEL.D16.19-001-R4.1 and “D16.18.S2 – Standard Motor " \
                        "Technical Specification (Size 2)” ref. A2015-AI-F-DELD16.18.S2-001-R2.1)."
        sentences = sample_airbus.split(". ")
        sentences = sentences_fixing(sentences)
        sentences = group_lists_in_sentences(sentences)
        sentences = sentences_cleaning(sentences)
        for sentence in sentences:
            print(sentence)
            print("****************************************")
        self.assertEqual(True, True)

    def test_sentences_cleaning(self):
        sentences = ["", ", ", "Page 5 of 965  1 apple, please.", " \n This is a sentence"]
        cleaned_sentences = sentences_cleaning(sentences)
        print(cleaned_sentences)
        self.assertEqual(cleaned_sentences, ['1 apple, please.', 'This is a sentence'])


if __name__ == '__main__':
    unittest.main()
