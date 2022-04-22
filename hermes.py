import os
import re
import json
import time
import subprocess

configFile=os.path.expanduser("~\\hermes.json")
config=json.load(open(configFile))

for item in config:
  config[item]=os.path.expanduser(config[item])

systemName=config["sysName"]
appDirectory=config["appDir"]
rulesDirectory=config["rulesDir"]
historyDirectory=config["histDir"]
msgDir=config["msgDir"]
messageFile=os.path.join(msgDir,f"{systemName}.txt")

print(f"""
Hermes: {systemName}
Configuration: {configFile}

Hermes started at {time.strftime('%Y%m%d-%H%M%S')} with the following values
Message File: {messageFile}
History Directory: {historyDirectory}
App Directory: {appDirectory}
Rules Folder: {rulesDirectory}
""")

while not time.sleep(1):
  if os.path.exists(messageFile):
    newMsg=json.load(open(messageFile))
    saveTo=os.path.join(historyDirectory,f"{time.strftime('%Y%m%d-%H%M%S')}.{systemName}.txt")
    os.rename(messageFile,saveTo)         
    print(f"""
Device: {newMsg.get("device")}
Message: {newMsg.get("message")}
Timestamp: {newMsg.get("timestamp")}""")

    for file in os.listdir(rulesDirectory):
      if file.endswith(".json"):
        rule=json.load(open(os.path.join(rulesDirectory,file)))
        for pattern in rule.get("patterns"):
          if re.search(pattern, newMsg.get("message")):
            matched=True
            print(f"""
Rule: {rule.get("name")}
Pattern: {pattern}
Run Directory: {rule.get("runningDirectory")}
Run As Admin: {rule.get("runAsAdmin")}
Pass Message: {rule.get("passMessage")}
Active: {rule.get("active")}""")
            
            
            if rule["active"]:
              ruleRunningDir=os.path.expanduser(rule.get("runningDirectory"))
              if os.path.exists(ruleRunningDir): os.chdir(ruleRunningDir)
              for action in rule["actions"]:
                action=os.path.expanduser(action)
                if rule["passMessage"]:
                  cmd=(f"{action} \"{newMsg['message']}\"")
                else:
                  cmd=action
                print(f"execution action: {cmd}")
                subprocess.Popen(cmd)
              os.chdir(appDirectory)
              history=open(saveTo,"a")
              history.write(f"""
{rule}""")
              history.close()
    if not matched: 
      print(f"Undefined Pattern: {message}")
      history=open(saveTo,"a")
      history.write(f"""
Message:"{newMsg.message}" does not match any defined patterns""")
      history.close()