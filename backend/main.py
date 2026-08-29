from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from src.extraction.pdf_reader import extract_pdf
from src.ai.analyzer import analyze_paper


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
async def analyze(file: UploadFile = File(...)):

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

        paper = extract_pdf(
            FileWrapper(file_bytes)
        )

        from src.rag.chunker import chunk_text
        from src.rag.vector_store import create_vector_store
        import src.rag.chatbot

        chunks = chunk_text(
            paper.get("text", "")
        )

        vector_store = create_vector_store(
            chunks
        )

        answer = src.rag.chatbot.ask_question(
            vector_store,
            question
        )

        return {
            "question": question,
            "answer": answer
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

        vector_store = create_vector_store(
            chunks
        )

        answer = src.rag.chatbot.ask_question(
            vector_store,
            question
        )

        return {
            "question": question,
            "answer": answer
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )