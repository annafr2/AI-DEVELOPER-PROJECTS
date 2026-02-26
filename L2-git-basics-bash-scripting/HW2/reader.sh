#!/bin/bash

# Log file
LOG_FILE="time.log"

# Infinite loop
while true; do
    # Check if log exists
    if [ -f "$LOG_FILE" ]; then
        # Read last line from log
        last_time=$(tail -n 1 "$LOG_FILE" 2>/dev/null)
        
        if [ -n "$last_time" ]; then
                 echo "[$(date '+%H:%M:%S')] READER.sh - Last time in log: $last_time"
       
        fi
    fi
    
    # Wait 7 seconds
    sleep 7
done