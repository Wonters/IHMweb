#!/bin/bash

echo "starting scheduler.py as deamon..."
screen -S acbbs python scheduler.py
echo "Enter : \"screen -x acbbs\" to see progression"
