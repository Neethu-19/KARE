# KARE: Knowledge Graph-Augmented Retrieval for reliable Drug Repurposing

## An Explainable Drug Repurposing System using Knowledge Graphs and RAG

---

## 1. Project Overview

**KARE** is an explainable biomedical reasoning system designed to identify potential drug–disease associations by combining:

- **Knowledge Graphs (Neo4j)** for structured biological reasoning
- **Retrieval-Augmented Generation (RAG)** for scientific literature support
- **Multi-hop reasoning** across drugs, genes, pathways, and diseases

The system focuses on **explainability** and **evidence-backed predictions**, avoiding black-box outputs.

---

## 2. System Architecture

### High-Level Workflow

```
User Query
   ↓
Knowledge Graph Reasoning (Neo4j)
   ↓
Multi-hop Traversal (Drug → Gene → Disease)
   ↓
Literature Retrieval (FAISS)
   ↓
Explainable Final Output
```

---

## 3. Dataset Design

### 3.1 Knowledge Graph Entities

The Knowledge Graph consists of the following entity types:

| Entity | Description |
|--------|-------------|
| **Drug** | Therapeutic compounds |
| **Gene / Protein** | Biological targets |
| **Pathway** | Biological signaling mechanisms |
| **Disease** | Clinical conditions |

Each entity is stored as a node in Neo4j.

### 3.2 Knowledge Graph Relationships

Entities are connected using biologically meaningful relationships:

| Relationship | Direction | Purpose |
|--------------|-----------|---------|
| **INHIBITS** | Drug → Gene | Drug inhibits gene expression |
| **ACTIVATES** | Drug → Gene | Drug activates gene expression |
| **ASSOCIATED_WITH** | Gene → Disease | Gene linked to disease |
| **PARTICIPATES_IN** | Gene → Pathway | Gene involved in pathway |
| **POTENTIAL_REPURPOSE** | Drug → Disease | Drug candidate for disease treatment |

These relationships enable **multi-hop biological reasoning**.

---

## 4. Project Folder Structure

```
KARE/
│
├── data/
│   ├── kg/
│   │   ├── drugs.csv
│   │   ├── diseases.csv
│   │   ├── genes.csv
│   │   ├── pathways.csv
│   │   └── relationships.csv
│   │
│   └── literature/
│       └── papers.csv
│
├── rag/
│   ├── build_faiss.py
│   ├── retrieve.py
│   └── literature.index
│
├── pipeline/
│   └── run_kare.py
│
├── neo4j.txt
└── README.md
```

---

## 5. Prerequisites & Setup

### 5.1 Software Requirements

- **Python** 3.10 or above
- **Neo4j Desktop** (latest version)
- **Operating System**: Windows / Linux / macOS

### 5.2 Python Libraries

Install all required dependencies using:

```bash
pip install neo4j pandas numpy sentence-transformers faiss-cpu
```

**Library Purposes:**

| Library | Purpose |
|---------|---------|
| `neo4j` | Database connectivity |
| `pandas` | Data preprocessing |
| `numpy` | Numerical operations |
| `sentence-transformers` | Text embedding generation |
| `faiss-cpu` | Vector similarity search (RAG) |

---

## 6. Step-by-Step Implementation Guide

### Step 1: Neo4j Setup (Knowledge Graph)

1. Open **Neo4j Desktop**
2. Create a new local instance named: `KARE_KG`
3. Start the instance (status should be **RUNNING**)
4. Create a database named: `kare`
5. Select the database:
   ```cypher
   :use kare
   ```

### Step 2: Load Knowledge Graph Data

1. Copy all CSV files from: `data/kg/` into Neo4j's import folder
2. Load entities (Drugs, Diseases, Genes, Pathways) using LOAD CSV / MERGE queries
3. Load relationships from `relationships.csv`
4. Verify graph creation:
   ```cypher
   MATCH (n)-[r]->(m) RETURN n, r, m;
   ```
   You should see a connected biomedical graph.

### Step 3: Knowledge Graph Reasoning

Multi-hop reasoning is performed using Cypher queries such as:

```cypher
MATCH (d:Drug)-[:INHIBITS]->(g:Gene)-[:ASSOCIATED_WITH]->(ds:Disease)
RETURN DISTINCT d.name AS Drug, g.name AS Gene, ds.name AS Disease;
```

This implements the reasoning chain: **Drug → Gene → Disease**

### Step 4: Literature Dataset Preparation (RAG)

Ensure the literature dataset exists at: `data/literature/papers.csv`

Each row should contain:
- `paper_id` - Unique identifier
- Text content - Biomedical text evidence

### Step 5: Build FAISS Vector Index

From the project root directory, run:

```bash
python rag/build_faiss.py
```

**Expected output:**
```
FAISS index created successfully
```

This step converts literature text into vector embeddings and stores them in FAISS.

### Step 6: Literature Retrieval (RAG)

To test standalone literature retrieval:

```bash
python rag/retrieve.py
```

This retrieves semantically relevant scientific evidence for a given query.

### Step 7: Run the Complete Pipeline (KG + RAG)

1. Update Neo4j credentials in `pipeline/run_kare.py`:
   ```python
   NEO4J_USER = "neo4j"
   NEO4J_PASSWORD = "<your_neo4j_password>"
   ```

2. Execute the full pipeline:
   ```bash
   python pipeline/run_kare.py
   ```

---

## 7. Expected Output

### 7.1 Knowledge Graph Reasoning

```
KG Reasoning:
Metformin → mTOR → Alzheimer's Disease
```

### 7.2 Supporting Literature

```
Supporting Literature:
- Metformin inhibits mTOR signaling and has shown neuroprotective effects.
- Dysregulation of the mTOR pathway is associated with Alzheimer's disease.
```

This confirms:
- ✅ Multi-hop KG reasoning
- ✅ Evidence-backed predictions
- ✅ Explainable outputs

---

## 8. Execution Flow Summary

1. Load structured biomedical data into Neo4j
2. Perform multi-hop reasoning using the Knowledge Graph
3. Retrieve relevant literature using FAISS
4. Combine KG reasoning and literature evidence
5. Generate final explainable output

---

## 9. Common Issues & Troubleshooting

| Issue | Solution |
|-------|----------|
| **Authentication error** | Reset Neo4j password in Neo4j Desktop |
| **CSV not found** | Ensure CSVs are placed in Neo4j import folder |
| **Duplicate outputs** | Use `DISTINCT` in Cypher queries |
| **FAISS error** | Rebuild index using `build_faiss.py` |

---

## 10. Extending the System

The system can be extended by:

- ✨ Adding more entities and relationships to the Knowledge Graph
- ✨ Expanding the literature dataset and rebuilding FAISS
- ✨ Adding confidence scores based on number of KG paths
- ✨ Integrating an LLM for natural language response generation
- ✨ Implementing user authentication and query logging

---

## 11. Key Features

- **Explainability**: Every prediction includes reasoning paths and evidence
- **Multi-hop Reasoning**: Traverses complex biological networks
- **Evidence-Backed**: Literature support for all recommendations
- **Modular Design**: Easy to extend and maintain
- **Biomedically Sound**: Uses validated biological relationships

---

## 12. Conclusion

**KARE** demonstrates how Knowledge Graphs and Retrieval-Augmented Generation can be combined to build an explainable biomedical reasoning system.

The modular design makes it suitable for:
- 🎓 Academic research
- 📊 System demonstrations
- 🔧 Further extensions and improvements

---

## 📝 License

This project is part of academic research. For usage rights and citations, refer to your institution's guidelines.

---

## 🤝 Contributing

Contributions are welcome! Please ensure all code follows the project's structure and includes documentation.
