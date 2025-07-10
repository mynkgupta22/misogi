"""
Data downloader utility for medical documents.
"""
import os
from pathlib import Path
from typing import List
from src.config import RAW_DATA_DIR

def download_sample_documents() -> List[str]:
    """
    Create sample medical documents.
    Returns a list of file paths.
    """
    print("Creating sample medical documents...")
    
    # Create raw data directory if it doesn't exist
    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    
    # Sample documents
    sample_docs = {
        "hypertension.txt": """
Title: Hypertension Management Guidelines

1. Definition and Classification
- Hypertension is defined as persistent elevation of blood pressure ≥130/80 mmHg
- Classifications:
  * Normal: <120/80 mmHg
  * Elevated: 120-129/<80 mmHg
  * Stage 1: 130-139/80-89 mmHg
  * Stage 2: ≥140/90 mmHg
  * Hypertensive Crisis: >180/120 mmHg

2. Risk Factors
- Non-modifiable:
  * Age (>65 years)
  * Family history
  * Gender
  * Ethnicity
- Modifiable:
  * Obesity
  * High sodium intake
  * Physical inactivity
  * Excessive alcohol consumption
  * Smoking

3. Treatment Approach
- Lifestyle Modifications:
  * Reduce sodium intake (<2300mg/day)
  * Regular physical activity
  * Weight management
  * DASH diet
  * Limit alcohol consumption
- Pharmacological Treatment:
  * First-line medications:
    - ACE inhibitors
    - ARBs
    - Calcium channel blockers
    - Thiazide diuretics
  * Second-line medications:
    - Beta blockers
    - Alpha blockers
    - Central alpha agonists

4. Monitoring and Follow-up
- Regular blood pressure measurements
- Medication adherence assessment
- Laboratory monitoring
- Lifestyle modification progress
- Complications screening
""",
        "diabetes.txt": """
Title: Type 2 Diabetes Management Protocol

1. Diagnosis Criteria
- Fasting Plasma Glucose ≥126 mg/dL
- 2-hour Plasma Glucose ≥200 mg/dL during OGTT
- HbA1c ≥6.5%
- Random Plasma Glucose ≥200 mg/dL with symptoms

2. Initial Assessment
- Medical history
- Physical examination
- Laboratory evaluation
- Cardiovascular risk assessment
- Screening for complications

3. Treatment Goals
- Glycemic targets:
  * HbA1c <7.0% for most adults
  * Individualized targets based on:
    - Age
    - Comorbidities
    - Life expectancy
    - Hypoglycemia risk
- Blood pressure <140/90 mmHg
- LDL cholesterol reduction

4. Management Strategy
- Lifestyle Modifications:
  * Medical nutrition therapy
  * Regular physical activity
  * Weight management
  * Smoking cessation
- Pharmacological Therapy:
  * First-line: Metformin
  * Second-line options:
    - Sulfonylureas
    - DPP-4 inhibitors
    - SGLT2 inhibitors
    - GLP-1 receptor agonists
  * Insulin therapy when indicated

5. Monitoring and Follow-up
- Regular HbA1c testing
- Blood glucose monitoring
- Cardiovascular risk assessment
- Complications screening
- Medication adjustment
""",
        "asthma.txt": """
Title: Asthma Management Guidelines

1. Diagnosis
- Clinical history
- Physical examination
- Pulmonary function testing
- Bronchial challenge testing
- Allergy testing when indicated

2. Classification
- Intermittent
- Mild persistent
- Moderate persistent
- Severe persistent

3. Treatment Approach
- Quick-Relief Medications:
  * Short-acting beta agonists (SABA)
  * Anticholinergics
- Long-Term Control:
  * Inhaled corticosteroids
  * Long-acting beta agonists (LABA)
  * Leukotriene modifiers
  * Biologics for severe asthma

4. Action Plan
- Daily management
- Recognition of worsening symptoms
- Emergency response protocol
- When to seek medical attention

5. Monitoring
- Symptom diary
- Peak flow measurements
- Medication adherence
- Environmental trigger control
- Regular follow-up visits
"""
    }
    
    downloaded_files = []
    for filename, content in sample_docs.items():
        file_path = Path(RAW_DATA_DIR) / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        downloaded_files.append(str(file_path))
    
    print(f"Successfully created {len(downloaded_files)} sample documents")
    return downloaded_files

if __name__ == "__main__":
    download_sample_documents() 