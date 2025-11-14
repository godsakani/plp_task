# Student Success Predictor - Project Report

## Executive Summary

This project develops an AI-driven solution to predict student dropout and academic success, directly supporting **UN Sustainable Development Goal 4: Quality Education**. Using machine learning on real higher education data, the system identifies at-risk students early, enabling timely interventions to improve retention and graduation rates.

## Problem Statement

Student dropout is a critical challenge in higher education, affecting:

- Individual career prospects and lifetime earnings
- Institutional reputation and funding
- National education quality metrics
- Achievement of UN SDG 4 targets

Early identification of at-risk students allows institutions to provide targeted support before it's too late.

## Dataset Overview

**Source:** UCI Machine Learning Repository (ID: 697)

**Scope:** Higher education institution data covering multiple undergraduate programs including agronomy, design, education, nursing, journalism, management, social service, and technologies.

**Features:** 37 attributes including:

- Demographics (age, gender, nationality)
- Academic background (previous qualifications, admission grades)
- Socio-economic factors (scholarship status, tuition fees, parental education)
- Academic performance (semester grades, approved units, evaluations)

**Target Variable:** Three-class classification

- Dropout
- Enrolled
- Graduate

**Dataset Characteristics:**

- Total samples: 4,424 students
- Imbalanced classes (majority: Graduate)
- Mix of numerical and categorical features

## Methodology

### 1. Data Preprocessing

- Handled duplicate column names
- Cleaned feature names for model compatibility
- Encoded categorical target variable
- Split data: 80% training, 20% testing

### 2. Feature Engineering

- Analyzed feature importance using LightGBM
- Selected top 10 most predictive features:
  1. Curricular units 2nd semester (approved)
  2. Curricular units 2nd semester (grade)
  3. Curricular units 1st semester (approved)
  4. Tuition fees up to date
  5. Curricular units 1st semester (grade)
  6. Curricular units 2nd semester (evaluations)
  7. Age at enrollment
  8. Curricular units 1st semester (evaluations)
  9. Admission grade
  10. Curricular units 2nd semester (enrolled)

### 3. Model Selection & Training

**Models Evaluated:**

- Random Forest Classifier
- K-Nearest Neighbors (KNN)
- Support Vector Machine (SVM)
- LightGBM Classifier ⭐
- Logistic Regression

**Best Performer:** LightGBM Classifier

- Accuracy: ~78%
- Balanced performance across all three classes
- Fast training and prediction
- Handles imbalanced data well

### 4. Model Optimization

- Feature selection reduced dimensionality from 37 to 10 features
- Maintained prediction accuracy while improving interpretability
- Optimized hyperparameters for production deployment

## Results

### Model Performance

| Metric               | Score |
| -------------------- | ----- |
| Accuracy             | 78.0% |
| Precision (weighted) | 77.8% |
| Recall (weighted)    | 78.0% |
| F1-Score (weighted)  | 77.5% |

### Key Insights

**Critical Success Factors:**

- Second semester performance is the strongest predictor
- First semester grades provide early warning signals
- Tuition payment status correlates with dropout risk
- Age at enrollment affects completion likelihood

**Risk Indicators:**

- Low approval rates in first semester
- Poor grades despite multiple evaluations
- Delayed or missing tuition payments
- High number of enrolled units with low completion

## Application Features

### 1. Interactive Dashboard

- Clean, intuitive interface built with Streamlit
- Multi-page navigation for different functionalities
- Responsive design for various screen sizes

### 2. Data Visualization

- Student outcome distribution (pie chart)
- Feature correlation heatmap
- Feature importance rankings
- Age distribution by outcome

### 3. Prediction System

- User-friendly input form for student data
- Real-time prediction with probability scores
- Visual representation of prediction confidence
- Automated risk assessment and recommendations

### 4. Real-time Tracking

- Session-based prediction history
- Statistical summaries of predictions
- Distribution analysis of predicted outcomes
- Export capability for further analysis

### 5. Insights & Analysis

- Key findings from data analysis
- Intervention strategy recommendations
- Interactive Q&A system
- Best practices for dropout prevention

## Impact on UN SDG 4

This solution contributes to **SDG 4: Quality Education** by:

1. **Ensuring Inclusive Education:** Identifies students who need additional support regardless of background
2. **Improving Completion Rates:** Early intervention prevents dropouts
3. **Enhancing Education Quality:** Data-driven insights improve institutional practices
4. **Promoting Equal Access:** Highlights socio-economic barriers to completion
5. **Supporting Lifelong Learning:** Helps students stay on track to complete their education

## Implementation Recommendations

### For Educational Institutions

**Short-term (0-3 months):**

- Deploy prediction system for incoming cohort
- Train staff on system usage and interpretation
- Establish intervention protocols for at-risk students

**Medium-term (3-12 months):**

- Integrate with existing student information systems
- Develop automated alert mechanisms
- Create targeted support programs based on risk factors

**Long-term (1+ years):**

- Continuously retrain model with new data
- Expand to predict other outcomes (GPA, time to graduation)
- Share insights across departments for holistic support

### Technical Deployment

**Infrastructure:**

- Cloud hosting (AWS, Azure, or GCP) for scalability
- Secure database for student data (GDPR/FERPA compliant)
- API integration with student management systems

**Monitoring:**

- Track prediction accuracy over time
- Monitor for model drift
- Regular retraining with updated data

**Security:**

- Encrypt sensitive student data
- Implement role-based access control
- Audit trail for all predictions and interventions

## Limitations & Future Work

### Current Limitations

- Model trained on single institution data (may not generalize)
- Class imbalance affects minority class predictions
- Requires complete data for accurate predictions
- No temporal analysis of student progression

### Future Enhancements

1. **Multi-institutional Model:** Train on data from multiple universities
2. **Temporal Modeling:** Use LSTM/RNN for time-series student data
3. **Explainable AI:** Implement SHAP values for individual predictions
4. **Intervention Tracking:** Measure effectiveness of support programs
5. **Mobile Application:** Enable on-the-go access for advisors
6. **Automated Alerts:** Email/SMS notifications for high-risk students
7. **Integration:** Connect with LMS, financial systems, and counseling services

## Conclusion

The Student Success Predictor demonstrates how AI can meaningfully contribute to achieving UN SDG 4 by providing educational institutions with actionable insights to support student success. With 78% accuracy, the system reliably identifies at-risk students, enabling timely interventions that can significantly improve retention and graduation rates.

By combining machine learning with an intuitive interface and actionable recommendations, this solution empowers educators to make data-driven decisions that positively impact student outcomes and advance quality education for all.

## Technical Stack

- **Machine Learning:** scikit-learn, LightGBM
- **Data Processing:** pandas, numpy
- **Visualization:** plotly, seaborn, matplotlib
- **Web Framework:** Streamlit
- **Model Persistence:** pickle
- **Data Source:** UCI ML Repository

## References

1. UCI Machine Learning Repository - Predict Students' Dropout and Academic Success Dataset
2. United Nations Sustainable Development Goal 4: Quality Education
3. LightGBM Documentation
4. Streamlit Documentation

---

**Project Date:** November 2025  
**Model Version:** 1.0  
**Last Updated:** November 14, 2025
