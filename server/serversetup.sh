#!/bin/bash

sudo apt update

sudo pip3 install socket
sudo pip3 install json
sudo pip3 install multiprocessing
sudo pip3 install flask

sudo python3 server.py
