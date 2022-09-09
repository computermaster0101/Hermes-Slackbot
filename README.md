# Hermes

Hermes is the messenger of the gods! The purpose of this utility is to allow command and control of a system using pattern matching and json files.

## Requirements: 

* python version 3.10.4
* dropbox, onedrive, nextcloud, etc

## Quick Start:
1. Copy example.hermes.json to ~/hermes.json
2. Configure the following values in the hermes.json config file
   * sysName: Name of the system. Used for listening for messages. 
   * appDir: Hermes Application directory. This is the directory containing hermes.py.
   * msgDir: Message directory used by Hermes to listen for {sysName}.txt message files.
   * rulesDir: Rules directory containing .json files formatted as hermes rules.
   * histDir: History directory containing all processed messages as well as the results of any actions.
3. Execute hermes.py

## Details:

When Hermes starts, it attempts to load a configuration file from the users home directory (~/hermes.json). 
This file is a requirement as it configures the directories and files that are to be used by Hermes. 
After loading the configuration file, Hermes begins watching the message directory for files named {sysame}.txt. 
When a message intended for the system is identified, Hermes will pick up the file, look for matching patterns in the configured rules, executes the configured actions, and logs everything to a new file in the history directory.

__IMPORTANT: Hermes is not responsible for placing the message file into the message directory in the correct format. Placing the file in the right location with the right content is the responsibility of the user__ 


## File Details:
* message file name: ```system{{NumberField}}.txt``` 
* message file content:```"device":"system{{NumberField}}","message":"{{TextField}}","timestamp":"{{CreatedAt}}"}```
* rule file content: ```{
  "name": "",
  "patterns": [
    ""
  ],
  "actions": [
    ""
  ],
  "runningDirectory": "",
  "passMessage": false,
  "active": false
}```



  
**Inspired by Push2Run**

See https://www.push2run.com/help/setup_dropbox.html for example backend file integration using dropbox solutions.
Use a number and a text ingredient where the number is attached to a keyword such as system or jarvis. 
This will be used to identify which system should pickup the file. (ie javis7 or system23).
I've added some images of my ifttt.com setup to aid in configuration.
