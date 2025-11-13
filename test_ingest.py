import os
import json

def test_ingest():
    # Ejecutar ingest.py si no existe corpus
    if not os.path.exists('corpus.jsonl'):
        os.system('python ingest.py')
    
    assert os.path.exists('corpus.jsonl'), "corpus.jsonl no creado"
    
    with open('corpus.jsonl', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        assert len(lines) > 0, "Corpus vacío"
        
        entry = json.loads(lines[0])
        required_keys = ['id', 'fecha', 'hora', 'autor', 'texto_raw', 'source']
        for key in required_keys:
            assert key in entry, f"Falta clave {key} en entrada"
    
    print("Test ingest pasado.")

if __name__ == "__main__":
    test_ingest()