import json

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
            self.runningDirectory = rule_data.get('runningDirectory')
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
        patterns = '\n '.join(self.patterns)
        actions = '\n'.join(self.actions)
        return f"Name: {self.name}\nPatterns: \n{patterns}\nActions: \n{actions}\nRunning Directory: {self.runningDirectory}\nPass Message: {self.passMessage}\nActive: {self.active}"
