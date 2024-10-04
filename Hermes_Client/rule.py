"""
This script defines a Rule class that takes a file name as an argument in its 
constructor. The file is expected to be a JSON file containing data that defines 
the rule, including a name, patterns, actions, running directory, pass message, 
and active status. The constructor reads the file, loads the JSON data, and 
assigns the data to class variables. If any of the required attributes are missing, 
a MissingattributeError is raised. If the file is not found or there is a JSON 
decode error, the appropriate error is raised. The class also has a __str__ method, 
which formats the class variables as a string for printing.
"""

import json
import os


class MissingAttributeError(Exception):
    pass


class Rule:
    def __init__(self, file):
        try:
            with open(file) as f:
                rule_data = json.load(f)
            self.name = rule_data.get('name')
            self.patterns = rule_data.get('patterns')
            self.actions = rule_data.get('actions')
            self.actions = [os.path.expanduser(a) for a in self.actions]
            self.runningDirectory = './' if rule_data.get('runningDirectory') == "" else os.path.expanduser(rule_data.get('runningDirectory'))
            self.passMessage = rule_data.get('passMessage', False)
            self.active = rule_data.get('active', False)

            if self.name is None:
                raise MissingAttributeError(f"Error loading rule from {file}: Missing 'name' attribute.")
            if self.patterns is None:
                raise MissingAttributeError(f"Error loading rule from {file}: Missing 'patterns' attribute.")
            if self.actions is None:
                raise MissingAttributeError(f"Error loading rule from {file}: Missing 'actions' attribute.")
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Error loading rule from {file}: {e}")
        except json.decoder.JSONDecodeError as e:
            raise json.decoder.JSONDecodeError(f"Error loading rule from {file}: {e}")
        except Exception as e:
            raise

    def __str__(self):
        patterns = "\n".join(self.patterns)
        actions = "\n".join(self.actions)
        return f"Name: {self.name}\nPatterns: \n{patterns}\nActions: \n{actions}\nRunning Directory: {self.runningDirectory}\nPass Message: {self.passMessage}\nActive: {self.active} "
