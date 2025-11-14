import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

def load_corpus(corpus_path):
    """Carga el corpus desde jsonl."""
    corpus = []
    with open(corpus_path, 'r', encoding='utf-8') as f:
        for line in f:
            corpus.append(json.loads(line))
    return corpus

def main():
    model_name = 'sentence-transformers/all-MiniLM-L6-v2'
    model = SentenceTransformer(model_name)
    
    corpus = load_corpus('corpus.jsonl')
    texts = [entry['texto_raw'] for entry in corpus]
    ids = [entry['id'] for entry in corpus]
    
    print(f"Generando embeddings para {len(texts)} textos...")
    embeddings = model.encode(texts, show_progress_bar=True, normalize_embeddings=True)
    
    # Guardar embeddings
    np.save('embeddings.npy', embeddings)
    
    # Crear índice FAISS
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)  # Inner product para cosine (ya normalizados)
    index.add(embeddings)
    
    # Guardar índice
    faiss.write_index(index, 'index.faiss')
    
    # Guardar mapping de ids
    with open('ids_mapping.json', 'w') as f:
        json.dump(ids, f)
    
    print("Índice creado y guardado.")

if __name__ == "__main__":
    main()