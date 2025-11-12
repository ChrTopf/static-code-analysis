import unittest

from checks.csharp_method_length import CSharpMethodLength
from util.test_butler import TestButler


class TestStringMethods(unittest.TestCase):

    def test_csharp_method_length(self):
        sample_file = "samples/CoffeeShop.cs"
        expected_result = [48]
        check_config = {"max_lines": 20}
        check = CSharpMethodLength()

        butler = TestButler(self)
        diff = butler.generate_new_file_diff(sample_file)
        check.parse_config(check_config)
        actual_result = check.execute_on_changed_file(diff) 
        butler.verify_check_results(expected_result, actual_result)

if __name__ == '__main__':
    unittest.main()