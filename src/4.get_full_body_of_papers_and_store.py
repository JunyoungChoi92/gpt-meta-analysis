import json
import os
from urllib.request import urlretrieve
import metapub

# Load the selected papers
path_selected_paper = os.path.join(os.getcwd(), '../docs/results/selected_papers.txt')
with open(path_selected_paper, 'r', encoding='utf-8') as file:
    txt_content = file.readlines()

raw_papers_path = os.path.join(os.getcwd(), '../docs/papers')
selected_papers, error_papers = [], []

# Process each paper
for line in txt_content:
    if line:
        try:
            paper = json.loads(line)
            selected_papers.append(paper)
            paper_name = paper['Short Title'].replace('/', '_')
            pdf_path = f'{raw_papers_path}/{paper_name}.pdf'

            if not os.path.exists(pdf_path):
                try:
                    doi = paper['DOI']
                except Exception as e:
                    print(f"Error getting DOI {e}")
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
        except json.decoder.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            print(f"Problematic line: {line}")