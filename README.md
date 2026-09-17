📘 CAG-FastAPI

A FastAPI-based application for file upload, text extraction, and conversational AI integration.
It supports multiple file types, extracts their textual content, stores structured data in MongoDB, and allows querying via LLMs (Google GenAI).

🚀 Features

📂 Multi-format file upload
Supports: TXT, PDF (with OCR fallback), DOCX, XLS/XLSX/CSV, PPTX, EPUB, and Images (JPG, JPEG, PNG, BMP).

🔎 Content Extraction
Uses specialized parsers:
- PDF: PyPDF with OCR.space API fallback for scanned documents
- DOCX: python-docx
- Excel/CSV: pandas with openpyxl/xlrd
- PPTX: python-pptx
- EPUB: ebooklib with BeautifulSoup
- Images: OCR.space API for text extraction
- TXT: Direct text reading

🗄 MongoDB Integration
Stores extracted content and metadata using Pydantic schemas (FILES, FILE_INFO) with async Motor driver.

🤖 LLM Response Generation
Integrates with Google GenAI (Gemini 2.5 Flash Lite) for contextual query answering based on uploaded document content.

⏰ Timezone-aware timestamps
Upload date/time saved in ISO 8601 format with Pakistan Standard Time (PKT/Asia/Karachi).

🌐 REST API + Web Template
Clean FastAPI endpoints with automatic OpenAPI documentation and optional Jinja2 template (home.html).

🔒 File Management
Duplicate file prevention, ID-based file grouping, update and delete operations.

📂 Project Structure

Cag-fastapi/
    .gitignore
    .python-version
    pyproject.toml
    requirements.txt
    README.md
    uv.lock
    src/
        main.py                 # FastAPI entry point with MongoDB connection
        file_router.py          # API routes for file operations
        file_handler.py         # File upload and processing logic
        file_models.py          # Pydantic models for validation
        helpers.py              # Utility functions (ID verification, datetime)
        cag_fastapi/
            __init__.py        # Package initialization
        templates/
            home.html           # Landing page with API docs link
        utils/
            file_processing.py  # File format extractors
            llm_response.py     # Google GenAI integration
            __init__.py

📌 How It Works

1. **File Upload Process**
   - User uploads file via `/file/upload` endpoint
   - File_Handler validates file type and extracts metadata
   - Appropriate extractor processes the file based on extension
   - Extracted content and metadata structured via Pydantic models
   - Data stored in MongoDB with unique ID assignment

2. **Content Extraction**
   - Each file type has dedicated extractor function
   - PDFs attempt text extraction first, fallback to OCR for scanned pages
   - Images processed via OCR.space API for text extraction
   - Extracted text combined and stored with metadata

3. **Query Process**
   - User queries stored content via `/query/{id}` endpoint
   - System retrieves combined content from MongoDB using ID
   - Context and query sent to Google Gemini LLM
   - LLM generates response based on document context
   - Response returned as structured JSON

4. **File Management**
   - Files grouped by user/document ID
   - Additional files can be appended to existing IDs via `/file/update/{id}`
   - Entire file groups can be deleted via `/file/delete/{id}`
   - List all stored files via `/list_files` endpoint
   - Admin can reset database via `/reset_files` endpoint

🛠 Tech Stack

**Backend Framework**: FastAPI with Uvicorn/Gunicorn

**Database**: MongoDB with Motor (async driver)

**File Processing**:
- PyPDF for PDF text extraction
- python-docx for Word documents
- pandas for Excel/CSV files
- python-pptx for PowerPoint
- ebooklib for EPUB files
- BeautifulSoup for HTML parsing
- OCR.space API for OCR functionality
- pdf2image for PDF to image conversion

**AI/ML**: Google GenAI (Gemini 2.5 Flash Lite)

**Utilities**: python-dotenv, pathlib, asyncio

**Templating**: Jinja2

⚙️ Setup & Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Cag-fastapi
   ```

2. **Install dependencies**
   ```bash
   # Using uv (recommended)
   uv sync
   
   # Or using pip
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   Create a `.env` file in the project root:
   ```
   MONGO_URL=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/<database>
   DB_name=<database_name>
   collection_name=<collection_name>
   GOOGLE_API_KEY=<your_google_gemini_api_key>
   OCR_SPACE_API=<your_ocr_space_api_key>
   ```

4. **Run the application**
   ```bash
   # Development mode
   python src/main.py
   
   # Or using uvicorn directly
   uvicorn src.main:app --reload
   
   # Production mode
   gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

5. **Access the application**
   - Home page: http://localhost:8000/
   - API documentation: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc

📡 API Endpoints

**Root & Documentation**
- `GET /` - Landing page with API docs link
- `GET /docs` - Interactive Swagger UI documentation
- `GET /redoc` - ReDoc documentation

**File Management**
- `POST /file/upload` - Upload a new file (returns assigned ID)
- `PUT /file/update/{id}` - Add file to existing ID
- `DELETE /file/delete/{id}` - Delete all files for given ID
- `GET /list_files` - List all stored filenames

**Query & Admin**
- `GET /query/{id}?query=<text>` - Query uploaded files via LLM
- `DELETE /reset_files` - Admin endpoint to clear all data

🔐 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `MONGO_URL` | MongoDB connection string | Yes |
| `DB_name` | Database name | Yes |
| `collection_name` | Collection name | Yes |
| `GOOGLE_API_KEY` | Google Gemini API key | Yes |
| `OCR_SPACE_API` | OCR.space API key for PDF/image OCR | Yes |

📝 Notes

- The application uses a global counter for ID assignment (resets on server restart)
- All timestamps are in Pakistan Standard Time (Asia/Karachi)
- PDF files with no selectable text automatically fall back to OCR
- Duplicate filenames are prevented across the entire database
- The database collection is dropped on application shutdown (can be disabled in production)
- Temporary files are stored in `tmp/uploads` directory during processing