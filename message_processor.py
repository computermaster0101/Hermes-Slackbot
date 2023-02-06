import re
import subprocess


class MessageProcessor:
    def __init__(self, rule_set):
        self.rule_set = rule_set

    def process_message(self, message, rules):
        try:
            self.rule_set=rules
            for rule in self.rule_set.rules.values():
                print(f"Processing rule: {rule}")
                if not rule.active:
                    print(f"Rule {rule} is inactive. Skipping.")
                    continue
                for pattern in rule.patterns:
                    print(f"Matching message '{message.text}' against pattern '{pattern}'")
                    match = re.search(pattern, message.text)
                    if match:
                        print(f"Message '{message.text}' matches pattern '{pattern}'")
                        if not rule.passMessage:
                            print(f"Rule {rule} is set to not pass message. Returning.")
                            return
                        for action in rule.actions:
                            print(f"Running action '{action}' in directory '{rule.runningDirectory}'")
                            try:
                                subprocess.run(action, cwd=rule.runningDirectory, shell=True, check=True)
                            except subprocess.CalledProcessError as e:
                                print(f"Error running action {action}: {e}")
        except Exception as e:
            print(f"An error occurred while processing message: {e}")
