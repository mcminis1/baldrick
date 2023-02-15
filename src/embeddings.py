import os
import pandas as pd
from sentence_transformers import SentenceTransformer, util
from .data import DATA_PATH, MODEL_PATH

queries_csv = os.path.join(DATA_PATH, 'queries.csv')
df = pd.read_csv(queries_csv)
prompts = df["Prompt"].to_list()

model = SentenceTransformer(MODEL_PATH)

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
    prompt_length = 0
    for (_, p, q) in sorted(matches, reverse=True)[:top_k]:
        prompt_length += len(p) + len(q)
        if prompt_length < mex_length:
            winners.append((p, q))
    return winners
