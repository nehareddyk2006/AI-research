
import os

from dotenv import load_dotenv
from google import genai


load_dotenv()


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.1-flash-lite"
)


def ask_question(vector_store, question):

    print(
        f"RAG: Searching for question: {question}",
        flush=True
    )

    # Retrieve only the most relevant chunks.
    docs = vector_store.similarity_search(
        question,
        k=4
    )

    print(
        f"RAG: Retrieved {len(docs)} documents.",
        flush=True
    )

    if not docs:

        return (
            "I couldn't find relevant information "
            "in the uploaded paper."
        )

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    print(
        f"RAG: Context length: {len(context)} characters.",
        flush=True
    )

    prompt = f"""
You are ResearchWeaver AI, a research paper assistant.

Answer the user's question using the retrieved paper context.

Rules:
- Treat the paper context as the primary source.
- Do not invent facts or quotes.
- If the paper does not directly answer the question,
  clearly say that and provide a reasonable inference if useful.
- Keep the answer concise and useful.
- Use bullets when appropriate.

PAPER CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""

    print(
        "RAG: Sending context to Gemini...",
        flush=True
    )

    try:

        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        print(
            "RAG: Gemini response received.",
            flush=True
        )

        if response.text:

            return response.text.strip()

        return (
            "I couldn't generate a response. "
            "Please try asking the question differently."
        )

    except Exception as e:

        print(
            f"RAG: Gemini error: {e}",
            flush=True
        )

        return (
            "An error occurred while generating the answer:\n\n"
            f"{str(e)}"
        )
