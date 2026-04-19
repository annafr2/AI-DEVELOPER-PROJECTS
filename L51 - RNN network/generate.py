import torch
import numpy as np
from config import GENERATE_LENGTH, TEMPERATURE, SEED_WORDS


def generate_text(model, word2idx, idx2word, seed_word,
                  length=GENERATE_LENGTH, temperature=TEMPERATURE, device="cpu"):
    """
    Generate a sequence of words by sampling from the RNN one step at a time.
    temperature > 1 = more random, temperature < 1 = more conservative.
    """
    model.eval()
    unk_idx = word2idx.get("<UNK>", 1)
    start_idx = word2idx.get(seed_word.lower(), unk_idx)

    generated = [seed_word]
    x = torch.tensor([[start_idx]], dtype=torch.long, device=device)
    hidden = model.init_hidden(1, device)

    with torch.no_grad():
        for _ in range(length - 1):
            logits, hidden = model(x, hidden)
            logits = logits[0, -1, :] / max(temperature, 1e-6)
            probs = torch.softmax(logits, dim=-1).cpu().numpy().astype(np.float64)
            probs = probs / probs.sum()  # renormalize for numerical stability
            next_idx = int(np.random.choice(len(probs), p=probs))
            next_word = idx2word.get(next_idx, "<UNK>")
            generated.append(next_word)
            x = torch.tensor([[next_idx]], dtype=torch.long, device=device)

    return " ".join(generated)


def generate_multiple(model, word2idx, idx2word, seeds=SEED_WORDS, device="cpu"):
    """Generate text for a list of seed words."""
    results = {}
    for seed in seeds:
        if seed in word2idx:
            results[seed] = generate_text(model, word2idx, idx2word, seed, device=device)
        else:
            results[seed] = f"(word '{seed}' not in vocabulary)"
    return results
