import os
import json
import re
from datetime import datetime
import pdfplumber
from dateutil import parser as date_parser

def extract_text_from_pdf(pdf_path):
    """Extrae texto de un PDF usando pdfplumber."""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def parse_messages(text, source):
    """Parsea el texto para extraer mensajes con fecha, hora, autor, texto."""
    messages = []
    # Encontrar todas las fechas
    date_pattern = r'(\d{4}-\d{2}-\d{2})'
    dates = re.findall(date_pattern, text)
    date_positions = []
    for match in re.finditer(date_pattern, text):
        date_positions.append((match.start(), match.group()))
    
    # Encontrar todos los mensajes
    message_pattern = r'\s*\[(\d{1,2}:\d{2} (?:AM|PM))\]\s*(.+?):\s*(.+?)(?=\s*\[|\d{4}-\d{2}-\d{2}|$)'
    for match in re.finditer(message_pattern, text, re.DOTALL):
        hora, autor, texto_raw = match.groups()
        # Encontrar la fecha más cercana antes de este mensaje
        pos = match.start()
        current_date = None
        for d_pos, d in reversed(date_positions):
            if d_pos < pos:
                current_date = d
                break
        messages.append({
            'fecha': current_date,
            'hora': hora,
            'autor': autor.strip(),
            'texto_raw': texto_raw.strip(),
            'source': source
        })
    return messages

def chunk_text(text, chunk_size=200, overlap=30):
    """Divide texto en chunks de palabras con overlap."""
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk = ' '.join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
        if start >= len(words):
            break
    return chunks

def process_file(file_path):
    """Procesa un archivo (PDF o TXT) y extrae mensajes."""
    if file_path.endswith('.pdf'):
        text = extract_text_from_pdf(file_path)
    elif file_path.endswith('.txt'):
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        return []
    return parse_messages(text, os.path.basename(file_path))

def main():
    data_dir = 'data'
    corpus = []
    doc_id = 0
    for filename in os.listdir(data_dir):
        file_path = os.path.join(data_dir, filename)
        if filename.endswith(('.pdf', '.txt')):
            messages = process_file(file_path)
            for msg in messages:
                doc_id += 1
                msg['id'] = doc_id
                # Si el texto es largo, chunkear
                if len(msg['texto_raw'].split()) > 300:
                    chunks = chunk_text(msg['texto_raw'])
                    for chunk_idx, chunk in enumerate(chunks):
                        chunk_entry = msg.copy()
                        chunk_entry['texto_raw'] = chunk
                        chunk_entry['chunk_id'] = chunk_idx
                        chunk_entry['doc_id'] = doc_id
                        corpus.append(chunk_entry)
                else:
                    msg['chunk_id'] = 0
                    msg['doc_id'] = doc_id
                    corpus.append(msg)
    
    with open('corpus.jsonl', 'w', encoding='utf-8') as f:
        for entry in corpus:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    print(f"Procesados {len(corpus)} chunks en corpus.jsonl")

if __name__ == "__main__":
    main()