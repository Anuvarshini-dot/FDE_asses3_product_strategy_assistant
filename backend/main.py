import io
import os
from typing import List

from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from agents.chat_agent import run_chat
from graph.workflow import build_workflow
from utils.document_processor import extract_text
from utils.pdf_generator import generate_pdf
from utils.vector_store import VectorStore

load_dotenv()

app = FastAPI(title="Product Strategy Assistant API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

vector_store = VectorStore()
document_texts: List[str] = []
document_names: List[str] = []
analysis_results: dict = {}
doc_counter = 0


class ChatRequest(BaseModel):
    message: str
    history: list = []


@app.get("/")
def root():
    return {"status": "ok", "service": "Product Strategy Assistant"}


@app.get("/documents")
def get_documents():
    return {"documents": document_names, "count": len(document_names)}


@app.post("/upload")
async def upload_documents(files: List[UploadFile] = File(...)):
    global doc_counter
    texts = []
    for file in files:
        content = await file.read()
        text = extract_text(content, file.filename)
        if text.strip():
            texts.append(text)
            document_texts.append(text)
            document_names.append(file.filename)

    if texts:
        ids = [f"doc_{doc_counter + i}" for i in range(len(texts))]
        doc_counter += len(texts)
        vector_store.add_documents(texts, ids)

    return {"uploaded": len(texts), "total_documents": len(document_texts)}


@app.post("/analyze")
async def run_analysis():
    if not document_texts:
        raise HTTPException(status_code=400, detail="No documents uploaded. Please upload documents first.")

    combined = "\n\n---\n\n".join(document_texts)
    workflow = build_workflow()
    result = workflow.invoke({"documents": combined})
    analysis_results.clear()
    analysis_results.update(result)
    return {"status": "complete", "sections": [k for k in result if k != "documents"]}


@app.get("/results")
def get_results():
    if not analysis_results:
        raise HTTPException(status_code=404, detail="No analysis results yet. Run /analyze first.")
    return {k: v for k, v in analysis_results.items() if k != "documents"}


@app.post("/chat")
async def chat(request: ChatRequest):
    if not document_texts and not analysis_results:
        raise HTTPException(status_code=400, detail="No data available. Upload documents first.")

    relevant = vector_store.search(request.message, n_results=3)
    context_parts = [f"Document excerpt:\n{doc[:800]}" for doc in relevant]

    if analysis_results:
        summary = analysis_results.get("executive_summary", "")[:1500]
        if summary:
            context_parts.append(f"Executive Summary:\n{summary}")

    context = "\n\n".join(context_parts)
    reply = run_chat(request.message, request.history, context)
    return {"response": reply}


@app.get("/report/pdf")
def download_pdf():
    if not analysis_results:
        raise HTTPException(status_code=404, detail="No analysis results yet. Run /analyze first.")

    pdf_bytes = generate_pdf(analysis_results)
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=product_strategy_report.pdf"},
    )


@app.delete("/reset")
def reset():
    global doc_counter
    document_texts.clear()
    document_names.clear()
    analysis_results.clear()
    vector_store.clear()
    doc_counter = 0
    return {"status": "reset complete"}
