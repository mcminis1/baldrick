import os
import pandas as pd
from sentence_transformers import SentenceTransformer, util

path = os.path.dirname(__file__)
df = pd.read_csv(f"{path}/data/queries.csv")
prompts = df["Prompt"].to_list()

model_path = f"{path}/data/embedding_model"
model = SentenceTransformer(model_path)

# Sentences are encoded by calling model.encode()
embeddings = model.encode(prompts)
queries = df["Query"].to_list()
lookup = [(e, p.strip(), q.strip()) for e, p, q in zip(embeddings, prompts, queries)]


def get_top_k_matches(user_query, top_k=4, mex_length=512):
    matches = []
    e = model.encode(user_query)
    for embedding, prompt, query in lookup:
        score = util.dot_score(e, embedding)
        matches.append((score, prompt, query))
    winners = []
    len = 0
    for _, p, q in sorted(matches, reverse=True)[:top_k]:
        len += len(p) + len(q)
        if len < mex_length:
            winners.append((p, q))
    return winners
