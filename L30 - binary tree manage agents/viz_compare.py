"""Tree Visualization - Comparison and Charts."""
import matplotlib.pyplot as plt
import networkx as nx
from typing import Optional
import os


def visualize_comparison(tree1, tree2, 
                        title1: str = "Before",
                        title2: str = "After",
                        save_path: Optional[str] = None) -> None:
    """Side-by-side comparison."""
    from visualizer import TreeVisualizer
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
    
    viz1 = TreeVisualizer(tree1)
    viz2 = TreeVisualizer(tree2)
    
    _visualize_on_axis(ax1, tree1, title1, viz1)
    _visualize_on_axis(ax2, tree2, title2, viz2)
    
    plt.tight_layout()
    
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved: {save_path}")
    else:
        plt.show()
    plt.close()


def _visualize_on_axis(ax, tree, title, viz):
    """Helper to visualize on axis."""
    G = nx.DiGraph()
    pos = {}
    labels = {}
    colors = []
    
    viz._build_graph(G, pos, labels, colors, tree.root, 0, 0, 0, 4.0)
    
    nx.draw_networkx_edges(G, pos, ax=ax, arrows=False, 
                          edge_color='gray', width=2)
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=colors,
                          node_size=3000, alpha=0.9)
    nx.draw_networkx_labels(G, pos, labels, ax=ax, 
                           font_size=9, font_weight='bold')
    
    imb = tree.calculate_imbalance()
    ax.set_title(f"{title}\nImbalance: {imb:.1f}", 
                fontsize=14, fontweight='bold')
    ax.axis('off')


def create_progress_chart(history: list, initial_imbalance: float = None,
                          save_path: Optional[str] = None) -> None:
    """Chart showing improvement."""
    if not history:
        print("No history to visualize")
        return
    
    # Add initial imbalance as iteration 0
    if initial_imbalance is not None:
        iterations = [0] + [s['iteration'] for s in history]
        imbalances = [initial_imbalance] + [s['imbalance'] for s in history]
    else:
        iterations = [s['iteration'] for s in history]
        imbalances = [s['imbalance'] for s in history]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.plot(iterations, imbalances, marker='o', linewidth=2, 
           markersize=8, color='#2E86AB')
    ax.fill_between(iterations, imbalances, alpha=0.3, color='#2E86AB')
    
    ax.set_xlabel('Iteration', fontsize=12, fontweight='bold')
    ax.set_ylabel('Imbalance Score', fontsize=12, fontweight='bold')
    ax.set_title('Balance Improvement', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    ax.annotate(f'Start: {imbalances[0]:.1f}', 
               xy=(iterations[0], imbalances[0]),
               xytext=(10, 20), textcoords='offset points',
               bbox=dict(boxstyle='round', fc='yellow', alpha=0.7),
               arrowprops=dict(arrowstyle='->', color='black'))
    
    ax.annotate(f'End: {imbalances[-1]:.1f}', 
               xy=(iterations[-1], imbalances[-1]),
               xytext=(10, -30), textcoords='offset points',
               bbox=dict(boxstyle='round', fc='lightgreen', alpha=0.7),
               arrowprops=dict(arrowstyle='->', color='black'))
    
    plt.tight_layout()
    
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved: {save_path}")
    else:
        plt.show()
    plt.close()