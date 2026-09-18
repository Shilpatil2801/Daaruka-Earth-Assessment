import os

import fitz
import chromadb

from sentence_transformers import SentenceTransformer


# ============================================================
# CONFIGURATION
# ============================================================

DOCUMENTS_FOLDER = "./knowledge_base/documents"
VECTOR_STORE_PATH = "./vector_store"
COLLECTION_NAME = "environmental_knowledge"

# Local embedding model — no API key required
embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# ============================================================
# CHROMA DATABASE
# ============================================================

chroma_client = chromadb.PersistentClient(
    path=VECTOR_STORE_PATH
)

collection = chroma_client.get_or_create_collection(
    name=COLLECTION_NAME
)


# ============================================================
# PDF TEXT EXTRACTION
# ============================================================

def extract_pdf_text(pdf_path):

    document = fitz.open(pdf_path)

    pages = []

    for page_number, page in enumerate(document):

        text = page.get_text()

        if text.strip():

            pages.append({
                "page": page_number + 1,
                "text": text
            })

    document.close()

    return pages


# ============================================================
# TEXT CHUNKING
# ============================================================

def chunk_text(text, chunk_size=1200, overlap=200):

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end]

        if chunk.strip():

            chunks.append(chunk.strip())

        start += chunk_size - overlap

    return chunks


# ============================================================
# CREATE EMBEDDING
# ============================================================

def create_embedding(text):

    embedding = embedding_model.encode(
        text,
        normalize_embeddings=True
    )

    return embedding.tolist()


# ============================================================
# PROCESS ONE PDF
# ============================================================

def ingest_document(pdf_path):

    filename = os.path.basename(pdf_path)

    print()
    print("=" * 60)
    print(f"Processing: {filename}")
    print("=" * 60)

    pages = extract_pdf_text(pdf_path)

    print(f"Pages with text: {len(pages)}")

    total_chunks = 0

    for page in pages:

        chunks = chunk_text(
            page["text"]
        )

        for chunk_index, chunk in enumerate(chunks):

            embedding = create_embedding(
                chunk
            )

            document_id = (
                f"{filename}"
                f"_page_{page['page']}"
                f"_chunk_{chunk_index}"
            )

            collection.add(
                ids=[document_id],

                documents=[chunk],

                embeddings=[embedding],

                metadatas=[{
                    "source": filename,
                    "page": page["page"],
                    "chunk": chunk_index
                }]
            )

            total_chunks += 1

    print(f"Chunks created: {total_chunks}")
    print(f"Finished: {filename}")


# ============================================================
# INGEST ALL DOCUMENTS
# ============================================================

def ingest_all_documents():

    if not os.path.exists(
        DOCUMENTS_FOLDER
    ):

        raise FileNotFoundError(
            f"Folder not found: "
            f"{DOCUMENTS_FOLDER}"
        )

    pdf_files = [
        filename
        for filename in os.listdir(
            DOCUMENTS_FOLDER
        )
        if filename.lower().endswith(".pdf")
    ]

    if not pdf_files:

        raise FileNotFoundError(
            "No PDF files found in "
            "knowledge_base/documents/"
        )

    print()
    print("=" * 60)
    print("DARUKAA.EARTH")
    print("ENVIRONMENTAL KNOWLEDGE INGESTION")
    print("=" * 60)

    print(
        f"PDF files found: {len(pdf_files)}"
    )

    for filename in pdf_files:

        pdf_path = os.path.join(
            DOCUMENTS_FOLDER,
            filename
        )

        ingest_document(
            pdf_path
        )

    print()
    print("=" * 60)
    print("KNOWLEDGE BASE CREATED SUCCESSFULLY")
    print("=" * 60)

    print(
        f"Total chunks stored: "
        f"{collection.count()}"
    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    ingest_all_documents()