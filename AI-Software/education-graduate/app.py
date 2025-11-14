import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import os

# Page configuration
st.set_page_config(
    page_title="Student Success Predictor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Load model artifacts
@st.cache_resource
def load_model():
    try:
        with open('model_artifacts.pkl', 'rb') as f:
            artifacts = pickle.load(f)
        return artifacts
    except FileNotFoundError:
        st.error("Model file not found. Please run train_model.py first.")
        return None

# Load data for visualization
@st.cache_data
def load_data():
    from ucimlrepo import fetch_ucirepo
    education = fetch_ucirepo(id=697)
    X = education.data.features
    y = education.data.targets
    
    # Clean column names
    cols = pd.Series(X.columns)
    for dup in cols[cols.duplicated()].unique():
        dup_indices = cols[cols == dup].index
        for i, idx in enumerate(dup_indices):
            if i > 0:
                cols[idx] = f"{dup}_{i}"
    X.columns = cols
    X.columns = X.columns.str.replace('[^A-Za-z0-9_]+', '_', regex=True)
    X.columns = X.columns.str.strip('_')
    
    df = X.copy()
    df['Target'] = y.values.ravel()
    return df

# Initialize session state for tracking
if 'predictions_history' not in st.session_state:
    st.session_state.predictions_history = []

# Main app
def main():
    st.markdown('<h1 class="main-header">🎓 Student Success Predictor</h1>', unsafe_allow_html=True)
    st.markdown("### AI-Driven Solution for UN SDG 4: Quality Education")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["🏠 Home", "📊 Data Visualization", "🔮 Prediction", "📈 Real-time Tracking", "💬 Insights & Chat"])
    
    model_artifacts = load_model()
    
    if page == "🏠 Home":
        show_home()
    elif page == "📊 Data Visualization":
        show_visualizations()
    elif page == "🔮 Prediction":
        if model_artifacts:
            show_prediction(model_artifacts)
        else:
            st.error("Please train the model first by running: python train_model.py")
    elif page == "📈 Real-time Tracking":
        show_tracking()
    elif page == "💬 Insights & Chat":
        show_insights()

def show_home():
    st.header("Welcome to the Student Success Predictor")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Project Overview")
        st.write("""
        This application uses machine learning to predict student outcomes and help educational 
        institutions identify at-risk students early, supporting **UN SDG 4: Quality Education**.
        
        **Key Features:**
        - Predict student dropout risk
        - Visualize educational data patterns
        - Track predictions in real-time
        - Generate actionable insights
        """)
        
    with col2:
        st.subheader("📚 About the Dataset")
        st.write("""
        The dataset includes information from a higher education institution covering:
        - **Demographics**: Age, gender, nationality
        - **Academic Path**: Previous qualifications, grades
        - **Socio-economic Factors**: Scholarship status, tuition fees
        - **Performance**: First and second semester results
        
        **Target Classes:**
        - Dropout
        - Enrolled
        - Graduate
        """)
    
    st.divider()
    
    # Quick stats
    st.subheader("📊 Quick Statistics")
    df = load_data()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Students", f"{len(df):,}")
    with col2:
        st.metric("Features", f"{len(df.columns)-1}")
    with col3:
        dropout_rate = (df['Target'] == 'Dropout').sum() / len(df) * 100
        st.metric("Dropout Rate", f"{dropout_rate:.1f}%")
    with col4:
        st.metric("Model Accuracy", "~78%")

def show_visualizations():
    st.header("📊 Data Visualization & Analysis")
    
    df = load_data()
    
    # Target distribution
    st.subheader("1. Student Outcome Distribution")
    target_counts = df['Target'].value_counts()
    fig = px.pie(values=target_counts.values, names=target_counts.index, 
                 title="Distribution of Student Outcomes",
                 color_discrete_sequence=px.colors.qualitative.Set3)
    st.plotly_chart(fig, use_container_width=True)
    
    # Feature correlation
    st.subheader("2. Top Feature Correlations")
    model_artifacts = load_model()
    if model_artifacts:
        top_features = model_artifacts['feature_names']
        corr_data = df[top_features].corr()
        
        fig = px.imshow(corr_data, 
                       title="Correlation Matrix of Top 10 Features",
                       color_continuous_scale='RdBu_r',
                       aspect='auto')
        st.plotly_chart(fig, use_container_width=True)
    
    # Feature importance
    st.subheader("3. Feature Importance")
    if model_artifacts:
        model = model_artifacts['model']
        feature_names = model_artifacts['feature_names']
        importances = model.feature_importances_
        
        feat_imp_df = pd.DataFrame({
            'Feature': feature_names,
            'Importance': importances
        }).sort_values('Importance', ascending=True)
        
        fig = px.bar(feat_imp_df, x='Importance', y='Feature', orientation='h',
                    title="Feature Importance for Prediction",
                    color='Importance', color_continuous_scale='Viridis')
        st.plotly_chart(fig, use_container_width=True)
    
    # Age distribution by outcome
    st.subheader("4. Age Distribution by Outcome")
    if 'Age_at_enrollment' in df.columns:
        fig = px.box(df, x='Target', y='Age_at_enrollment', 
                    title="Age Distribution Across Student Outcomes",
                    color='Target')
        st.plotly_chart(fig, use_container_width=True)

def show_prediction(model_artifacts):
    st.header("🔮 Student Outcome Prediction")
    
    st.write("Enter student information to predict their likelihood of dropout, enrollment, or graduation.")
    
    model = model_artifacts['model']
    feature_names = model_artifacts['feature_names']
    label_encoder = model_artifacts['label_encoder']
    
    # Create input form
    st.subheader("Student Information")
    
    col1, col2 = st.columns(2)
    
    input_data = {}
    
    # Common features with reasonable defaults
    feature_defaults = {
        'Curricular_units_2nd_sem_approved': (0, 10, 5),
        'Curricular_units_2nd_sem_grade': (0.0, 20.0, 12.0),
        'Curricular_units_1st_sem_approved': (0, 10, 5),
        'Tuition_fees_up_to_date': (0, 1, 1),
        'Curricular_units_1st_sem_grade': (0.0, 20.0, 12.0),
        'Curricular_units_2nd_sem_evaluations': (0, 20, 6),
        'Age_at_enrollment': (17, 60, 20),
        'Curricular_units_1st_sem_evaluations': (0, 20, 6),
        'Admission_grade': (0.0, 200.0, 120.0),
        'Curricular_units_2nd_sem_enrolled': (0, 10, 6)
    }
    
    for i, feature in enumerate(feature_names):
        col = col1 if i % 2 == 0 else col2
        
        with col:
            if feature in feature_defaults:
                min_val, max_val, default_val = feature_defaults[feature]
                if isinstance(default_val, float):
                    input_data[feature] = st.number_input(
                        feature.replace('_', ' ').title(),
                        min_value=float(min_val),
                        max_value=float(max_val),
                        value=float(default_val),
                        step=0.1
                    )
                else:
                    input_data[feature] = st.number_input(
                        feature.replace('_', ' ').title(),
                        min_value=int(min_val),
                        max_value=int(max_val),
                        value=int(default_val)
                    )
            else:
                input_data[feature] = st.number_input(
                    feature.replace('_', ' ').title(),
                    value=0.0
                )
    
    if st.button("🎯 Predict Outcome", type="primary"):
        # Prepare input
        input_df = pd.DataFrame([input_data])
        
        # Make prediction
        prediction = model.predict(input_df)[0]
        prediction_proba = model.predict_proba(input_df)[0]
        
        # Decode prediction
        predicted_class = label_encoder.inverse_transform([prediction])[0]
        
        # Display results
        st.divider()
        st.subheader("Prediction Results")
        
        col1, col2, col3 = st.columns(3)
        
        classes = label_encoder.classes_
        for i, (col, class_name, prob) in enumerate(zip([col1, col2, col3], classes, prediction_proba)):
            with col:
                is_predicted = class_name == predicted_class
                st.metric(
                    class_name,
                    f"{prob*100:.1f}%",
                    delta="Predicted" if is_predicted else None
                )
        
        # Visualization
        fig = go.Figure(data=[
            go.Bar(x=classes, y=prediction_proba*100, 
                  marker_color=['#ff6b6b' if c == predicted_class else '#4ecdc4' for c in classes])
        ])
        fig.update_layout(
            title="Prediction Probabilities",
            xaxis_title="Outcome",
            yaxis_title="Probability (%)",
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Save to history
        st.session_state.predictions_history.append({
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'prediction': predicted_class,
            'probabilities': {c: f"{p*100:.1f}%" for c, p in zip(classes, prediction_proba)}
        })
        
        # Recommendations
        st.subheader("💡 Recommendations")
        if predicted_class == "Dropout":
            st.warning("""
            **High Risk of Dropout Detected**
            - Schedule immediate counseling session
            - Review academic support options
            - Consider financial aid assessment
            - Implement mentorship program
            """)
        elif predicted_class == "Enrolled":
            st.info("""
            **Student Currently Enrolled**
            - Monitor academic progress regularly
            - Encourage participation in study groups
            - Provide career guidance resources
            """)
        else:
            st.success("""
            **On Track for Graduation**
            - Continue current support level
            - Offer advanced learning opportunities
            - Prepare for career placement
            """)

def show_tracking():
    st.header("📈 Real-time Prediction Tracking")
    
    if not st.session_state.predictions_history:
        st.info("No predictions made yet. Go to the Prediction page to make your first prediction.")
        return
    
    # Display history
    st.subheader("Prediction History")
    
    history_df = pd.DataFrame(st.session_state.predictions_history)
    st.dataframe(history_df, use_container_width=True)
    
    # Statistics
    st.subheader("Session Statistics")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Predictions", len(st.session_state.predictions_history))
    
    with col2:
        dropout_count = sum(1 for p in st.session_state.predictions_history if p['prediction'] == 'Dropout')
        st.metric("Dropout Predictions", dropout_count)
    
    with col3:
        graduate_count = sum(1 for p in st.session_state.predictions_history if p['prediction'] == 'Graduate')
        st.metric("Graduate Predictions", graduate_count)
    
    # Visualization
    prediction_counts = history_df['prediction'].value_counts()
    fig = px.bar(x=prediction_counts.index, y=prediction_counts.values,
                title="Distribution of Predictions in This Session",
                labels={'x': 'Outcome', 'y': 'Count'},
                color=prediction_counts.index)
    st.plotly_chart(fig, use_container_width=True)
    
    # Clear history button
    if st.button("🗑️ Clear History"):
        st.session_state.predictions_history = []
        st.rerun()

def show_insights():
    st.header("💬 Insights & Analysis")
    
    st.subheader("🎯 Key Findings")
    
    st.write("""
    Based on the analysis of student data, here are the critical insights:
    
    **1. Most Important Predictors:**
    - Second semester approved curricular units
    - Second semester grades
    - First semester performance
    - Tuition fee payment status
    - Age at enrollment
    
    **2. Risk Factors for Dropout:**
    - Low grades in first semester
    - Few approved curricular units
    - Delayed tuition payments
    - High number of evaluations without approvals
    
    **3. Success Indicators:**
    - Consistent academic performance
    - Timely completion of curricular units
    - Strong admission grades
    - Regular attendance and evaluation participation
    """)
    
    st.divider()
    
    st.subheader("📋 Intervention Strategies")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Early Warning System:**
        - Monitor first semester performance closely
        - Flag students with <50% approval rate
        - Track tuition payment status
        - Identify students with multiple failed evaluations
        """)
    
    with col2:
        st.markdown("""
        **Support Programs:**
        - Academic tutoring for struggling students
        - Financial counseling and aid programs
        - Peer mentorship initiatives
        - Career guidance and motivation workshops
        """)
    
    st.divider()
    
    st.subheader("💭 Interactive Q&A")
    
    question = st.selectbox(
        "Select a question:",
        [
            "What is the most important factor in predicting dropout?",
            "How accurate is the prediction model?",
            "What can institutions do to reduce dropout rates?",
            "How does this support UN SDG 4?",
            "What data is needed for prediction?"
        ]
    )
    
    answers = {
        "What is the most important factor in predicting dropout?": 
            "The most important factor is the number of curricular units approved in the second semester, followed by the grades achieved. These metrics directly reflect student engagement and academic capability.",
        
        "How accurate is the prediction model?":
            "The LightGBM model achieves approximately 78% accuracy with balanced precision and recall across all three classes (Dropout, Enrolled, Graduate). This provides reliable predictions for early intervention.",
        
        "What can institutions do to reduce dropout rates?":
            "Institutions should implement early warning systems, provide targeted academic support, offer financial counseling, create mentorship programs, and maintain regular communication with at-risk students identified by the model.",
        
        "How does this support UN SDG 4?":
            "This solution directly supports SDG 4 (Quality Education) by helping institutions identify at-risk students early, enabling timely interventions, improving retention rates, and ensuring more students complete their education successfully.",
        
        "What data is needed for prediction?":
            "The model requires student demographic information, academic performance data (grades, approved units, evaluations), enrollment details, and socio-economic indicators like tuition payment status and scholarship information."
    }
    
    st.info(answers[question])

if __name__ == "__main__":
    main()
