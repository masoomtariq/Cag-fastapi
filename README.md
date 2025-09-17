**📘 CAG-FastAPI

A FastAPI-based application for file upload, text extraction, and conversational AI integration.
It supports multiple file types, extracts their textual content, stores structured data in MongoDB, and allows querying via LLMs (Google GenAI).

🚀 Features

📂 Multi-format file upload
Supports: TXT, PDF (with OCR fallback), DOCX, XLS/XLSX/CSV, PPTX, EPUB, and Images.

🔎 Content Extraction
Uses specialized parsers (PyPDF, python-docx, pandas, python-pptx, ebooklib, BeautifulSoup, pytesseract).

🗄 MongoDB Integration
Stores extracted content and metadata using Pydantic schemas (FILES, FILE_INFO).

🤖 LLM Response Generation
Passes document content into Google GenAI for contextual query answering.

⏰ Timezone-aware timestamps
Upload date/time saved in ISO 8601 format with Pakistan Standard Time (PKT).

🌐 REST API + Web Template
Clean FastAPI endpoints and optional Jinja2 template (home.html).

📂 Project Structure
Cag-fastapi-main/
    .gitignore
    README.md
    req.txt
    src/
        db.py               # MongoDB connection + helpers
        file_handler.py     # Handles file uploads
        file_models.py      # Pydantic models for validation
        file_router.py      # API routes
        main.py             # FastAPI entry point
        templates/
            home.html       # Sample Jinja2 template
        utils/
            file_processing.py  # Extractors for different file formats
            helpers.py          # Utility functions (datetime, etc.)
            llm_response.py     # Google GenAI integration