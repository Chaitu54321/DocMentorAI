# app/main.py

from fastapi import FastAPI, UploadFile, File, Form
from pathlib import Path
import uuid

from app.ingestion.pdf_loader import load_pdf
from app.ingestion.chunker import chunk_documents
from app.ingestion.embeddings import get_embedding_model
from app.vectorstore.chroma_db import get_vectorstore

app = FastAPI(title="DocMentor AI")

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

embedding_model = get_embedding_model()
vectorstore = get_vectorstore(embedding_model)

@app.get("/")
def read_root():
    return {
        "name": "DocMentor AI",
        "status": "online",
        "docs_url": "/docs"
    }

@app.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...),
    user_id: str = Form(...)
):
    if file.content_type != "application/pdf":
        return {"error": "Only PDF files are supported."}

    document_id = str(uuid.uuid4())
    file_path = UPLOAD_DIR / f"{document_id}.pdf"

    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    documents = load_pdf(str(file_path))
    chunks = chunk_documents(documents)

    for chunk in chunks:
        chunk.metadata["user_id"] = user_id
        chunk.metadata["document_id"] = document_id
        chunk.metadata["filename"] = file.filename

    vectorstore.add_documents(documents=chunks)

    return {
        "message": "PDF uploaded successfully",
        "user_id": user_id,
        "document_id": document_id,
        "filename": file.filename,
        "pages": len(documents),
        "chunks": len(chunks)
    }
