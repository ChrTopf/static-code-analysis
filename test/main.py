import unittest

from checks.csharp_method_length import CSharpMethodLength
from util.test_butler import TestButler
from util.test_config import TestConfig


class TestStringMethods(unittest.TestCase):

    def test_csharp_method_length(self):
        sample_file = "samples/CoffeeShop.cs"
        expected_result = [48]
        check_config = {"max_lines": 20}
        check = CSharpMethodLength()

        butler = TestButler(self)
        butler.execute_test(TestConfig(sample_file, expected_result, check_config, check))

if __name__ == '__main__':
    unittest.main()