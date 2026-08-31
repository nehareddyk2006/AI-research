
import hashlib

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


_embedding_model = None

# Cache vector stores by PDF/content hash.
_vector_store_cache = {}


def get_embedding_model():

    global _embedding_model

    if _embedding_model is None:

        print(
            "RAG: Loading embedding model...",
            flush=True
        )

        _embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        print(
            "RAG: Embedding model loaded.",
            flush=True
        )

    return _embedding_model


def get_file_hash(file_bytes):

    return hashlib.sha256(
        file_bytes
    ).hexdigest()


def create_vector_store(chunks):

    print(
        f"RAG: Creating vector store from {len(chunks)} chunks...",
        flush=True
    )

    embedding_model = get_embedding_model()

    print(
        "RAG: Creating FAISS index...",
        flush=True
    )

    vector_store = FAISS.from_texts(
        texts=chunks,
        embedding=embedding_model
    )

    print(
        "RAG: FAISS index created.",
        flush=True
    )

    return vector_store


def get_or_create_vector_store(
    file_bytes,
    chunks
):

    file_hash = get_file_hash(
        file_bytes
    )

    if file_hash in _vector_store_cache:

        print(
            "RAG: Reusing cached FAISS index.",
            flush=True
        )

        return _vector_store_cache[file_hash]

    print(
        "RAG: No cached index found. Creating one...",
        flush=True
    )

    vector_store = create_vector_store(
        chunks
    )

    # Keep the cache small.
    # Only retain the most recent 3 papers.
    if len(_vector_store_cache) >= 3:

        oldest_key = next(
            iter(_vector_store_cache)
        )

        del _vector_store_cache[
            oldest_key
        ]

    _vector_store_cache[file_hash] = (
        vector_store
    )

    return vector_store

