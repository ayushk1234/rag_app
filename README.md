# Document Q&A RAG App

A simple and efficient RAG application that allows users to upload multiple pdf documents and ask questions about their content.

## Features
- **PDF Processing**: Extracts pdf text and create chunks of documents. Used `pyMuPDF` for PDF processing. For Chunking Used fixed size with overlap of 100 characters.
- **Vector Store**: Uses `FastEmbed` and `ChromaDB` for easy and fast semantic search.Used `jinaai/jina-embeddings-v2-small-en` for fast and accurate embedding of text.
- **AI-Powered Answers**: Used OpenAI's `gpt-4o-mini` to provide accurate, context-aware responses using prompt engineering.
- **Streamlit UI**: UI for uploading PDFs and chat web interface.

## Project Structure
```text
rag_app/
├── app/
│   ├── pdf_parser.py    # PDF extraction and chunking
│   ├── rag.py           # RAG pipeline logic
│   ├── vector_store.py  # Embedding and database management
│   └── prompts.py       # System prompts
├── data/uploads/        # Temporary storage for uploaded PDFs
├── chroma_db/           # Persistent vector database
├── streamlit_app.py     # Main application entry point
├── .env                 # API keys (not included)
└── requirements.txt     # Project dependencies
```

## Setup and Installation

### This project was created using python 3.12

### 1. Clone or Download the Project

Ensure you have the project files in a local directory.

### 2. Create a Virtual Environment

**Windows:**
```powershell
python -m venv venv```

Activate the venv
```
.\venv\Scripts\activate
```

**Linux/macOS:**
```bash
python3 -m venv venv```
Activate the venv
```
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```


### 4. Configure Environment Variables
Create a `.env` file in the root directory using `.env.example` as a template and add your OpenAI API key:
```text
OPENAI_API_KEY=your_openai_api_key_here
```

## How to Start the Project
After activating the virtual env , i`cd into the rag_app` folder run the following command to launch the Streamlit application in terminal:
```
streamlit run streamlit_app.py
```

Now navigate to the URL provided in your terminal (default `http://localhost:8501`) to start app.

## Future Scope
- Add a feature to delete documents.
- Having conversation history with the chatbot so that user can ask follow up questions .
- Adding chat and session history for the chatbot for next chat session.
- Not saving the files after processing. Instead upload and process on the go.
- Clickable citations in the chatbot response that will take user to the exact page in the document.
- Showing progress bar for the PDF processing.
- Using Next js for building the UI and fastapi for backend.
- Dockerizing the application for easy deployment.
- Modification in the metadata , chunking strategy, prompt engineering, top k values and embedding model for better RAG performance.
- Implementing vector db weaviate for better retrieval.
- Adding  hybrid search for better retrieval.
- For embeddings and pdf processing can be done using batch processing and multiprocessing.
