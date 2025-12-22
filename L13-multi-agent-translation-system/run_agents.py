"""
Multi-Agent Translation Turing Machine
Main orchestrator script that runs the translation experiment
"""

import os
import sys
import json
from anthropic import Anthropic
from dotenv import load_dotenv
from typing import List, Dict
import matplotlib.pyplot as plt

from agent1 import Agent1
from agent2 import Agent2
from agent3 import Agent3

load_dotenv()


def text_to_vector(text: str) -> dict:
    """Convert text to a simple character frequency vector"""
    text = text.lower()
    vector = {}
    for char in text:
        if char.isalnum() or char.isspace():
            vector[char] = vector.get(char, 0) + 1
    return vector


def cosine_distance(vec1: dict, vec2: dict) -> float:
    """Calculate cosine distance between two frequency vectors"""
    all_keys = set(vec1.keys()) | set(vec2.keys())
    dot_product = sum(vec1.get(k, 0) * vec2.get(k, 0) for k in all_keys)
    mag1 = sum(v ** 2 for v in vec1.values()) ** 0.5
    mag2 = sum(v ** 2 for v in vec2.values()) ** 0.5

    if mag1 == 0 or mag2 == 0:
        return 1.0

    similarity = dot_product / (mag1 * mag2)
    return 1.0 - similarity


def generate_sentences(client: Anthropic, count: int = 100) -> List[str]:
    """Generate diverse English sentences using Claude"""
    print(f"\nGenerating {count} sentences...")

    prompt = f"""Generate exactly {count} diverse English sentences for a translation experiment.

Requirements:
- Each sentence should be 5-20 words long
- Cover diverse topics: nature, technology, emotions, philosophy, daily life, science, art, etc.
- Use different sentence structures
- Make them meaningful and realistic
- One sentence per line
- DO NOT number them

Just output the sentences, one per line."""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}]
        )

        response = message.content[0].text.strip()
        sentences = [line.strip() for line in response.split('\n') if line.strip()]

        # Clean up any numbering that might have been added
        cleaned = []
        for sent in sentences:
            # Remove leading numbers like "1. " or "1) "
            if sent and sent[0].isdigit():
                sent = sent.split('.', 1)[-1].strip()
                sent = sent.split(')', 1)[-1].strip()
            if sent:
                cleaned.append(sent)

        print(f"Generated {len(cleaned)} sentences")
        return cleaned[:count]

    except Exception as e:
        print(f"ERROR generating sentences: {e}")
        return fallback_sentences(count)


def fallback_sentences(count: int) -> List[str]:
    """Fallback sentences if generation fails"""
    base = [
        "The cat sits on the mat.",
        "I love programming in Python.",
        "The weather is beautiful today.",
        "Coffee helps me work better.",
        "Books are windows to other worlds.",
        "Music makes everything more enjoyable.",
        "Learning new things is exciting.",
        "Time flies when you're having fun.",
        "Nature is full of wonders.",
        "Technology changes our daily lives."
    ]
    result = []
    while len(result) < count:
        result.extend(base)
    return result[:count]


def process_sentence(original: str, agent1: Agent1, agent2: Agent2, agent3: Agent3) -> Dict:
    """Process one sentence through the translation chain"""
    print(f"\n{'='*70}")
    print(f"Processing: {original}")

    # Translation chain: EN → RU → HE → EN
    russian_text = agent1.translate(original)
    hebrew_text = agent2.translate(russian_text)
    final_english = agent3.translate(hebrew_text)

    # Calculate cosine distance
    vec1 = text_to_vector(original)
    vec2 = text_to_vector(final_english)
    distance = cosine_distance(vec1, vec2)

    print(f"\nCOMPARISON:")
    print(f"  Original: {original}")
    print(f"  Final:    {final_english}")
    print(f"  Distance: {distance:.4f}")

    return {
        'original': original,
        'final': final_english,
        'distance': distance
    }


def create_visualization(results: List[Dict]):
    """Create and save visualization of translation degradation"""
    sentence_nums = [r['sentence_num'] for r in results]
    distances = [r['distance'] for r in results]

    plt.figure(figsize=(12, 6))
    plt.bar(sentence_nums, distances, color='steelblue', alpha=0.7, edgecolor='black')
    plt.xlabel('Sentence Number', fontsize=12)
    plt.ylabel('Cosine Distance', fontsize=12)
    plt.title('Translation Degradation: Cosine Distance per Sentence\n(EN→RU→HE→EN)', fontsize=14, fontweight='bold')
    plt.grid(axis='y', alpha=0.3, linestyle='--')

    # Add average line
    avg_distance = sum(distances) / len(distances)
    plt.axhline(y=avg_distance, color='red', linestyle='--', linewidth=2, label=f'Average: {avg_distance:.4f}')
    plt.legend()

    # Save plot
    os.makedirs('results', exist_ok=True)
    plot_file = 'results/translation_degradation.png'
    plt.savefig(plot_file, dpi=300, bbox_inches='tight')
    print(f"\n✓ Visualization saved to: {plot_file}")
    plt.close()


def run_experiment(num_sentences: int = 10):
    """Run the full translation experiment"""
    print("\n" + "="*70)
    print("MULTI-AGENT TRANSLATION TURING MACHINE")
    print("="*70)

    # Initialize API client
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not found in .env file")
    client = Anthropic(api_key=api_key)

    # Initialize translation agents
    agent1 = Agent1()
    agent2 = Agent2()
    agent3 = Agent3()

    # Generate sentences
    sentences = generate_sentences(client, num_sentences)

    # Process each sentence
    results = []
    for i, sentence in enumerate(sentences, 1):
        print(f"\n--- Sentence {i}/{num_sentences} ---")
        result = process_sentence(sentence, agent1, agent2, agent3)
        result['sentence_num'] = i
        results.append(result)

    # Analysis
    print("\n" + "="*70)
    print("ANALYSIS")
    print("="*70)

    distances = [r['distance'] for r in results]
    avg_distance = sum(distances) / len(distances)
    min_distance = min(distances)
    max_distance = max(distances)

    print(f"\nTotal sentences processed: {len(results)}")
    print(f"Average cosine distance: {avg_distance:.4f}")
    print(f"Min distance: {min_distance:.4f}")
    print(f"Max distance: {max_distance:.4f}")

    # Detailed sentence comparison
    print("\n" + "="*70)
    print("DETAILED SENTENCE COMPARISON")
    print("="*70)
    for i, r in enumerate(results, 1):
        print(f"\n{i}. Distance: {r['distance']:.4f}")
        print(f"   Original: {r['original']}")
        print(f"   Final:    {r['final']}")

    # Top 5 most degraded
    print("\n" + "="*70)
    print("TOP 5 MOST DEGRADED SENTENCES")
    print("="*70)
    sorted_results = sorted(results, key=lambda x: x['distance'], reverse=True)
    for i, r in enumerate(sorted_results[:5], 1):
        print(f"\n{i}. Distance: {r['distance']:.4f}")
        print(f"   Original: {r['original']}")
        print(f"   Final:    {r['final']}")

    # Create visualization
    create_visualization(results)

    # Save results
    os.makedirs('results', exist_ok=True)
    output_file = 'results/agent_results.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'summary': {
                'total_sentences': len(results),
                'avg_distance': avg_distance,
                'min_distance': min_distance,
                'max_distance': max_distance
            },
            'results': results
        }, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Results saved to: {output_file}")
    print("\n" + "="*70)
    print("EXPERIMENT COMPLETE!")
    print("="*70)

    return results


def main():
    """Main entry point"""
    # Get number of sentences from command line, default to 10
    num_sentences = 10
    if len(sys.argv) > 1:
        try:
            num_sentences = int(sys.argv[1])
        except ValueError:
            print(f"Invalid number: {sys.argv[1]}, using default (10)")

    print(f"\nStarting experiment with {num_sentences} sentences...\n")
    run_experiment(num_sentences)


if __name__ == "__main__":
    main()
