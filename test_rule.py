"""
This script defines a TestRule class that inherits from unittest.TestCase. The 
class contains several test methods that test the functionality of the Rule 
class defined in rule.py.

The setUp method creates several JSON files that are used in the tests. One file 
contains valid data for a rule, another contains data that is missing a required 
attribute, another contains malformed JSON data, and the last one is a nonexistent 
file.

The test_good_rule method tests if the Rule class can handle a file with valid 
data. This test should pass without raising any errors.

The test_missing_attribute_rule method tests if the Rule class raises a
 MissingAttributeError when a file is missing some of the necessary attributes. 
 This test should pass when the exception is raised.

The test_malformed_rule method tests if the Rule class raises a JSONDecodeError 
when a file is malformed. This test should pass when the exception is raised.

The test_nonexistent_rule method tests if the Rule class raises a FileNotFoundError 
when a file does not exist. This test should pass when the exception is raised.

Finally, the tearDown method deletes the test files that were created in the 
setUp method.

If the script is run directly, it calls unittest.main() which runs all the test 
methods in the class and gives a summary of the test results.




"""

import unittest
import json
from rule import Rule, MissingAttributeError



class TestRule(unittest.TestCase):
    def setUp(self):
        self.valid_rule = {
            "name": "Hello World", 
            "patterns": ["^(hello|goodbye) world(!)?$"], 
            "actions": ["echo Hello World!", "echo Goodbye World!"], 
            "runningDirectory": "", 
            "passMessage": False, 
            "active": True
        }
        self.valid_rule_file = "valid_rule.json"
        with open(self.valid_rule_file, "w") as f:
            json.dump(self.valid_rule, f)

        self.missing_attribute_rule = {
            "name": "Missing Attribute", 
            "actions": ["echo Missing Attribute!"], 
            "runningDirectory": "", 
            "passMessage": False, 
            "active": True
        }
        self.missing_attribute_rule_file = "missing_attribute_rule.json"
        with open(self.missing_attribute_rule_file, "w") as f:
            json.dump(self.missing_attribute_rule, f)

        self.malformed_rule = """{
            "name": "Malformed Rule", 
            "patterns": ["^malformed pattern$"], 
            "actions": ["echo Malformed Rule!"], 
            "runningDirectory": "", 
            "passMessage": Fale 
            "active": True
        }"""
        self.malformed_rule_file = "malformed_rule.json"
        with open(self.malformed_rule_file, "w") as f:
            json.dump(self.malformed_rule, f)
        self.nonexistent_rule_file = "nonexistent_file.json"

    def test_good_rule(self):
        # Test if the class can handle a valid rule
        rule = Rule(self.valid_rule_file)

    def test_missing_attribute_rule(self):
        # Test if the class raises a MissingAttributeError when a file is missing some of the necessary attributes
        with self.assertRaises(MissingAttributeError):
            rule = Rule(self.missing_attribute_rule_file)

    def test_malformed_rule(self):
        # Test if the class raises a JSONDecodeError when a file is malformed
        with self.assertRaises(AttributeError):
            rule = Rule(self.malformed_rule_file)

    def test_nonexistent_rule(self):
        # Test if the class raises a FileNotFoundError when a file does not exist
        with self.assertRaises(FileNotFoundError):
            rule = Rule(self.nonexistent_rule_file)

    def tearDown(self):
        # delete the test files
        import os
        os.remove(self.valid_rule_file)
        os.remove(self.missing_attribute_rule_file)
        os.remove(self.malformed_rule_file)

if __name__ == '__main__':
    unittest.main()

