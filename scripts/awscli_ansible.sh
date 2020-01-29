#!/bin/bash

#install python 3 & pip
sudo apt update
sudo apt install -y python3 python3-pip

#install awscli, ansible and boto3 dependencies
pip3 install --user --upgrade ansible awscli boto3

#add ansible to the path so anisble-playbook commands can be executed
echo 'PATH=$PATH:~/.local/bin' >> ~/.bashrc
source ~/.bashrc
