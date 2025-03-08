import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load the FAISS index
index = faiss.read_index("faiss_index.bin")

# Load text chunks
with open("text_chunks.txt", "r") as f:
    text_chunks = f.read().splitlines()

# Load the embedding model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


# Function to perform search
def search_faiss(query, top_k=5):
    # Convert query to embedding
    query_embedding = model.encode([query])

    # Search in FAISS
    distances, indices = index.search(query_embedding, top_k)

    # Retrieve relevant text chunks
    results = [text_chunks[i] for i in indices[0]]

    return results


# Example query
query = "Best places for entertainment near latitude 28.63"
retrieved_chunks = search_faiss(query)

print("Top Retrieved Chunks:")
for chunk in retrieved_chunks:
    print("-", chunk)
