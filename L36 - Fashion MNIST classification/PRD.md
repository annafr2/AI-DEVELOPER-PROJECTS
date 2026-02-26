# Product Requirements Document (PRD)

## Project: Fashion MNIST Image Classification

### Goal

Build a neural network using Keras that can classify grayscale images of clothing items into 10 categories with high accuracy.

### Background

Fashion MNIST is a dataset of 70,000 grayscale images (28x28 pixels) of 10 types of clothing. It is a common benchmark for image classification tasks. This project is part of the AI Expert Developer course (L36).

### Requirements

#### Functional Requirements

1. **Data Loading**
   - Load Fashion MNIST dataset from Keras
   - Split into training (60,000) and test (10,000) sets
   - Define the 10 class labels

2. **Data Preprocessing**
   - Normalize pixel values to range [0, 1]
   - Flatten 28x28 images to 784-element vectors
   - One-hot encode the labels for 10 classes

3. **Data Visualization**
   - Display a 4x4 grid of random training images with labels
   - Show class distribution for both training and test sets

4. **Model Architecture**
   - Build a Fully Connected (Dense) neural network
   - Minimum 3 hidden layers with decreasing neuron counts
   - Use Dropout for regularization
   - Use Softmax activation in the output layer

5. **Model Training**
   - Train with Categorical Crossentropy loss
   - Use Adam optimizer with configurable learning rate
   - Implement EarlyStopping to prevent overfitting
   - Use validation split to monitor generalization
   - Show training progress with loss and accuracy curves

6. **Model Evaluation**
   - Evaluate accuracy on the full test set
   - Show predictions on individual unseen images
   - Display confidence scores for each prediction

7. **Visualization and Reporting**
   - Confusion Matrix (raw counts and normalized percentages)
   - Per-class accuracy bar chart
   - Misclassified examples display
   - Final results summary dashboard
   - Classification report with precision, recall, F1-score

#### Non-Functional Requirements

- Code must run in Google Colab without additional installations
- Each code section must have clear English explanations
- All visualizations must be clean and readable
- The notebook must be self-contained and reproducible

### Target Accuracy

- Minimum: 85% test accuracy
- Expected: 88-90% test accuracy

### 10 Classes

| Label | Class Name |
|-------|------------|
| 0 | T-shirt/top |
| 1 | Trouser |
| 2 | Pullover |
| 3 | Dress |
| 4 | Coat |
| 5 | Sandal |
| 6 | Shirt |
| 7 | Sneaker |
| 8 | Bag |
| 9 | Ankle boot |

### Technical Decisions

| Decision | Choice | Reason |
|----------|--------|--------|
| Network type | Fully Connected | Course requirement; simple and effective |
| Loss function | Categorical Crossentropy | Standard for multi-class classification |
| Optimizer | Adam | Adaptive learning rate, good default |
| Learning rate | 0.001 | Standard starting point for Adam |
| Regularization | Dropout (20-30%) | Simple and effective against overfitting |
| Early stopping | patience=5 | Stop training if no improvement for 5 epochs |
| Batch size | 128 | Good balance of speed and stability |

### Success Criteria

1. Model achieves at least 85% accuracy on the test set
2. No significant overfitting (training and validation loss curves stay close)
3. All 7 notebook sections are complete with explanations
4. Confusion matrix shows reasonable performance across all classes
5. Visualizations are clear and informative
