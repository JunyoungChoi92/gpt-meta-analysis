import json
import os
from striprtf.striprtf import rtf_to_text

# read docs/selected_papers.txt
file_path = os.path.join(os.getcwd(), '../docs/results/selected_papers.txt')

with open(file_path, 'r', encoding='utf-8') as file:
    selected_papers = file.readlines()

# text to json
selected_papers = [json.loads(paper) for paper in selected_papers]

# sort by distance
selected_papers = sorted(selected_papers, key=lambda k: k['distance'])

titles = []
for paper in selected_papers:
    titles.append(paper['Title'])

# read docs/Covid-19 Scoring System_key Articles.rtf
file_path = os.path.join(os.getcwd(), '../docs/results/COVID-19 Scoring System_Key Ariticles.rtf')

with open(file_path, 'r', encoding='utf-8') as file:
    rtf_content = file.read()

# Specify the encoding explicitly when calling rtf_to_text
text_content = rtf_to_text(rtf_content, encoding='utf-8', errors='ignore')

# split text_content by \n\n and make it a list
key_articles = text_content.split('\n')
key_articles_title = []

for article in key_articles:
    if article:
        key_articles_title.append(article.split(".")[2][1:])
    
# check similarity of two lists
counter = 0
for title in titles:
    if title in key_articles_title:
        counter += 1

print(f"Total papers: {len(titles)} / Total key articles: {len(key_articles_title)} / Total matched: {counter}")