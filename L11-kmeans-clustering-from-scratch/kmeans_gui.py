"""
Interactive GUI application for K-means algorithm
Allows dragging clusters, exploding clusters, and running K-means with accuracy display
"""

import itertools
import tkinter as tk
from dataclasses import dataclass
from tkinter import ttk

import matplotlib
matplotlib.use("TkAgg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# =============================================================================
# Data creation
# =============================================================================

@dataclass
class ClusterData:
    """Holds cluster data"""
    points: np.ndarray           # All points
    original_labels: np.ndarray  # Original labels for each point
    centers: np.ndarray          # Original cluster centers


def create_gaussian_dataset(
    n_total: int = 6000,
    n_clusters: int = 3,
    shared_fraction: float = 1/3,
    seed: int = 42,
) -> ClusterData:
    """
    Creates data with 3 overlapping Gaussian clusters
    
    Args:
        n_total: Total number of points
        n_clusters: Number of clusters (3)
        shared_fraction: What fraction of points will be shared
        seed: Random seed
    """
    rng = np.random.default_rng(seed)
    n_per_cluster = n_total // n_clusters
    n_shared = int(n_total * shared_fraction)
    n_unique_per_cluster = n_per_cluster - n_shared // n_clusters

    # Centers of the 3 clusters
    centers = np.array([
        [0.0, 0.0],
        [5.0, 5.0],
        [10.0, 0.0],
    ])

    std_unique = 1.0   # Standard deviation for unique points
    std_shared = 2.5   # Standard deviation for shared points

    # Create unique points for each cluster
    cluster_unique = [
        rng.normal(centers[i], std_unique, (n_unique_per_cluster, 2))
        for i in range(n_clusters)
    ]

    # Create shared points (in the middle between all clusters)
    center_of_all = np.mean(centers, axis=0)
    shared_points = rng.normal(center_of_all, std_shared, (n_shared, 2))

    # Merge all points
    points = []
    labels = []

    # Add unique points
    for i in range(n_clusters):
        points.append(cluster_unique[i])
        labels.extend([i] * len(cluster_unique[i]))

    # Add shared points - each shared point is assigned to all 3 clusters
    for i in range(n_clusters):
        points.append(shared_points)
        labels.extend([i] * len(shared_points))

    return ClusterData(
        points=np.vstack(points),
        original_labels=np.asarray(labels),
        centers=centers.copy(),
    )


# =============================================================================
# K-means algorithm
# =============================================================================

def run_kmeans(
    points: np.ndarray, 
    k: int = 3, 
    max_iters: int = 200
) -> tuple[np.ndarray, np.ndarray]:
    """
    Runs K-means algorithm
    
    Returns:
        labels: Labels for each point (0, 1, or 2)
        centers: Found cluster centers
    """
    rng = np.random.default_rng()
    n_samples = points.shape[0]
    
    # Random initialization of centers
    initial_indices = rng.choice(n_samples, size=k, replace=False)
    centers = points[initial_indices].copy()

    # Iteration loop
    for _ in range(max_iters):
        # Calculate distances from each point to each center
        distances = np.linalg.norm(
            points[:, None, :] - centers[None, :, :], 
            axis=2
        )
        
        # Assign each point to the nearest center
        labels = distances.argmin(axis=1)

        # Update centers
        new_centers = np.zeros_like(centers)
        for i in range(k):
            mask = labels == i
            if mask.any():
                new_centers[i] = points[mask].mean(axis=0)
            else:
                new_centers[i] = centers[i]

        # Check convergence
        if np.allclose(new_centers, centers):
            centers = new_centers
            break
        centers = new_centers

    return labels, centers


# =============================================================================
# Accuracy calculation
# =============================================================================

def compute_confusion_matrix(
    true_labels: np.ndarray, 
    predicted_labels: np.ndarray, 
    k: int
) -> np.ndarray:
    """Creates confusion matrix"""
    matrix = np.zeros((k, k), dtype=int)
    for t, p in zip(true_labels, predicted_labels):
        matrix[t, p] += 1
    return matrix


def evaluate_clustering(
    true_labels: np.ndarray, 
    predicted_labels: np.ndarray, 
    k: int
) -> tuple[float, dict[int, float]]:
    """
    Calculates K-means accuracy
    
    Returns:
        accuracy: Overall accuracy (0-1)
        cluster_scores: Accuracy for each cluster
    """
    matrix = compute_confusion_matrix(true_labels, predicted_labels, k)

    # Find the best matching between original and predicted labels
    best_accuracy = 0.0
    best_mapping: dict[int, int] | None = None

    for permutation in itertools.permutations(range(k)):
        correct = sum(matrix[i, permutation[i]] for i in range(k))
        accuracy = correct / matrix.sum()
        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_mapping = {permutation[i]: i for i in range(k)}

    # Calculate accuracy for each cluster
    cluster_scores: dict[int, float] = {}
    if best_mapping is not None:
        for predicted_cluster, original_cluster in best_mapping.items():
            total = matrix[:, predicted_cluster].sum()
            if total:
                cluster_scores[original_cluster] = (
                    matrix[original_cluster, predicted_cluster] / total
                )
            else:
                cluster_scores[original_cluster] = 0.0

    return best_accuracy, cluster_scores


# =============================================================================
# GUI
# =============================================================================

class KMeansGUI:
    """Interactive graphical interface for K-means"""
    
    # Colors and markers for each cluster
    COLORS = np.array([
        [0.8, 0.1, 0.1],  # Red - Cluster 1
        [0.1, 0.6, 0.1],  # Green - Cluster 2
        [0.1, 0.2, 0.8]   # Blue - Cluster 3
    ])
    EDGE_COLORS = ["darkred", "darkgreen", "navy"]
    MARKERS = ["o", "s", "^"]  # Circle, square, triangle

    def __init__(self, cluster_data: ClusterData):
        self.data = cluster_data
        self.points = self.data.points.copy()
        self.original_labels = self.data.original_labels
        self.cluster_centers = self.data.centers.copy()

        # Variables for dragging
        self.dragging_cluster: int | None = None
        self._drag_reference: np.ndarray | None = None

        # Create main window
        self.root = tk.Tk()
        self.root.title("K-means Interactive Playground")
        self.root.geometry("1400x700")

        self._build_layout()
        self._create_plots()
        self._update_scatter()
        self._update_stats_labels()

    def _build_layout(self) -> None:
        """Builds the interface"""
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Graph area
        figure_frame = ttk.Frame(main_frame)
        figure_frame.grid(row=0, column=0, rowspan=3, sticky="nsew")
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)

        # Control panel
        controls_frame = ttk.LabelFrame(main_frame, text="Controls", padding=10)
        controls_frame.grid(row=0, column=1, sticky="new", padx=(10, 0))
        
        # Statistics panel
        stats_frame = ttk.LabelFrame(main_frame, text="Statistics", padding=10)
        stats_frame.grid(row=1, column=1, sticky="new", padx=(10, 0), pady=(10, 0))

        # Create graphs
        self.figure, (self.ax_points, self.ax_stats) = plt.subplots(
            1, 2, figsize=(12, 6)
        )
        self.figure.subplots_adjust(wspace=0.3)
        self.canvas = FigureCanvasTkAgg(self.figure, master=figure_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Connect mouse events
        self.canvas.mpl_connect("button_press_event", self._on_press)
        self.canvas.mpl_connect("motion_notify_event", self._on_motion)
        self.canvas.mpl_connect("button_release_event", self._on_release)

        # "Explode cluster" buttons
        ttk.Label(
            controls_frame, 
            text="Explode Cluster:", 
            font=("Arial", 11, "bold")
        ).grid(row=0, column=0, sticky="w", pady=(0, 5))

        for idx in range(3):
            button = ttk.Button(
                controls_frame,
                text=f"Explode Cluster {idx + 1}",
                command=lambda c=idx: self._explode_cluster(c),
            )
            button.grid(row=idx + 1, column=0, sticky="ew", pady=2)

        ttk.Separator(controls_frame, orient=tk.HORIZONTAL).grid(
            row=4, column=0, sticky="ew", pady=8
        )

        # Main buttons
        run_button = ttk.Button(
            controls_frame, 
            text="▶ Run K-means", 
            command=self._run_kmeans
        )
        run_button.grid(row=5, column=0, sticky="ew", pady=2)

        reset_button = ttk.Button(
            controls_frame, 
            text="🔄 Reset Data", 
            command=self._reset_points
        )
        reset_button.grid(row=6, column=0, sticky="ew", pady=2)

        # Statistics labels
        self.cluster_stat_labels: list[ttk.Label] = []
        for idx in range(3):
            label = ttk.Label(
                stats_frame, 
                text="", 
                justify=tk.LEFT,
                font=("Courier", 9)
            )
            label.grid(row=idx, column=0, sticky="w", pady=4)
            self.cluster_stat_labels.append(label)

        # Status line
        self.status_var = tk.StringVar(value="Drag clusters or press buttons")
        status_label = ttk.Label(
            stats_frame, 
            textvariable=self.status_var, 
            foreground="navy", 
            justify=tk.LEFT,
            wraplength=200
        )
        status_label.grid(row=4, column=0, sticky="w", pady=(10, 0))

    def _create_plots(self) -> None:
        """Creates the empty plots"""
        # Points graph
        self.ax_points.set_title("Point Clouds", fontsize=14, fontweight='bold')
        self.ax_points.set_xlabel("X")
        self.ax_points.set_ylabel("Y")
        self.ax_points.grid(True, alpha=0.3)
        
        # Set proper axis limits to show all clusters (0,0), (5,5), (10,0)
        self.ax_points.set_xlim(-3, 13)
        self.ax_points.set_ylim(-3, 8)

        # Scatter of all points (original colors)
        self.base_scatter = self.ax_points.scatter([], [], s=20, alpha=0.6)
        
        # Scatter of cluster centers
        self.center_scatter = self.ax_points.scatter(
            [], [], 
            marker="X", 
            s=200, 
            c="black", 
            edgecolors="white", 
            linewidths=2,
            zorder=10
        )
        
        # Lists for K-means results
        self.assignment_scatters: list = []
        self.kmeans_center_scatter = None

        # Accuracy graph
        self.ax_stats.set_title("K-means Accuracy", fontsize=14, fontweight='bold')
        self.ax_stats.set_ylim(0, 1.05)
        self.ax_stats.set_ylabel("Accuracy")
        self.ax_stats.grid(True, alpha=0.3, axis='y')

    def _update_scatter(self) -> None:
        """Updates the point display"""
        colors = self.COLORS[self.original_labels]
        self.base_scatter.set_offsets(self.points)
        self.base_scatter.set_facecolors(colors)
        self.base_scatter.set_edgecolors("none")
        self.center_scatter.set_offsets(self.cluster_centers)
        self._clear_assignments()
        
        # Auto-scale the axes to fit all points
        self.ax_points.relim()
        self.ax_points.autoscale_view()
        
        self.canvas.draw_idle()

    def _clear_assignments(self) -> None:
        """Clears previous K-means results"""
        for scatter in self.assignment_scatters:
            scatter.remove()
        self.assignment_scatters.clear()

        if self.kmeans_center_scatter is not None:
            self.kmeans_center_scatter.remove()
            self.kmeans_center_scatter = None

    # -------------------------------------------------------------------------
    # Cluster dragging
    # -------------------------------------------------------------------------

    def _on_press(self, event):
        """Mouse click - start dragging"""
        if event.inaxes != self.ax_points:
            return
        if event.xdata is None or event.ydata is None:
            return

        cursor = np.array([event.xdata, event.ydata])
        distances = np.linalg.norm(self.cluster_centers - cursor, axis=1)
        idx = distances.argmin()
        
        # If mouse is close enough to a center - start dragging
        if distances[idx] < 1.0:
            self.dragging_cluster = idx
            self._drag_reference = cursor

    def _on_motion(self, event):
        """Mouse motion - dragging"""
        if self.dragging_cluster is None or event.inaxes != self.ax_points:
            return
        if event.xdata is None or event.ydata is None:
            return
        if self._drag_reference is None:
            return

        current = np.array([event.xdata, event.ydata])
        delta = current - self._drag_reference
        self._drag_reference = current

        # Move all points in the cluster and the center
        mask = self.original_labels == self.dragging_cluster
        self.points[mask] += delta
        self.cluster_centers[self.dragging_cluster] += delta

        self._update_scatter()
        self._update_stats_labels()
        self.status_var.set(f"Dragging cluster {self.dragging_cluster + 1}")

    def _on_release(self, _event):
        """Mouse release - end dragging"""
        if self.dragging_cluster is not None:
            self.status_var.set(f"Cluster {self.dragging_cluster + 1} released")
        self.dragging_cluster = None
        self._drag_reference = None

    # -------------------------------------------------------------------------
    # Button actions
    # -------------------------------------------------------------------------

    def _explode_cluster(self, cluster_idx: int) -> None:
        """Recalculates mean and variance of a cluster"""
        mask = self.original_labels == cluster_idx
        if not mask.any():
            return

        cluster_points = self.points[mask]
        
        # Calculate new mean
        new_mean = cluster_points.mean(axis=0)
        
        # Move points around the new mean
        current_mean = self.cluster_centers[cluster_idx]
        shift = new_mean - current_mean
        self.points[mask] += shift
        self.cluster_centers[cluster_idx] = new_mean
        
        self._update_scatter()
        self._update_stats_labels()
        self.status_var.set(f"Cluster {cluster_idx + 1} exploded (re-centered)")

    def _reset_points(self) -> None:
        """Returns data to initial state"""
        self.points = self.data.points.copy()
        self.cluster_centers = self.data.centers.copy()
        self._update_scatter()
        self._update_stats_labels()
        self.status_var.set("Data reset to initial state")

    def _run_kmeans(self) -> None:
        """Runs the K-means algorithm"""
        labels, centers = run_kmeans(self.points, k=3)
        self._update_assignments(labels, centers)
        self._update_accuracy(labels)
        self.status_var.set("K-means completed!")

    # -------------------------------------------------------------------------
    # Display update
    # -------------------------------------------------------------------------

    def _update_assignments(
        self, 
        labels: np.ndarray, 
        centers: np.ndarray
    ) -> None:
        """Displays K-means results - frames around points"""
        self._clear_assignments()

        # Draw frames around each point according to its new cluster
        for cluster_idx in range(3):
            mask = labels == cluster_idx
            if not mask.any():
                continue
            
            scatter = self.ax_points.scatter(
                self.points[mask, 0],
                self.points[mask, 1],
                facecolors="none",
                edgecolors=self.EDGE_COLORS[cluster_idx],
                linewidths=1.2,
                marker=self.MARKERS[cluster_idx],
                s=60,
                alpha=0.8
            )
            self.assignment_scatters.append(scatter)

        # Draw new K-means centers
        self.kmeans_center_scatter = self.ax_points.scatter(
            centers[:, 0],
            centers[:, 1],
            marker="X",
            s=250,
            c=["darkred", "darkgreen", "navy"],
            edgecolors="yellow",
            linewidths=2,
            zorder=11
        )

        self.canvas.draw_idle()

    def _update_accuracy(self, labels: np.ndarray) -> None:
        """Updates the accuracy graph"""
        accuracy, per_cluster = evaluate_clustering(
            self.original_labels, labels, k=3
        )

        cluster_values = [per_cluster.get(idx, 0.0) for idx in range(3)]

        # Clear and redraw the graph
        self.ax_stats.cla()
        self.ax_stats.set_title("K-means Accuracy", fontsize=14, fontweight='bold')
        self.ax_stats.set_ylim(0, 1.05)
        self.ax_stats.set_ylabel("Accuracy")
        self.ax_stats.grid(True, alpha=0.3, axis='y')
        
        bars = self.ax_stats.bar(
            range(4),
            [accuracy] + cluster_values,
            color=["#555555", "#d94c4c", "#4cd96a", "#4c6cd9"],
            edgecolor='black',
            linewidth=1.5
        )
        
        # Add percentages on top of bars
        for bar, value in zip(bars, [accuracy] + cluster_values):
            height = bar.get_height()
            self.ax_stats.text(
                bar.get_x() + bar.get_width() / 2,
                height + 0.02,
                f"{value*100:.1f}%",
                ha="center",
                va="bottom",
                fontweight='bold',
                fontsize=10
            )
        
        self.ax_stats.set_xticks(range(4))
        self.ax_stats.set_xticklabels(
            ["Total", "Cluster 1", "Cluster 2", "Cluster 3"]
        )
        self.canvas.draw_idle()

    def _update_stats_labels(self) -> None:
        """Updates the statistics labels"""
        for idx in range(3):
            mask = self.original_labels == idx
            if not mask.any():
                self.cluster_stat_labels[idx].config(
                    text=f"Cluster {idx + 1}: No points"
                )
                continue

            cluster_points = self.points[mask]
            mean = cluster_points.mean(axis=0)
            cov = np.cov(cluster_points, rowvar=False)
            variance = np.diag(cov)
            
            text = (
                f"Cluster {idx + 1}:\n"
                f"  μ = ({mean[0]:.2f}, {mean[1]:.2f})\n"
                f"  σ² = ({variance[0]:.2f}, {variance[1]:.2f})\n"
                f"  Points: {cluster_points.shape[0]}"
            )
            self.cluster_stat_labels[idx].config(text=text)

    def run(self) -> None:
        """Starts the interface"""
        self.root.mainloop()


# =============================================================================
# Execution
# =============================================================================

def main() -> None:
    print("Creating data...")
    data = create_gaussian_dataset()
    print(f"Created {len(data.points)} points in {len(np.unique(data.original_labels))} clusters")
    
    print("Opening graphical interface...")
    app = KMeansGUI(data)
    app.run()


if __name__ == "__main__":
    main()