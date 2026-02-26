"""
Perceptron Network for AND & XOR Logic Gates
LIGHTWEIGHT VERSION - Uses only NumPy (no TensorFlow required!)
"""

import numpy as np
import matplotlib.pyplot as plt

class SimpleNeuralNetwork:
    """Simple neural network with one hidden layer"""
    
    def __init__(self, input_size=2, hidden_size=4, output_size=1):
        # Initialize weights randomly
        self.W1 = np.random.randn(input_size, hidden_size) * 0.5
        self.b1 = np.zeros((1, hidden_size))
        self.W2 = np.random.randn(hidden_size, output_size) * 0.5
        self.b2 = np.zeros((1, output_size))
        
    def relu(self, x):
        """ReLU activation function"""
        return np.maximum(0, x)
    
    def relu_derivative(self, x):
        """Derivative of ReLU"""
        return (x > 0).astype(float)
    
    def sigmoid(self, x):
        """Sigmoid activation function"""
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))
    
    def forward(self, X):
        """Forward propagation"""
        self.z1 = np.dot(X, self.W1) + self.b1
        self.a1 = self.relu(self.z1)
        self.z2 = np.dot(self.a1, self.W2) + self.b2
        self.a2 = self.sigmoid(self.z2)
        return self.a2
    
    def backward(self, X, y, learning_rate=0.1):
        """Backward propagation"""
        m = X.shape[0]
        
        # Output layer gradients
        dz2 = self.a2 - y
        dW2 = np.dot(self.a1.T, dz2) / m
        db2 = np.sum(dz2, axis=0, keepdims=True) / m
        
        # Hidden layer gradients
        da1 = np.dot(dz2, self.W2.T)
        dz1 = da1 * self.relu_derivative(self.z1)
        dW1 = np.dot(X.T, dz1) / m
        db1 = np.sum(dz1, axis=0, keepdims=True) / m
        
        # Update weights
        self.W2 -= learning_rate * dW2
        self.b2 -= learning_rate * db2
        self.W1 -= learning_rate * dW1
        self.b1 -= learning_rate * db1
    
    def train(self, X, y, epochs=200, learning_rate=0.5):
        """Train the network"""
        losses = []
        for epoch in range(epochs):
            # Forward pass
            predictions = self.forward(X)
            
            # Calculate MSE loss
            loss = np.mean((predictions - y) ** 2)
            losses.append(loss)
            
            # Backward pass
            self.backward(X, y, learning_rate)
            
            if (epoch + 1) % 50 == 0:
                accuracy = np.mean((predictions > 0.5) == y) * 100
                print(f"  Epoch {epoch+1}/{epochs} - Loss: {loss:.4f} - Accuracy: {accuracy:.2f}%")
        
        return losses
    
    def predict(self, X):
        """Make predictions"""
        return self.forward(X)

def generate_dataset(gate_type, num_samples=100, noise_percent=0):
    """Generate dataset for logic gates with optional noise"""
    samples_per_point = num_samples // 4
    X, y = [], []
    
    gates = {
        'AND': [(0,0,0), (0,1,0), (1,0,0), (1,1,1)],
        'XOR': [(0,0,0), (0,1,1), (1,0,1), (1,1,0)]
    }
    
    for x1, x2, label in gates[gate_type]:
        noise_std = noise_percent / 100.0
        x1_samples = np.random.normal(x1, noise_std, samples_per_point)
        x2_samples = np.random.normal(x2, noise_std, samples_per_point)
        X.extend(zip(x1_samples, x2_samples))
        y.extend([label] * samples_per_point)
    
    return np.array(X), np.array(y).reshape(-1, 1)

def plot_results(X, y, model, gate_type, noise_percent, losses):
    """Visualize decision boundary and training progress"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Plot decision boundary
    x_min, x_max = X[:, 0].min() - 0.5, X[:, 0].max() + 0.5
    y_min, y_max = X[:, 1].min() - 0.5, X[:, 1].max() + 0.5
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, 100),
                         np.linspace(y_min, y_max, 100))
    Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    
    ax1.contourf(xx, yy, Z, levels=20, cmap='RdYlBu', alpha=0.6)
    scatter = ax1.scatter(X[:, 0], X[:, 1], c=y, cmap='RdYlBu', 
                         edgecolors='black', s=50, linewidth=1.5)
    ax1.set_xlabel('Input X1', fontsize=12)
    ax1.set_ylabel('Input X2', fontsize=12)
    ax1.set_title(f'{gate_type} Gate - Decision Boundary\nNoise: {noise_percent}%', 
                  fontsize=14, fontweight='bold')
    plt.colorbar(scatter, ax=ax1, label='Output')
    ax1.grid(True, alpha=0.3)
    
    # Plot training loss
    ax2.plot(losses, linewidth=2, color='#2E86AB')
    ax2.set_xlabel('Epoch', fontsize=12)
    ax2.set_ylabel('Mean Squared Error', fontsize=12)
    ax2.set_title('Training Loss Curve', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    filename = f'{gate_type.lower()}_noise_{noise_percent}.png'
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"  Visualization saved: {filename}")
    plt.close()

def train_and_evaluate(gate_type, num_perceptrons=4, noise_percent=0, epochs=200):
    """Train model and display results"""
    print(f"\n{'='*60}")
    print(f"Training {gate_type} Gate | Perceptrons: {num_perceptrons} | Noise: {noise_percent}%")
    print('='*60)
    
    # Generate data
    X_train, y_train = generate_dataset(gate_type, num_samples=100, noise_percent=0)
    X_test, y_test = generate_dataset(gate_type, num_samples=100, noise_percent=noise_percent)
    
    # Create and train model
    model = SimpleNeuralNetwork(input_size=2, hidden_size=num_perceptrons, output_size=1)
    losses = model.train(X_train, y_train, epochs=epochs, learning_rate=0.5)
    
    # Evaluate
    predictions = model.predict(X_test)
    accuracy = np.mean((predictions > 0.5) == y_test) * 100
    final_loss = losses[-1]
    
    print(f"\nResults:")
    print(f"  Final Loss (MSE): {final_loss:.4f}")
    print(f"  Accuracy: {accuracy:.2f}%")
    
    # Visualize
    plot_results(X_test, y_test, model, gate_type, noise_percent, losses)
    
    return model, losses

# Main execution
if __name__ == "__main__":
    print("\n" + "="*60)
    print("LIGHTWEIGHT PERCEPTRON NETWORK")
    print("No TensorFlow Required - Pure NumPy Implementation!")
    print("="*60)
    
    # Part 1: Clean data
    print("\n" + "="*60)
    print("PART 1: Training on Clean Data")
    print("="*60)
    
    train_and_evaluate('AND', num_perceptrons=4, noise_percent=0)
    train_and_evaluate('XOR', num_perceptrons=4, noise_percent=0)
    
    # Part 2: Data with noise
    print("\n" + "="*60)
    print("PART 2: Training with Noise")
    print("="*60)
    
    noise_levels = [10, 20, 30]
    for noise in noise_levels:
        train_and_evaluate('AND', num_perceptrons=4, noise_percent=noise)
        train_and_evaluate('XOR', num_perceptrons=4, noise_percent=noise)
    
    print("\n" + "="*60)
    print("Training Complete! Check current folder for PNG files.")
    print("="*60 + "\n")