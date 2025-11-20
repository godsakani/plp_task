import streamlit as st
import numpy as np
import tensorflow as tf
from tensorflow import keras
from PIL import Image, ImageOps
import cv2
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(
    page_title="MNIST Digit Classifier",
    page_icon="🔢",
    layout="wide"
)

# Load the trained model
@st.cache_resource
def load_model():
    """Load the pre-trained MNIST CNN model"""
    try:
        model = keras.models.load_model('AI-Software/task_three/mnist_cnn_model.h5')
        return model
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

# Preprocess the image
def preprocess_image(image):
    """
    Preprocess the uploaded image to match MNIST format:
    - Convert to grayscale
    - Resize to 28x28
    - Invert colors (MNIST has white digits on black background)
    - Normalize pixel values
    """
    # Convert to grayscale
    img = ImageOps.grayscale(image)
    
    # Resize to 28x28
    img = img.resize((28, 28))
    
    # Convert to numpy array
    img_array = np.array(img)
    
    # Invert colors (MNIST has white digits on black background)
    img_array = 255 - img_array
    
    # Normalize to [0, 1]
    img_array = img_array.astype('float32') / 255.0
    
    # Reshape for model input (1, 28, 28, 1)
    img_array = img_array.reshape(1, 28, 28, 1)
    
    return img_array, img

def predict_digit(model, image_array):
    """Make prediction using the model"""
    predictions = model.predict(image_array, verbose=0)
    predicted_class = np.argmax(predictions[0])
    confidence = predictions[0][predicted_class] * 100
    
    return predicted_class, confidence, predictions[0]

# Main app
def main():
    st.title("🔢 MNIST Handwritten Digit Classifier")
    st.markdown("""
    This application uses a Convolutional Neural Network (CNN) to classify handwritten digits (0-9).
    Upload an image of a handwritten digit or draw one using the canvas below!
    """)
    
    # Load model
    model = load_model()
    
    if model is None:
        st.error("Failed to load the model. Please ensure 'mnist_cnn_model.h5' is in the same directory.")
        return
    
    # Sidebar
    st.sidebar.header("About")
    st.sidebar.info("""
    **Model Architecture:**
    - 3 Convolutional Blocks
    - Batch Normalization
    - MaxPooling & Dropout
    - 2 Dense Layers
    - ~1.5M Parameters
    
    **Performance:**
    - Test Accuracy: >95%
    - Training: MNIST Dataset (60k images)
    """)
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["📤 Upload Image", "✏️ Draw Digit", "ℹ️ Model Info"])
    
    with tab1:
        st.header("Upload an Image")
        st.markdown("Upload an image of a handwritten digit (preferably on white background)")
        
        uploaded_file = st.file_uploader(
            "Choose an image...", 
            type=['png', 'jpg', 'jpeg'],
            help="Upload a clear image of a single digit"
        )
        
        if uploaded_file is not None:
            # Display original image
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col1:
                st.subheader("Original Image")
                image = Image.open(uploaded_file)
                st.image(image, use_container_width=True)
            
            # Preprocess and display
            with col2:
                st.subheader("Preprocessed (28x28)")
                processed_array, processed_img = preprocess_image(image)
                st.image(processed_img, use_container_width=True)
            
            # Make prediction
            with col3:
                st.subheader("Prediction")
                with st.spinner("Analyzing..."):
                    predicted_digit, confidence, all_probs = predict_digit(model, processed_array)
                
                # Display result
                st.markdown(f"### Predicted Digit: **{predicted_digit}**")
                st.markdown(f"### Confidence: **{confidence:.2f}%**")
                
                # Confidence indicator
                if confidence > 90:
                    st.success("High Confidence ✓")
                elif confidence > 70:
                    st.warning("Medium Confidence")
                else:
                    st.error("Low Confidence")
            
            # Show probability distribution
            st.subheader("Probability Distribution")
            fig, ax = plt.subplots(figsize=(10, 4))
            bars = ax.bar(range(10), all_probs * 100, color='skyblue', edgecolor='black')
            bars[predicted_digit].set_color('green')
            ax.set_xlabel('Digit', fontsize=12)
            ax.set_ylabel('Probability (%)', fontsize=12)
            ax.set_title('Prediction Probabilities for Each Digit', fontsize=14)
            ax.set_xticks(range(10))
            ax.grid(axis='y', alpha=0.3)
            st.pyplot(fig)
            
            # Show detailed probabilities
            with st.expander("View Detailed Probabilities"):
                prob_df = {
                    'Digit': list(range(10)),
                    'Probability (%)': [f"{p*100:.2f}" for p in all_probs]
                }
                st.table(prob_df)
    
    with tab2:
        st.header("Draw a Digit")
        st.markdown("Use the canvas below to draw a digit (0-9)")
        
        try:
            from streamlit_drawable_canvas import st_canvas
            
            # Create canvas
            canvas_result = st_canvas(
                fill_color="rgba(255, 255, 255, 1)",
                stroke_width=20,
                stroke_color="rgb(0, 0, 0)",
                background_color="rgb(255, 255, 255)",
                height=280,
                width=280,
                drawing_mode="freedraw",
                key="canvas",
            )
            
            if canvas_result.image_data is not None:
                # Check if something is drawn
                if np.sum(canvas_result.image_data[:, :, 0] < 255) > 100:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("Your Drawing")
                        st.image(canvas_result.image_data, use_container_width=True)
                    
                    # Process canvas image
                    img = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA')
                    img = img.convert('L')
                    
                    # Preprocess
                    processed_array, processed_img = preprocess_image(img)
                    
                    with col2:
                        st.subheader("Preprocessed")
                        st.image(processed_img, use_container_width=True)
                    
                    # Predict
                    if st.button("Predict Drawn Digit", type="primary"):
                        with st.spinner("Analyzing your drawing..."):
                            predicted_digit, confidence, all_probs = predict_digit(model, processed_array)
                        
                        st.markdown(f"## Predicted Digit: **{predicted_digit}**")
                        st.markdown(f"## Confidence: **{confidence:.2f}%**")
                        
                        # Show probability chart
                        fig, ax = plt.subplots(figsize=(10, 4))
                        bars = ax.bar(range(10), all_probs * 100, color='lightcoral', edgecolor='black')
                        bars[predicted_digit].set_color('green')
                        ax.set_xlabel('Digit', fontsize=12)
                        ax.set_ylabel('Probability (%)', fontsize=12)
                        ax.set_title('Prediction Probabilities', fontsize=14)
                        ax.set_xticks(range(10))
                        ax.grid(axis='y', alpha=0.3)
                        st.pyplot(fig)
                else:
                    st.info("👆 Draw a digit on the canvas above")
        
        except ImportError:
            st.warning("""
            The drawing feature requires `streamlit-drawable-canvas`.
            Install it using: `pip install streamlit-drawable-canvas`
            """)
            st.info("For now, please use the 'Upload Image' tab.")
    
    with tab3:
        st.header("Model Information")
        
        st.subheader("Architecture Details")
        st.code("""
CNN Architecture:
================
Input: 28x28x1 grayscale images

Block 1:
- Conv2D(32, 3x3) + ReLU + BatchNorm
- Conv2D(32, 3x3) + ReLU + BatchNorm
- MaxPooling2D(2x2)
- Dropout(0.25)

Block 2:
- Conv2D(64, 3x3) + ReLU + BatchNorm
- Conv2D(64, 3x3) + ReLU + BatchNorm
- MaxPooling2D(2x2)
- Dropout(0.25)

Block 3:
- Conv2D(128, 3x3) + ReLU + BatchNorm
- MaxPooling2D(2x2)
- Dropout(0.25)

Fully Connected:
- Flatten
- Dense(256) + ReLU + BatchNorm + Dropout(0.5)
- Dense(128) + ReLU + BatchNorm + Dropout(0.5)
- Dense(10) + Softmax

Total Parameters: ~1.5M
        """, language="text")
        
        st.subheader("Training Details")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Dataset:**
            - MNIST Handwritten Digits
            - 60,000 training images
            - 10,000 test images
            - 10 classes (0-9)
            
            **Preprocessing:**
            - Normalization to [0, 1]
            - Reshape to 28x28x1
            - One-hot encoding for labels
            """)
        
        with col2:
            st.markdown("""
            **Training Configuration:**
            - Optimizer: Adam
            - Loss: Categorical Crossentropy
            - Batch Size: 128
            - Epochs: 20 (with early stopping)
            - Validation Split: 10%
            
            **Performance:**
            - Test Accuracy: >95%
            - Training Time: ~5-10 min (CPU)
            """)
        
        st.subheader("Tips for Best Results")
        st.markdown("""
        1. **For Upload:**
           - Use clear images with good contrast
           - Single digit centered in the image
           - White or light background preferred
           - Avoid cluttered backgrounds
        
        2. **For Drawing:**
           - Draw digits clearly and centered
           - Use bold strokes
           - Make digits reasonably large
           - Avoid touching the edges
        
        3. **Common Issues:**
           - Low confidence may indicate unclear writing
           - Similar digits (1/7, 3/8, 4/9) may confuse the model
           - Very thin or very thick strokes may affect accuracy
        """)

if __name__ == "__main__":
    main()
