import unittest

from sapientia.workflow.workflow import create_training_data


class TestWorkflow(unittest.TestCase):
    def test_create_training_data(self):
        create_training_data("data", "training_data/airbus_training_data.jsonl")
        training_data = open("training_data/airbus_training_data.jsonl", "r")
        self.assertIsInstance(training_data.readline(), str)
        training_data.close()


if __name__ == '__main__':
    unittest.main()
