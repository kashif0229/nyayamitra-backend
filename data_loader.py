# data_loader.py
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

CHUNKS = []
VECTORIZER = None
MATRIX = None
DB_FILE = "legal_db.pkl"

def load_legal_data():
    global CHUNKS, VECTORIZER, MATRIX

    if os.path.exists(DB_FILE):
        print("✅ Legal database already exists. Loading...")
        with open(DB_FILE, "rb") as f:
            data = pickle.load(f)
            CHUNKS = data["chunks"]
            VECTORIZER = data["vectorizer"]
            MATRIX = data["matrix"]
        print(f"✅ Loaded {len(CHUNKS)} legal sections.")
        return

    print("📚 Loading legal data into database...")

    legal_data_path = "./legal_data"

    for filename in os.listdir(legal_data_path):
        if filename.endswith(".txt"):
            with open(os.path.join(legal_data_path, filename), 'r', encoding='utf-8') as f:
                content = f.read()
            chunks = [c.strip() for c in content.split('\n\n') if len(c.strip()) > 50]
            CHUNKS.extend(chunks)

    print(f"🔄 Indexing {len(CHUNKS)} legal sections...")

    VECTORIZER = TfidfVectorizer(stop_words='english')
    MATRIX = VECTORIZER.fit_transform(CHUNKS)

    with open(DB_FILE, "wb") as f:
        pickle.dump({"chunks": CHUNKS, "vectorizer": VECTORIZER, "matrix": MATRIX}, f)

    print(f"✅ Legal database ready with {len(CHUNKS)} sections!")


def search_legal_database(query: str, n_results: int = 5):
    global CHUNKS, VECTORIZER, MATRIX

    if not CHUNKS:
        load_legal_data()

    query_vec = VECTORIZER.transform([query])
    scores = cosine_similarity(query_vec, MATRIX).flatten()
    top_indices = np.argsort(scores)[::-1][:n_results]

    return [CHUNKS[i] for i in top_indices if scores[i] > 0]
```

Then also update `requirements.txt` — make sure it has **no chromadb**:
```
fastapi==0.111.0
uvicorn==0.30.1
python-dotenv==1.0.1
groq==0.9.0
scikit-learn==1.5.0
numpy==1.26.4
python-multipart==0.0.9
requests==2.32.3