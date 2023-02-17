import unittest
# from validator.topino import Validator
from validator.main import Validator
from os import getcwd


class ValidateCase(unittest.TestCase):
    def test_validate(self):
        v = Validator('validation_process/validation/test_files/sample_cits.csv', 'test/output')
        v.validate()
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
