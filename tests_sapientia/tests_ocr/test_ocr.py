import unittest

from sapientia.ocr.ocr import parse


class TestOCR(unittest.TestCase):
    def test_parse_text_file(self):
        text_file = "data/test_txt.txt"
        content_test_file = "Fichier de test (Apache Tika)"
        parsed_content_test_file = parse(text_file)
        self.assertIsInstance(parsed_content_test_file, str)
        self.assertIn(content_test_file, parsed_content_test_file)

    def test_parse_odt_file(self):
        text_file = "data/test_odt.odt"
        content_test_file = "Fichier de test (Apache Tika)"
        parsed_content_test_file = parse(text_file)
        self.assertIsInstance(parsed_content_test_file, str)
        self.assertIn(content_test_file, parsed_content_test_file)

    def test_parse_docx_file(self):
        text_file = "data/test_docx.docx"
        content_test_file = "Fichier de test (Apache Tika)"
        parsed_content_test_file = parse(text_file)
        self.assertIsInstance(parsed_content_test_file, str)
        self.assertIn(content_test_file, parsed_content_test_file)

    def test_parse_pdf_file(self):
        text_file = "data/test_pdf.pdf"
        content_test_file = "Fichier de test (Apache Tika)"
        parsed_content_test_file = parse(text_file)
        self.assertIsInstance(parsed_content_test_file, str)
        self.assertIn(content_test_file, parsed_content_test_file)


if __name__ == '__main__':
    unittest.main()
