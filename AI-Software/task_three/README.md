# MNIST Digit Classifier - Streamlit App

# [Deploy Link](https://taskthree-rwtyrhb934kevyyswg7wt2.streamlit.app/)

A web application for classifying handwritten digits using a trained CNN model.

## Features

- **Upload Image**: Upload an image of a handwritten digit for classification
- **Draw Digit**: Draw a digit directly on the canvas for real-time prediction
- **Model Info**: View detailed information about the CNN architecture and training

## Installation

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Running the App

Run the Streamlit application:

```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

## Usage

### Upload Image Tab

1. Click "Browse files" to upload an image
2. Supported formats: PNG, JPG, JPEG
3. The app will automatically preprocess and classify the digit
4. View the prediction, confidence score, and probability distribution

### Draw Digit Tab

1. Draw a digit on the canvas using your mouse
2. Click "Predict Drawn Digit" to classify
3. View the results and probability distribution

### Model Info Tab

- View the CNN architecture details
- See training configuration and performance metrics
- Read tips for best results

## Model Details

- **Architecture**: Deep CNN with 3 convolutional blocks
- **Parameters**: ~1.5M trainable parameters
- **Test Accuracy**: >95%
- **Dataset**: MNIST (60k training, 10k test images)

## Tips for Best Results

1. Use clear images with good contrast
2. Ensure the digit is centered
3. Avoid cluttered backgrounds
4. Draw digits clearly and boldly on the canvas

## Requirements

- Python 3.7+
- TensorFlow 2.x
- Streamlit
- See `requirements.txt` for full list

## Model File

The app requires `mnist_cnn_model.h5` to be in the same directory. This file contains the trained CNN model weights.
