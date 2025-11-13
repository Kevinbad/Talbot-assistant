import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import streamlit as st

def load_index_and_mappings():
    """Carga el índice FAISS, embeddings y mappings."""
    index = faiss.read_index('index.faiss')
    embeddings = np.load('embeddings.npy')
    with open('ids_mapping.json', 'r') as f:
        ids_mapping = json.load(f)
    with open('corpus.jsonl', 'r', encoding='utf-8') as f:
        corpus = [json.loads(line) for line in f]
    return index, embeddings, ids_mapping, corpus

def is_yes_no_question(question):
    """Detecta si la pregunta es de sí/no."""
    yes_no_keywords = ['puedo', 'se puede', 'es posible', 'debo', 'hay que', 'tengo que', 'está permitido']
    question_lower = question.lower()
    return any(keyword in question_lower for keyword in yes_no_keywords)

def extract_yes_no_answer(relevant_texts):
    """Extrae respuesta sí/no de los textos relevantes."""
    combined_text = ' '.join([text for _, text in relevant_texts]).lower()
    # Palabras que indican NO
    no_words = ['no', 'no puedes', 'no se puede', 'no podemos', 'prohibido', 'cancelado']
    # Palabras que indican SÍ
    yes_words = ['si', 'sí', 'puedes', 'se puede', 'podemos', 'tenemos', 'volvemos', 'disponible', 'licencia', 'habilitado']
    
    has_no = any(word in combined_text for word in no_words)
    has_yes = any(word in combined_text for word in yes_words)
    
    if has_no and not has_yes:
        return "No"
    elif has_yes:
        return "Sí"
    else:
        return None

@st.cache_resource
def load_model():
    model_name = 'sentence-transformers/all-MiniLM-L6-v2'
    return SentenceTransformer(model_name)

def answer_query(question, top_k=5):
    """Responde a una consulta usando búsqueda semántica."""
    model = load_model()
    
    index, embeddings, ids_mapping, corpus = load_index_and_mappings()
    
    # Generar embedding de la pregunta
    query_embedding = model.encode([question], normalize_embeddings=True)[0]
    
    # Buscar en FAISS
    distances, indices = index.search(np.array([query_embedding]), top_k)
    
    hits = []
    relevant_texts = []
    for i, idx in enumerate(indices[0]):
        if idx == -1:
            continue
        entry = corpus[idx]
        score = distances[0][i]
        hits.append({
            "id": entry['id'],
            "score": float(score),
            "fecha": entry.get('fecha', ''),
            "autor": entry.get('autor', ''),
            "text_snippet": entry['texto_raw'],
            "source": entry.get('source', '')
        })
        relevant_texts.append((score, entry['texto_raw']))
    
    # Generar respuesta extractiva simple
    # Ordenar por score, tomar primeras oraciones hasta ~250 chars
    relevant_texts.sort(key=lambda x: x[0], reverse=True)
    answer_parts = []
    char_count = 0
    for _, text in relevant_texts:
        sentences = text.split('. ')
        for sent in sentences:
            if char_count + len(sent) > 250:
                break
            answer_parts.append(sent)
            char_count += len(sent) + 2  # +2 por '. '
        if char_count > 250:
            break
    extractive_answer = '. '.join(answer_parts) + '.'
    
    # Si es pregunta sí/no, intentar respuesta directa
    direct_answer = None
    relevant_hit = None
    if is_yes_no_question(question):
        direct_answer = extract_yes_no_answer(relevant_texts)
        # Encontrar el hit más relevante que contenga palabras clave
        keywords = [word.lower() for word in question.split() if len(word) > 3]
        for hit in hits:
            if any(keyword in hit['text_snippet'].lower() for keyword in keywords):
                relevant_hit = hit
                break
        if not relevant_hit and hits:
            relevant_hit = hits[0]  # Top hit si no hay match
    
    if direct_answer and relevant_hit:
        full_answer = f"{direct_answer}. Según Management en {relevant_hit['fecha']}: {relevant_hit['text_snippet']}"
    else:
        full_answer = extractive_answer
    
    return {
        "answer": full_answer,
        "hits": hits
    }

if __name__ == "__main__":
    # Ejemplo
    result = answer_query("procesamiento de pólizas", top_k=3)
    print(result)