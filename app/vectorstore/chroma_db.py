# app/vectorstore/chroma_db.py

from langchain_chroma import Chroma

CHROMA_PATH = "./chroma_db"

def get_vectorstore(embedding_model):
    vectorstore = Chroma(
        collection_name="docmentor",
        embedding_function=embedding_model,
        persist_directory=CHROMA_PATH
    )
    return vectorstore
