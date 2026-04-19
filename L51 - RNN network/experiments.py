import torch
from dataset import get_dataloaders, get_test_tokens
from model import create_model
from train import train_model, evaluate_test
from generate import generate_multiple
from visualize import plot_training, plot_comparison, plot_sweep, plot_generation
from config import (EXPERIMENTS, SWEEP_HIDDEN_SIZES, SWEEP_NUM_LAYERS,
                    SWEEP_SEQ_LENS, SWEEP_EPOCHS, SEED_WORDS)


def run_experiment(name, device):
    cfg = EXPERIMENTS[name]
    print(f"\n{'='*55}")
    print(f"  Experiment: {cfg['label']}")
    print(f"  {cfg['desc']}")
    print(f"{'='*55}")

    train_loader, val_loader, word2idx, idx2word, vocab_size = get_dataloaders(cfg["seq_len"])
    model = create_model(vocab_size).to(device)
    print(f"  Parameters: {model.count_parameters():,}")

    history = train_model(model, train_loader, val_loader, device)
    plot_training(history, f"Experiment: {cfg['label']}", cfg["color"], f"exp_{name}_training.png")
    return history, model, word2idx, idx2word


def run_all_experiments(device):
    results, models, word_maps = {}, {}, {}
    for name in EXPERIMENTS:
        history, model, w2i, i2w = run_experiment(name, device)
        results[name] = history
        models[name] = model
        word_maps[name] = (w2i, i2w)
    plot_comparison(results)
    return results, models, word_maps


def run_generation(model, word2idx, idx2word, device):
    print(f"\n{'='*55}")
    print("  Experiment 3: Text Generation")
    print("  Seeding the RNN and watching it dream...")
    print(f"{'='*55}")
    generated = generate_multiple(model, word2idx, idx2word, SEED_WORDS, device=device)
    for seed, text in generated.items():
        print(f"  [{seed}] {text}")
    plot_generation(generated)
    return generated


def run_final_test(model, seq_len, device):
    """Evaluate the trained model on the 20% test tokens held out from the start."""
    print(f"\n{'='*55}")
    print("  Final Test — The 20% We Saved for the End")
    print(f"{'='*55}")
    test_tokens, _, _ = get_test_tokens()
    evaluate_test(model, test_tokens, seq_len, device)


def run_sweep(device):
    """Train 27 models (3 hidden x 3 layers x 3 seq_lens) and plot the results."""
    print(f"\n{'='*55}")
    print("  Parameter Sweep (27 configurations)")
    print(f"{'='*55}")
    sweep_results = {}
    combos = [(h, nl, s)
              for s in SWEEP_SEQ_LENS
              for nl in SWEEP_NUM_LAYERS
              for h in SWEEP_HIDDEN_SIZES]

    cached_loaders = {}
    for i, (h, nl, s) in enumerate(combos, 1):
        if s not in cached_loaders:
            tr, vl, _, _, vs = get_dataloaders(s)
            cached_loaders[s] = (tr, vl, vs)
        tr, vl, vs = cached_loaders[s]
        key = f"h{h}_l{nl}_s{s}"
        print(f"  [{i:2d}/{len(combos)}] {key}")
        m = create_model(vs, hidden_size=h, num_layers=nl).to(device)
        hist = train_model(m, tr, vl, device, epochs=SWEEP_EPOCHS)
        sweep_results[key] = {
            "final_val_ppl": hist["val_ppl"][-1],
            "final_val_acc": hist["val_acc"][-1],
        }

    plot_sweep(sweep_results)
    return sweep_results
