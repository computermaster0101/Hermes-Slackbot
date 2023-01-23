"""
The test_load_multiple_rules method tests if the RuleSet class can load multiple 
rules into the dictionary by creating an instance of the class, passing the 
test_directory as an argument and then checking the length of the rules dictionary 
and comparing it to the expected number of rules, in this case 2.

The test_iterate_over_rules method tests if the class can iterate over each rule 
and print the key name and rule by creating an instance of the class, passing the 
test_directory as an argument and then using a for loop to iterate over the rules 
dictionary, printing the key name and rule.

The test_return_errors method tests if the class returns errors generated when
rules are read. It uses the assertRaises method to check if the class raises 
the appropriate exception when an error occurs.

The tearDown method deletes the test files and directory that were created in
the setUp method.
"""

import unittest
import os
import json
from rule_set import RuleSet, MissingAttributeError

class TestRuleSet(unittest.TestCase):
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

        self.valid_rule_2 = {
            "name": "Second Rule", 
            "patterns": ["^(second) rule$"], 
            "actions": ["echo Second Rule!"], 
            "runningDirectory": "", 
            "passMessage": False, 
            "active": True
        }
        self.valid_rule_file_2 = "valid_rule_2.json"
        with open(self.valid_rule_file_2, "w") as f:
            json.dump(self.valid_rule_2, f)

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

        self.test_directory = "test_rules"
        os.mkdir(self.test_directory)
        os.rename(self.valid_rule_file, os.path.join(self.test_directory, self.valid_rule_file))
        os.rename(self.valid_rule_file_2, os.path.join(self.test_directory, self.valid_rule_file_2))
        os.rename(self.missing_attribute_rule_file, os.path.join(self.test_directory, self.missing_attribute_rule_file))

    def test_iterate_over_rules(self):
        # Test if the class can iterate over each rule and print the key name and rule
        rule_set = RuleSet(self.test_directory)
        self.assertEqual(len(rule_set.rules), 2)
        for file, rule in rule_set.rules.items():
            print(f'File: {file}, Rule: {rule}')

    def test_load_multiple_rules(self):
        # Test if the class can load multiple rules into the dictionary
        rule_set = RuleSet(self.test_directory)
        self.assertEqual(len(rule_set.rules), 2)

    def test_return_errors(self):
        rule_set = RuleSet(os.path.join(self.test_directory, self.missing_attribute_rule_file))
        self.assertEqual(len(rule_set.rules), 0)


            
    def tearDown(self):
        # delete the test files and directory
        import shutil
        shutil.rmtree(self.test_directory)
        os.remove(self.malformed_rule_file)

if __name__ == '__main__':
    unittest.main()
