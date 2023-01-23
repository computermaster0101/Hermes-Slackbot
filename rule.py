import json


def test_rule(test_file="temp_test_rule.json", write=True, delete=True):
    test_file_data = {
        "name": "Hello World",
        "patterns": [
            "^(hello|goodbye) world(!)?$"
        ],
        "actions": [
            "echo Hello World!",
            "echo Goodbye World!"
        ],
        "runningDirectory": "",
        "passMessage": False,
        "active": True
    }
    if write:
        with open(test_file, "w") as outfile:
            json.dump(test_file_data, outfile)

    Rule(test_file)

    if delete:
        import os
        os.remove(test_file)


class Rule:
    def __init__(self, file):
        try:
            rule_data = json.load(open(file))  # load the rule file
            self.name = rule_data['name']
            self.patterns = rule_data['patterns']
            self.actions = rule_data['actions']
            self.runningDirectory = rule_data['runningDirectory']
            self.passMessage = rule_data['passMessage']
            self.active = rule_data['active']
            output = str(self)
        except FileNotFoundError as err:
            output = '\n'.join([
                f"Failed Loading Rule: {file}",
                f"Error: {err}",
                ""
            ])
        except AttributeError as err:
            output = '\n'.join([
                f"Failed Loading Rule: {file}",
                f"Error: {err}",
                ""
            ])
        finally:
            print(output)

    def __str__(self):
        patterns = '\n'.join(self.patterns)
        actions = '\n'.join(self.actions)
        return '\n'.join([
            f"Name: {self.name}",
            "",
            f"Patterns: \n{patterns}",
            "",
            f"Actions: \n{actions}",
            "",
            f"Running Directory: {self.runningDirectory}",
            f"Pass Message: {self.passMessage}",
            f"Active: {self.active}",
            ""
        ])




