import unittest
from validator.main import Validator

class ValidateCase(unittest.TestCase):
    def test_validate(self):
        v = Validator('test_files/valid_cits.csv', 'test/output')
        output = v.validate()
        self.assertEqual(output, {})  # add assertion here


if __name__ == '__main__':
    unittest.main()
