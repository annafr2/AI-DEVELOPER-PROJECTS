"""AI Agent Tree Balancing Game - Main Application."""
import sys
import os
import copy

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from tree import AgentTree
from balancer import TreeBalancer
from visualizer import TreeVisualizer
from viz_compare import visualize_comparison, create_progress_chart
from viz_report import create_summary_report


def get_images_dir():
    """Get path to images directory in current location."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    images_dir = os.path.join(project_root, 'images')
    os.makedirs(images_dir, exist_ok=True)
    return images_dir


def print_sep():
    print("\n" + "=" * 70 + "\n")


def print_tree_info(tree: AgentTree, title: str = "Tree Info"):
    info = tree.get_tree_info()
    print(f"\n{title}")
    print("-" * 50)
    print(f"Depth: {info['depth']} | Leaves: {info['num_leaves']}")
    print(f"Total Tokens: {info['total_tokens']}")
    print(f"Leaf Values: {info['leaf_values']}")
    print(f"Imbalance: {info['imbalance']:.2f}")


def run_simulation(depth: int = 3, create_viz: bool = True):
    """Run complete simulation with random token values."""
    print_sep()
    print(f"🎮 SIMULATION (Depth {depth} = {2**depth} leaves)")
    print_sep()
    
    print("Generating random tree with random token values...")
    tree = AgentTree(depth=depth)
    tree.build_random_tree()  # Random tokens generated here!
    print_tree_info(tree, "Initial Random Tree")
    
    initial_tree = copy.deepcopy(tree)
    
    print_sep()
    print("Running optimization algorithm...")
    
    balancer = TreeBalancer(tree)
    results = balancer.optimize_greedy()
    
    print(f"\n✨ Optimization Complete!")
    print(f"   Iterations: {results['iterations']}")
    print(f"   Initial Imbalance: {results['initial_imbalance']:.2f}")
    print(f"   Final Imbalance: {results['final_imbalance']:.2f}")
    print(f"   Improvement: {results['improvement_percentage']:.1f}%")
    
    if create_viz:
        images_dir = get_images_dir()
        print_sep()
        print("Creating visualizations...")
        
        v1 = TreeVisualizer(initial_tree)
        v1.visualize_tree("Initial Random Tree", 
            os.path.join(images_dir, "01_initial_tree.png"))
        
        v2 = TreeVisualizer(tree)
        v2.visualize_tree("Optimized Tree",
            os.path.join(images_dir, "02_optimized_tree.png"))
        
        visualize_comparison(initial_tree, tree, "Before Optimization", "After Optimization",
            os.path.join(images_dir, "03_comparison.png"))
        
        if results['history']:
            create_progress_chart(results['history'],
                initial_imbalance=results['initial_imbalance'],
                save_path=os.path.join(images_dir, "04_progress_chart.png"))
        
        create_summary_report(initial_tree, tree, results,
            os.path.join(images_dir, "05_complete_report.png"))
        
        print(f"\n📊 All visualizations saved to: {images_dir}")
    
    print_sep()
    print("🎉 Simulation Complete!")
    print(f"📁 Check images/ folder for 5 visualization files")
    print_sep()
    
    return tree, results


def main():
    print("\n" + "=" * 70)
    print("  🌳 AI AGENT TREE BALANCING GAME 🌳")
    print("=" * 70)
    print("\nSimulating AI agent tree with random token consumption...")
    
    run_simulation(depth=3, create_viz=True)


if __name__ == "__main__":
    main()