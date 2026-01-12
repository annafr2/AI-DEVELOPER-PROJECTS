"""Tree Visualization - Summary Reports."""
import matplotlib.pyplot as plt
from typing import Optional
import os


def create_summary_report(initial_tree, optimized_tree, results: dict,
                         save_path: Optional[str] = None) -> None:
    """Create comprehensive report."""
    from visualizer import TreeVisualizer
    from viz_compare import _visualize_on_axis
    
    fig = plt.figure(figsize=(18, 12))
    gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)
    
    # Trees
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    
    viz1 = TreeVisualizer(initial_tree)
    viz2 = TreeVisualizer(optimized_tree)
    
    _visualize_on_axis(ax1, initial_tree, "Before", viz1)
    _visualize_on_axis(ax2, optimized_tree, "After", viz2)
    
    # Progress
    if results.get('history'):
        ax3 = fig.add_subplot(gs[1, :])
        
        # Add initial imbalance as iteration 0
        initial_imb = results.get('initial_imbalance')
        if initial_imb is not None:
            iterations = [0] + [s['iteration'] for s in results['history']]
            imbalances = [initial_imb] + [s['imbalance'] for s in results['history']]
        else:
            iterations = [s['iteration'] for s in results['history']]
            imbalances = [s['imbalance'] for s in results['history']]
        
        ax3.plot(iterations, imbalances, marker='o', linewidth=2, 
                markersize=8, color='#2E86AB')
        ax3.fill_between(iterations, imbalances, alpha=0.3, color='#2E86AB')
        ax3.set_xlabel('Iteration', fontsize=11, fontweight='bold')
        ax3.set_ylabel('Imbalance', fontsize=11, fontweight='bold')
        ax3.set_title('Progress', fontsize=12, fontweight='bold')
        ax3.grid(True, alpha=0.3)
    
    # Statistics
    ax4 = fig.add_subplot(gs[2, :])
    ax4.axis('off')
    
    stats = f"""
    OPTIMIZATION RESULTS
    {'=' * 60}
    
    Initial Imbalance:     {results['initial_imbalance']:.2f}
    Final Imbalance:       {results['final_imbalance']:.2f}
    Improvement:           {results['improvement']:.2f} ({results['improvement_percentage']:.1f}%)
    Iterations:            {results['iterations']}
    
    Initial Values:   {results['initial_values']}
    Final Values:     {results['final_values']}
    """
    
    ax4.text(0.1, 0.5, stats, fontsize=11, family='monospace',
            verticalalignment='center',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.suptitle('AI Agent Tree Balancing Report', 
                fontsize=16, fontweight='bold', y=0.98)
    
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved: {save_path}")
    else:
        plt.show()
    plt.close()