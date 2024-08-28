from utils import get_embedding, get_mata_information_by_json
import faiss
import numpy as np
import json
import os 
meta_information_file_path = os.path.join(os.getcwd(), '../docs/results/papers_meta_informations_by_json.txt')
embedding_file_path = os.path.join(os.getcwd(), '../docs/results/papers_meta_informations_by_json_with_embedding.txt')
index_file_path = os.path.join(os.getcwd(), '../docs/large.index')

papers_meta_information = get_mata_information_by_json(meta_information_file_path)

Index = faiss.IndexFlatL2(1536)

for paper in papers_meta_information:
    title = paper['Title']
    abstract = paper['Abstract']
    keywords = paper['Keywords']

    if abstract == None:
        continue
    
    connected_text = title + '\n' + keywords + '\n' + abstract
    try:
        embedding = get_embedding(connected_text)

        if embedding is not None:
            paper['embedding'] = embedding.tolist()
            Index.add(embedding)
        else:
            print(f"Embedding not found for paper: {title}")
    except:
        print(f"Error getting embedding for paper: {paper}")

print(f"Total papers: {len(papers_meta_information)} / Total embeddings: {Index.ntotal}")

# write new paers_meta_information to file
with open(embedding_file_path, 'w') as outfile:
    json.dump(papers_meta_information, outfile)

faiss.write_index(Index, index_file_path)
