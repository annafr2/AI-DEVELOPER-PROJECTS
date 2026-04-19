# How Much Does an RNN Remember?
### A Memory Experiment on Language Modeling

We train a small AI brain to predict the next word in a sentence.
Then we push it to its limits — and watch it struggle.

---

## What is an RNN?

Imagine reading a book, one word at a time.
After each word, your brain remembers a little of what came before.
An **RNN** (Recurrent Neural Network) works the same way.

It reads words one by one, keeps a tiny "memory" in numbers,
and tries to guess what word comes next.

The tricky part? The memory fades. The longer the sentence, the more it forgets.

---

## The Dataset

We use the **Brown Corpus** — about **1 million English words** from news, stories, and more.
It is free and comes with the NLTK library.

- Vocabulary: **10,000 most common words**
- Training sequences: **100,000**
- Split: **80% for training**, 20% kept secret until the very end

---

## The 3 Experiments

### Experiment 1 — Short Sentences (5 words)
**Question:** "Can the RNN learn from just 5 words?"

We train on short sequences like:
> "the man walked to the"

**Result:** The RNN does well. Low perplexity, good accuracy, clean learning curves.

See the results:
**[exp_short_training.png](outputs/exp_short_training.png)**
- 3 panels: Loss going down, Accuracy going up, Perplexity going down
- All good signs!

---

### Experiment 2 — Long Sentences (15 words)
**Question:** "What happens when the sentence gets longer?"

We train on longer sequences like:
> "the man who used to live in the house next to the market"

**Result:** The RNN struggles. The perplexity is higher, accuracy is lower.

Why? Because of the **Vanishing Gradient Problem**.
When the sentence is 15 words long, the learning signal has to travel backward through 15 steps.
By the time it reaches the beginning of the sentence, it has nearly disappeared.
The RNN simply forgets what it learned from early words.

See the results:
**[exp_long_training.png](outputs/exp_long_training.png)**

See the side-by-side comparison of both experiments:
**[experiment_comparison.png](outputs/experiment_comparison.png)**
- The short curve is lower (better)
- The long curve is higher and choppier
- This is the vanishing gradient, visible in a picture

---

### Experiment 3 — Text Generation
**Question:** "What does the RNN imagine when given one seed word?"

We give the RNN a single word, and it keeps predicting the next word, 20 times in a row.

Examples:
- `"the"` → ...
- `"she"` → ...
- `"they"` → ...

Some sentences will make sense. Some will be funny nonsense. Both are interesting!
The nonsense tells us where the RNN's memory runs out.

See all 7 generated texts:
**[generation_results.png](outputs/generation_results.png)**

---

## The WOW Factor — Parameter Map

We trained **27 different versions** of the RNN by changing three things:

| Setting | Options |
|---------|---------|
| Hidden size (brain size) | 64, 128, 256 |
| Number of layers | 1, 2, 3 |
| Sentence length | 5, 10, 20 words |

The result is a color map. **Green = smart (low perplexity). Red = confused (high perplexity).**

**[parameter_sweep.png](outputs/parameter_sweep.png)**

What to look for:
- Bigger brain (hidden=256) is usually greener
- Longer sentences (seq=20) tend to be redder
- More layers helps — up to a point

---

## How to Run

```bash
# Install requirements
pip install -r requirements.txt

# Full run (includes the 27-model sweep, takes ~3 hours on CPU)
python main.py

# Faster run — skips the sweep, ~10-15 minutes
python main.py --no-sweep
```

---

## Outputs Explained

Here is a simple explanation of every image generated during the run:

### 1. [exp_short_training.png](outputs/exp_short_training.png)
- **What is in the image:** Three training graphs (Loss, Accuracy, and Perplexity) for the short-sentences experiment (5 words).
- **Explanation:** The lines for training and validation are very close together, which means the model learns well without simply memorizing the data. The Perplexity (which measures confusion) goes down nicely to around 130-140. Overall, it shows the RNN easily masters learning from short sentences.

### 2. [exp_long_training.png](outputs/exp_long_training.png)
- **What is in the image:** The same three graphs, but for the long-sentences experiment (15 words).
- **Explanation:** The shape of the graphs is similar to the short experiment, but the final results are worse. The Perplexity only drops to around 160. This means the model struggles more to predict words accurately when the sentences get longer.

### 3. [experiment_comparison.png](outputs/experiment_comparison.png)
- **What is in the image:** A direct comparison between the "Short" (green line) and "Long" (red line) models.
- **Explanation:** The green line clearly beats the red line by reaching a lower perplexity (132.7 vs 156.4). This visually proves the **Vanishing Gradient Problem**. The RNN forgets the beginning of a 15-word sentence because the network struggles to pass memory backward across so many steps.

### 4. [generation_results.png](outputs/generation_results.png)
- **What is in the image:** Next-word predictions generated by the AI after we give it just one starting word (like "he", "she", or "it").
- **Explanation:** The AI manages to create text that looks like English with proper grammar structures (like placing nouns after "a"). However, the sentences make no logical sense. You will also see many `<UNK>` tags, which stand for "Unknown" — these are words that were too rare to be included in the AI's 10,000-word vocabulary.

### 5. [parameter_sweep.png](outputs/parameter_sweep.png)
- **What is in the image:** A colorful map (heatmap) comparing 27 different model setups. Green blocks mean the model performed great (low perplexity).
- **Explanation:** 
  - **Short sequences win:** The left columns (seq=5) are greener, proving shorter sequences are easier to learn.
  - **Wider is better:** Rows with a larger "brain" (hidden size of 256) almost always beat rows with 64 or 128.
  - **Fewer layers actually helped:** Surprisingly, the 1-layer RNN models outperformed the complicated 3-layer models. The absolute best model on the board was 1-layer, hidden size 256, and sequence length 5 (getting the best score of 126).

---

## Project Files

| File | What it does |
|------|-------------|
| `config.py` | All settings (vocab size, epochs, hidden size...) |
| `dataset.py` | Loads text, builds vocabulary, creates sequences |
| `model.py` | The RNN brain |
| `train.py` | Teaching the brain |
| `generate.py` | Making the brain write sentences |
| `visualize.py` | Drawing all the graphs |
| `experiments.py` | Running all 3 experiments + the sweep |
| `main.py` | Start here |

---

## What We Learned

1. RNNs learn short sequences very well — low perplexity, good accuracy
2. Long sequences are hard — the gradient vanishes before reaching the start
3. Bigger hidden size helps, but has diminishing returns
4. More layers help with short sequences but can hurt on very long ones
5. Text generation is creative — sometimes poetic, sometimes random

---

## Why Not Use LSTM?

LSTM (Long Short-Term Memory) was invented specifically to fix the vanishing gradient problem.
Using plain RNN here is intentional — we want to **see** the problem, not hide it.
Once you understand why RNN fails, you understand why LSTM was invented.
