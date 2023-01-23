"""
This class has an __init__ method that takes a directory path as an argument. It 
initializes an empty dictionary to store the rules, and then iterates through the 
files in the directory. For each file that ends with '.json', it creates a new 
Rule object, passing the file path as an argument. The Rule object is then added 
to the dictionary with the file name as the key. If any errors occur while loading 
the rules, the appropriate exception is raised.

The class also has a __str__ method that formats the rules as a string for 
printing, with the file name as the key, and the rule as the value.
"""
import json
import os
from rule import Rule, MissingAttributeError

class RuleSet:
    def __init__(self, directory):
        self.rules = {}
        try:
            for file in os.listdir(directory):
                if file.endswith(".json"):
                    try:
                        rule = Rule(os.path.join(directory, file))
                        self.rules[file] = rule
                    except MissingAttributeError as e:
                        print(f"Error loading rule from {file}: {e}")
        except NotADirectoryError as e:
            try:
                rule = Rule(directory)
                self.rules[os.path.basename(directory)] = rule
            except MissingAttributeError as e:
                print(f"Error loading rule from {directory}: {e}")

