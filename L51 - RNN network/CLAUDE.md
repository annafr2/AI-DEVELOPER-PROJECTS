# CLAUDE.md — L51: How Much Does an RNN Remember?

## Project Summary
Vanilla RNN language model experiments on the Brown corpus (~1M words, NLTK).
Three structured experiments: short sequences, long sequences (vanishing gradient), text generation.
Topped with a 27-model parameter sweep plotted as a heatmap.

## File Architecture

| File | Purpose | Lines |
|------|---------|-------|
| `config.py` | All hyperparameters and experiment configurations | ~55 |
| `dataset.py` | Load Brown corpus, build 10k vocab, create 100k sequences | ~75 |
| `model.py` | Vanilla RNN language model (nn.RNN, not LSTM/GRU) | ~55 |
| `train.py` | Training loop: loss, accuracy, perplexity | ~70 |
| `generate.py` | Temperature-based text generation from seed words | ~45 |
| `visualize.py` | All matplotlib plots, saved to outputs/ | ~130 |
| `experiments.py` | Orchestrate the 3 experiments + parameter sweep | ~80 |
| `main.py` | CLI entry point | ~55 |

## Rules
- All Python files: max 150 lines (enforced)
- All code, comments, prints: English only
- Outputs saved as .png to outputs/
- No emojis in code or docs

## Key Design Decisions
- **Brown corpus, not PTB**: freely available via NLTK, ~1M words, comparable quality
- **Vanilla nn.RNN**: chosen intentionally over LSTM/GRU to expose vanishing gradient
- **80/20 split**: 80% used for training, 20% held as a final test set (never seen during training)
- **MAX_SEQUENCES = 100,000**: capped to keep training manageable on CPU
- **Parameter sweep is optional**: `--no-sweep` flag skips it (~30-40 min saved)

## Running
```bash
pip install -r requirements.txt
python main.py             # full run including parameter sweep
python main.py --no-sweep  # faster, skips the 27-model sweep
python main.py --device cpu
```

## Output Files
| File | What it shows |
|------|--------------|
| `outputs/exp_short_training.png` | Experiment 1: loss / acc / perplexity curves |
| `outputs/exp_long_training.png` | Experiment 2: same metrics, visibly worse |
| `outputs/experiment_comparison.png` | Short vs Long perplexity showdown |
| `outputs/generation_results.png` | RNN-generated text from 7 seed words |
| `outputs/parameter_sweep.png` | 3x3x3 parameter map heatmap |
