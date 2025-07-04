#!/bin/bash
# This script runs the bot in a loop, restarting on failure.

while true; do
    python start.py
    echo "Bot crashed with exit code $?. Restarting in 10 seconds..."
    sleep 10
done