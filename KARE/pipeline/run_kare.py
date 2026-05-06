from neo4j import GraphDatabase
import faiss
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer

# ---------- Neo4j connection ----------
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "Jayappa@123"  # same as Neo4j Desktop

driver = GraphDatabase.driver(
    NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD)
)

# ---------- FAISS + Embeddings ----------
model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.read_index("rag/literature.index")
df = pd.read_csv("data/literature/papers.csv")
texts = df["text"].tolist()

# ---------- KG Query ----------
def query_kg(drug_name):
    query = """
    MATCH (d:Drug)-[:INHIBITS]->(g:Gene)-[:ASSOCIATED_WITH]->(ds:Disease)
    WHERE d.name = $drug
    RETURN DISTINCT d.name AS Drug, g.name AS Gene, ds.name AS Disease
    """
    with driver.session(database="kare") as session:
        return session.run(query, drug=drug_name).data()


# ---------- RAG Retrieval ----------
def retrieve_evidence(question, k=2):
    q_emb = model.encode([question])
    D, I = index.search(np.array(q_emb), k)
    return [texts[i] for i in I[0]]

# ---------- MAIN ----------
if __name__ == "__main__":
    drug = "Metformin"
    question = "Can Metformin be repurposed for Alzheimer's disease?"

    kg_results = query_kg(drug)
    evidence = retrieve_evidence(question)

    print("\n--- KG Reasoning ---")
    for r in kg_results:
        print(f"{r['Drug']} → {r['Gene']} → {r['Disease']}")

    print("\n--- Supporting Literature ---")
    for e in evidence:
        print("-", e)
