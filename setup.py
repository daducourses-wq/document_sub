from setuptools import setup, find_packages

setup(
    name="document_sub", 
    author="swapnil shinde",   
    version="0.1.0",
    packages=find_packages(),
)
import os
from typing import List, Optional, Any, Dict
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

from src.document_ingestion.data_ingestion import (
DocHandler,
DocumentComparator,
ChatIngestor,
)
from src.document_analyzer.data_analysis import DocumentAnalyzer
from src.document_compare.document_comparator import DocumentComparatorLLM
from src.document_chat.retrieval import ConversationalRAG
from utils.document_ops import FastAPIFileAdapter,read_pdf_via_handler
from logger import GLOBAL_LOGGER as log

FAISS_BASE = os.getenv("FAISS_BASE", "faiss_index")
UPLOAD_BASE = os.getenv("UPLOAD_BASE", "data")
@@ -37,33 +38,39 @@

@app.get("/", response_class=HTMLResponse)
async def serve_ui(request: Request):
    log.info("Serving UI homepage.")
resp = templates.TemplateResponse("index.html", {"request": request})
resp.headers["Cache-Control"] = "no-store"
return resp

@app.get("/health")
def health() -> Dict[str, str]:
    log.info("Health check passed.")
return {"status": "ok", "service": "document-portal"}

# ---------- ANALYZE ----------
@app.post("/analyze")
async def analyze_document(file: UploadFile = File(...)) -> Any:
try:
        log.info(f"Received file for analysis: {file.filename}")
dh = DocHandler()
saved_path = dh.save_pdf(FastAPIFileAdapter(file))
text = read_pdf_via_handler(dh, saved_path)
analyzer = DocumentAnalyzer()
result = analyzer.analyze_document(text)
        log.info("Document analysis complete.")
return JSONResponse(content=result)
except HTTPException:
raise
except Exception as e:
        log.exception("Error during document analysis")
raise HTTPException(status_code=500, detail=f"Analysis failed: {e}")

# ---------- COMPARE ----------
@app.post("/compare")
async def compare_documents(reference: UploadFile = File(...), actual: UploadFile = File(...)) -> Any:
try:
        log.info(f"Comparing files: {reference.filename} vs {actual.filename}")
dc = DocumentComparator()
ref_path, act_path = dc.save_uploaded_files(
FastAPIFileAdapter(reference), FastAPIFileAdapter(actual)
@@ -72,10 +79,12 @@
combined_text = dc.combine_documents()
comp = DocumentComparatorLLM()
df = comp.compare_documents(combined_text)
        log.info("Document comparison completed.")
return {"rows": df.to_dict(orient="records"), "session_id": dc.session_id}
except HTTPException:
raise
except Exception as e:
        log.exception("Comparison failed")
raise HTTPException(status_code=500, detail=f"Comparison failed: {e}")

# ---------- CHAT: INDEX ----------
@@ -89,6 +98,7 @@
k: int = Form(5),
) -> Any:
try:
        log.info(f"Indexing chat session. Session ID: {session_id}, Files: {[f.filename for f in files]}")
wrapped = [FastAPIFileAdapter(f) for f in files]
# this is my main class for storing a data into VDB
# created a object of ChatIngestor
@@ -103,10 +113,12 @@
ci.built_retriver(  # if your method name is actually build_retriever, fix it there as well
wrapped, chunk_size=chunk_size, chunk_overlap=chunk_overlap, k=k
)
        log.info(f"Index created successfully for session: {ci.session_id}")
return {"session_id": ci.session_id, "k": k, "use_session_dirs": use_session_dirs}
except HTTPException:
raise
except Exception as e:
        log.exception("Chat index building failed")
raise HTTPException(status_code=500, detail=f"Indexing failed: {e}")

# ---------- CHAT: QUERY ----------
@@ -118,6 +130,7 @@
k: int = Form(5),
) -> Any:
try:
        log.info(f"Received chat query: '{question}' | session: {session_id}")
if use_session_dirs and not session_id:
raise HTTPException(status_code=400, detail="session_id is required when use_session_dirs=True")

@@ -128,6 +141,7 @@
rag = ConversationalRAG(session_id=session_id)
rag.load_retriever_from_faiss(index_dir, k=k, index_name=FAISS_INDEX_NAME)  # build retriever + chain
response = rag.invoke(question, chat_history=[])
        log.info("Chat query handled successfully.")

return {
"answer": response,
@@ -138,13 +152,9 @@
except HTTPException:
raise
except Exception as e:
        log.exception("Chat query failed")
raise HTTPException(status_code=500, detail=f"Query failed: {e}")






# command for executing the fast api
# uvicorn api.main:app --reload    
# uvicorn api.main:app --port 8080 --reload    
#uvicorn api.main:app --host 0.0.0.0 --port 8080 --reload