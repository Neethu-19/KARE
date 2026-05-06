import faiss
import pandas as pd
from sentence_transformers import SentenceTransformer
import numpy as np

# Load data
df = pd.read_csv("data/literature/papers.csv")
texts = df["text"].tolist()

# Load FAISS index
index = faiss.read_index("rag/literature.index")

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

# User query
query = "Can Metformin be repurposed for Alzheimer's disease?"
query_embedding = model.encode([query])

# Search
D, I = index.search(np.array(query_embedding), k=2)

print("Retrieved Evidence:\n")
for idx in I[0]:
    print("-", texts[idx])
