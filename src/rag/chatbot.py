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
    """
    Answer questions about the uploaded research paper using RAG.

    The vector store retrieves the most relevant sections
    from the uploaded paper, which are then provided to Gemini.
    """

    print(
        f"RAG: Searching for question: {question}",
        flush=True
    )

    # --------------------------------------------------
    # Retrieve relevant chunks from the paper
    # --------------------------------------------------

    docs = vector_store.max_marginal_relevance_search(
        question,
        k=5,
        fetch_k=15
    )

    print(
        f"RAG: Retrieved {len(docs)} documents.",
        flush=True
    )

    if not docs:
        return (
            "I couldn't retrieve any relevant sections from "
            "the uploaded paper. Please try rephrasing your question."
        )

    # --------------------------------------------------
    # Build context
    # --------------------------------------------------

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    print(
        f"RAG: Context length: {len(context)} characters.",
        flush=True
    )

    # --------------------------------------------------
    # Gemini prompt
    # --------------------------------------------------

    prompt = f"""
You are ResearchWeaver AI, an intelligent research assistant.

Your job is to help users understand an uploaded research paper.

The retrieved context below comes directly from the paper.

=========================
GUIDELINES
=========================

1. Use the retrieved context as your PRIMARY source.

2. If the answer is explicitly stated in the context,
answer confidently.

3. If the answer is only partially available,
provide the best possible answer from the available context.

4. If the paper does not explicitly answer the question,
use your own research knowledge to provide a helpful inference.

5. Clearly separate:

• Information from the paper

• Your own inference or general research knowledge

6. Never invent quotes.

7. Never claim the paper says something it doesn't.

8. Avoid replying only with:

"I couldn't find that information."

Instead, explain what the paper discusses and provide useful
inferences whenever appropriate.

9. Keep answers concise but informative.

10. Use bullet points whenever helpful.

=========================
RETRIEVED CONTEXT
=========================

{context}

=========================
QUESTION
=========================

{question}

=========================
ANSWER
=========================
"""

    # --------------------------------------------------
    # Generate Gemini response
    # --------------------------------------------------

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
            "I couldn't generate a response for that question. "
            "Please try asking it differently."
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