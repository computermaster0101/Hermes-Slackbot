import re
import subprocess
from sys import exception


class MessageProcessor:
    def __init__(self, rule_set):
        self.rule_set = rule_set

    def process_message(self, message, rules):
        try:
            output = []
            match = False
            self.rule_set = rules
            output.append("")
            output.append(f"Processing message '{message}' against rule dictionary")
            for rule in self.rule_set.rules.values():
                # print(f"Processing rule: {rule.name}")
                for pattern in rule.patterns:
                    # print(f"Matching message '{message.text}' against pattern '{pattern}'")
                    try:
                        if re.search(pattern, message.text):
                            match = True
                            output.append(f"Message '{message.text}' matched pattern '{pattern}'")
                            if rule.active:
                                for action in rule.actions:
                                    if rule.passMessage: 
                                        print(message.text)
                                        cmd = f"{action} \"{message.text}\""
                                    else:
                                        cmd = action
                                    output.append(f"Running action '{action}' in directory '{rule.runningDirectory}'")
                                    try:
                                        subprocess.Popen(cmd, cwd=rule.runningDirectory, shell=True)
                                    except subprocess.CalledProcessError as e:
                                        output.append(f"Error running action {action}: {e}")
                            else:
                                output.append(f"Rule '{rule.name}' is inactive. Skipping.")
                                continue
                    except Exception as e:
                        output.append(f"An error occured while matching patterns for rule '{rule.name}'\nError: {e}")
                        print(f"An error occured while matching patterns for rule '{rule.name}'\nError: {e}")
                        pass
            if not match:  # if the pattern/message does not match log it
                output.append(f"Undefined Pattern: {message.text}")
            return output

        except Exception as e:
            print(f"An error occurred while processing message: {e}")
