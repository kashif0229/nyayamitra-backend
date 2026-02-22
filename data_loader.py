# data_loader.py
import chromadb
from sentence_transformers import SentenceTransformer
import os

# Initialize ChromaDB - this creates a local database folder called 'chroma_db'
client = chromadb.PersistentClient(path="./chroma_db")

# This is our embedding model - it converts text into numbers so we can search it
# Think of it like converting words into coordinates on a map
model = SentenceTransformer('all-MiniLM-L6-v2')

def load_legal_data():
    """
    Reads all .txt files from legal_data/ folder
    Splits them into chunks and stores in ChromaDB
    """
    
    # Create or get a collection (like a table in a database)
    try:
        collection = client.get_collection("legal_docs")
        print("✅ Legal database already exists. Skipping load.")
        return collection
    except:
        collection = client.create_collection("legal_docs")
    
    print("📚 Loading legal data into database...")
    
    legal_data_path = "./legal_data"
    all_chunks = []
    all_ids = []
    all_metadata = []
    
    chunk_id = 0
    
    # Loop through every .txt file in the legal_data folder
    for filename in os.listdir(legal_data_path):
        if filename.endswith(".txt"):
            filepath = os.path.join(legal_data_path, filename)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Split the file into chunks by double newline
            # Each "chunk" is one legal section
            chunks = [c.strip() for c in content.split('\n\n') if c.strip()]
            
            for chunk in chunks:
                if len(chunk) > 50:  # Skip very short chunks
                    all_chunks.append(chunk)
                    all_ids.append(f"chunk_{chunk_id}")
                    all_metadata.append({"source": filename, "chunk_id": chunk_id})
                    chunk_id += 1
    
    # Convert all text chunks to embeddings (numbers) using our model
    print(f"🔄 Converting {len(all_chunks)} legal sections to embeddings...")
    embeddings = model.encode(all_chunks).tolist()
    
    # Store everything in ChromaDB
    collection.add(
        documents=all_chunks,
        embeddings=embeddings,
        ids=all_ids,
        metadatas=all_metadata
    )
    
    print(f"✅ Successfully loaded {len(all_chunks)} legal sections into database!")
    return collection


def search_legal_database(query: str, n_results: int = 5):
    """
    Given a user query, find the most relevant legal sections
    """
    collection = client.get_collection("legal_docs")
    
    # Convert the user's query to an embedding
    query_embedding = model.encode([query]).tolist()
    
    # Search ChromaDB for the most similar legal sections
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results
    )
    
    # Return the matching legal text
    return results['documents'][0]  # List of relevant legal sections