from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

with open("text_chunks.txt", "r") as f:
    text_chunks = f.read().splitlines()

embeddings = model.encode(text_chunks, show_progress_bar=True)

np.save("embeddings.npy", embeddings)
print("Embeddings saved to embeddings.npy")
