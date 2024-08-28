import metapub
import json
from urllib.request import urlretrieve
import textract
import os
from utils import send_message

system_message = """
Suppose you are a competent medical researcher. 
You want to develop an algorithm that can predict whether a person with COVID-19 will become critically ill by investigating the risk factors for predicting the progression of the disease to critical illness and the weight of each risk factor. 
Read the documentation I have provided, and fill in the empty values in the following json template. 
If it appears that there is no information for that key, put "None" for value.
To answer the question, your response must reflect all the necessary information from the paper. 
An answer consisting of a few short sentences should be assigned to value. 
You should only return a json template with the value filled in. You should not return any other text. 
Think step by step and fill in the values one by one.
"""

resp_format = """
    {
        "Study_Characteristics": {
            "Study_Design": "Type of research study",
            "Study_Period": "Time frame of the study",
            "Location_of_the_Study": "Geographic location",
            "Sample_Size": "Number of participants"
        },
        "Participant_Demographics": {
            "Age_Distribution": "Age range and average",
            "Gender_Distribution": "Breakdown by gender",
            "Ethnicity": "Ethnic backgrounds",
            "Pre-existing_Health_Conditions": "Existing medical conditions",
            "Socioeconomic_Status": "Economic and social position"
        },
        "COVID-19_Specific_Information": {
            "Criteria_for_COVID-19_Diagnosis": "Diagnosis methods",
            "Severity_Classification_Method": "How severity is defined",
            "Duration_of_Illness_before_Hospital_Admission": "Time to hospitalization",
            "Symptoms_Presented": "Reported symptoms"
        },
        "Risk_Factor_Data": {
            "Comorbidities": "Other medical conditions",
            "Lifestyle_Factors": "Behaviors like smoking, diet",
            "Immunization_Status": "Vaccination status",
            "Previous_Infections_or_Co-infections": "History of other infections"
        },
        "Statistical_Analysis": {
            "Statistical_Methods_Used": "Techniques for data analysis",
            "Outcome_Variables_Measured": "Specific outcomes measured",
            "Adjustments_for_Confounders": "Handling of confounders",
            "Results_of_the_Analyses": "Key findings and statistics"
        },
        "Quality_Assessment": {
            "Risk_of_Bias_in_the_Study": "Evaluation of potential bias",
            "Methodological_Quality": "Study’s methodology assessment"
        },
        "Funding_and_Conflicts_of_Interest": {
            "Funding_Sources": "Who funded the study",
            "Declarations_of_Potential_Conflicts_of_Interest": "Potential biases"
        },
        "Supplementary_Information": {
            "Supplementary_Data_or_Material": "Additional data provided",
            "Correspondence_Information_for_Lead_Authors": "Contact information"
        }
    }
"""

# Load the selected papers
selected_papers_path = os.path.join(os.getcwd(), '../docs/results/selected_papers.txt')
raw_papers_path = os.path.join(os.getcwd(), '../docs/papers/')
paper_body_analysis_path = os.path.join(os.getcwd(), '../docs/results/selected_papers_with_papers_body_analysis.txt')

with open(selected_papers_path, 'r', encoding='utf-8') as file:
    txt_content = file.readlines()

selected_papers, error_papers = [], []

# Process each paper
for line in txt_content:
    if line:
        try:
            paper = json.loads(line)
            selected_papers.append(paper)
            paper_name = paper['Short Title'].replace('/', '_')
            pdf_path = f'{raw_papers_path}/{paper_name}.pdf'

            # Check if the PDF already exists
            if not os.path.exists(pdf_path):
                try:
                    doi = paper['DOI']
                except KeyError as e:
                    print(f"Error getting DOI: {e}")
                    continue
                try:
                    url = metapub.FindIt(doi=doi).url
                    if url:
                        urlretrieve(url, pdf_path)
                    else:
                        print(f"Couldn't find a URL for {doi}")
                        continue
                except Exception as e:
                    print(f"Error fetching URL for DOI: {e}")
                    continue

            # Extract text from PDF
            try:
                extracted_text = textract.process(pdf_path, method='pdftotext', encoding='utf-8', extension='pdf')
                full_text = extracted_text.decode('utf-8')
            except Exception as e:
                print(f"Error extracting text from PDF: {e}")
                continue

            # Process the text with OpenAI API
            user_message = f"""
            first, this is a template for you to fill in.
            {resp_format}
            second, this is a document for you to read.
            {full_text}
            """
            response = send_message(system_message, user_message)
            content = response.content.replace('\n', '').replace('\t', '').replace('```json', '').replace('```', '')
            try:
                content = json.loads(content)
                paper['Paper_Analysis'] = content
            except json.decoder.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                error_papers.append(paper)

        except json.decoder.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            print(f"Problematic line: {line}")

# Save the final papers
with open(paper_body_analysis_path, 'w', encoding='utf-8') as file:
    for paper in selected_papers:
        json_string = json.dumps(paper)
        file.write(json_string + '\n')