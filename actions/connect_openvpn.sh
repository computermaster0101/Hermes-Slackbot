#!/bin/bash

echo connecting openvpn please wait
cd ~/.ovpn
sudo openvpn ~/.ovpn/openvpnclient.conf
echo vpn disconnected
read -n 1 -s -r -p "Press any key to continue"