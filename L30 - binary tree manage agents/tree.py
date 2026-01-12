"""Binary Tree for AI Agent Token Management."""
from typing import Optional, List, Tuple
import random


class TreeNode:
    """Node in the binary tree."""
    def __init__(self, value: int = 0, is_leaf: bool = False, node_id: str = ""):
        self.value = value
        self.left: Optional[TreeNode] = None
        self.right: Optional[TreeNode] = None
        self.is_leaf = is_leaf
        self.node_id = node_id


class AgentTree:
    """Binary tree for AI agent hierarchy."""
    def __init__(self, depth: int = 3, min_tokens: int = 1, max_tokens: int = 100):
        self.depth = depth
        self.min_tokens = min_tokens
        self.max_tokens = max_tokens
        self.root: Optional[TreeNode] = None
        self.leaves: List[TreeNode] = []
        
    def build_random_tree(self) -> None:
        """Build tree with random token values."""
        self.leaves = []
        self.root = self._build_recursive(0, "root")
        self._aggregate(self.root)
    
    def _build_recursive(self, level: int, node_id: str) -> TreeNode:
        """Recursively build tree."""
        if level == self.depth:
            value = random.randint(self.min_tokens, self.max_tokens)
            node = TreeNode(value=value, is_leaf=True, node_id=node_id)
            self.leaves.append(node)
            return node
        
        node = TreeNode(is_leaf=False, node_id=node_id)
        node.left = self._build_recursive(level + 1, f"{node_id}_L")
        node.right = self._build_recursive(level + 1, f"{node_id}_R")
        return node
    
    def _aggregate(self, node: Optional[TreeNode]) -> int:
        """Sum tokens bottom-up."""
        if node is None or node.is_leaf:
            return node.value if node else 0
        node.value = self._aggregate(node.left) + self._aggregate(node.right)
        return node.value
    
    def calculate_imbalance(self) -> float:
        """Calculate tree imbalance."""
        return self._calc_imbalance(self.root)
    
    def _calc_imbalance(self, node: Optional[TreeNode]) -> float:
        """Recursive imbalance calculation."""
        if not node or node.is_leaf:
            return 0.0
        left_val = node.left.value if node.left else 0
        right_val = node.right.value if node.right else 0
        return (left_val - right_val) ** 2 + \
               self._calc_imbalance(node.left) + \
               self._calc_imbalance(node.right)
    
    def get_leaf_values(self) -> List[int]:
        """Get all leaf values."""
        return [leaf.value for leaf in self.leaves]
    
    def set_leaf_values(self, values: List[int]) -> None:
        """Set new leaf values."""
        if len(values) != len(self.leaves):
            raise ValueError(f"Expected {len(self.leaves)} values")
        for leaf, value in zip(self.leaves, values):
            leaf.value = value
        self._aggregate(self.root)
    
    def swap_leaves(self, i: int, j: int) -> None:
        """Swap two leaf values."""
        if i >= len(self.leaves) or j >= len(self.leaves):
            raise ValueError("Index out of range")
        self.leaves[i].value, self.leaves[j].value = \
            self.leaves[j].value, self.leaves[i].value
        self._aggregate(self.root)
    
    def get_tree_info(self) -> dict:
        """Get tree statistics."""
        vals = self.get_leaf_values()
        return {
            'depth': self.depth,
            'num_leaves': len(self.leaves),
            'total_tokens': self.root.value if self.root else 0,
            'min_leaf': min(vals) if vals else 0,
            'max_leaf': max(vals) if vals else 0,
            'avg_leaf': sum(vals) / len(vals) if vals else 0,
            'imbalance': self.calculate_imbalance(),
            'leaf_values': vals
        }
    
    def get_all_nodes(self) -> List[Tuple[TreeNode, int]]:
        """Get all nodes with levels."""
        nodes = []
        self._collect(self.root, 0, nodes)
        return nodes
    
    def _collect(self, node: Optional[TreeNode], level: int, 
                 nodes: List[Tuple[TreeNode, int]]) -> None:
        """Collect nodes recursively."""
        if not node:
            return
        nodes.append((node, level))
        self._collect(node.left, level + 1, nodes)
        self._collect(node.right, level + 1, nodes)