import json
from utils import get_mata_information_by_json, send_message_with_function_call, add_text
import os
import textract

selected_paper_path = os.path.join(os.getcwd(), 'docs/results/selected_papers.txt')
meta_information_of_selected_papers = get_mata_information_by_json(selected_paper_path)

raw_papers_path = os.path.join(os.getcwd(), 'docs/papers')
paper_names = os.listdir(raw_papers_path)

syetem_message = """
Let's say you're a competent researcher. 
You have been asked to read a document I provide and fill in whether the information in the sentence below exists and, if so, at what value it is defined in the paper. 
You must extract all the information you need to answer. Follow the response form I provide, and don't leave anything out.
Think step by step.

and here is The paper.
"""

statistics = []
counter = 0

statistics_path = os.path.join(os.getcwd(), 'docs/results/statistics.txt')

if not os.path.exists(statistics_path):
    with open(statistics_path, 'w', encoding='utf-8') as file:
        file.write('')

for paper in meta_information_of_selected_papers:
    paper_name = paper['Short Title'].replace('/', '_')+ '.pdf'

    if paper_name not in paper_names:
        print(f"Couldn't find a PDF for {paper_name}")
        counter += 1
        continue

    print("start processing paper: ", paper_name)
    paper_path = f'{raw_papers_path}/{paper_name}'
    try:
        extracted_text = textract.process(paper_path, method='pdftotext', encoding='utf-8', extension='pdf')
        full_text = extracted_text.decode('utf-8')
    except Exception as e:
        print(f"Error loading paper: {e}")
        continue

    user_message = f"""
    {full_text}
    """

    try:
        response = send_message_with_function_call(syetem_message, user_message)
    except Exception as e:
        print(f"Error sending message to openai: {e}, paper: {paper_name}")
        continue
    
    try:
        json_response = json.loads(response)
        json_response['Short Title'] = paper['Short Title']
        print(f"Successfully processed paper: {paper_name}")
        json_string = json.dumps(json_response)
        
        add_text(json_string)
    except json.decoder.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}, paper: {paper_name}")
        continue


print(f"Successfully processed {len(meta_information_of_selected_papers)-counter} papers, {counter} papers failed to process")
