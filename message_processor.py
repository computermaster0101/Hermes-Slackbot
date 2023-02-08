import re
import shlex
import subprocess
import os


class MessageProcessor:
    def __init__(self, rule_set):
        self.rule_set = rule_set

    def process_message(self, message, rules):
        try:
            output = []
            match = False
            self.rule_set = rules
            for rule in self.rule_set.rules.values():
                output.append(f"Processing rule: {rule}")
                for pattern in rule.patterns:
                    output.append(f"Matching message '{message.text}' against pattern '{pattern}'")
                    if re.search(pattern, message.text):
                        match = True
                        output.append(f"Message '{message.text}' matches pattern '{pattern}'")
                        if rule.active:
                            # return_path = os.getcwd()  # Store the current working directory in return_path
                            # if os.path.exists(rule.runningDirectory): os.chdir(rule.runningDirectory)  # if the running directory exists move to it
                            for action in rule.actions:
                                if rule.passMessage:  # if the message should be sent with the action update the command
                                    cmd = f"{action} \"{message.text}\""
                                else:
                                    cmd = action
                                output.append(f"Running action '{action}' in directory '{rule.runningDirectory}'")
                                try:
                                    subprocess.run(action, cwd=rule.runningDirectory, shell=True, check=True)
                                    # subprocess.Popen(shlex.split(cmd))
                                except subprocess.CalledProcessError as e:
                                    output.append(f"Error running action {action}: {e}")
                            # os.chdir(return_path)
                        else:
                            output.append(f"Rule {rule} is inactive. Skipping.")
                            continue
            if not match:  # if the pattern/message does not match log it
                output.append(f"Undefined Pattern: {message.text}")
            return match, output

        except Exception as e:
            print(f"An error occurred while processing message: {e}")
