import os

from rule import Rule


class RuleDictionary:

    def __init__(self, rules_directory):
        self.ruleDictionary = []
        for file in os.listdir(rules_directory):  # for every file in the rules directory
            if file.endswith(".json"):  # only process json files
                try:
                    new_rule = Rule(os.path.join(self.rules_directory, file))
                    self.ruleDictionary[new_rule.name] = new_rule
                except:
                    print("could not load rule file")
