#!/bin/bash

sudo apt update

sudo pip3 install hashlib
sudo pip3 install socket
sudo pip3 install json
sudo pip3 install multiprocessing
sudo pip3 install math

sudo python3 client.py $1