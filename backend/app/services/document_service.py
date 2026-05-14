import shutil
from pathlib import Path
from uuid import uuid4

import chromadb
from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.ai.embeddings import generate_embedding, generate_embeddings
from app.ai.llm_client import generate_ai_response
from app.ai.prompts import DOCUMENT_QA_SYSTEM_PROMPT, build_document_qa_prompt
from app.config import settings
from app.models.document import Document as DocumentModel
from app.models.document_chunk import DocumentChunk
from app.utils.pdf_reader import extract_text_from_pdf
from app.utils.text_splitter import split_text_into_chunks


def get_chroma_collection():
    client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIR)

    return client.get_or_create_collection(
        name=settings.CHROMA_COLLECTION_NAME,
    )


def ensure_upload_dir() -> Path:
    upload_dir = Path(settings.UPLOAD_DIR)
    upload_dir.mkdir(parents=True, exist_ok=True)
    return upload_dir


def validate_pdf_file(file: UploadFile) -> None:
    filename = file.filename or ""

    if not filename.lower().endswith(".pdf"):
        raise ValueError("Only PDF files are supported in this version.")


async def save_uploaded_file(file: UploadFile) -> Path:
    upload_dir = ensure_upload_dir()

    original_name = file.filename or "uploaded.pdf"
    safe_name = original_name.replace(" ", "_")
    unique_name = f"{uuid4().hex}_{safe_name}"

    file_path = upload_dir / unique_name

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return file_path


async def process_uploaded_document(db: Session, file: UploadFile) -> dict:
    validate_pdf_file(file)

    file_path = await save_uploaded_file(file)

    document = DocumentModel(
        file_name=file.filename or file_path.name,
        file_type="pdf",
        file_path=str(file_path),
        processed_status="Pending",
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    try:
        extracted_text = extract_text_from_pdf(str(file_path))
        chunks = split_text_into_chunks(extracted_text)

        if not chunks:
            document.processed_status = "Failed"
            db.commit()
            raise ValueError("No readable text could be extracted from the PDF.")

        chunk_objects = []

        for index, chunk_text in enumerate(chunks):
            chunk = DocumentChunk(
                document_id=document.id,
                chunk_index=index,
                chunk_text=chunk_text,
                chroma_collection=settings.CHROMA_COLLECTION_NAME,
            )
            chunk_objects.append(chunk)

        db.add_all(chunk_objects)
        db.commit()

        for chunk in chunk_objects:
            db.refresh(chunk)

        embeddings = generate_embeddings(chunks)
        collection = get_chroma_collection()

        collection.add(
            ids=[f"chunk-{chunk.id}" for chunk in chunk_objects],
            documents=chunks,
            embeddings=embeddings,
            metadatas=[
                {
                    "document_id": document.id,
                    "chunk_id": chunk.id,
                    "file_name": document.file_name,
                    "chunk_index": chunk.chunk_index,
                }
                for chunk in chunk_objects
            ],
        )

        document.processed_status = "Processed"
        db.commit()
        db.refresh(document)

        return {
            "id": document.id,
            "file_name": document.file_name,
            "file_type": document.file_type,
            "processed_status": document.processed_status,
            "chunks_created": len(chunks),
            "uploaded_at": document.uploaded_at,
        }

    except Exception:
        document.processed_status = "Failed"
        db.commit()
        raise


def list_documents(db: Session) -> list[dict]:
    documents = (
        db.query(DocumentModel)
        .order_by(DocumentModel.uploaded_at.desc())
        .all()
    )

    return [
        {
            "id": document.id,
            "file_name": document.file_name,
            "file_type": document.file_type,
            "processed_status": document.processed_status,
            "uploaded_at": document.uploaded_at,
        }
        for document in documents
    ]


def retrieve_relevant_chunks(question: str, top_k: int = 5) -> list[dict]:
    question_embedding = generate_embedding(question)

    collection = get_chroma_collection()

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=top_k,
    )

    retrieved_context: list[dict] = []

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    for document_text, metadata, distance in zip(documents, metadatas, distances):
        retrieved_context.append(
            {
                "text": document_text,
                "metadata": metadata,
                "distance": distance,
            }
        )

    return retrieved_context


def ask_document_question(
    db: Session,
    question: str,
    top_k: int = 5,
) -> dict:
    retrieved_context = retrieve_relevant_chunks(
        question=question,
        top_k=top_k,
    )

    user_prompt = build_document_qa_prompt(
        question=question,
        retrieved_context=retrieved_context,
    )

    answer = generate_ai_response(
        system_prompt=DOCUMENT_QA_SYSTEM_PROMPT,
        user_prompt=user_prompt,
    )

    return {
        "question": question,
        "answer": answer,
        "retrieved_chunks": retrieved_context,
    }