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

