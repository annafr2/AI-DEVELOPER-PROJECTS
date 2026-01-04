"""
Temperature Conversion Neural Network
Converts Celsius to Fahrenheit without using the formula
Uses Keras/TensorFlow to learn the relationship f = 1.8 * c + 32
"""

import numpy as np
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt

# Set random seed for reproducibility
np.random.seed(42)
tf.random.set_seed(42)

print("TensorFlow version:", tf.__version__)

# ==================== DATA PREPARATION ====================
# Training data - 7 temperature pairs
celsius_q = np.array([-40, -10, 0, 8, 15, 22, 38], dtype=float)
fahrenheit_a = np.array([-40, 14, 32, 46.4, 59, 71.6, 100], dtype=float)

print(f"\nTraining data:")
print(f"Celsius: {celsius_q}")
print(f"Fahrenheit: {fahrenheit_a}")

# ==================== MODEL ARCHITECTURE ====================
# Building a simple neural network with 3 Dense layers
l0 = keras.layers.Dense(units=4, input_shape=[1], name='layer_0')
l1 = keras.layers.Dense(units=4, name='layer_1')
l2 = keras.layers.Dense(units=1, name='layer_2')

model = keras.Sequential([l0, l1, l2], name='temp_converter')

print("\n" + "="*60)
print("MODEL ARCHITECTURE")
print("="*60)
model.summary()

# ==================== COMPILATION ====================
# Loss function: Mean Squared Error
# Optimizer: Adam with learning rate 0.1
model.compile(
    loss='mean_squared_error',
    optimizer=keras.optimizers.Adam(learning_rate=0.1)
)

print("\nCompilation complete:")
print(f"  Loss function: Mean Squared Error")
print(f"  Optimizer: Adam (learning_rate=0.1)")

# ==================== TRAINING ====================
print("\n" + "="*60)
print("TRAINING PHASE - 500 EPOCHS")
print("="*60)

history = model.fit(
    celsius_q, 
    fahrenheit_a, 
    epochs=500,
    batch_size=7,  # Using all data in each batch
    verbose=False
)

print("Training completed!")
print(f"Final loss: {history.history['loss'][-1]:.4f}")

# ==================== VISUALIZATION - LOSS CURVE ====================
plt.figure(figsize=(10, 6))
plt.plot(history.history['loss'], color='#8B4513', linewidth=2)
plt.title('Learning Curve: Loss Over Training', fontsize=16, fontweight='bold')
plt.xlabel('Epoch Number', fontsize=12)
plt.ylabel('Loss (Mean Squared Error)', fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('/mnt/user-data/outputs/loss_curve.png', dpi=300, bbox_inches='tight')
print("\n✓ Loss curve saved: loss_curve.png")

# ==================== TEST PREDICTIONS ====================
print("\n" + "="*60)
print("TESTING ON NEW VALUES")
print("="*60)

# Test on values the model hasn't seen
test_celsius = np.array([100.0, 50.0, -20.0, 25.0])
predictions = model.predict(test_celsius, verbose=0)

# Calculate expected values using the formula
expected = test_celsius * 1.8 + 32

print("\nTest Results:")
print(f"{'Celsius':<12} {'Predicted F':<15} {'Expected F':<15} {'Error':<10}")
print("-" * 55)
for c, pred, exp in zip(test_celsius, predictions.flatten(), expected):
    error = abs(pred - exp)
    print(f"{c:<12.1f} {pred:<15.2f} {exp:<15.2f} {error:<10.4f}")

# Special test: 100°C should be 212°F
celsius_100 = np.array([100.0])
result = model.predict(celsius_100, verbose=0)
print(f"\nSpecial test - 100°C = {result[0][0]:.2f}°F (Expected: 212°F)")

# ==================== EXTRACT LEARNED WEIGHTS ====================
print("\n" + "="*60)
print("LEARNED WEIGHTS (THE 'BRAIN' OF THE MODEL)")
print("="*60)

print("\nLayer 0 weights and biases:")
weights_l0, biases_l0 = l0.get_weights()
print(f"  Weights shape: {weights_l0.shape}")
print(f"  Weights: {weights_l0.flatten()}")
print(f"  Biases: {biases_l0}")

print("\nLayer 1 weights and biases:")
weights_l1, biases_l1 = l1.get_weights()
print(f"  Weights shape: {weights_l1.shape}")

print("\nLayer 2 weights and biases:")
weights_l2, biases_l2 = l2.get_weights()
print(f"  Weights: {weights_l2.flatten()}")
print(f"  Biases: {biases_l2}")

# ==================== FORMULA ANALYSIS ====================
print("\n" + "="*60)
print("DID THE MODEL DISCOVER THE FORMULA?")
print("="*60)
print(f"True formula: f = 1.8 * c + 32")
print(f"\nThe model uses a complex network of weights across 3 layers.")
print(f"It approximates the formula through learned parameters,")
print(f"but doesn't explicitly use f = 1.8 * c + 32")

# ==================== VISUALIZATION - PREDICTIONS ====================
plt.figure(figsize=(12, 6))

# Create a range of celsius values for plotting
celsius_range = np.linspace(-50, 120, 100)
predictions_range = model.predict(celsius_range, verbose=0)
expected_range = celsius_range * 1.8 + 32

plt.plot(celsius_range, predictions_range, 'r-', linewidth=2, label='Model Predictions')
plt.plot(celsius_range, expected_range, 'b--', linewidth=2, label='True Formula (f = 1.8c + 32)')
plt.scatter(celsius_q, fahrenheit_a, color='green', s=100, zorder=5, label='Training Data')
plt.scatter(test_celsius, predictions.flatten(), color='orange', s=100, marker='x', zorder=5, label='Test Predictions')

plt.xlabel('Celsius (°C)', fontsize=12)
plt.ylabel('Fahrenheit (°F)', fontsize=12)
plt.title('Temperature Conversion: Model vs. True Formula', fontsize=16, fontweight='bold')
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('/mnt/user-data/outputs/prediction_comparison.png', dpi=300, bbox_inches='tight')
print("\n✓ Prediction comparison saved: prediction_comparison.png")

print("\n" + "="*60)
print("ALL TASKS COMPLETED SUCCESSFULLY!")
print("="*60)
