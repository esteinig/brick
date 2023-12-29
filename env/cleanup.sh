#!/bin/bash

# Directory to check
DIR="$WORK_DIRECTORY"

if [ ! -d "$DIR" ]; then
    echo "Could not find directory in"
    exit 1
fi

# Infinite loop to run the cleaning task every 24 hours
while true; do
    # Delete directories older than 24 hours
    find "$DIR" -mindepth 1 -maxdepth 1 -type d -mmin +1440 -exec rm -rf {} \;

    # Wait for 24 hours (86400 seconds) before next run
    sleep 86400
done
