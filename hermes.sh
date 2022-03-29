#!/bin/bash
#install jq if its not installed
if ! [ $(which jq) ]; then sudo apt -y install jq || exit; fi
#set file paths. this should be pulled from options file but i've had some issues
messageFile=~/OneDrive/Apps/Commands/$1.txt
history=~/OneDrive/Apps/Commands/history
appDirectory=~/OneDrive/Apps/Hermes
rulesFolder=~/OneDrive/Apps/Hermes/rules
#if a message exists process it
if [ -f ${messageFile} ]; then
  #read the message
  device=$(jq '.device' ${messageFile})
  message=$(jq '.message' ${messageFile})
  timestamp=$(jq '.timestamp' ${messageFile})
  #display the message
  echo Device: ${device}
  echo Message: ${message}
  echo Timestamp: ${timestamp}
  ## for each rule file
  for rule in ${rulesFolder}/*.json
  do
    ## read the patterns
    (jq '.patterns[]' ${rule}) | while IFS='' read pattern;
    do
      ## compare the message to each pattern
      if [[ ${message} =~ ${pattern} ]]; then
        active=$(jq '.active' ${rule})
        ## if the pattern is matched display the rule
        echo
        echo Rule: ${rule}
        echo Pattern: ${pattern}
        echo Active: ${active}
        echo
        if (${active}); then
          ## read the rule
          runningDirectory=$(jq -r '.runningDirectory' ${rule})
          runAsAdmin=$(jq -r '.runAsAdmin' ${rule})
          passMessage=$(jq -r '.passMessage' ${rule})
          echo Run Directory=${runningDirectory}
          echo Run As Admin=${runAsAdmin}
          echo Pass Message=${passMessage}
          echo
          ## cd to the running directory
          cd ${runningDirectory/#~/$HOME}
          ## read the actions
          (jq -r '.actions[]' ${rule}) | while IFS='' read action
          do
            ## execute the action
            if (${runAsAdmin}) && (${passMessage}); then
              echo Action: sudo ${action} ${message}
              $(gnome-terminal -- sudo ${action} "${message}")
            elif (${passMessage}); then
              echo Action: ${action} ${message}
              $(gnome-terminal -- ${action} "${message}")
            elif (${runAsAdmin}); then
              echo Action: sudo ${action}
              $(gnome-terminal -- sudo ${action})
            else
              echo Action: ${action}
              $(gnome-terminal -- ${action})
            fi
          done
        else
            echo Rule is not active.
        fi
      fi
    done
  done
  ## cd back to the application directory
  cd ${appDirectory}
  ## backup the message
  mkdir -p ${history}
  mv ${messageFile} ${history}/${messageFile##*/}.$(date +"%Y%m%d%H%M%S")
  ## ToDo: Add rule data / status to the history message
fi
sleep 1s
