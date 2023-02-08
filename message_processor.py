import re
import shlex
import subprocess
import os


class MessageProcessor:
    def __init__(self, rule_set):
        self.rule_set = rule_set

    def process_message(self, message, rules):
        try:
            match = False
            self.rule_set = rules
            for rule in self.rule_set.rules.values():
                print(f"Processing rule: {rule}")
                for pattern in rule.patterns:
                    print(f"Matching message '{message.text}' against pattern '{pattern}'")
                    if re.search(pattern, message.text):
                        match = True
                        print(f"Message '{message.text}' matches pattern '{pattern}'")
                        if rule.active:
                            # return_path = os.getcwd()  # Store the current working directory in return_path
                            # if os.path.exists(rule.runningDirectory): os.chdir(rule.runningDirectory)  # if the running directory exists move to it
                            for action in rule.actions:
                                if rule.passMessage:  # if the message should be sent with the action update the command
                                    cmd = f"{action} \"{message.text}\""
                                else:
                                    cmd = action
                                print(f"Running action '{action}' in directory '{rule.runningDirectory}'")
                                try:
                                    subprocess.run(action, cwd=rule.runningDirectory, shell=True, check=True)
                                    # subprocess.Popen(shlex.split(cmd))
                                except subprocess.CalledProcessError as e:
                                    print(f"Error running action {action}: {e}")
                            # os.chdir(return_path)
                        else:
                            print(f"Rule {rule} is inactive. Skipping.")
                            continue
            if not match:  # if the pattern/message does not match log it
                print(f"Undefined Pattern: {message.text}")
        except Exception as e:
            print(f"An error occurred while processing message: {e}")
