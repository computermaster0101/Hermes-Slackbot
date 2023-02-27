#!/bin/bash
message=$1

#read -n 1 -s -r -p "Press any key to continue"

## identify pattern for ticket numbers
regexIp='[0-9]{2,3}'
if [[ "${message}" =~ ${regexIp} ]]; then
    number=${BASH_REMATCH[0]}
    ticket=("${number}")
fi
number=${BASH_REMATCH[0]}
ticket=("${number}")
gnome-www-browser https://example.atlassian.net/browse/MF-${ticket}