# Multi-Agent Translation Turing Machine

## Project Status: ✅ COMPLETED

## Project Overview
This project implements a multi-agent "Turing Machine" that tests the degradation of meaning through sequential machine translations across different languages.

## Architecture
The system consists of 3 translation agents orchestrated by the main script:
1. **Agent 1 (EN→RU)**: Translates English to Russian
2. **Agent 2 (RU→HE)**: Translates Russian to Hebrew
3. **Agent 3 (HE→EN)**: Translates Hebrew back to English
4. **run_agents.py**: Orchestrator that generates sentences, coordinates translations, and analyzes results

## Flow
```
run_agents.py (Generate) → Agent 1 (EN→RU) → Agent 2 (RU→HE) → Agent 3 (HE→EN) → run_agents.py (Analysis)
```

## Implementation Details
- **LLM Model**: Claude 4.5 (claude-sonnet-4-5-20250929)
- **API**: Anthropic API
- **Vector Representation**: Character frequency vectors
- **Distance Metric**: Cosine distance (1 - cosine similarity)
- **Visualization**: matplotlib bar chart with average line

## Analysis Metrics
- **Cosine Vector Distance**: Measures semantic similarity between original and final sentences
- **Average Error**: Average cosine distance across all sentences
- **Visualization**: Bar graph showing distance per sentence with average line
- **Detailed Output**: Shows all sentence pairs with their distances

## Technical Stack
- **Python 3.12+**
- **Anthropic API**: Claude 4.5 for translations
- **Vector Similarity**: Character frequency-based cosine distance
- **Visualization**: matplotlib for graphing
- **Environment**: python-dotenv for API key management

## Project Structure
```
L13/
├── agent1.py          # English → Russian translator
├── agent2.py          # Russian → Hebrew translator
├── agent3.py          # Hebrew → English translator
├── run_agents.py      # Main orchestrator + analysis
├── requirements.txt   # Python dependencies
├── .env.example       # Example environment variables
├── .gitignore        # Git ignore rules
└── results/          # Output directory (generated)
    ├── agent_results.json           # JSON results
    └── translation_degradation.png  # Visualization
```

## Completed Stages
### ✅ Stage 1: Core NLP Foundation
- Implemented character frequency vectorization
- Implemented cosine distance calculation
- Tested with sample sentences

### ✅ Stage 2: Translation Agents
- Built Agent 1 (EN→RU translator)
- Built Agent 2 (RU→HE translator)
- Built Agent 3 (HE→EN translator)
- Built orchestrator in run_agents.py (sentence generation + coordination)

### ✅ Stage 3: Integration & Analysis
- Orchestrator coordinates all 3 translation agents
- Process any number of sentences through pipeline
- Calculate cosine distances
- Generate bar chart visualization
- Output detailed results to console and JSON

## Success Criteria - ALL MET ✅
- ✅ System successfully processes sentences through all translation stages
- ✅ Cosine distances are accurately calculated
- ✅ Clear visualization of translation degradation (bar chart)
- ✅ Average error metric is computed and reported
- ✅ Detailed sentence comparison in console output
