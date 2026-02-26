# L36 - Fashion MNIST Classification with Keras
LINK to Colab - https://drive.google.com/file/d/1O46QahVFW6ngfVCpnPwYvSVSLdTMJYSU/view?usp=sharing

## What is this project?

This project builds a neural network that can look at a picture of a clothing item and tell you what it is. It can recognize 10 types of fashion items: T-shirts, trousers, pullovers, dresses, coats, sandals, shirts, sneakers, bags, and ankle boots.

## Dataset

We use the **Fashion MNIST** dataset from Keras:
- 60,000 training images
- 10,000 test images
- Each image is 28x28 pixels, grayscale
- 10 clothing categories

## How it works

### 1. Load Data
We load the Fashion MNIST dataset directly from Keras. It comes pre-split into training and test sets.

### 2. Preprocess
- **Normalize**: Scale pixel values from 0-255 to 0-1 (helps the network learn faster)
- **Flatten**: Reshape each 28x28 image into a flat row of 784 numbers
- **One-Hot Encode**: Convert labels like `3` into vectors like `[0,0,0,1,0,0,0,0,0,0]`

### 3. Visualize Data
Display a 4x4 grid of sample images and class distribution charts.

### 4. Build the Neural Network
A Fully Connected network with 3 hidden layers:

| Layer | Neurons | Activation | Dropout |
|-------|---------|------------|---------|
| Hidden 1 | 512 | ReLU | 30% |
| Hidden 2 | 256 | ReLU | 30% |
| Hidden 3 | 128 | ReLU | 20% |
| Output | 10 | Softmax | - |

- **Loss**: Categorical Crossentropy
- **Optimizer**: Adam (learning rate = 0.001)

### 5. Train the Model
- 30 epochs maximum with EarlyStopping (patience = 5)
- Batch size: 128
- 15% validation split
- Learning rate reduction on plateau

### 6. Test on Unseen Images
Evaluate on the test set and show individual predictions with confidence scores.

### 7. Visualizations
- Confusion Matrix (counts and percentages)
- Per-class accuracy bar chart
- Misclassified examples
- Final results dashboard

## How to run

1. Open `fashion_mnist_classification.ipynb` in Google Colab
2. Run all cells from top to bottom
3. No installation needed - all libraries are pre-installed in Colab

## Tech stack

- Python 3
- TensorFlow / Keras
- NumPy
- Matplotlib
- Seaborn
- scikit-learn

## Expected results

The model achieves approximately 88-90% accuracy on the test set. Some categories like Trousers and Bags are easier to classify, while Shirts and T-shirts are often confused with each other.
