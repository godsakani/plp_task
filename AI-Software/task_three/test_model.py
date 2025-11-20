"""
Simple script to test if the MNIST model loads correctly
"""
import tensorflow as tf
from tensorflow import keras
import numpy as np

def test_model():
    print("Testing MNIST CNN Model...")
    print("=" * 50)
    
    try:
        # Load model
        print("\n1. Loading model...")
        model = keras.models.load_model('mnist_cnn_model.h5')
        print("   ✓ Model loaded successfully!")
        
        # Display model summary
        print("\n2. Model Summary:")
        model.summary()
        
        # Test prediction with random input
        print("\n3. Testing prediction with random input...")
        test_input = np.random.rand(1, 28, 28, 1).astype('float32')
        prediction = model.predict(test_input, verbose=0)
        predicted_class = np.argmax(prediction[0])
        confidence = prediction[0][predicted_class] * 100
        
        print(f"   ✓ Prediction successful!")
        print(f"   Predicted digit: {predicted_class}")
        print(f"   Confidence: {confidence:.2f}%")
        
        print("\n" + "=" * 50)
        print("✓ All tests passed! Model is ready to use.")
        print("\nRun the Streamlit app with: streamlit run app.py")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nMake sure 'mnist_cnn_model.h5' is in the current directory.")

if __name__ == "__main__":
    test_model()
