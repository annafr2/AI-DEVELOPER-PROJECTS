#!/bin/bash

# Log file
LOG_FILE="time.log"

# Clear old log if exists
> "$LOG_FILE"

# Infinite loop
while true; do
    # Write current time to log
     echo "WRITER.SH - $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"
    # Wait 10 seconds
    sleep 10
done