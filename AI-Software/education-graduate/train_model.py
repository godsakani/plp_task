"""
Train and export the best performing model for student dropout prediction
"""
from ucimlrepo import fetch_ucirepo
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from lightgbm import LGBMClassifier
import pickle
import warnings
warnings.filterwarnings('ignore')

print("Fetching dataset...")
education = fetch_ucirepo(id=697)

X = education.data.features
y = education.data.targets

# Convert target to 1D array
y = y.values.ravel()

# Handle duplicate columns
cols = pd.Series(X.columns)
for dup in cols[cols.duplicated()].unique():
    dup_indices = cols[cols == dup].index
    for i, idx in enumerate(dup_indices):
        if i > 0:
            cols[idx] = f"{dup}_{i}"
X.columns = cols

# Clean column names
X.columns = X.columns.str.replace('[^A-Za-z0-9_]+', '_', regex=True)
X.columns = X.columns.str.strip('_')

print(f"Dataset shape: {X.shape}")

# Encode target
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# Train initial model to get feature importance
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

print("Training initial model for feature selection...")
lgbm_initial = LGBMClassifier(random_state=42, verbose=-1, n_estimators=100)
lgbm_initial.fit(X_train, y_train)

# Get top 10 features
feature_importances = lgbm_initial.feature_importances_
features_df = pd.DataFrame({'Feature': X.columns, 'Importance': feature_importances})
features_df = features_df.sort_values(by='Importance', ascending=False)
top_features_names = features_df.head(10)['Feature'].tolist()

print(f"\nTop 10 features selected:")
for i, feat in enumerate(top_features_names, 1):
    print(f"{i}. {feat}")

# Train final model with selected features
X_selected = X[top_features_names]
X_train_final, X_test_final, y_train_final, y_test_final = train_test_split(
    X_selected, y_encoded, test_size=0.2, random_state=42
)

print("\nTraining final model...")
final_model = LGBMClassifier(random_state=42, verbose=-1, n_estimators=150, learning_rate=0.05)
final_model.fit(X_train_final, y_train_final)

# Calculate accuracy
accuracy = final_model.score(X_test_final, y_test_final)
print(f"Model accuracy: {accuracy:.4f}")

# Save model, scaler, label encoder, and feature names
model_artifacts = {
    'model': final_model,
    'label_encoder': le,
    'feature_names': top_features_names,
    'all_feature_names': X.columns.tolist(),
    'target_classes': le.classes_
}

with open('model_artifacts.pkl', 'wb') as f:
    pickle.dump(model_artifacts, f)

print("\nModel artifacts saved to 'model_artifacts.pkl'")
print(f"Target classes: {le.classes_}")
