# CNN for Handwritten Digit Classification (MNIST)

## Project Overview

This project implements a Convolutional Neural Network (CNN) to classify handwritten digits from the MNIST dataset with >95% accuracy. The model uses deep learning techniques to recognize digits 0-9 from 28x28 grayscale images.

## Dataset

**MNIST (Modified National Institute of Standards and Technology)**

- Training samples: 60,000 images
- Test samples: 10,000 images
- Image dimensions: 28x28 pixels (grayscale)
- Classes: 10 (digits 0-9)
- Balanced distribution across all digit classes

## Technologies Used

- **TensorFlow/Keras**: Deep learning framework
- **NumPy**: Numerical computations
- **Matplotlib**: Data visualization
- **scikit-learn**: Evaluation metrics

## Model Architecture

### Convolutional Neural Network Structure

**First Convolutional Block:**

- Conv2D: 32 filters, 3x3 kernel, ReLU activation
- BatchNormalization
- Conv2D: 32 filters, 3x3 kernel, ReLU activation
- BatchNormalization
- MaxPooling2D: 2x2 pool size
- Dropout: 25%

**Second Convolutional Block:**

- Conv2D: 64 filters, 3x3 kernel, ReLU activation
- BatchNormalization
- Conv2D: 64 filters, 3x3 kernel, ReLU activation
- BatchNormalization
- MaxPooling2D: 2x2 pool size
- Dropout: 25%

**Third Convolutional Block:**

- Conv2D: 128 filters, 3x3 kernel, ReLU activation
- BatchNormalization
- MaxPooling2D: 2x2 pool size
- Dropout: 25%

**Fully Connected Layers:**

- Flatten layer
- Dense: 256 neurons, ReLU activation
- BatchNormalization
- Dropout: 50%
- Dense: 128 neurons, ReLU activation
- BatchNormalization
- Dropout: 50%
- Output Dense: 10 neurons, Softmax activation

**Total Parameters:** ~1.5M trainable parameters

## Data Preprocessing

1. **Reshape**: Images reshaped from (28, 28) to (28, 28, 1) for CNN input
2. **Normalization**: Pixel values scaled from [0, 255] to [0, 1]
3. **One-Hot Encoding**: Labels converted to categorical format
4. **Train-Validation Split**: 90% training, 10% validation

## Training Configuration

- **Optimizer**: Adam (adaptive learning rate)
- **Loss Function**: Categorical Crossentropy
- **Batch Size**: 128
- **Maximum Epochs**: 50
- **Validation Split**: 10%

### Training Callbacks

1. **Early Stopping**

   - Monitor: validation loss
   - Patience: 5 epochs
   - Restores best weights

2. **Learning Rate Reduction**
   - Monitor: validation loss
   - Factor: 0.5 (reduces LR by half)
   - Patience: 3 epochs
   - Minimum LR: 1e-7

## Results

- **Test Accuracy**: >95% (target achieved)
- **Training Time**: 5-10 minutes on CPU, <2 minutes on GPU
- **Model Performance**: High accuracy with good generalization

## Key Features

### Model Strengths

- High accuracy on digit classification
- Robust to variations in handwriting styles
- Good generalization to unseen data
- Efficient architecture with reasonable size
- Prevents overfitting through dropout and batch normalization

### Techniques Used

- **Batch Normalization**: Stabilizes and accelerates training
- **Dropout**: Prevents overfitting by randomly dropping neurons
- **MaxPooling**: Reduces spatial dimensions and computational cost
- **Data Normalization**: Improves convergence speed
- **Early Stopping**: Prevents overfitting and saves training time

## Evaluation Metrics

1. **Accuracy**: Overall classification accuracy
2. **Confusion Matrix**: Visualizes classification performance per digit
3. **Classification Report**: Precision, recall, F1-score per class
4. **Training History**: Plots of accuracy and loss over epochs

## Visualizations

The notebook includes:

- Sample MNIST digit images with labels
- Training/validation accuracy curves
- Training/validation loss curves
- Prediction examples with confidence scores
- Confusion matrix heatmap
- Misclassified examples analysis

## Model Deployment

The trained model is saved in two formats:

1. **HDF5 format**: `mnist_cnn_model.h5` (legacy format)
2. **SavedModel format**: `mnist_cnn_model/` (recommended for TensorFlow 2.x)

## Potential Improvements

1. **Data Augmentation**: Rotation, scaling, shifting to increase robustness
2. **Ensemble Methods**: Combine multiple models for better accuracy
3. **Transfer Learning**: Use pre-trained models as feature extractors
4. **Hyperparameter Tuning**: Grid search or Bayesian optimization
5. **Architecture Optimization**: Experiment with different layer configurations
6. **Regularization**: L1/L2 regularization for better generalization

## Usage

### Training the Model

```python
# Load and preprocess data
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# Build and compile model
model = build_cnn_model()
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train model
history = model.fit(x_train, y_train, epochs=5, validation_split=0.1, callbacks=[early_stopping, reduce_lr])
```

### Making Predictions

```python
# Load saved model
model = keras.models.load_model('mnist_cnn_model.h5')

# Predict on new images
predictions = model.predict(x_test)
predicted_classes = np.argmax(predictions, axis=1)
```

## Project Structure

```
task_three/
├── notebooks/
│   └── digits_class_cnn.ipynb    # Main notebook with CNN implementation
├── mnist_cnn_model.h5             # Saved model (HDF5 format)
├── mnist_cnn_model/               # Saved model (SavedModel format)
├── requirements.txt               # Python dependencies
└── project.md                     # This file
```

## Dependencies

- tensorflow>=2.0.0
- numpy>=1.19.0
- matplotlib>=3.3.0
- scikit-learn>=0.24.0

## Conclusion

This project successfully demonstrates the implementation of a CNN for handwritten digit classification, achieving >95% accuracy on the MNIST test set. The model uses modern deep learning techniques including batch normalization, dropout, and adaptive learning rate scheduling to achieve robust performance while preventing overfitting.
