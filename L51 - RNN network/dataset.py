import torch
from torch.utils.data import Dataset, DataLoader, random_split
import nltk
from collections import Counter
from config import VOCAB_SIZE, TRAIN_RATIO, BATCH_SIZE, MAX_SEQUENCES

SPECIAL_TOKENS = ["<PAD>", "<UNK>", "<EOS>"]


def load_corpus():
    """Load Brown corpus from NLTK (~1M words, free, no authentication needed)."""
    nltk.download("brown", quiet=True)
    from nltk.corpus import brown
    words = [w.lower() for w in brown.words()]
    print(f"  Corpus loaded: {len(words):,} words")
    return words


def build_vocab(words, vocab_size=VOCAB_SIZE):
    """Build word <-> index mappings from the most common words."""
    counter = Counter(words)
    most_common = counter.most_common(vocab_size - len(SPECIAL_TOKENS))
    vocab = SPECIAL_TOKENS + [w for w, _ in most_common]
    word2idx = {w: i for i, w in enumerate(vocab)}
    idx2word = {i: w for i, w in enumerate(vocab)}
    print(f"  Vocabulary size: {len(vocab):,} words")
    return word2idx, idx2word, vocab


def encode_words(words, word2idx):
    unk = word2idx["<UNK>"]
    return [word2idx.get(w, unk) for w in words]


class SequenceDataset(Dataset):
    """Creates (input, target) pairs: target is input shifted by 1 word."""

    def __init__(self, tokens, seq_len, max_sequences=MAX_SEQUENCES):
        self.data = []
        stride = max(1, seq_len // 2)
        for i in range(0, len(tokens) - seq_len - 1, stride):
            x = torch.tensor(tokens[i:i + seq_len], dtype=torch.long)
            y = torch.tensor(tokens[i + 1:i + seq_len + 1], dtype=torch.long)
            self.data.append((x, y))
            if len(self.data) >= max_sequences:
                break
        print(f"  Sequences created: {len(self.data):,} (seq_len={seq_len})")

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]


def get_dataloaders(seq_len, batch_size=BATCH_SIZE):
    """Return train/val DataLoaders, vocab mappings, and vocab size."""
    words = load_corpus()
    word2idx, idx2word, vocab = build_vocab(words)
    tokens = encode_words(words, word2idx)

    # 80% training, 20% held as final test (never seen during training)
    split = int(len(tokens) * TRAIN_RATIO)
    train_tokens = tokens[:split]

    dataset = SequenceDataset(train_tokens, seq_len)
    n_val = max(1, int(len(dataset) * 0.1))
    n_train = len(dataset) - n_val
    train_ds, val_ds = random_split(dataset, [n_train, n_val])

    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False, num_workers=0)
    print(f"  Train batches: {len(train_loader):,} | Val batches: {len(val_loader):,}")
    return train_loader, val_loader, word2idx, idx2word, len(vocab)


def get_test_tokens():
    """Returns the 20% held-out test tokens for final evaluation."""
    words = load_corpus()
    word2idx, idx2word, _ = build_vocab(words)
    tokens = encode_words(words, word2idx)
    split = int(len(tokens) * TRAIN_RATIO)
    return tokens[split:], word2idx, idx2word
