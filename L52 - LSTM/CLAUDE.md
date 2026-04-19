# CLAUDE.md — L52 LSTM Signal Filter

## Project Summary
An LSTM neural network that filters a chosen frequency from a noisy mixed signal.

## File Map

| File            | Role                                                    |
|-----------------|---------------------------------------------------------|
| `config.py`     | All hyperparameters — change things here only           |
| `signals.py`    | Generate 4 sinusoids (clean + noisy)                    |
| `dataset.py`    | Sliding-window dataset and DataLoaders                  |
| `model.py`      | LSTMFilter nn.Module definition                         |
| `train.py`      | Training loop, evaluation, model saving                 |
| `visualize.py`  | 5 PNG visualizations → outputs/                         |
| `main.py`       | Entry point — runs everything in order                  |

## How to Run
```bash
python main.py
```

## Key Config Parameters to Experiment With

| Parameter          | Location in config.py    | Effect                            |
|--------------------|--------------------------|-----------------------------------|
| `TARGET_FREQ_HZ`   | line 17                  | Which frequency to filter (1/3/5/7) |
| `AMP_NOISE_STD`    | line 13                  | How noisy the amplitude is        |
| `PHASE_NOISE_STD`  | line 16                  | How noisy the phase is            |
| `WINDOW_SIZE`      | line 20                  | Context window length             |
| `HIDDEN_SIZE`      | line 24                  | LSTM capacity                     |
| `EPOCHS`           | line 29                  | Training duration                 |

## Code Rules
- Each Python file <= 150 lines
- All code, comments, and prints in English
- Visualizations saved as .png to outputs/
- No emojis in code or docs
