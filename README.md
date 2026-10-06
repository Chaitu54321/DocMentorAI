# DocMentor AI

**DocMentor AI — Initial Implementation Milestone: PDF Upload → Extraction → Chunking → Embeddings → Chroma**

DocMentor AI is an intelligent document mentorship and learning assistant. This milestone implements the foundational document processing pipeline: accepting PDF uploads from users, extracting text, splitting text into semantically overlapping chunks, computing dense vector embeddings locally using BAAI/bge-small-en-v1.5, and persisting them in Chroma vector DB with multi-user metadata isolation (`user_id`, `document_id`, `filename`, `page`).

---

## 1. Initial Architecture Flow

```
User uploads PDF
       │
       ▼
FastAPI POST /upload
       │
       ▼
PDF Text Extraction (PyPDFLoader)
       │
       ▼
Chunking (RecursiveCharacterTextSplitter: chunk_size=1000, chunk_overlap=200)
       │
       ▼
Dense Embeddings (BAAI/bge-small-en-v1.5 via HuggingFaceEmbeddings)
       │
       ▼
Chroma Vector DB (with user_id, document_id, filename, page metadata)
```

---

## 2. Project Structure

```
DocMentor/
├── app/
│   ├── __init__.py
│   ├── main.py                     # FastAPI application & /upload endpoint
│   ├── config.py                   # App configuration & environment loader
│   ├── ingestion/
│   │   ├── __init__.py
│   │   ├── pdf_loader.py           # PyPDF text extraction
│   │   ├── chunker.py              # Recursive text splitting
│   │   └── embeddings.py           # HuggingFace BAAI/bge-small-en-v1.5 embeddings
│   └── vectorstore/
│       ├── __init__.py
│       └── chroma_db.py            # Chroma vector database initialization
├── data/
│   └── uploads/                    # Stored user-uploaded PDF files
├── chroma_db/                      # Persistent Chroma vector store files
├── test_db.py                      # Vectorstore similarity search test script
├── .env                            # Local environment variables & API keys
├── .env.example                    # Template for environment variables
├── .gitignore                      # Git ignore file
├── requirements.txt                # Python dependencies
└── README.md                       # Documentation
```

---

## 3. Installation & Setup

### Prerequisites
- Python 3.10+ (Tested on Python 3.13)
- pip

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

Or install individual packages:
```bash
pip install fastapi uvicorn python-multipart
pip install langchain langchain-community langchain-text-splitters
pip install langchain-huggingface
pip install langchain-chroma chromadb
pip install sentence-transformers
pip install pypdf
```

---

## 4. Configuration (`.env`)

A `.env` file is located at the root of the project:

```env
# DocMentor AI Configuration

# Groq API Key (Used in subsequent milestones for grounded RAG and agents)
GROQ_API_KEY=your_groq_api_key_here

# Embedding & Vector Database Settings
EMBEDDING_MODEL_NAME=BAAI/bge-small-en-v1.5
CHROMA_PERSIST_DIRECTORY=./chroma_db
COLLECTION_NAME=docmentor
```

### What to Replace:
- **`GROQ_API_KEY`**: When moving to the next milestone (LLM answer generation & LangGraph agents), replace `your_groq_api_key_here` with your actual Groq API key obtained from [Groq Console](https://console.groq.com/keys).
- For Milestone 1 (Document Upload, Chunking, Embedding, and Chroma Storage), no paid API key is needed because embeddings run locally with `BAAI/bge-small-en-v1.5`.

---

## 5. Running the Application

### Start the FastAPI Server:
```bash
uvicorn app.main:app --reload
```

The server will be available at:
- **API Base**: `http://127.0.0.1:8000`
- **Interactive Swagger Docs**: `http://127.0.0.1:8000/docs`

---

## 6. How to Use & Test

### Step 1: Upload a PDF via Swagger UI
1. Navigate to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).
2. Expand the `POST /upload` endpoint.
3. Click **Try it out**.
4. In the `file` field, choose any `.pdf` document.
5. In the `user_id` field, enter a string identifier (e.g. `user123`).
6. Click **Execute**.

**Response:**
```json
{
  "message": "PDF uploaded successfully",
  "user_id": "user123",
  "document_id": "8b51d8b2-5f60-449e-862d-959c991f86b4",
  "filename": "physics.pdf",
  "pages": 1,
  "chunks": 2
}
```

### Step 2: Query the Vector Store
Run the standalone test script to verify similarity search:
```bash
python test_db.py
```
This queries Chroma with `"What is Newton's first law?"` and prints the top 3 matching chunks with full metadata (`user_id`, `document_id`, `filename`, `page`).

---

## 7. Upcoming Milestones
1. **User-filtered retrieval**: Restricting semantic searches by `user_id` and `document_id`.
2. **Groq API LLM integration**: Grounded RAG answering with citations.
3. **LangGraph Multi-Agent Workflows**: QA, Summary, Quiz, and Flashcard study agents.
