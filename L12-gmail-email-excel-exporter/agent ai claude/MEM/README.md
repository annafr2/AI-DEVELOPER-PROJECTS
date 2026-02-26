# MEM (Mail Excel Manager)

Gmail OAuth integration system that fetches emails and exports them to Excel, with MCP server support for Claude AI integration.

## Project Structure

```
agent ai claude/
├── MEM/                    # Documentation folder
│   ├── PLANNING.md         # Architecture and design
│   ├── TASKS.md            # Implementation tasks
│   ├── TASK.md             # Tasks (alternate)
│   ├── TEST.md             # Test plan
│   └── CLAUDE.md           # Claude integration guide
│
├── gmail_auth.py           # Gmail OAuth authentication
├── email_fetcher.py        # Email search and parsing
├── excel_handler.py        # Excel export functionality
├── main.py                 # CLI application
├── mcp_server.py           # MCP server for Claude
├── requirements.txt        # Python dependencies
└── .gitignore             # Git ignore rules
```

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Authenticate with Gmail
```bash
python main.py --auth
```

### 3. Fetch Emails
```bash
python main.py --query "is:inbox" --max 10
```

### 4. Start MCP Server for Claude
```bash
python mcp_server.py
```

## Documentation

All detailed documentation is in the `MEM/` folder:
- **MEM/PLANNING.md** - Project architecture
- **MEM/TASKS.md** - Implementation roadmap
- **MEM/TEST.md** - Testing strategy
- **MEM/CLAUDE.md** - Claude integration guide

## Requirements

- Python 3.8+
- Gmail API credentials (credentials.json)
- See requirements.txt for Python packages
