import chromadb
from sentence_transformers import SentenceTransformer


# ============================================================
# CONFIGURATION
# ============================================================

VECTOR_STORE_PATH = "./vector_store"

COLLECTION_NAME = "environmental_knowledge"


# ============================================================
# LOAD EMBEDDING MODEL
# ============================================================

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# ============================================================
# CONNECT TO CHROMADB
# ============================================================

chroma_client = chromadb.PersistentClient(
    path=VECTOR_STORE_PATH
)

collection = chroma_client.get_collection(
    name=COLLECTION_NAME
)


# ============================================================
# CREATE QUERY EMBEDDING
# ============================================================

def create_query_embedding(query):

    embedding = embedding_model.encode(
        query,
        normalize_embeddings=True
    )

    return embedding.tolist()


# ============================================================
# RETRIEVE RELEVANT DOCUMENTS
# ============================================================

def retrieve_documents(query, top_k=5):

    query_embedding = create_query_embedding(
        query
    )

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    documents = results["documents"][0]

    metadatas = results["metadatas"][0]

    distances = results["distances"][0]

    retrieved_documents = []

    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances
    ):

        retrieved_documents.append({

            "text": document,

            "source": metadata.get(
                "source",
                "Unknown"
            ),

            "page": metadata.get(
                "page",
                "Unknown"
            ),

            "chunk": metadata.get(
                "chunk",
                "Unknown"
            ),

            "distance": distance

        })

    return retrieved_documents


# ============================================================
# TEST RETRIEVAL
# ============================================================

if __name__ == "__main__":

    query = """
    How does climate change affect biodiversity,
    ecosystems, land degradation and water availability?
    """

    results = retrieve_documents(
        query,
        top_k=5
    )

    print()
    print("=" * 70)
    print("DARUKAA.EARTH — KNOWLEDGE RETRIEVAL")
    print("=" * 70)

    print(f"\nQuery:\n{query}")

    for i, result in enumerate(results):

        print()
        print("-" * 70)

        print(f"RESULT {i + 1}")

        print(
            f"Source: {result['source']}"
        )

        print(
            f"Page: {result['page']}"
        )

        print(
            f"Distance: {result['distance']:.4f}"
        )

        print("\nRetrieved text:")

        print(
            result["text"][:1000]
        )