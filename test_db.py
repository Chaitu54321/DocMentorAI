# test_db.py

from app.ingestion.embeddings import get_embedding_model
from app.vectorstore.chroma_db import get_vectorstore

embedding_model = get_embedding_model()
vectorstore = get_vectorstore(
    embedding_model
)

results = vectorstore.similarity_search(
    "What is Newton's first law?",
    k=3
)

for result in results:
    print("\n--------------------")
    print(result.page_content)
    print(result.metadata)
