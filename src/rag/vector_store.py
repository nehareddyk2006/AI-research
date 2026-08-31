import hashlib
import os

from dotenv import load_dotenv
from google import genai
from langchain_community.vectorstores import FAISS
from langchain_core.embeddings import Embeddings

load_dotenv()


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


EMBEDDING_MODEL = "gemini-embedding-001"

_vector_store_cache = {}


class GeminiEmbeddings(Embeddings):

    def embed_documents(self, texts):

        print(
            f"RAG: Embedding {len(texts)} chunks...",
            flush=True
        )

        embeddings = []

        for text in texts:

            response = client.models.embed_content(
                model=EMBEDDING_MODEL,
                contents=text
            )

            embeddings.append(
                response.embeddings[0].values
            )

        return embeddings

    def embed_query(self, text):

        response = client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=text
        )

        return response.embeddings[0].values


_embedding_model = None


def get_embedding_model():

    global _embedding_model

    if _embedding_model is None:

        print(
            "RAG: Initializing Gemini embeddings...",
            flush=True
        )

        _embedding_model = GeminiEmbeddings()

        print(
            "RAG: Gemini embeddings ready.",
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

    if len(_vector_store_cache) >= 3:

        oldest_key = next(
            iter(_vector_store_cache)
        )

        del _vector_store_cache[
            oldest_key
        ]

    _vector_store_cache[file_hash] = vector_store

    return vector_store