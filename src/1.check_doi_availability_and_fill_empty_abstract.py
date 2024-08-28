from utils import split_papers_from_the_endnotes_rtf_form
from striprtf.striprtf import rtf_to_text
import json
import os 

result_file_path = os.path.join(os.getcwd(), 'docs/results/papers_meta_informations_by_json.txt')
meta_information_file_path = os.path.join(os.getcwd(), 'docs/COVID-19 Scoring System.rtf')

with open(meta_information_file_path, 'r', encoding='utf-8') as file:
    rtf_content = file.read()

# Specify the encoding explicitly when calling rtf_to_text
text_content = rtf_to_text(rtf_content, encoding='utf-8', errors='ignore')
papers_meta_information = split_papers_from_the_endnotes_rtf_form(text_content)

# store the meta information in a file
with open(result_file_path, 'w', encoding='utf-8') as file:
    for meta_information in papers_meta_information:
        json_string = json.dumps(meta_information)
        file.write(json_string + '\n')

