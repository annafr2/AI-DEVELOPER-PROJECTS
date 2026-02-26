# Tasks Checklist

## Project: Fashion MNIST Classification with Keras

### Part 1: Load Data
- [x] Import TensorFlow, Keras, NumPy, Matplotlib, Seaborn, scikit-learn
- [x] Load Fashion MNIST dataset using `keras.datasets.fashion_mnist.load_data()`
- [x] Define the 10 class names
- [x] Print dataset shapes and info

### Part 2: Preprocessing
- [x] Normalize pixel values: divide by 255 to get range [0, 1]
- [x] Flatten images: reshape from (28, 28) to (784,)
- [x] One-hot encode labels: convert integer labels to 10-element vectors
- [x] Print shapes before and after each step

### Part 3: Visualize Data
- [x] Display 4x4 grid of random training images with class labels
- [x] Show class distribution bar charts for training and test sets
- [x] Verify dataset is balanced (6,000 per class in training)

### Part 4: Build the Neural Network
- [x] Create Sequential model with Keras
- [x] Add Hidden Layer 1: 512 neurons, ReLU, Dropout 30%
- [x] Add Hidden Layer 2: 256 neurons, ReLU, Dropout 30%
- [x] Add Hidden Layer 3: 128 neurons, ReLU, Dropout 20%
- [x] Add Output Layer: 10 neurons, Softmax
- [x] Compile with Adam optimizer (lr=0.001), categorical crossentropy loss
- [x] Print model summary with explanation of choices

### Part 5: Train the Model
- [x] Set up EarlyStopping callback (patience=5)
- [x] Set up ReduceLROnPlateau callback
- [x] Train for max 30 epochs, batch size 128, 15% validation split
- [x] Plot training vs validation loss curves
- [x] Plot training vs validation accuracy curves
- [x] Mark best epoch on the plots
- [x] Check for overfitting (compare training and validation loss gap)

### Part 6: Test on Unseen Images
- [x] Evaluate model on full test set (10,000 images)
- [x] Print test loss and accuracy
- [x] Show 8 random test predictions with correct/wrong indicators
- [x] Show 4 detailed predictions with confidence bar charts

### Part 7: Visualizations
- [x] Create Confusion Matrix with raw counts
- [x] Create Confusion Matrix with normalized percentages
- [x] Create per-class accuracy bar chart with color coding
- [x] Print full classification report (precision, recall, F1)
- [x] Show 12 misclassified examples
- [x] Create final results dashboard (accuracy over time, per-class sorted, pie chart)

### Documentation
- [x] Create README.md with project overview and instructions
- [x] Create PRD.md with requirements and technical decisions
- [x] Create TASKS.md with detailed task breakdown

### Key Concepts Explained in the Notebook
- [x] What normalization does and why
- [x] What flattening does and why
- [x] What one-hot encoding does and why
- [x] What each layer does in the network
- [x] What the loss function measures
- [x] What the optimizer and learning rate do
- [x] What ReLU and Softmax activations do
- [x] What Dropout does and why it prevents overfitting
- [x] How to read a Confusion Matrix
- [x] How to check for overfitting using loss curves
