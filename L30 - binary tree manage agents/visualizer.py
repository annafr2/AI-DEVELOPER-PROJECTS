"""Tree Visualization Module - Core Functions."""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
from typing import Optional
import os


class TreeVisualizer:
    """Creates visual representations of trees."""
    
    def __init__(self, tree):
        self.tree = tree
        self.fig_size = (14, 10)
        
    def visualize_tree(self, title: str = "AI Agent Tree", 
                      save_path: Optional[str] = None,
                      show_imbalance: bool = True) -> None:
        """Create tree visualization."""
        fig, ax = plt.subplots(figsize=self.fig_size)
        
        G = nx.DiGraph()
        pos = {}
        labels = {}
        colors = []
        
        self._build_graph(G, pos, labels, colors, self.tree.root, 0, 0, 0, 4.0)
        
        nx.draw_networkx_edges(G, pos, ax=ax, arrows=False, 
                              edge_color='gray', width=2)
        nx.draw_networkx_nodes(G, pos, ax=ax, node_color=colors,
                              node_size=3000, alpha=0.9)
        nx.draw_networkx_labels(G, pos, labels, ax=ax, 
                               font_size=10, font_weight='bold')
        
        if show_imbalance:
            imb = self.tree.calculate_imbalance()
            ax.set_title(f"{title}\nImbalance Score: {imb:.1f}", 
                        fontsize=16, fontweight='bold')
        else:
            ax.set_title(title, fontsize=16, fontweight='bold')
        
        self._add_legend(ax)
        ax.axis('off')
        plt.tight_layout()
        
        if save_path:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Saved: {save_path}")
        else:
            plt.show()
        plt.close()
    
    def _build_graph(self, G, pos, labels, colors, node, level, x, min_x, max_x):
        """Build graph structure."""
        if not node:
            return
        
        name = node.node_id
        G.add_node(name)
        
        y = -level
        x_pos = (min_x + max_x) / 2
        pos[name] = (x_pos, y)
        
        if node.is_leaf:
            labels[name] = f"Leaf\n{node.value} tokens"
            colors.append('#90EE90')
        else:
            left_val = node.left.value if node.left else 0
            right_val = node.right.value if node.right else 0
            imb = abs(left_val - right_val)
            labels[name] = f"Node\n{node.value} total\nΔ={imb}"
            
            if imb == 0:
                colors.append('#00FF00')
            elif imb < 10:
                colors.append('#ADFF2F')
            elif imb < 30:
                colors.append('#FFFF00')
            elif imb < 60:
                colors.append('#FFA500')
            else:
                colors.append('#FF6347')
        
        if node.left:
            mid = (min_x + max_x) / 2
            self._build_graph(G, pos, labels, colors, node.left, 
                            level + 1, x, min_x, mid)
            G.add_edge(name, node.left.node_id)
        
        if node.right:
            mid = (min_x + max_x) / 2
            self._build_graph(G, pos, labels, colors, node.right, 
                            level + 1, x, mid, max_x)
            G.add_edge(name, node.right.node_id)
    
    def _add_legend(self, ax):
        """Add color legend."""
        legend = [
            mpatches.Patch(color='#00FF00', label='Perfect (Δ=0)'),
            mpatches.Patch(color='#ADFF2F', label='Good (Δ<10)'),
            mpatches.Patch(color='#FFFF00', label='Fair (Δ<30)'),
            mpatches.Patch(color='#FFA500', label='Poor (Δ<60)'),
            mpatches.Patch(color='#FF6347', label='Bad (Δ≥60)'),
            mpatches.Patch(color='#90EE90', label='Leaves')
        ]
        ax.legend(handles=legend, loc='upper right', fontsize=9, framealpha=0.9)