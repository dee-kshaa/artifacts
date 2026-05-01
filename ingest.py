"""Ingestion module for building vector index from corpus."""
import json
import os
from typing import Dict, Any, List
import numpy as np

try:
    import faiss
    from sentence_transformers import SentenceTransformer
except ImportError:
    print("Warning: faiss and/or sentence-transformers not installed")
    faiss = None
    SentenceTransformer = None


def ingest_corpus(corpus_path: str, config: Dict[str, Any], output_dir: str = '.') -> None:
    """
    Load corpus and build FAISS vector index.
    
    Args:
        corpus_path: Path to JSON corpus file
        config: Configuration dict with model settings
        output_dir: Directory to save index and metadata
    """
    if not os.path.exists(corpus_path):
        print(f"Corpus file not found: {corpus_path}")
        return
    
    # Load corpus
    with open(corpus_path, 'r') as f:
        corpus = json.load(f)
    
    documents = corpus.get('documents', [])
    if not documents:
        print("No documents in corpus")
        return
    
    print(f"Loading {len(documents)} documents...")
    
    if SentenceTransformer is None:
        print("Skipping vectorization - sentence-transformers not installed")
        # Save corpus as-is
        with open(os.path.join(output_dir, 'corpus.json'), 'w') as f:
            json.dump(corpus, f)
        return
    
    # Initialize model
    model_name = config.get('embedding_model', 'all-MiniLM-L6-v2')
    print(f"Using model: {model_name}")
    model = SentenceTransformer(model_name)
    
    # Extract texts
    texts = [doc.get('content', doc.get('text', '')) for doc in documents]
    
    # Generate embeddings
    print("Generating embeddings...")
    embeddings = model.encode(texts, show_progress_bar=True)
    embeddings = embeddings.astype('float32')
    
    # Build FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    
    # Save index and metadata
    faiss.write_index(index, os.path.join(output_dir, 'faiss_index.bin'))
    
    metadata = {
        'documents': documents,
        'model': model_name,
        'dimension': dimension,
        'count': len(documents)
    }
    with open(os.path.join(output_dir, 'index_metadata.json'), 'w') as f:
        json.dump(metadata, f)
    
    print(f"Index built with {len(documents)} documents")
