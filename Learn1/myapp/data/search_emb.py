import faiss
import numpy as np

embeddings = np.load("embeddings.npy")

embedding_dim = embeddings.shape[1]

index = faiss.IndexFlatL2(embedding_dim)

index.add(embeddings)

faiss.write_index(index, "faiss_index.bin")
print("FAISS index saved as faiss_index.bin")
