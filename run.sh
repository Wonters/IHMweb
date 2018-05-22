#!/bin/bash

echo "starting scheduler.py as deamon..."
screen -dmS acbbs python scheduler.py
echo "Enter : \"screen -x acbbs\" to see progression"
