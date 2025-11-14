# 🎓 Student Success Predictor

## Deploy Link

[Deploy-Link](https://education-graduate-3cgwdpvhysywuznyhjk6du.streamlit.app/)
An AI-driven solution for predicting student dropout and academic success, supporting **UN SDG 4: Quality Education**.

## Overview

This application uses machine learning to analyze student data and predict their likelihood of dropout, continued enrollment, or graduation. By identifying at-risk students early, educational institutions can provide timely interventions to improve retention and success rates.

## Features

- **📊 Data Visualization:** Interactive charts showing student outcome distributions, feature correlations, and importance rankings
- **🔮 Prediction System:** Real-time prediction of student outcomes with probability scores
- **📈 Real-time Tracking:** Monitor prediction history and session statistics
- **💬 Insights & Analysis:** Key findings, intervention strategies, and interactive Q&A

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or download this repository**

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

### Running the Application

**Step 1: Train the model**

```bash
python train_model.py
```

This will:

- Download the dataset from UCI ML Repository
- Train the LightGBM model
- Save model artifacts to `model_artifacts.pkl`

**Step 2: Launch the Streamlit app**

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

## Usage Guide

### 1. Home Page

- View project overview and quick statistics
- Understand the dataset and target classes

### 2. Data Visualization

- Explore student outcome distributions
- Analyze feature correlations and importance
- View demographic patterns

### 3. Prediction

- Enter student information in the form
- Click "Predict Outcome" to get results
- View probability scores for each outcome class
- Receive automated recommendations

### 4. Real-time Tracking

- Monitor all predictions made in the current session
- View session statistics and distributions
- Export prediction history

### 5. Insights & Chat

- Read key findings from the analysis
- Explore intervention strategies
- Get answers to common questions

## Model Information

**Algorithm:** LightGBM Classifier

**Performance:**

- Accuracy: ~78%
- Precision: ~78%
- Recall: ~78%
- F1-Score: ~78%

**Top 10 Features:**

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

## Dataset

**Source:** UCI Machine Learning Repository (ID: 697)

**Description:** Data from a higher education institution covering students enrolled in various undergraduate programs including agronomy, design, education, nursing, journalism, management, social service, and technologies.

**Target Classes:**

- **Dropout:** Student left the program
- **Enrolled:** Student currently active
- **Graduate:** Student completed the program

## Project Structure

```
.
├── app.py                      # Main Streamlit application
├── train_model.py              # Model training script
├── education_analysis.ipynb    # Exploratory data analysis
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── Report.md                   # Detailed project report
└── model_artifacts.pkl         # Trained model (generated)
```

## Contributing to UN SDG 4

This project supports **UN Sustainable Development Goal 4: Quality Education** by:

- Identifying at-risk students early for timely intervention
- Providing data-driven insights to improve educational outcomes
- Helping institutions allocate support resources effectively
- Reducing dropout rates and improving graduation rates
- Promoting inclusive and equitable quality education

## Technical Stack

- **Python 3.8+**
- **Streamlit** - Web application framework
- **LightGBM** - Machine learning model
- **scikit-learn** - ML utilities and preprocessing
- **pandas & numpy** - Data manipulation
- **plotly** - Interactive visualizations
- **ucimlrepo** - Dataset access

## Troubleshooting

**Issue:** Model file not found error

- **Solution:** Run `python train_model.py` first to generate the model

**Issue:** Package installation errors

- **Solution:** Ensure you're using Python 3.8+ and try: `pip install --upgrade pip` then reinstall requirements

**Issue:** Dataset download fails

- **Solution:** Check your internet connection and try again. The UCI repository must be accessible.

## Future Enhancements

- [ ] Multi-institutional model training
- [ ] Temporal analysis with LSTM/RNN
- [ ] SHAP values for explainable predictions
- [ ] Mobile application
- [ ] Automated email alerts
- [ ] Integration with student information systems
- [ ] Intervention effectiveness tracking

## License

This project is for educational purposes and supports the UN Sustainable Development Goals.

## Acknowledgments

- UCI Machine Learning Repository for the dataset
- United Nations for the Sustainable Development Goals framework
- Open-source community for the excellent tools and libraries

## Contact

For questions or suggestions about this project, please open an issue in the repository.

---

**Built with ❤️ to support Quality Education for All**
