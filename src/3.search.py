from utils import get_mata_information_by_json, convert_float32, search
import json
import faiss
import numpy as np
import os

index_path = os.path.join(os.getcwd(), '../docs/large.index')
Index = faiss.read_index(index_path)
file_path = os.path.join(os.getcwd(), '../docs/results/papers_meta_informations_by_json_with_embedding.txt')
selected_papers_path = os.path.join(os.getcwd(), '../docs/results/selected_papers.txt')
papers_meta_information = get_mata_information_by_json(file_path)[0]

k = 300
query = """
Seeking articles providing statistical analysis (odds ratios, relative risks, hazard ratios) on COVID-19 patient risk factors. 
Focus on: Age, BMI, vaccination status, medication use, vital signs (temperature, chills, shortness of breath, respiratory rate), symptoms (cough, headache, sore throat, voice changes, nasal congestion, muscle pain), and comorbidities (diabetes, immune disorders like rheumatism, lung diseases including asthma, COPD, tuberculosis, interstitial lung disease, post-lung resection, chronic kidney failure, chronic heart failure, post-solid organ transplant, neurological diseases, cirrhosis of the liver, history of major surgeries like splenectomy).
"""
# deep copy papers_meta_information's content to pmi_copy
new_list = []
for paper in papers_meta_information:
    if "embedding" in paper.keys():
        new_list.append(paper)

D, I = search(query, k)
selected_papers = []

for i in range(k):
    paper = new_list[I[0][i]]
    paper['distance'] = D[0][i]
    selected_papers.append(paper)

with open(selected_papers_path, 'w', encoding='utf-8') as file:
    for paper in selected_papers:
        paper = convert_float32(paper)
        json_string = json.dumps(paper)
        file.write(json_string + '\n')

