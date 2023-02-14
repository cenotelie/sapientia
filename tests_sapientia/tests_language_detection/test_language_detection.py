import unittest

from sapientia.language_detection.language_detection import detect_language


class TestLanguageDetection(unittest.TestCase):
    def test_detect_language_english(self):
        self.assertEqual(detect_language("This is a text written in English."), "en")

    def test_detect_language_french(self):
        self.assertEqual(detect_language("Ce texte est écrit en français."), "fr")

if __name__ == '__main__':
    unittest.main()
