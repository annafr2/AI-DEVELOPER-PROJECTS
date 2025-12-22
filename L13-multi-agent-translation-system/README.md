# Multi-Agent Translation Turing Machine

A Python-based experiment that demonstrates semantic degradation through sequential machine translations across multiple languages using Claude 4.5 AI.

## Overview

This project implements a multi-agent system that:
1. Generates English sentences
2. Translates them through a chain: English → Russian → Hebrew → English
3. Measures semantic degradation using cosine distance
4. Visualizes the results

## Features

- **Multi-Agent Architecture**: 4 specialized agents working in sequence
- **LLM-Powered Translations**: Uses Claude 4.5 for accurate translations
- **Semantic Analysis**: Calculates cosine distance between original and final sentences
- **Visual Results**: Generates bar charts showing translation degradation
- **Detailed Reports**: Console output with all sentence comparisons
- **JSON Export**: Saves results for further analysis

## Requirements

- Python 3.12+
- Anthropic API key (Claude 4.5 access)
- Virtual environment (recommended)

## Installation

1. **Clone the repository:**
```bash
cd L13
```

2. **Create and activate virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env and add your Anthropic API key:
# ANTHROPIC_API_KEY=your-key-here
```

## Usage

Run the experiment with a specified number of sentences:

```bash
python run_agents.py [number_of_sentences]
```

**Examples:**
```bash
# Run with 5 sentences
python run_agents.py 5

# Run with 10 sentences (default)
python run_agents.py

# Run with 100 sentences
python run_agents.py 100
```

## Output

The system generates:

1. **Console Output:**
   - Real-time translation progress
   - Summary statistics (avg, min, max distance)
   - Detailed sentence comparisons
   - Top 5 most degraded sentences

2. **Visual Output:**
   - `results/translation_degradation.png` - Bar chart visualization

3. **Data Export:**
   - `results/agent_results.json` - Complete results in JSON format

## Architecture

### Agent Flow
```
run_agents.py (Orchestrator)
    ↓ generates sentences
Agent 1 (EN→RU)
    ↓ translates to Russian
Agent 2 (RU→HE)
    ↓ translates to Hebrew
Agent 3 (HE→EN)
    ↓ translates back to English
run_agents.py (Analysis & Visualization)
```

### Components

- **agent1.py**: English → Russian translator
- **agent2.py**: Russian → Hebrew translator
- **agent3.py**: Hebrew → English translator
- **run_agents.py**: Main orchestrator (generates sentences, coordinates translations, analyzes results)

## How It Works

1. **Sentence Generation**: run_agents.py uses Claude 4.5 to generate diverse English sentences
2. **Translation Chain**: Each sentence passes through 3 translation agents (EN→RU→HE→EN)
3. **Vector Comparison**: Original and final sentences are converted to character frequency vectors
4. **Distance Calculation**: Cosine distance measures semantic drift
5. **Visualization**: Results are plotted and saved as a bar chart

## Example Results

```
Sentence 1:
  Distance: 0.0174
  Original: The ancient oak tree stood silent while autumn leaves danced...
  Final:    The ancient oak stood in silence, while the autumn leaves swirled...

Average cosine distance: 0.0145
```

## Technical Details

- **LLM Model**: claude-sonnet-4-5-20250929
- **Vector Method**: Character frequency vectors
- **Distance Metric**: Cosine distance (1 - cosine similarity)
- **Visualization**: matplotlib bar charts

## Project Structure

```
L13/
├── agent1.py              # EN→RU translator
├── agent2.py              # RU→HE translator
├── agent3.py              # HE→EN translator
├── agent4.py              # Orchestrator
├── run_agents.py          # Main script
├── requirements.txt       # Dependencies
├── .env.example          # Environment template
├── .gitignore            # Git ignore rules
├── README.md             # This file
├── CLAUDE.md             # Project documentation
├── HOW_TO_RUN.md         # Detailed instructions
├── PLANNING.md           # Planning notes
├── PRD.md                # Product requirements
├── TASKS.md              # Task breakdown
└── results/              # Generated output (not in git)
    ├── agent_results.json
    └── translation_degradation.png
```

## Notes

- The `results/` directory is auto-generated and excluded from git
- API costs depend on the number of sentences and translation length
- Character frequency vectors provide a simple but effective similarity measure

## License

Educational project - Free to use and modify

## Author

Created as part of a machine learning course exploring semantic degradation in machine translation.
