# Part 2: Case Study Application (40 points)

## Scenario

A hospital wants an AI system to predict patient readmission risk within 30 days of discharge.

---

## Problem Scope (5 points)

### Problem Definition

**Problem Statement:**
Develop an AI-powered predictive system to identify patients at high risk of hospital readmission within 30 days of discharge, enabling proactive intervention and improved patient outcomes while reducing healthcare costs.

### Objectives

1. **Primary Clinical Objective**:

   - Achieve ≥80% accuracy in predicting 30-day readmission risk
   - Maintain high recall (≥75%) to minimize missed high-risk patients
   - Provide predictions at discharge to enable timely intervention

2. **Operational Objective**:

   - Reduce hospital readmission rates by 15-20% through targeted interventions
   - Optimize allocation of post-discharge care resources (home health, follow-up appointments)
   - Decrease readmission-related costs by $2-3 million annually

3. **Quality Improvement Objective**:
   - Improve patient outcomes and satisfaction through personalized discharge planning
   - Enhance care coordination between hospital and community providers
   - Meet CMS quality metrics and avoid readmission penalties

### Stakeholders

**1. Clinical Staff**

- **Physicians**: Need accurate risk assessments for discharge planning decisions
- **Nurses**: Require actionable insights for patient education and discharge instructions
- **Case Managers**: Use predictions to prioritize patients for intensive care coordination
- **Social Workers**: Address social determinants of health for high-risk patients

**2. Hospital Administration**

- **Quality Improvement Teams**: Track readmission metrics and intervention effectiveness
- **Financial Officers**: Manage readmission penalties and cost savings
- **IT Department**: Implement, maintain, and integrate the AI system with existing infrastructure
- **Chief Medical Officer**: Oversee clinical validation and adoption

**3. Patients and Families**

- **Patients**: Benefit from personalized discharge plans and reduced readmission risk
- **Family Caregivers**: Receive clear instructions and support for home care
- **Patient Advocates**: Ensure system fairness and patient rights protection

**4. External Stakeholders**

- **Insurance Payers**: Monitor quality metrics and cost-effectiveness
- **CMS (Centers for Medicare & Medicaid Services)**: Track hospital performance
- **Regulatory Bodies**: Ensure compliance with healthcare regulations
- **Community Healthcare Providers**: Coordinate post-discharge care

---

## Data Strategy (10 points)

### Proposed Data Sources

#### 1. Electronic Health Records (EHR)

**Demographics:**

- Age, gender, race, ethnicity, marital status
- Primary language, education level
- Geographic location (zip code)

**Clinical Data:**

- Primary and secondary diagnoses (ICD-10 codes)
- Procedures performed (CPT codes)
- Comorbidities (Charlson Comorbidity Index)
- Vital signs (blood pressure, heart rate, temperature, oxygen saturation)
- Laboratory results (complete blood count, metabolic panel, cardiac markers)
- Medications (current prescriptions, medication adherence history)
- Allergies and adverse drug reactions

**Utilization History:**

- Previous hospitalizations (number, dates, reasons)
- Emergency department visits in past year
- Outpatient visits and specialty consultations
- Length of current hospital stay
- ICU admissions and duration

#### 2. Administrative and Billing Data

- Insurance type (Medicare, Medicaid, Private, Uninsured)
- Insurance authorization status
- Discharge disposition (home, skilled nursing facility, rehabilitation, hospice)
- Admission source (ER, transfer, elective)
- Hospital service line (medicine, surgery, cardiology, etc.)

#### 3. Social Determinants of Health (SDOH)

- Socioeconomic status indicators (income level, employment status)
- Housing stability and living situation
- Caregiver availability and support system
- Transportation access
- Food security status
- Health literacy level

#### 4. Post-Discharge Planning Data

- Scheduled follow-up appointments
- Home health services ordered
- Durable medical equipment needs
- Medication reconciliation status
- Patient education completion

#### 5. External Data Sources

- Pharmacy fill data (medication adherence)
- Claims data from payers
- Community health resources availability
- Area deprivation index (neighborhood socioeconomic conditions)

### Two Ethical Concerns

#### Ethical Concern 1: Patient Privacy and Data Security

**Issue:**
Electronic Health Records contain highly sensitive Protected Health Information (PHI) including medical diagnoses, mental health conditions, substance abuse history, and genetic information. Unauthorized access or data breaches could cause severe harm to patients.

**Specific Risks:**

- **Data Breaches**: Exposure of PHI to unauthorized parties leading to identity theft, discrimination, or stigmatization
- **Re-identification Risk**: De-identified data could be re-identified through linkage with other datasets
- **Insider Threats**: Hospital staff accessing patient records without legitimate clinical need
- **Third-Party Access**: AI vendors or cloud providers potentially accessing sensitive data
- **Data Retention**: Storing data longer than necessary increases exposure risk

**Mitigation Strategies:**

1. **HIPAA Compliance**: Implement comprehensive HIPAA safeguards

   - Encryption at rest (AES-256) and in transit (TLS 1.3)
   - Multi-factor authentication for system access
   - Role-based access control (RBAC) limiting data access to authorized personnel only
   - Comprehensive audit logging of all data access and modifications

2. **Data Minimization**: Collect and use only necessary data

   - Apply "minimum necessary" principle for data access
   - De-identify data for model training when possible
   - Implement data retention policies with automatic deletion

3. **Security Infrastructure**:

   - Regular security assessments and penetration testing
   - Intrusion detection and prevention systems
   - Secure development lifecycle for AI system
   - Business Associate Agreements (BAA) with all vendors

4. **Patient Rights**:
   - Obtain informed consent for data use in AI systems
   - Provide transparency about how data is used
   - Allow patients to opt-out of AI-based predictions
   - Establish clear data access and correction procedures

#### Ethical Concern 2: Algorithmic Bias and Health Equity

**Issue:**
AI models trained on historical healthcare data may perpetuate or amplify existing healthcare disparities, leading to unequal care for underrepresented populations.

**Specific Risks:**

- **Demographic Underrepresentation**: Training data may not adequately represent minority racial/ethnic groups, low-income populations, or rural communities
- **Historical Bias**: Past discriminatory practices embedded in historical data (e.g., unequal access to care, biased clinical decisions)
- **Proxy Discrimination**: Using features like zip code or insurance type as proxies for protected characteristics
- **Measurement Bias**: Medical devices and tests may have different accuracy across populations (e.g., pulse oximeters less accurate on darker skin)
- **Outcome Bias**: Using healthcare costs as proxy for health needs disadvantages populations with less access to care

**Real-World Example:**
A widely-used algorithm for managing chronic diseases systematically underestimated the health needs of Black patients because it used healthcare costs as a proxy for health needs. Black patients historically had less access to care and thus lower costs, despite having greater health needs.

**Mitigation Strategies:**

1. **Diverse and Representative Data**:

   - Actively collect data from diverse patient populations
   - Ensure adequate representation across demographics (race, ethnicity, age, gender, socioeconomic status)
   - Partner with community health centers serving underrepresented populations
   - Use stratified sampling to balance training data

2. **Fairness-Aware Model Development**:

   - Evaluate model performance separately for each demographic subgroup
   - Track multiple fairness metrics (demographic parity, equal opportunity, predictive parity)
   - Set minimum performance thresholds for all subgroups (e.g., F1 score ≥ 0.75 for every group)
   - Apply fairness-aware machine learning techniques (reweighting, adversarial debiasing)

3. **Bias Detection and Auditing**:

   - Conduct regular bias audits throughout development and deployment
   - Use tools like IBM AI Fairness 360 or Google's What-If Tool
   - Implement continuous monitoring for disparate impact
   - Establish bias response team to investigate and address disparities

4. **Stakeholder Engagement**:

   - Include diverse perspectives in model development (clinicians from various backgrounds, patient advocates, community representatives)
   - Conduct community review sessions before deployment
   - Establish transparent reporting of model performance across groups
   - Create feedback mechanisms for reporting bias concerns

5. **Clinical Validation**:
   - Prospective validation on diverse patient cohorts
   - External validation at hospitals serving different populations
   - Regular retraining with updated, diverse data
   - Human oversight for all high-stakes decisions

### Preprocessing Pipeline Design

#### Step 1: Data Collection and Integration

**Actions:**

- Extract data from multiple sources (EHR, billing, SDOH databases)
- Merge datasets using unique patient identifiers
- Create master patient record with all relevant features
- Document data lineage and sources

**Output:** Raw integrated dataset

#### Step 2: Data Quality Assessment

**Actions:**

- Identify missing values (percentage per feature)
- Detect duplicate records
- Check for data entry errors and outliers
- Assess data completeness and consistency
- Document data quality issues

**Output:** Data quality report

#### Step 3: Handling Missing Data

**Actions:**

- **Categorical Variables**:
  - Create "Unknown" category for missing values
  - Use mode imputation for low missingness (<5%)
- **Numerical Variables**:
  - Mean/median imputation for lab values with low missingness
  - KNN imputation for correlated features (e.g., vital signs)
  - Multiple imputation for high missingness (>20%)
- **Indicator Variables**: Create binary flags for missingness patterns
- **Threshold**: Drop features with >50% missing data

**Output:** Dataset with imputed values

#### Step 4: Outlier Detection and Handling

**Actions:**
