import os
from sentence_transformers import SentenceTransformer

model_name = "sentence-transformers/all-mpnet-base-v1"
DATA_PATH = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(DATA_PATH, 'embedding_model')

if not os.path.exists(MODEL_PATH):
    model = SentenceTransformer(model_name)
    model.save(MODEL_PATH)
