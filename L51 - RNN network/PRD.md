# PRD — L51: How Much Does an RNN Remember?
## A Memory Experiment on Language Modeling

---

### Goal
Build a vanilla RNN language model and run 3 structured experiments to understand:
- What RNNs are good at
- Where they fail (and why)
- How hyperparameters affect the result

---

### Problem Statement
RNNs process sequences word by word, keeping a "memory" in their hidden state.
But this memory degrades for long sequences — a fundamental limitation called the **vanishing gradient problem**.

This project makes that limitation visible with numbers, graphs, and generated text.

---

### Dataset
| Property | Value |
|----------|-------|
| Source | Brown Corpus (NLTK) |
| Size | ~1 million words |
| Vocabulary | 10,000 most common words + 3 special tokens |
| Max sequences | 100,000 training sequences (sliding window) |
| Split | 80% training, 20% final test (never seen during training) |

**Why Brown corpus instead of Penn Treebank?**
The full PTB requires a paid license. The Brown corpus is freely available via NLTK,
has ~1M words, and is equally good for demonstrating RNN behavior.

---

### The 3 Experiments

#### Experiment 1 — Short Sentences (seq_len = 5)
> "How much can an RNN learn from just 5 words?"

- Train RNN on 5-word sequences
- Expected: low perplexity, good accuracy, clean convergence curves
- Output: `outputs/exp_short_training.png`

#### Experiment 2 — Long Sentences (seq_len = 15)
> "What happens when the sentence gets longer?"

- Train the same RNN on 15-word sequences
- Expected: noticeably higher perplexity, lower accuracy
- Why: gradients must travel back through 15 steps and vanish along the way
- Output: `outputs/exp_long_training.png`

Both experiments compared: `outputs/experiment_comparison.png`

#### Experiment 3 — Text Generation
> "What does the trained RNN imagine when given one seed word?"

- Feed one seed word, sample next word, repeat 20 times
- Uses temperature softmax: temperature=0.8 (slightly conservative)
- Seed words: "the", "a", "he", "she", "they", "in", "it"
- Expected: mix of plausible and nonsensical output — both are educational
- Output: `outputs/generation_results.png`

---

### Parameter Sweep — The WOW Factor
Train 27 model variants by changing:

| Parameter | Values |
|-----------|--------|
| Hidden size | 64, 128, 256 |
| Number of RNN layers | 1, 2, 3 |
| Sequence length | 5, 10, 20 |

Results displayed as a **3-panel heatmap** (one panel per layer count):
- X-axis: sequence length
- Y-axis: hidden size
- Color: final validation perplexity (green = smart, red = confused)

Output: `outputs/parameter_sweep.png`

---

### Model Architecture
```
Input tokens → Embedding(10000, 128) → nn.RNN(tanh) → Dropout → Linear(128, 10000) → Logits
```
- Loss: CrossEntropyLoss (predict next word)
- Optimizer: Adam, lr=0.001, StepLR scheduler
- Gradient clipping: norm=5.0

**Why vanilla RNN and not LSTM?**
LSTMs were invented specifically to fix vanishing gradients. Using plain RNN lets us
observe the problem directly — that is the educational point of Experiment 2.

---

### Success Criteria
| Metric | Target |
|--------|--------|
| Exp 1 val_perplexity | < 200 |
| Exp 2 val_perplexity | Visibly higher than Exp 1 |
| Text generation | At least 3 seeds produce grammatically plausible output |
| Sweep | Clear trend: larger hidden + shorter seq = lower perplexity |

---

### Tech Stack
- Python 3.10+
- PyTorch 2.0+ (nn.RNN, Adam, CrossEntropyLoss)
- NLTK (Brown corpus)
- Matplotlib (visualizations — dark theme)
- No external ML frameworks beyond PyTorch
