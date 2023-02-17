import unittest
from validator.topino import Validator


class ValidateCase(unittest.TestCase):
    def test_validate(self):
        v = Validator('validation_process/validation/test_files/sample_cits.csv', 'test/output')
        v.validate()
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
