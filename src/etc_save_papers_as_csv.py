import json
import csv
from utils import flatten_smallest_unit
import os

txt_path = os.path.join(os.getcwd(), '../docs/results/papers_meta_informations_by_json.txt')

# read txt from txt_path and tranform it into a list of dictionaries
with open(txt_path, 'r', encoding='utf-8') as file:
    txt_content = file.readlines()

data = []
for line in txt_content:
    if line:
        try:
            paper = json.loads(line)
            data.append(paper)
        except Exception as e:
            print(f"Error loading json: {e}")
            continue

all_keys = [
    "distance",
    "Record Number",
    "Year",
    "Title",
    "Journal",
    "Volume",
    "Issue",
    "Epub Date",
    "Date",
    "Short Title",
    "ISSN",
    "DOI",
    "PMCID",
    "Accession Number",
    "Keywords",
    "Abstract",
    "Notes",
    "Orcid",
    "Author Address",
    "Journal Article",
    "Author Address",
    "Database Provider",
    "Language",
]

flat_pa = flatten_smallest_unit(data[0]["Paper_Analysis"])
for k in flat_pa:
    all_keys.append(list(k.keys())[0])

result = []
temp = {}

for paper in data:
    keys = paper.keys()
    for key in keys:
        if ";" in key or "," in key or "." in key or "/" in key or "(" in key:
            temp.update({paper['Short Title']: key + " " + paper[key]})

for paper in data:
    if paper['Short Title'] in temp.keys():
        paper.update({"publication of this article": temp[paper['Short Title']]})
    else:
        paper.update({"publication of this article": ""})

indexed_data = []


for paper in data:
    if "Paper_Analysis" in paper:
        flat_pa = flatten_smallest_unit(paper["Paper_Analysis"])
        for k in flat_pa:
            paper.update(k)

        indexed_paper = {}
        for key in all_keys:
            if key in paper.keys():
                indexed_paper.update({key: paper[key]})
            else:
                indexed_paper.update({key: ""})
        indexed_data.append(indexed_paper)
    else:
        print(f"Paper_Analysis not found in paper: {paper.get('Title', 'No title')}")

with open('./result.csv', 'w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=all_keys)
    writer.writeheader()
    for row in data:
        row_with_all_keys = {key: row.get(key, '') for key in all_keys}
        writer.writerow(row_with_all_keys)
