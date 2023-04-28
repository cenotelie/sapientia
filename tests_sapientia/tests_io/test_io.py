import unittest
from pathlib import PosixPath

from sapientia.io.io import load_files, replace_extension


class TestIO(unittest.TestCase):

    def test_load_files(self):
        files = load_files("data")
        self.assertEqual(files, ['data/3.txt', 'data/1.txt', 'data/2.txt', 'data/subdirectory/4.txt'])

    def test_replace_extension(self):
        new_file = replace_extension("data/subdirectory/4.txt", ".doc")
        self.assertEqual(new_file, PosixPath("data/subdirectory/4.doc"))


if __name__ == '__main__':
    unittest.main()
