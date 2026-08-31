from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from src.extraction.pdf_reader import extract_pdf
from src.ai.analyzer import analyze_paper

print("🔥 RESEARCHWEAVER MAIN.PY LOADED", flush=True)
print(f"🔥 MAIN FILE: {__file__}", flush=True)

app = FastAPI(
    title="ResearchWeaver AI API",
    description="Backend API for ResearchWeaver AI",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():

    return {
        "message": "ResearchWeaver AI API is running",
        "status": "ok",
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


@app.post("/analyze")
async def analyze(
    file: UploadFile = File(...)
):

    if not file.filename.lower().endswith(".pdf"):

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )

    try:

        file_bytes = await file.read()

        class FileWrapper:

            def __init__(self, data):
                self.data = data

            def read(self):
                return self.data

        paper = extract_pdf(
            FileWrapper(file_bytes)
        )

        analysis = analyze_paper(
            paper.get("text", "")
        )

        return {
            "paper": paper,
            "analysis": analysis,
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.post("/chat")
async def chat(
    file: UploadFile = File(...),
    question: str = ""
):

    if not file.filename.lower().endswith(".pdf"):

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )

    if not question.strip():

        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    try:

        file_bytes = await file.read()

        class FileWrapper:

            def __init__(self, data):
                self.data = data

            def read(self):
                return self.data

        print("CHAT: PDF received", flush=True)

        # -----------------------------------------
        # Extract paper
        # -----------------------------------------

        paper = extract_pdf(
            FileWrapper(file_bytes)
        )

        print("CHAT: PDF extracted", flush=True)

        # -----------------------------------------
        # Build chunks
        # -----------------------------------------

        from src.rag.chunker import chunk_text

        chunks = chunk_text(
            paper.get("text", "")
        )

        print(f"CHAT: {len(chunks)} chunks created", flush=True)

        if not chunks:

            raise HTTPException(
                status_code=400,
                detail="No readable text was found in the PDF."
            )

        # -----------------------------------------
        # Get cached / new vector store
        # -----------------------------------------

        from src.rag.vector_store import (
            get_or_create_vector_store
        )

        vector_store = get_or_create_vector_store(
            file_bytes,
            chunks
        )

        print("CHAT: Vector store ready", flush=True)

        # -----------------------------------------
        # Ask chatbot
        # -----------------------------------------

        from src.rag.chatbot import ask_question

        answer = ask_question(
            vector_store,
            question
        )

        return {
            "question": question,
            "answer": answer
        }

    except HTTPException:
        raise

    except Exception as e:

        print(
            f"CHAT ERROR: {e}",
            flush=True
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
