import re
import subprocess


class MessageProcessor:
    def __init__(self, rule_set):
        self.rule_set = rule_set

    def process_message(self, message, rules):
        self.rule_set=rules
        for rule in self.rule_set.rules.values():
            if not rule.active:
                continue
            for pattern in rule.patterns:
                match = re.search(pattern, message.text)
                if match:
                    if not rule.passMessage:
                        return
                    for action in rule.actions:
                        try:
                            subprocess.run(action, cwd=rule.runningDirectory, shell=True, check=True)
                        except subprocess.CalledProcessError as e:
                            print(f"Error running action {action}: {e}")
