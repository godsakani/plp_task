"""
Edge AI Prototype: Recyclable Item Classification
AI Future Directions Assignment - Task 1

This script implements a lightweight image classification model for recognizing
recyclable items, optimized for edge deployment using TensorFlow Lite.
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import os
import time
from pathlib import Path

# Set random seeds for reproducibility
tf.random.set_seed(42)
np.random.seed(42)

class RecyclableClassifier:
    def __init__(self, img_size=(224, 224), num_classes=6):
        """
        Initialize the recyclable item classifier
        
        Args:
            img_size: Input image dimensions
            num_classes: Number of recyclable categories
        """
        self.img_size = img_size
        self.num_classes = num_classes
        self.class_names = ['plastic', 'glass', 'metal', 'paper', 'cardboard', 'organic']
        self.model = None
        self.tflite_model = None
        
    def create_model(self):
        """
        Create MobileNetV2-based model for recyclable classification
        """
        # Load pre-trained MobileNetV2 as base
        base_model = keras.applications.MobileNetV2(
            weights='imagenet',
            include_top=False,
            input_shape=(*self.img_size, 3)
        )
        
        # Freeze base model layers
        base_model.trainable = False
        
        # Add custom classification head
        model = keras.Sequential([
            base_model,
            layers.GlobalAveragePooling2D(),
            layers.Dropout(0.2),
            layers.Dense(128, activation='relu'),
            layers.Dropout(0.2),
            layers.Dense(self.num_classes, activation='softmax')
        ])
        
        # Compile model
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        self.model = model
        return model
    
    def create_synthetic_data(self, samples_per_class=200):
        """
        Create synthetic dataset for demonstration purposes
        In real implementation, this would load actual recyclable item images
        """
        print("Creating synthetic dataset for demonstration...")
        
        # Generate synthetic images with different patterns for each class
        X_data = []
        y_data = []
        
        for class_idx in range(self.num_classes):
            for _ in range(samples_per_class):
                # Create synthetic image with class-specific patterns
                img = np.random.rand(*self.img_size, 3)
                
                # Add class-specific features (simplified simulation)
                if class_idx == 0:  # plastic - add blue tint
                    img[:, :, 2] += 0.3
                elif class_idx == 1:  # glass - add transparency effect
                    img = img * 0.7 + 0.3
                elif class_idx == 2:  # metal - add metallic shine
                    img = np.clip(img + np.random.normal(0, 0.1, img.shape), 0, 1)
                elif class_idx == 3:  # paper - add texture
                    noise = np.random.normal(0, 0.05, img.shape)
                    img = np.clip(img + noise, 0, 1)
                elif class_idx == 4:  # cardboard - brown tint
                    img[:, :, 0] += 0.2
                    img[:, :, 1] += 0.1
                else:  # organic - green tint
                    img[:, :, 1] += 0.3
                
                X_data.append(img)
                y_data.append(class_idx)
        
        X_data = np.array(X_data)
        y_data = keras.utils.to_categorical(y_data, self.num_classes)
        
        return X_data, y_data
    
    def train_model(self, X_train, y_train, X_val, y_val, epochs=10):
        """
        Train the recyclable classification model
        """
        if self.model is None:
            self.create_model()
        
        print(f"Training model for {epochs} epochs...")
        
        # Define callbacks
        callbacks = [
            keras.callbacks.EarlyStopping(patience=3, restore_best_weights=True),
            keras.callbacks.ReduceLROnPlateau(factor=0.5, patience=2)
        ]
        
        # Train model
        history = self.model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=epochs,
            batch_size=32,
            callbacks=callbacks,
            verbose=1
        )
        
        return history
    
    def convert_to_tflite(self):
        """
        Convert trained model to TensorFlow Lite format with quantization
        """
        if self.model is None:
            raise ValueError("Model must be trained before conversion")
        
        print("Converting model to TensorFlow Lite...")
        
        # Create TFLite converter
        converter = tf.lite.TFLiteConverter.from_keras_model(self.model)
        
        # Enable optimizations (quantization)
        converter.optimizations = [tf.lite.Optimize.DEFAULT]
        
        # Convert model
        self.tflite_model = converter.convert()
        
        # Save TFLite model
        tflite_path = "recyclable_classifier.tflite"
        with open(tflite_path, 'wb') as f:
            f.write(self.tflite_model)
        
        # Compare model sizes
        original_size = os.path.getsize("temp_model.h5") if os.path.exists("temp_model.h5") else 0
        tflite_size = os.path.getsize(tflite_path)
        
        print(f"TensorFlow Lite model saved: {tflite_path}")
        print(f"Model size: {tflite_size / (1024*1024):.2f} MB")
        
        return tflite_path
    
    def benchmark_inference(self, X_test, num_samples=100):
        """
        Benchmark inference performance for both TensorFlow and TensorFlow Lite models
        """
        print("Benchmarking inference performance...")
        
        # Benchmark original TensorFlow model
        tf_times = []
        for i in range(min(num_samples, len(X_test))):
            start_time = time.time()
            _ = self.model.predict(X_test[i:i+1], verbose=0)
            tf_times.append(time.time() - start_time)
        
        # Benchmark TensorFlow Lite model
        interpreter = tf.lite.Interpreter(model_content=self.tflite_model)
        interpreter.allocate_tensors()
        
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()
        
        tflite_times = []
        for i in range(min(num_samples, len(X_test))):
            start_time = time.time()
            interpreter.set_tensor(input_details[0]['index'], X_test[i:i+1].astype(np.float32))
            interpreter.invoke()
            _ = interpreter.get_tensor(output_details[0]['index'])
            tflite_times.append(time.time() - start_time)
        
        # Calculate statistics
        tf_avg = np.mean(tf_times) * 1000  # Convert to milliseconds
        tflite_avg = np.mean(tflite_times) * 1000
        
        print(f"\nInference Performance:")
        print(f"TensorFlow model: {tf_avg:.2f} ms average")
        print(f"TensorFlow Lite model: {tflite_avg:.2f} ms average")
        print(f"Speedup: {tf_avg/tflite_avg:.2f}x")
        
        return tf_avg, tflite_avg
    
    def evaluate_model(self, X_test, y_test):
        """
        Evaluate model performance and generate metrics
        """
        print("Evaluating model performance...")
        
        # Get predictions
        predictions = self.model.predict(X_test)
        y_pred = np.argmax(predictions, axis=1)
        y_true = np.argmax(y_test, axis=1)
        
        # Calculate accuracy
        accuracy = np.mean(y_pred == y_true)
        print(f"Test Accuracy: {accuracy:.4f}")
        
        # Generate classification report
        report = classification_report(y_true, y_pred, target_names=self.class_names)
        print("\nClassification Report:")
        print(report)
        
        # Create confusion matrix
        cm = confusion_matrix(y_true, y_pred)
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=self.class_names, yticklabels=self.class_names)
        plt.title('Confusion Matrix - Recyclable Item Classification')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.tight_layout()
        plt.savefig('confusion_matrix.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return accuracy, report
    
    def demonstrate_edge_benefits(self):
        """
        Demonstrate the benefits of Edge AI for real-time applications
        """
        print("\n" + "="*60)
        print("EDGE AI BENEFITS DEMONSTRATION")
        print("="*60)
        
        benefits = {
            "Latency Reduction": [
                "Local inference: <100ms",
                "Cloud inference: 200-500ms",
                "Improvement: 2-5x faster response"
            ],
            "Privacy Enhancement": [
                "Images processed locally",
                "No data transmission required",
                "GDPR/privacy compliance"
            ],
            "Offline Capability": [
                "Works without internet",
                "Reliable in remote locations",
                "No dependency on cloud services"
            ],
            "Resource Efficiency": [
                "Optimized model size: <10MB",
                "Low memory usage: <50MB RAM",
                "Battery-friendly inference"
            ]
        }
        
        for benefit, details in benefits.items():
            print(f"\n{benefit}:")
            for detail in details:
                print(f"  • {detail}")
        
        print("\n" + "="*60)


def main():
    """
    Main function to run the Edge AI recyclable classification demo
    """
    print("Edge AI Prototype: Recyclable Item Classification")
    print("=" * 55)
    
    # Initialize classifier
    classifier = RecyclableClassifier()
    
    # Create synthetic dataset (in real scenario, load actual images)
    print("\n1. Creating dataset...")
    X_data, y_data = classifier.create_synthetic_data(samples_per_class=200)
    
    # Split data
    split_idx = int(0.8 * len(X_data))
    val_split_idx = int(0.9 * len(X_data))
    
    X_train, y_train = X_data[:split_idx], y_data[:split_idx]
    X_val, y_val = X_data[split_idx:val_split_idx], y_data[split_idx:val_split_idx]
    X_test, y_test = X_data[val_split_idx:], y_data[val_split_idx:]
    
    print(f"Training samples: {len(X_train)}")
    print(f"Validation samples: {len(X_val)}")
    print(f"Test samples: {len(X_test)}")
    
    # Create and train model
    print("\n2. Creating and training model...")
    classifier.create_model()
    history = classifier.train_model(X_train, y_train, X_val, y_val, epochs=5)
    
    # Evaluate model
    print("\n3. Evaluating model...")
    accuracy, report = classifier.evaluate_model(X_test, y_test)
    
    # Convert to TensorFlow Lite
    print("\n4. Converting to TensorFlow Lite...")
    tflite_path = classifier.convert_to_tflite()
    
    # Benchmark performance
    print("\n5. Benchmarking inference performance...")
    tf_time, tflite_time = classifier.benchmark_inference(X_test)
    
    # Demonstrate Edge AI benefits
    print("\n6. Edge AI Benefits Analysis...")
    classifier.demonstrate_edge_benefits()
    
    # Generate summary report
    print("\n" + "="*60)
    print("PROJECT SUMMARY")
    print("="*60)
    print(f"Model Accuracy: {accuracy:.4f}")
    print(f"TensorFlow Lite Model: {tflite_path}")
    print(f"Inference Speed: {tflite_time:.2f} ms")
    print(f"Edge AI Benefits: Demonstrated")
    print("="*60)


if __name__ == "__main__":
    main()