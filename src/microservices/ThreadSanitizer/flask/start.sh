#!/bin/bash

docker pull racedetection/rds:tsan-tool
cd /flask && python3 server.py
