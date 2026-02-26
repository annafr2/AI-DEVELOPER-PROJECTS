# How to Run the Multi-Agent Translation Turing Machine

## Setup (One-time)

### 1. Install Python dependencies
```bash
pip install anthropic python-dotenv
```

### 2. Set up your API key
Create a file called `.env` in this directory:
```bash
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

## Running the Agents

### Quick Start (10 sentences)
```bash
python3 run_agents.py
```

### Run with custom number of sentences
```bash
python3 run_agents.py 5      # 5 sentences
python3 run_agents.py 50     # 50 sentences
python3 run_agents.py 100    # 100 sentences (full experiment)
```

## How It Works

```
┌─────────────────────────────────────────────────┐
│  Agent 4 (Orchestrator)                         │
│  - Generates English sentences                  │
│  - Starts the translation chain                 │
│  - Compares original vs final                   │
│  - Calculates cosine distance                   │
└──────────────┬──────────────────────────────────┘
               │
               │ Calls with English text
               ▼
┌──────────────────────────────────────────────────┐
│  Agent 1: EN → RU                                │
│  Translates English to Russian                   │
└──────────────┬───────────────────────────────────┘
               │
               │ Calls with Russian text
               ▼
┌──────────────────────────────────────────────────┐
│  Agent 2: RU → HE                                │
│  Translates Russian to Hebrew                    │
└──────────────┬───────────────────────────────────┘
               │
               │ Calls with Hebrew text
               ▼
┌──────────────────────────────────────────────────┐
│  Agent 3: HE → EN                                │
│  Translates Hebrew back to English               │
└──────────────┬───────────────────────────────────┘
               │
               │ Returns English text
               ▼
         Back to Agent 4
         (compares & calculates distance)
```

## Output

Results are saved to: `results/agent_results.json`

Contains:
- Summary statistics (avg, min, max distance)
- All sentences with their translations and distances
- Top degraded sentences

## Test Individual Agents

```bash
python3 agent1.py    # Test Agent 1 alone
python3 agent2.py    # Test Agent 2 alone
python3 agent3.py    # Test Agent 3 alone
python3 agent4.py    # Test Agent 4 (runs full experiment)
```

## Troubleshooting

**Error: "ANTHROPIC_API_KEY not found"**
- Make sure you created `.env` file with your API key

**Error: "No module named 'anthropic'"**
- Run: `pip install anthropic python-dotenv`

**Taking too long?**
- Start with fewer sentences: `python3 run_agents.py 3`
- Each sentence requires 4 API calls (generate + 3 translations)
