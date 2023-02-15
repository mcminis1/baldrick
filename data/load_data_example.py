import pandas as pd
from sentence_transformers import SentenceTransformer, util

df = pd.read_csv("../src/data/queries.csv")
prompts = df["Prompt"].to_list()
model_name = "sentence-transformers/all-mpnet-base-v1"
model = SentenceTransformer(model_name)

modelPath = '../src/data/embedding_model'
model.save(modelPath)



# Sentences are encoded by calling model.encode()
embeddings = model.encode(prompts)

queries = df["Query"].to_list()
lookup = [(p, q) for p, q in zip(embeddings, queries)]

matches = []
print(prompts[0])
e = model.encode(prompts[0])
for embedding, query in lookup:
    score = util.dot_score(e, embedding)
    matches.append((score, query))
print(sorted(matches, reverse=True)[0])
