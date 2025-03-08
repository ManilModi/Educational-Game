import os
import faiss
import groq
import numpy as np
from sentence_transformers import SentenceTransformer

# Set your Groq API key
os.environ["GROQ_API_KEY"] = "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"

# Initialize Groq client
client = groq.Client(api_key=os.getenv("GROQ_API_KEY"))

# Load FAISS index
index = faiss.read_index("faiss_index.bin")

# Load text chunks
with open("text_chunks.txt", "r") as f:
    text_chunks = f.read().splitlines()

# Load embedding model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


# Function to search FAISS
def search_faiss(query, top_k=5):
    """Search the FAISS index for the most relevant text chunks."""
    query_embedding = model.encode([query])
    distances, indices = index.search(query_embedding, top_k)
    results = [text_chunks[i] for i in indices[0]]
    return results


# Function to query Groq with retrieved context
def query_groq(query, retrieved_chunks):
    """Query the Groq LLM with retrieved chunks for a contextual response."""
    context = "\n".join(retrieved_chunks)

    prompt = f"""
    You are an AI assistant helping with location-based queries. 
    Use the following information to answer the question:

    {context}

    Question: {query}
    Answer:
    """

    response = client.chat.completions.create(
        model="llama3-8b-8192",  # ✅ Using a free model
        messages=[{"role": "system", "content": "You are a helpful AI."},
                  {"role": "user", "content": prompt}],
        max_tokens=300
    )

    return response.choices[0].message.content  # ✅ Corrected response extraction


# Example usage
if __name__ == "__main__":
    query = "Where are the best places for entertainment near latitude 28.63?"
    retrieved_chunks = search_faiss(query)
    answer = query_groq(query, retrieved_chunks)

    print("Groq Response:", answer)
