# Hermes

Hermes is the messenger of the gods! The purpose of this utility is to allow command and control of a system using pattern matching and json files.

* NOTE: this readme is very very out of date and needs to be updated however the program still works (validated 10/4/2024)
* Update: the api can be ran ouside of Lambda and there's a rebuilt container in dockerhub at mherber2/hermes-server that just needs env vars (see Hermes_Server/.env for example)
* Coming soon: chatgpt hook for automatic rule generation (BEWARE!)

## Requirements: 

* python version 3.11.3

## Disclaimer: 
This utility provides command and control ability over a computer or server using text, audio, or files as input. There is no authentication or authorization to 
determine if a message should be ingested if it is received. Use at your own risk and always validate the rules or actions used before executing. 

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
After loading the configuration file, Hermes begins watching for messages. Messages can come from users text input, 
users audio input, or files named {sysame}.txt message directory. When a message intended for the system is identified, 
Hermes will ingest the message, look for matching patterns in the configured rules, executes the configured actions,
and log everything to a new file in the history directory.

__IMPORTANT: Hermes is not responsible for placing the message file into the message directory in the correct format. This feature is 
built in to allow creating messages on one machine and syncing them with a backend solution such as dropbox, onedrive, or nextcound. 
If using files for messages, placing the file in the right location with the right content is the responsibility of the user__ 


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
