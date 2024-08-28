import os
import json
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math 
# read docs/statistics.txt
stat_path = os.path.join(os.getcwd(), 'docs/results/statistics.txt')

with open(stat_path, 'r', encoding='utf-8') as file:
    statistics = file.readlines()

new_key_list = []
# text to json
for stat in statistics:
    stat = json.loads(stat)
    for key in stat.keys():
        if key == "Predictor_Variables":
            vars = stat[key]
            for var in vars:
                if var == "Detailed_Variables":
                    new_key_list.append(vars[var])

temp = []
variables = []

for nk in new_key_list:
    for n in nk:
        variables.append(n['Variable'])

processed_variables = []
def flatten_list(lst):
    """
    Flattens a list of lists, removing duplicates.
    """
    flat_list = []
    for item in lst:
        if isinstance(item, list):
            flat_list.extend(item)
        else:
            flat_list.append(item)
    return list(set(flat_list))

def combine_and_flatten_dictionaries(dict1, dict2):
    """
    Combines two dictionaries, flattening and removing duplicates from value lists.
    """
    combined_dict = {}

    # Combine keys and values from both dictionaries
    for key in set(dict1) | set(dict2):
        values = []
        if key in dict1:
            values.extend(dict1[key])
        if key in dict2:
            values.extend(dict2[key])
        
        combined_dict[key] = flatten_list(values)

    return combined_dict

def extract_odds_ratios(data):
    # Extract the detailed variables
    detailed_vars = data['Detailed_Variables']
    
    # Create a list of tuples (Variable, Odds_Ratio_OR)
    extracted_data = [(entry['Variable'], entry['Odds_Ratio_OR']) for entry in detailed_vars]
    
    return extracted_data

def calculate_mean_std(data):
    # Filter out non-numeric values
    numeric_values = []
    for item in data:
        # Check if the item can be converted to float
        try:
            numeric_values.append(float(item))
        except:
            # Ignore non-numeric values
            pass

    # Calculate mean and standard deviation
    mean = np.mean(numeric_values)
    std = np.std(numeric_values)

    return mean, std


a = {
  "Age": [
    ">75",
    "per year increase",
    ">65 years",
    ">60 years",
    ">70 years",
    ">80 years",
    ">45 years",
    ">=65 years"
  ],
  "Gender": [
    "male sex",
    "Male gender",
    "Female sex"
  ],
  "Obesity": [
    "severe obesity",
    "Obesity (BMI>30)",
    "obese",
    "BMI > 35",
    "higher BMI",
    "obesity class III"
  ],
  "Cancer": [
    "active cancer",
    "cancer"
  ],
  "Diabetes": [
    "Diabetes",
    "complicated diabetes mellitus",
    "Diabetes Mellitus"
  ],
  "Respiratory Diseases": [
    "COPD",
    "Chronic Obstructive Pulmonary Disease (COPD)",
    "ARDS",
    "Respiratory disease",
    "COPD/lung disease",
    "chronic hypoxemic respiratory failure with oxygen requirement"
  ],
  "Cardiovascular Diseases": [
    "Hyperlipidemia",
    "Cardiovascular Disease (CVD)",
    "heart failure",
    "Congestive heart failure (CHF)",
    "Coronary heart disease",
    "arrhythmia"
  ],
  "Kidney Diseases": [
    "Chronic kidney disease",
    "CKD",
    "acute kidney injury"
  ],
  "Smoking Status": [
    "current smoker"
  ],
  "Blood Pressure and Heart Conditions": [
    "Hypertension",
    "higher heart rate",
    "arrhythmia"
  ],
  "Coagulation and Blood Issues": [
    "increase D-dimer",
    "Coagulation dysfunctions",
    "D-dimer > 0.5mg/L",
    "Neutrophil/Lymphocyte ratio"
  ],
  "Blood Type": [
    "O+ Blood Group"
  ],
  "Liver Diseases": [
    "liver disease"
  ],
  "Immunocompromised Status": [
    "Immunocompromised Status",
    "primary immunodeficiency",
    "long-term steroid/immunomodulatory use"
  ],
  "Socioeconomic Factors": [
    "government insurance or no insurance",
    "residence in low-income areas",
    "non-white races",
    "black race/ethnicity",
    "homelessness",
    "low income",
    "Bangladeshi ethnicity"
  ],
  "Neurological Conditions": [
    "dementia",
    "Cerebrovascular disease (CVD)",
    "Chronic neurological diseases"
  ],
  "Infection and Inflammation Markers": [
    "C-reactive protein (CRP)",
    "H-CRP"
  ],
  "Symptoms": [
    "Dyspnea",
    "Shortness of Breath",
    "Body Weakness",
    "Fever",
    "Weakness",
    "Shivering",
    "Fatigue",
    "Dry cough",
    "Anorexia",
    "Anosmia",
    "Ageusia",
    "Dizziness",
    "Sweating",
    "Nausea",
    "Vomiting",
    "Abdominal pain",
    "Pharyngalgia",
    "dyspnoea",
    "lymphocytes (lower)",
    "reticulation (CT)",
    "intrathoracic lymph node enlargement (CT)",
    "pleural effusions (CT)"
  ],
  "Other Comorbidities": [
    "malnutrition",
    "metabolic syndrome",
    "taking opioids",
    "Malignancy",
    "Sequential organ failure assessment score",
    "Acute physiology and chronic health evaluation-2 score",
    "Chronic obstructive pulmonary disease",
    "Pneumonia",
    "Decreased oxygen saturation",
    "Emphysema",
    "Vaccination \">=2 doses\"",
    "Respiratory rate > 24 breaths per min",
    "SOFA score >= 2",
    "chronic hypoxemic respiratory failure with oxygen requirement",
    "Socioeconomic Status",
    "Specific diagnoses potentially associated with severe COVID-19",
    "HIV/AIDS",
    "SatO2/FiO2 ratio",
    "SOFA score",
    "CURB-65 score",
    "Presentation from long-term care facility",
    "Elevated total bilirubin",
    "Vasopressor initiation",
    "Development of renal failure",
    "Increased leukocyte count",
    "Alanine aminotransferase",
    "Aspartate transaminase",
    "Elevated lactate dehydrogenase",
    "Increased procalcitonin",
    "Corticosteroids (associated with a higher rate of ARDS)",
    "Any comorbidity",
    "neutrophil to lymphocyte ratio",
    "albumin",
    "chest computed tomography abnormalities",
    "Systolic blood pressure < 90 mmHg",
    "Respiratory rate > 24 per min",
    "Peripheral oxygen saturation < 92%",
    "Estimated glomerular filtration rate < 60 mL/min/1.73m2",
    "IL-6 > 100 pg/mL",
    "D-dimer > 2 mcg/mL",
    "Troponin > 0.03 ng/mL",
    "African American race",
    "Hydroxychloroquine use",
    "Previous history of pneumonia",
    "Residential area (Urban)",
    "Educational level"
  ]
}

b = {
  "Respiratory Diseases": ["Respiratory diseases", "Shortness of breath", "Loss of smell", "Loss of taste", "Runny nose", "Pulmonary circulation disorders", "COPD", "Asthma", "Chronic Obstructive Pulmonary Disease (COPD)", "Respiratory Rate", "Respiratory distress", "Respiratory frequency", "Dyspnea", "Chest distress", "Cough", "Pneumopathy", "Chronic obstructive pulmonary disease (COPD)", "Previous pneumonia"],
  "Cardiovascular Diseases": ["Cardiovascular diseases", "High blood pressure", "Hypertension", "Coronary Arteriosclerosis", "Heart failure", "Cardiomyopathy", "Ischemic heart disease", "Arrhythmia", "Stroke", "Cardiovascular Disease (CVD)", "Coronary artery disease", "Chronic heart disease", "Coronary heart disease (CHD)", "Cardiac disease"],
  "Metabolic and Endocrine Disorders": ["Obesity", "Diabetes Mellitus (DM)", "Diabetes", "Severe obesity", "Hyperlipidemia", "Dyslipidemia", "Type 1 diabetes", "Type 2 diabetes", "Type 2 diabetes (complications)", "Metabolic syndrome"],
  "Immunological and Hematological Disorders": ["Comorbidity", "Lymphopenia", "Immune checkpoint inhibitors", "Immunosuppression", "Lymphocyte count", "Hematological disease", "Immunodepression", "Autoimmune diseases"],
  "Kidney and Liver Diseases": ["Chronic kidney disease", "Chronic Kidney Disease (CKD)", "Chronic kidney failure", "Renal failure", "Kidney diseases", "Liver disease", "Chronic Liver Disease (CLD)", "Renal disease", "Kidney disease"],
  "Neurological and Psychiatric Disorders": ["Dementia (all causes)", "Neurological manifestations", "Neurological disease", "Severe mental illness", "Dementia", "Chronic neurological diseases", "Neuropathy", "Cognitive impairment"],
  "Cancer": ["Cancer", "Malignancy", "Neoplastic diseases"],
  "Other Comorbidities": ["Older age (> 65 years vs. < 65 years)", "Solid organ transplant", "Osteoporosis", "Down syndrome", "Chronic skin ulcers", "Sepsis", "Bacterial infections", "Acidosis", "Tuberculosis", "Immune deficiency or suppression", "Chronic lower respiratory tract disease", "Polypharmacy"],
  "Infection-Related Factors": ["ICU admitted patients", "Hospitalization in ICU", "Admission to ICU", "Intensive care unit admission", "Influenza vaccination", "Influenza antiviral", "COVID-19-positive or suspect close contact", "Large gathering attendance with a COVID-19-positive individual"],
  "Lifestyle Factors": ["Snacks and meals/day prior to COVID-19 infection", "Dietary habits (meat consumption) during COVID-19 infection", "Dietary supplements during COVID-19 infection", "Smokeless tobacco use", "Tobacco consumption", "Smoking", "Current smoker"],
  "Demographic Factors": ["Age", "Gender-male", "Sex", "Male sex", "Non-Hispanic black race/ethnicity", "gender", "race (Black vs. Other race)", "Asian ethnicity", "Hispanic ethnicity", "Urban residence", "Black race", "American Indian/Alaska Native/Pacific Islander race", "Hispanic ethnicity versus White", "Native American versus White", "Medicare insurance", "Publicly insured (Medicare)", "Publicly insured (Medicaid)", "Limited English proficiency"],
  "Vaccination Status": ["Triple vaccinated", "Double vaccinated"],
  "Clinical Measurements and Scores": ["SOFA score", "Length of hospital stay", "AKI", "Radiographic assessment of lung edema score", "Modified Early Warning Score (MEWS)", "Higher blood LDH at time of admission", "BMI", "Blood Oxygen Saturation", "Creatinine", "ALT", "Procalcitonin", "Lactic Acid", "Hemoglobin (Hb)", "Creatine kinase-MB (CK-MB)", "Lactate dehydrogenase (LDH)", "Procalcitonin (PCT)", "CT score", "Elevated C-reactive protein", "Increased Neutrophil count", "Low Lymphocyte count", "Platelets <150 × 10^3/μl", "C-reactive protein ≥100 μg/ml", "Oxygen saturation", "Elevated creatinine", "White cell count", "Body mass index (BMI)", "Initial C-reactive protein (CRP)", "AST", "Blood urea nitrogen", "Serum creatinine", "Platelet count", "C-reactive protein (CRP)", "Plasma albumin", "Blood glucose", "Urea level", "CRP", "IL-6", "Imaging manifestations", "White blood cell count (WBC)", "Platelet count (PLT)", "Fibrin degradation products (FDP)", "Oxygenation index (OI)", "Lymphocyte count (LYMPH)", "D-dimer", "Calcium ions (Ca+)"],
  "Symptoms": ["Fever", "Fatigue", "Headache", "Skeletal muscle pain", "Hospitalization", "Vomit", "Chest pain", "Muscle or joint pain", "Levels of lymphocytes", "Damage in both lungs within 3 days of admission", "Diarrhea", "Other symptom", "Chest tightness"],
  "Socioeconomic Factors": ["Median Household Income", "GDP per capita", "Medicaid dual-eligibility", "Age groups >35 years", "Male sex", "Age 80 versus 65", "Age \n(\">=80 vs. <50 years\")"],
  "Other Factors": ["Decreased taste/smell", "Systolic blood pressures \"/<=120", "Temperatures \"/>=99.0\\u00b0F", "Combined underlying diseases", "Acid-base balance disorder", "White blood cell diseases", "Hydronephrosis", "Morbid obesity", "Admission temperature per \x08C increase", "Log10 neutrophil-to-lymphocyte ratio (NLR)", "Platelets per 10 E + 9/L decrease", "Activated partial thromboplastin (aPTT) per second increase", "Log10 D-dimer per mg/l increase", "Log10 serum creatinine per \x085mol/L increase", "abnormal thorax computed tomography (CT)", "lower doses of anticoagulation", "high values of white blood cell", "aspartate aminotransferase", "lactate dehydrogenase", "ferritin", "chronic pulmonary disease", "Oxygen requirement at hospitalization", "Acute renal injury", "Oxygen supply", "Hemoptysis", "elderly age (>65 years)", "severe illness at admission", "critical illness at admission", "deep venous thrombosis", "hypernatremia", "elevated aspartate aminotransferase", "hypoalbuminemia", "low platelets level", "any comorbidity", "Time interval between onset and diagnosis", "Source of cases (imported or local)", "ICU admission", "Low oxygen saturation", "NIV", "residence in a care home"]
}

c1 = {
    "Age": ["Increasing age", "Older age", "age", "age over 65 years old", "Age", "Age", "Age", "Age", "Age", "Age", "Age", "Age over 65 years", "Older age (\">= 60 years\")", "Patient age", "Age", "Age", "Age", "Age", "Age"],
    "Gender": ["Male gender", "sex (male)", "Male", "male", "male sex"],
    "Ethnicity/Race": ["Hispanic ethnicity", "Non-Hispanic Black race", "Asian race"],
    "Cardiovascular and Renal Diseases": ["Hypertension without CVD or kidney disease", "Congestive heart failure", "Cerebrovascular disease", "Myocardial infarction history", "Hypertension", "Cardiovascular disease", "Chronic obstructive pulmonary disease", "hypertension", "cardiovascular disease (CVD)", "Essential hypertension", "Disorders of lipid metabolism", "Hypertension", "Cardiovascular disease", "Hypertension", "Diabetes mellitus", "Cardiovascular diseases", "Cerebrovascular disease", "Chronic kidney disease (CKD)", "Chronic obstructive pulmonary disease (COPD)", "Chronic kidney disease (CKD)", "Heart failure (HF)", "Hypertension", "Diabetes", "Smoking", "Hypertension", "Diabetes", "Smoking", "Diabetes", "heart disease", "hypertension", "lung disease", "chronic obstructive pulmonary disease/chronic bronchitis/emphysema", "kidney disease", "chronic respiratory system diseases", "chronic renal disease", "cardiovascular disease"],
    "Respiratory Conditions": ["Asthma history", "Chronic Kidney Disease", "Chronic obstructive pulmonary disease", "Respiratory diseases", "Asthma", "chronic obstructive pulmonary disease (COPD)", "interstitial lung disease"],
    "Metabolic and Endocrine Disorders": ["Obesity", "Diabetes", "obesity (BMI ≥25)", "diabetes", "Obesity", "Diabetes with complication", "obesity", "diabetes", "Diabetes", "Diabetes mellitus", "obesity", "morbid obesity", "diabetes", "insulin dependent diabetes mellitus"],
    "Blood and Immune Disorders": ["Leukocytosis", "Sepsis/Septic Shock", "collagen disease", "leukemia/lymphoma", "metastatic solid tumor", "Leukocytosis (>10 x 109/L)", "Neutrophilia (>75 x 109/L)", "anemia"],
    "Gastrointestinal Symptoms": ["GI symptoms", "Diarrhea", "abdominal pain", "diarrhea"],
    "Other Conditions": ["liver disease", "renal disease or dialysis", "cancer", "neurologic/neurodevelopmental condition", "mental health condition", "HIV/AIDS", "adrenal insufficiency", "prior transplantation", "chronic kidney disease", "history of chronic kidney disease"],
    "Clinical Findings and Symptoms": ["Household exposure", "Dyspnea on presentation", "Respiratory system compliance", "PaO2/FiO2", "Driving pressure", "PaCO2", "Lactate", "pH", "Creatinine", "Urea", "C-reactive protein", "Ferritin", "Neutrophils", "Lymphocytes", "Neutrophil-Lymphocyte Ratio", "Bilirubin", "Platelets", "Admission D-dimer >1000 ng/mL", "Admission CRP >200 mg/L", "Admission lymphopenia", "First recorded respiratory rate", "First recorded pulse oximetry", "Highest creatinine level on day of presentation", "Hospital's COVID-19 mortality rate", "Mechanical ventilation therapy", "highest creatinine > 1.5 mg/dL", "combined blood stream infection", "Exposure history", "Fatigue", "White blood cell count less than 4 × 10⁹ per L", "Lymphocyte count less than 0.8 × 10⁹ per L", "Ground glass opacity", "Both lungs affected", "White blood cell count", "Glucose", "Fever", "Duration from onset to admission", "Lactate level upon admission", "LYM (%) at admission", "Critical disease status", "High hypersensitive troponin I (>0.04 pg/mL)", "Administration of hypnotics", "BMI", "oxygen saturation", "temperature", "respiratory rate", "dyspnea", "lactate dehydrogenase level > 400 IU/L", "C-reactive protein > 20 mg/dl", "ferritin > 2000 ng/ml", "creatinine kinase > 1000 iu/l", "procalcitonin > 2.5 ng/ml", "D-dimer level > 3.0 \n/ml", "creatinine > 2 mg/dl", "dyspnea", "low oxygen saturation (SpO2 < 95%)", "respiratory discomfort", "supplemental oxygen required at admission", "sputum production", "Shortness of breath", "Fraction of inspired oxygen (FiO2) and respiratory rate", "Deoxyhaemoglobin levels", "Blood lactate levels", "Troponin T and creatinine levels", "Eosinophil counts", "CRP quartiles 3", "CRP quartiles 4", "Charlson index", "SaO2 upon admission", "Hydroxychloroquine prescription", "Systemic corticosteroids prescription", "Tocilizumab prescription", "Ratio admissions/hospital beds", "Wuhan exposure history greater than 2 weeks", "Myoglobin higher than 106 μg/L", "White blood cell higher than 10×10^9/L", "C-reactive protein higher than 10 mg/L", "chest tightness", "shortness of breath"]
}

c2 = {
  "Blood Parameters": [
    "C-reactive protein",
    "Blood urea nitrogen",
    "Blood creatinine",
    "Blood glucose",
    "Aspartate aminotransferase",
    "Platelets",
    "Mean corpuscular volume",
    "White blood cell count",
    "CRP (>4 mg/L)",
    "D-dimer (>0.55 mg/L)",
    "IL-2R (>710 U/mL)",
    "IL-8 (>62 pg/mL)",
    "IL-10 (>9.1 pg/mL)",
    "Fasting blood glucose (FBS)",
    "Total cholesterol (TC)",
    "Triglycerides (TG)",
    "LDL cholesterol",
    "HDL cholesterol",
    "Serum creatinine",
    "D-dimer",
    "Hemoglobin",
    "Neutrophils",
    "LDH",
    "High-sensitivity C-reactive protein",
    "Ferritin",
    "Lactate",
    "Prothrombin time",
    "Partial thromboplastin time",
    "Creatinine",
    "Alanine transaminase",
    "Alkaline phosphatase",
    "Total bilirubin",
    "Direct bilirubin",
    "Total protein",
    "Serum albumin"
  ],
  "Comorbidities": [
    "Asthma",
    "Diabetes",
    "Hypertension",
    "Cardiovascular Diseases",
    "Chronic liver disease",
    "Cancer",
    "Solid malignant tumor",
    "Chronic obstructive pulmonary disease (COPD)",
    "Myalgia or fatigue",
    "Acute cardiac injury",
    "Acute kidney injury",
    "Tumor/Cancer",
    "Chronic lung disease",
    "Arrhythmia",
    "Heart disease",
    "Pneumonia",
    "Dementia",
    "Atrial fibrillation",
    "Kidney failure",
    "Substance abuse",
    "Diabetes mellitus",
    "Liver dysfunction",
    "Bronchial asthma",
    "Cardiovascular and metabolic diseases",
    "Dyslipidemia",
    "Heart failure",
    "Chronic renal failure",
    "Ischemic heart disease",
    "Cardiac dysrhythmia",
    "OSA",
    "Anxiety",
    "Menstrual disorders",
    "Menopausal disorders",
    "Active malignancy",
    "Coagulopathy",
    "Fluid and electrolyte disorders",
    "Blood loss anemia",
    "Anorexia",
    "LDH elevation",
    "SOFA score increase",
    "Osmotic Pressure abnormality",
    "Chronic cerebrovascular disease",
    "Increased procalcitonin",
    "Thrombocytopenia",
    "Type 2 diabetes",
    "Depression",
    "Chronic kidney disease"
  ],
  "Demographic Factors": [
    "Age",
    "Sex",
    "Male sex",
    "Older age",
    "Age '>= 60 years'",
    "Age 65 or older"
  ],
  "Clinical Parameters": [
    "Number of Comorbidities",
    "CT score",
    "O2 saturation",
    "Body mass index (BMI)",
    "Dyspnea",
    "ARDS",
    "Shock",
    "Mechanical Ventilation",
    "Continuous Renal Replacement Therapy/Hemodialysis (CRRT/HD)",
    "Vasopressors",
    "Chills",
    "Body temperature",
    "Findings of pneumonia in chest X-ray",
    "Having one underlying disease",
    "Having two underlying diseases",
    "Having three or more underlying diseases",
    "NEWS2 Category II and higher",
    "Low lymphocyte counts",
    "NEWS2 Category III",
    "Decreasing lymphocyte count",
    "PF ratio",
    "Lymphocyte (LYM) count",
    "Obesity",
    "Active smoking",
    "SpO2 levels",
    "Acute respiratory distress syndrome (ARDS)",
    "Chronic cardiovascular disease",
    "Prevalent cerebrovascular disease",
    "Prevalent cardiovascular disease",
    "Smoking",
    "Increased D-Dimer",
    "History of diabetes",
    "Lymphopenia",
    "BMI",
    "Self-reported dizziness/lightheadedness",
    "Temperature >= 99.5°F",
    "Tachycardia",
    "Oxygen saturation < 95%",
    "Primary language (Spanish)"
  ]
}

d1 = {
  "Inflammatory Markers": ["Procalcitonin", "White blood cell count", "Lymphocyte count", "Neutrophil-to-lymphocyte ratio (NLR)", "Platelet-to-lymphocyte ratio (PLR)", "Interleukin-6 (IL-6)", "C-reactive protein (CRP)", "Platelet counts", "Serum sodium level", "C-reactive protein (CRP) level", "Neutrophil count"],
  "Nutritional and Metabolic Parameters": ["Total Protein (TP)", "Albumin (ALB)", "Nutrition support needed", "Correction of electrolyte imbalance", "Body mass index (BMI)", "Albumin", "Blood glucose", "Prothrombin time", "Total cholesterol"],
  "Cardiovascular and Respiratory Conditions": ["Hypertension", "Cardiovascular disease", "Bronchial asthma", "Chronic Kidney Disease", "Chronic heart disease", "Chronic respiratory disease", "Congestive heart failure", "COPD and bronchiectasis"],
  "COVID-19 Specific Factors": ["Complications from COVID-19", "Previous history of COVID-19 infection", "Hospitalisation due to COVID-19"],
  "Symptoms and Clinical Signs": ["Dyspnea", "Low Triage Oxygenation", "Fever", "Shortness of breath", "Chills", "Frailty", "Renal failure", "Liver failure", "Cough", "Chest pain", "Headache", "Muscle ache", "Runny nose", "Sore throat", "Abdominal pain", "Diarrhoea", "Temperature between 37.5 and 37.9 °C", "Temperature above 38 °C"],
  "Chronic Diseases and Conditions": ["Obesity", "Diabetes", "Malignancy", "Chronic liver disease", "Non-traumatic cerebral infarction", "Diabetes mellitus", "Chronic kidney disease", "Tuberculosis", "Chronic ulcer of skin", "Acute cerebrovascular disease", "Rheumatoid arthritis", "Menstrual disorders"],
  "Immunological and Infectious Diseases": ["Oncology/oncohematology patient", "HIV infection", "Immunodeficiencies", "Autoimmune diseases", "Organ transplant", "Asplenia", "Other immunosuppressive condition", "Immune related disease"],
  "Neurological and Psychological Factors": ["Stroke/dementia", "Other neurological disease", "Altered sensorium/seizures", "WHO ordinal scale 4 or above"],
  "Demographic Factors": ["Age", "Sex", "Ethnicity (Black)", "Education level (medium)", "Education level (low)", "female biological sex", "male gender", "non-white ethnicity"],
  "Lifestyle Factors": ["Smoking", "Body mass index (Obese class III '>=40 kg/m2')", "Smoking (Former)", "Smoking (Current)", "Cigarette smoking in the last 30 days", "Sanitizing one’s phone", "At least weekly exercise"],
  "Clinical and Laboratory Parameters": ["Affected lobe numbers", "CRP level", "Chest tightness/dyspnea", "Smoking history", "Age >65", "Creatinine", "LDH", "Respiratory Rate"],
  "Other Risk Factors": ["Deprivation (IMD quintile)", "Presence of any treatment limitation", "Anemia", "Any viral symptoms among household members 6–12 days prior", "The maximum number of individuals the participant interacted with within 6 feet in the past 6–12 days", "Higher subjective social status", "Cancer diagnosis", "30-day mortality", "Oxygen saturation", "Radiological severity score", "Previous ventricular arrhythmia", "Use of P2Y12-inhibitors", "Higher C-reactive protein", "Lower albumin", "Higher troponin T", "Female infertility", "Obstructive sleep apnea", "Hepatic steatosis and other liver diseases"]
}

d2 = {
  "Age and Gender": ["Increasing age", "Age", "Age 31-45", "Age > 46", "Age >50 years", "Age 65+ years", "older age", "Older age", "Advanced age (>= 65 years)", "Male sex", "Gender", "Sex"],
  "Cardiovascular and Respiratory Conditions": [
    "High systolic blood pressure", "Hypertension", "cardiovascular disease", "chronic obstructive pulmonary disease", "Coronary artery disease", "Heart disease", "Heart failure", "IHD", "Lung diseases", "Chronic lung disease", "Chronic respiratory disease", "Supraventricular tachyarrhythmia", "Respiratory failure", "Cardiovascular complications during COVID-19", "Cardiovascular comorbidities or risk factors", "Cardiovascular diseases", "Systolic pressure", "Cardiovascular disease (CVD)", "Chronic obstructive pulmonary disease (COPD)"
  ],
  "Metabolic and Nutritional Factors": ["diabetes", "obesity", "BMI", "Low BMI", "inadequate fruit and vegetable consumption", "mortality (BMI \">=\" 35 kg/m2)", "need for IMV (BMI \">=\" 35 kg/m2)", "Diabetes", "Diabetes mellitus", "Diabetes mellitus type II", "Diabetic mellitus", "Coexisting Diabetes Mellitus"],
  "Lifestyle and Behavioral Factors": ["ever smoking", "sedentary lifestyle", "Smoking", "Current smoker", "history of smoking status"],
  "Genetic and Familial Factors": ["number of affected persons in family"],
  "Socioeconomic and Demographic Factors": ["Median household income", "ethnicity", "Black versus White ethnicity", "Higher education"],
  "Comorbid Conditions": ["Neoplasms", "Cancer", "Neoplasia", "Anorexia", "Dyspnea", "Autoimmune disease", "Oral steroid use", "type of hematologic malignancy", "cancer-related life expectancy", "Allergies", "Alzheimer disease", "Immunodeficiency", "Liver disease", "Malignancy", "Chronic comorbid conditions (at least one)", "Chronic comorbid conditions (two)", "Chronic comorbid conditions (three or more)", "Other chronic diseases", "Any type of cancer", "Colorectal cancer", "Gastrointestinal malignancies", "active cancer", "Active cancer diagnosis", "Chronic kidney disease", "end stage renal disease or stage 5 CKD", "stage 4 CKD", "stage 5 CKD/dialysis", "kidney transplant", "stage 3 CKD", "Renal insufficiency", "Renal failure", "Asthma", "Urinary incontinence", "Chronic kidney disease (CKD)", "Prostate malignant neoplasm", "Acute myocardial infarction", "Other ischemic heart disease", "Hemorrhagic conditions and other diseases of blood and blood-forming organs"],
  "Infectious Diseases and Related Conditions": ["HIV/AIDS", "HIV", "HIV positive", "Corticosteroid Therapy"],
  "Clinical Signs and Symptoms": ["Respiratory Symptoms", "Cardiac Symptoms", "Neurological Symptoms", "Other Symptoms", "Decreased consciousness", "Coma", "Seizures", "Nausea", "Fever", "Chills", "Myalgia or arthralgia", "Depression", "Anosmia", "Dyspnoea", "Dyspnea or tachypnea", "Cough", "Travel", "Heart rate", "fever", "Dyspnea"],
  "Laboratory and Diagnostic Findings": ["Lymphopenia", "Neutrophil-lymphocytic ratio (NLR) >3", "Lactate dehydrogenase (LDH)", "SaO2<95%", "Urea \">50 mg/dl", "Pulse Rate \">100/min", "C-reactive protein (CRP)", "PO2 < 80 mm Hg", "Blood injection", "Injection of platelets or FFP", "High number of comorbidities", "Neutrophil/lymphocyte ratio", "Elevated lactate dehydrogenase", "Elevated D-dimer", "Elevated C-reactive protein", "multilobe involvement of the chest", "Bilateral pulmonary infiltrates", "Aspartate aminotransferase (AST)", "D-dimer", "Lactate dehydrogenase"],
  "Therapeutic and Procedural Factors": ["mechanical ventilation with oxygen therapy", "Mechanical ventilation", "Dialysis", "Surgery/Trauma", "Intranasal oxygen care", "Anti-TNF drugs", "mechanical ventilation with oxygen therapy", "Mechanical ventilation", "Admission to ICU", "Lactate dehydrogenase (LDH)", "Urea \">50 mg/dl"],
  "Epidemiological Factors": ["Travel", "Resident", "Being a healthcare worker", "European region", "sample size <= 500", "Previous contact with COVID"],
  "Age-Specific Factors": ["Children in the household (aged <5 years)", "Children in the household (aged 5-18 years)", "age >79", "higher European Cooperative Oncology Group/World Health Organization performance status"],
  "Other Risk Factors": ["COVID-19 symptoms", "COVID-19-directed therapy", "severity of COVID-19", "race", "comorbidities", "hypertension", "diabetes", "ethnicity", "age", "Respiratory Rate", "Previous contact with COVID", "History of coronary heart disease", "C-reactive protein (CRP)", "Aspartate aminotransferase (AST)", "D-dimer", "Neutrophil/lymphocyte ratio", "Autoimmune disease", "Bilateral pulmonary infiltrates", "Elevated lactate dehydrogenase", "Elevated D-dimer", "Elevated C-reactive protein", "Myalgia or arthralgia", "Chills", "Fever", "Dyspnoea", "Depression", "Lymphopenia", "Anosmia", "Any type of cancer", "Colorectal cancer", "Gastrointestinal malignancies", "older age", "history of smoking status", "number of comorbidities", "more advanced performance status", "active cancer", "diabetes", "hypertension", "heart disease", "Age", "Renal insufficiency", "Lactate dehydrogenase", "Thrombocytopenia", "Older age", "Male", "Cardiovascular disease", "Chronic respiratory disease", "Diabetes", "Obesity", "Hypertension", "end stage renal disease or stage 5 CKD", "congestive heart failure", "chronic airway obstruction", "type 2 diabetes", "stage 4 CKD", "stage 5 CKD/dialysis", "kidney transplant", "stage 3 CKD", "Age", "Diabetes", "Cardiovascular disease", "Malignancy", "Surgery/Trauma", "HIV", "Chronic pulmonary disease", "Asthma", "Chronic kidney disease", "Diabetic mellitus", "HIV positive", "Worsening conditions", "Age 55 and above years", "obesity", "mortality (BMI \">=\" 35 kg/m2)", "need for IMV (BMI \">=\" 35 kg/m2)", "Any type of chronic comorbid condition", "Hypertension", "Diabetes", "Cardiovascular diseases", "Respiratory diseases", "Other chronic diseases", "Chronic comorbid conditions (at least one)", "Chronic comorbid conditions (two)", "Chronic comorbid conditions (three or more)", "Comorbidities (>=2)", "Cough", "Active cancer diagnosis", "Advanced age (>= 65 years)"]
}


keys = {
  "Age": ["Age", "Age-Specific Factors", "Age and Gender"],
  "Gender": ["Gender", "Age and Gender"],
  "Ethnicity/Race": ["Ethnicity/Race"],
  "Obesity": ["Obesity"],
  "Cancer": ["Cancer", "Other Comorbidities"],
  "Diabetes": ["Diabetes", "Metabolic and Endocrine Disorders"],
  "Respiratory Diseases": ["Respiratory Diseases", "Respiratory Conditions", "Cardiovascular and Respiratory Conditions", "Respiratory Conditions"],
  "Cardiovascular Diseases": ["Cardiovascular Diseases", "Blood Pressure and Heart Conditions", "Cardiovascular and Renal Diseases", "Cardiovascular and Respiratory Conditions"],
  "Kidney Diseases": ["Kidney Diseases", "Kidney and Liver Diseases", "Cardiovascular and Renal Diseases"],
  "Liver Diseases": ["Liver Diseases", "Kidney and Liver Diseases"],
  "Smoking Status": ["Smoking Status", "Lifestyle Factors", "Lifestyle and Behavioral Factors"],
  "Blood Type": ["Blood Type"],
  "Immunocompromised Status": ["Immunocompromised Status"],
  "Socioeconomic Factors": ["Socioeconomic Factors", "Socioeconomic and Demographic Factors"],
  "Neurological Conditions": ["Neurological Conditions", "Neurological and Psychiatric Disorders", "Neurological and Psychological Factors"],
  "Infection and Inflammation Markers": ["Infection and Inflammation Markers", "Inflammatory Markers"],
  "Symptoms": ["Symptoms", "Clinical Findings and Symptoms", "Symptoms and Clinical Signs", "Clinical Signs and Symptoms"],
  "Metabolic and Endocrine Disorders": ["Metabolic and Endocrine Disorders", "Metabolic and Nutritional Factors"],
  "Immunological and Hematological Disorders": ["Immunological and Hematological Disorders", "Blood and Immune Disorders"],
  "Gastrointestinal Symptoms": ["Gastrointestinal Symptoms"],
  "Other Conditions": ["Other Conditions", "Other Risk Factors", "Other Factors"],
  "Clinical Measurements and Scores": ["Clinical Measurements and Scores", "Clinical Parameters"],
  "Vaccination Status": ["Vaccination Status"],
  "Demographic Factors": ["Demographic Factors", "Socioeconomic and Demographic Factors"],
  "Clinical Findings and Symptoms": ["Clinical Findings and Symptoms", "Clinical Signs and Symptoms"],
  "Blood Parameters": ["Blood Parameters"],
  "Comorbidities": ["Comorbidities", "Comorbid Conditions", "Other Comorbidities"],
  "Inflammatory Markers": ["Inflammatory Markers"],
  "Nutritional and Metabolic Parameters": ["Nutritional and Metabolic Parameters"],
  "COVID-19 Specific Factors": ["COVID-19 Specific Factors"],
  "Chronic Diseases and Conditions": ["Chronic Diseases and Conditions"],
  "Immunological and Infectious Diseases": ["Immunological and Infectious Diseases"],
  "Lifestyle Factors": ["Lifestyle Factors", "Lifestyle and Behavioral Factors"],
  "Clinical and Laboratory Parameters": ["Clinical and Laboratory Parameters"],
  "Genetic and Familial Factors": ["Genetic and Familial Factors"],
  "Infectious Diseases and Related Conditions": ["Infectious Diseases and Related Conditions"],
  "Laboratory and Diagnostic Findings": ["Laboratory and Diagnostic Findings"],
  "Therapeutic and Procedural Factors": ["Therapeutic and Procedural Factors"],
  "Epidemiological Factors": ["Epidemiological Factors"]
}

summarized_dict = combine_and_flatten_dictionaries(d2, combine_and_flatten_dictionaries(d1, combine_and_flatten_dictionaries(c2, combine_and_flatten_dictionaries(c1, combine_and_flatten_dictionaries(a,b)))))

Predictor_Variables = []
for stat in statistics:
    stat = json.loads(stat)
    for key in stat.keys():
        if key == "Predictor_Variables":
            Predictor_Variables.append(stat[key])


cd = combine_and_flatten_dictionaries(keys, summarized_dict)
print(cd)
new_dict = {}
for key in cd.keys():
    new_dict[key] = []

var_and_odds = []
for var in Predictor_Variables:
    try:
        Detailed_Variables = (var['Detailed_Variables'])
        extracted_data = [(entry['Variable'], entry['Odds_Ratio_OR']) for entry in Detailed_Variables]
        var_and_odds.append(extracted_data)
    except:
        continue

for k, v in cd.items():
    for var in var_and_odds:
        for item in var:
            if item[0] in v:
                new_dict[k].append(item[1])

c = 0
result = []

for key, values in new_dict.items():
    mean, std = calculate_mean_std(values)
    if math.isnan(mean):
        continue
    if math.isnan(std):
        continue
    
    result.append({'Category': key, 'Mean': mean, 'Std': std})

for item in result:
    item['Mean'] = np.log(item['Mean'])
# sort by mean
result = sorted(result, key=lambda k: k['Mean'], reverse=True)

data = result

df = pd.DataFrame(data)

# Plotting the graph
plt.figure(figsize=(10, 6))
plt.gca().invert_yaxis()
bars = plt.barh(df['Category'], df['Mean'], color='blue', alpha=0.5, align='center', ecolor='black', capsize=10)

plt.ylabel('Category')
plt.xlabel('Mean Value')
plt.title('Inverted Vertical Bar Graph')
plt.tight_layout()
plt.show()
