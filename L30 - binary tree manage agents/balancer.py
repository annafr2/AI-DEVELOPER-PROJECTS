"""Tree Balancing Algorithm for AI Agents."""
from typing import List


class TreeBalancer:
    """Optimizes token distribution in agent trees."""
    
    def __init__(self, tree):
        self.tree = tree
        self.history = []
    
    def optimize_greedy(self, max_iter: int = 100) -> dict:
        """Greedy swap optimization algorithm."""
        initial_imb = self.tree.calculate_imbalance()
        initial_vals = self.tree.get_leaf_values().copy()
        
        self.history = []
        iterations = 0
        improved = True
        
        while improved and iterations < max_iter:
            improved = False
            current_imb = self.tree.calculate_imbalance()
            best_swap = None
            best_imb = current_imb
            
            # Try all swaps
            n = len(self.tree.leaves)
            for i in range(n):
                for j in range(i + 1, n):
                    self.tree.swap_leaves(i, j)
                    new_imb = self.tree.calculate_imbalance()
                    
                    if new_imb < best_imb:
                        best_imb = new_imb
                        best_swap = (i, j)
                    
                    self.tree.swap_leaves(i, j)  # Swap back
            
            # Apply best swap
            if best_swap and best_imb < current_imb:
                i, j = best_swap
                self.tree.swap_leaves(i, j)
                self.history.append({
                    'iteration': iterations + 1,
                    'swap': best_swap,
                    'imbalance': best_imb,
                    'improvement': current_imb - best_imb
                })
                improved = True
                iterations += 1
        
        final_imb = self.tree.calculate_imbalance()
        improvement = initial_imb - final_imb
        imp_pct = (improvement / initial_imb * 100) if initial_imb > 0 else 0
        
        return {
            'initial_imbalance': initial_imb,
            'final_imbalance': final_imb,
            'improvement': improvement,
            'improvement_percentage': imp_pct,
            'iterations': iterations,
            'initial_values': initial_vals,
            'final_values': self.tree.get_leaf_values(),
            'history': self.history
        }
    
    def find_best_swap(self) -> tuple:
        """Find best single swap."""
        current_imb = self.tree.calculate_imbalance()
        best = (0, 0, current_imb)
        
        n = len(self.tree.leaves)
        for i in range(n):
            for j in range(i + 1, n):
                self.tree.swap_leaves(i, j)
                new_imb = self.tree.calculate_imbalance()
                if new_imb < best[2]:
                    best = (i, j, new_imb)
                self.tree.swap_leaves(i, j)
        
        return best
    
    def get_summary(self) -> str:
        """Get optimization summary."""
        if not self.history:
            return "No optimization performed."
        
        lines = ["=== Optimization Summary ===\n"]
        for step in self.history:
            lines.append(
                f"Iteration {step['iteration']}: "
                f"Swap {step['swap'][0]}↔{step['swap'][1]} → "
                f"Imbalance: {step['imbalance']:.1f}"
            )
        return "\n".join(lines)


def compare_configs(tree, config_a: List[int], config_b: List[int]) -> dict:
    """Compare two configurations."""
    original = tree.get_leaf_values()
    
    tree.set_leaf_values(config_a)
    imb_a = tree.calculate_imbalance()
    
    tree.set_leaf_values(config_b)
    imb_b = tree.calculate_imbalance()
    
    tree.set_leaf_values(original)
    
    return {
        'config_a': config_a,
        'config_b': config_b,
        'imbalance_a': imb_a,
        'imbalance_b': imb_b,
        'better': 'A' if imb_a < imb_b else 'B',
        'difference': abs(imb_a - imb_b)
    }