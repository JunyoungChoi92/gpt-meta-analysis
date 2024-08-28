import os
import json
import metapub
from metapub import PubMedFetcher
from urllib.request import urlretrieve
import textract
from openai import OpenAI
import numpy as np
import faiss
from faiss import write_index, read_index
from striprtf.striprtf import rtf_to_text
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

schema = {
    "type": "object",
    "properties": {
        "Predictor_Variables": {
            "type": "object",
            "description": "Specific to COVID-19 severity with a list of variables.",
            "properties": {
                "Specific_to_COVID_19_Severity": {
                    "type": "string",
                    "description": "Indicates whether the predictor variables are specifically relevant to COVID-19 severity (Yes/No)"
                },
                "Detailed_Variables": {
                    "type": "array",
                    "description": "List of Variables (risk factors) with OR and 95% CI score.",
                    "items": {
                        "type": "object",
                        "properties": {
                                "Variable": {
                                    "type": "string",
                                    "description": "Risk Factors for estimating COVID-19 severity. for example, Age, BMI, vaccination status, medication use, temperature, chills, shortness of breath, respiratory rate, cough, headache, sore throat, voice changes, nasal congestion, muscle pain, diabetes, rheumatism, asthma, COPD, tuberculosis, interstitial lung disease, post-lung resection, chronic kidney failure, chronic heart failure, post-solid organ transplant, neurological diseases, cirrhosis of the liver, splenectomy, etc.  "
                                },
                                "Odds_Ratio_OR": {
                                    "type": "string",
                                    "description": "Odds Ratio (OR)"
                                },
                                "OR_95%_Confidence_Interval": {
                                    "type": "string",
                                    "description": "95% Confidence Interval"
                                },
                                "Relative Risk_RR": {
                                    "type": "string",
                                    "description": "Relative Risk (RR)"
                                },
                                "RR_95%_Confidence_Interval": {
                                    "type": "string",
                                    "description": "95% Confidence Interval"
                                },
                                "Hazard_Ratio_HR": {
                                    "type": "string",
                                    "description": "Hazard Ratio (HR)"
                                },
                                "HR_95%_Confidence_Interval": {
                                    "type": "string",
                                    "description": "95% Confidence Interval"
                                },
                            }
                        }
                    }
            },
            "required": ["Specific_to_COVID_19_Severity", "Detailed_Variables"]
        },
        "Statistical_Measures_of_Association": {
            "type": "object",
            "description": "Traditional metrics like ORs, HRs, RRs, and confidence intervals.",
            "properties": {
                "Odds_Ratios_OR": {
                    "type": "string",
                    "description": "Presence of Odds Ratios (OR) (Present/Absent)"
                },
                "Hazard_Ratios_HR": {
                    "type": "string",
                    "description": "Presence of Hazard Ratios (HR) (Present/Absent)"
                },
                "Relative_Risks_RRs": {
                    "type": "string",
                    "description": "Presence of Relative Risks (RRs) (Present/Absent)"
                },
                "Confidence_Intervals": {
                    "type": "string",
                    "description": "Presence of Confidence Intervals (Present/Absent)"
                }
            },
            "required": ["Odds_Ratios_OR", "Hazard_Ratios_HR", "Relative_Risks_RRs", "Confidence_Intervals"]
        },
        "Meta_Analysis_Specific_Metrics": {
            "type": "object",
            "description": "Metrics specific to meta-analyses like heterogeneity assessment, sensitivity analysis, cumulative sample size, and subgroup analysis.",
            "properties": {
                "Heterogeneity_Assessment": {
                    "type": "string",
                    "description": "Type of Heterogeneity Assessment used (I² Statistic, Cochran’s Q Test, etc.)"
                },
                "Sensitivity_Analysis": {
                    "type": "string",
                    "description": "Whether Sensitivity Analysis was conducted (Conducted/Not Conducted)"
                },
                "Cumulative_Sample_Size": {
                    "type": "string",
                    "description": "Status of reporting Cumulative Sample Size (Reported/Not Reported)"
                },
                "Subgroup_Analysis": {
                    "type": "string",
                    "description": "Presence of Subgroup Analysis (Present/Absent)"
                }
            },
            "required": ["Heterogeneity_Assessment", "Sensitivity_Analysis", "Cumulative_Sample_Size", "Subgroup_Analysis"]
        },
        "Study_Quality_Assessment": {
            "type": "object",
            "description": "Evaluating the quality of included studies and risk of bias.",
            "properties": {
                "Quality_of_Included_Studies": {
                    "type": "string",
                    "description": "Assesses the overall quality and reliability of the studies included in the meta-analysis."
                },
                "Risk_of_Bias": {
                    "type": "string",
                    "description": "Evaluates if the meta-analysis examines potential biases in the included studies."
                }
            },
            "required": ["Quality_of_Included_Studies", "Risk_of_Bias"]
        },
        "P-Values": {
            "type": "object",
            "description": " Reporting on specific variables and significance thresholds.",
            "properties": {
                "Specific_Variables": {
                    "type": "array",
                    "description": "List of risk factors with P < threshold_for_Significance, including P-value.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "Variable": {
                                "type": "string",
                                "description": "Name of the variable"
                            },
                            "P_Value": {
                                "type": "string",
                                "description": "P-value"
                            }
                        }
                    }
                },
                "Threshold_for_Significance": {
                    "type": "string",
                    "description": "The threshold level for significance (e.g., P < 0.05)"
                }
            },
            "required": ["Specific_Variables", "Threshold_for_Significance"]
        },
        "Publication_Bias": {
            "type": "object",
            "description": "Assessment through funnel plot analysis or other methods.",
            "properties": {
                "Funnel_Plot_Analysis": {
                    "type": "string",
                    "description": "Indicates if Funnel Plot Analysis was conducted (Conducted/Not Conducted)"
                },
                "Other_Methods": {
                    "type": "string",
                    "description": "List of other methods used for assessing publication bias"
                }
            },
            "required": ["Funnel_Plot_Analysis", "Other_Methods"]
        },
        "Sample_Size": {
            "type": "string",
            "description": "Reporting on the cumulative sample size in the meta-analysis."
        },
        "Generalizability": {
            "type": "string",
            "description": "Evaluating the applicability of the findings to a wider population."
        },
        "Additional_Considerations": {
            "type": "object",
            "description": "Assessing the specificity to the research question, consistency of methods across studies, and appropriateness of statistical methods.",
            "properties": {
                "Specificity_to_Research_Question": {
                    "type": "string",
                    "description": "Checks whether the studies directly address the research question. (Yes/No)"
                },
                "Consistency_of_Methods_Across_Studies": {
                    "type": "string",
                    "description": "Evaluates if the statistical methods used are suitable for the type of data and research question. (Yes/No)"
                },
                "Appropriateness_of_Statistical_Methods": {
                    "type": "string",
                    "description": "Evaluates if the statistical methods used are suitable for the type of data and research question. (Yes/No)"
                }
            },
            "required": ["Specificity_to_Research_Question", "Consistency_of_Methods_Across_Studies", "Appropriateness_of_Statistical_Methods"]
        }
        },
    "required": ["Predictor_Variables", "Statistical_Measures_of_Association", "Meta_Analysis_Specific_Metrics", "Study_Quality_Assessment", "P-Values", "Publication_Bias", "Sample_Size", "Generalizability", "Additional_Considerations"]
}


def get_embedding(text, model="text-embedding-ada-002"):
    response = client.embeddings.create(input=[text], model=model)
    if response.data:
            embedding = np.array(response.data[0].embedding).reshape(1, -1)
            return embedding
    else:
            raise ValueError("No embedding returned from the API")

def send_message(system_message, user_message):
    completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]
    )
    message_content = completion.choices[0].message
    return message_content

def send_message_with_function_call(system_message, user_message):
    completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ],
        functions=[{
            "name": "schema",
            "description": "a function that get the metrics from the papers for meta-analyzing medical papers",
            "parameters": schema
        }],
        function_call = {
            "name": "schema",
        }
    )
    message_content = completion.choices[0].message.function_call.arguments
    return message_content

def convert_float32(data):
    if isinstance(data, dict):
        for key, value in data.items():
            data[key] = convert_float32(value)
    elif isinstance(data, list):
        data = [convert_float32(item) for item in data]
    elif isinstance(data, np.float32):
        data = float(data)
    return data

def add_text(statistic: dict):
    current_path = os.path.join(os.getcwd(), 'docs/results/statistics.txt')
    with open(current_path, 'r', encoding='utf-8') as file:
        original_content = file.read()

    original_content += str(statistic) + '\n'

    with open(current_path, 'w', encoding='utf-8') as file:
        file.write(original_content)

def search(query, k=100):
    current_path = os.path.join(os.getcwd(), 'docs/large.index')
    query_embedding = get_embedding(query)
    Index = read_index(current_path)

    D, I = Index.search(query_embedding.reshape(1, -1), k)
    return D, I

def flatten_smallest_unit(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = k
        if isinstance(v, dict):
            items.extend(flatten_smallest_unit(v, new_key, sep=sep))
        else:
            items.append({new_key: v})
    return items


def split_papers_from_the_endnotes_rtf_form(text):
    papers = text.split('\n\n')
    meta_informations = []
    known_keys = {"Reference Type", "Record Number", "Year", "Title", "Journal", "Volume", "Issue", "Epub Date", "Date", "Short Title", "ISSN", "DOI", "PMCID", "Accession Number", "Keywords", "Abstract", "Notes", "Author Address", "Database Provider", "Language"}
    errored_papers = []

    for paper in papers:
        lines = paper.split('\n')
        a_papers_meta_information = {}

        for line in lines:
            if ':' in line and (line.split(':', 1)[0] in known_keys):
                key, value = line.split(':', 1)
                a_papers_meta_information[key] = value.strip()
            else:
                try:
                    a_papers_meta_information[key] += ' ' + line.strip()
                except:
                    continue
        
        if "Abstract" not in a_papers_meta_information.keys():
            a_papers_meta_information['Abstract'] = ''
            fetch = PubMedFetcher()
            try:
                doi = a_papers_meta_information['DOI']
                article = fetch.article_by_pmid(doi)
                a_papers_meta_information['Abstract'] = article.abstract
            except:
                try:
                    pmcid = a_papers_meta_information['PMCID']
                    article = fetch.article_by_pmcid(pmcid)
                    a_papers_meta_information['Abstract'] = article.abstract
                except:
                    try:
                        title = a_papers_meta_information['Title']
                        print(f"a error on fetching: {title}")
                    except:
                        print(f"a error on fetching: {a_papers_meta_information}")
                    errored_papers.append(a_papers_meta_information)
                    continue

        meta_informations.append(a_papers_meta_information)

    # store errored_papers in a file
    current_path = os.path.join(os.getcwd(), 'docs/results/no_abstract_paper_list.txt')
    with open(current_path, 'w', encoding='utf-8') as file:
        for paper in errored_papers:
            json_string = json.dumps(paper)
            file.write(json_string + '\n')

    return meta_informations

def get_mata_information_by_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        txt_content = file.readlines()

    papers_meta_information = []
    for line in txt_content:
        if line:
            try:
                papers_meta_information.append(json.loads(line))
            except json.decoder.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                print(f"Problematic line: {line}")
                continue
    
    return papers_meta_information

def flatten_dict(d):
    flattened = []

    for key, value in d.items():
        if isinstance(value, dict):
            flattened.extend(flatten_dict(value))
        else:
            flattened.append({key: value})

    return flattened
