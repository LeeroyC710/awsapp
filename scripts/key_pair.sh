#!/bin/bash

#make sure ssh folder exists with the correct permissions
mkdir -p ~/.ssh && chmod 700 $_

#set the key pair name
key_name="CloudFormationKeyPair"

#create a key pair 
aws ec2 create-key-pair --key-name ${key_name} --query 'KeyMaterial' --output text > ~/.ssh/${key_name}.pem

#make sure the private key has the correct permissions
chmod 600 ~/.ssh/${key_name}.pem
