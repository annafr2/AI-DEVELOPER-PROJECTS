# Log Writer and Reader Scripts

## Files:
- `writer.sh` - Writes current time to log every 10 seconds
- `reader.sh` - Reads and displays last time from log every 7 seconds

## Setup:
```bash
chmod +x writer.sh reader.sh
```

## Running the scripts:
```bash
# Start both scripts in background
./writer.sh &
./reader.sh &
```

## Managing processes:
```bash
# View running processes
jobs

# Bring to foreground
fg %1    # writer
fg %2    # reader

# Send to background (after Ctrl+Z)
bg

# Stop processes
kill %1 %2
# or
killall writer.sh reader.sh
```

## Output:
- **writer.sh** creates `time.log` file with entries like: `WRITER.SH WRITE- 2025-09-15 14:30:15`
- **reader.sh** displays: `[14:30:22] READER- Last time in log: WRITER.SH WRITE- 2025-09-15 14:30:15`