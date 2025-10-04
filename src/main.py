from fastapi import FastAPI, Request, Path, Query
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from file_router import router, counter
from utils.llm_response import get_llm_response
from db import verify_id, get_collection, delete_collection
from pathlib import Path as path
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
connection_url = os.getenv('MONGO_URL')
db_name = os.getenv('DB_name')
collection_name = os.getenv('collection_name')

# Initialize FastAPI app
app = FastAPI(title="CAG Project - File Upload & Query System")

# Get the current directory of this file
BASE_DIR = path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"

# Jinja2 template directory (⚠️ Update path if running outside /workspaces)
templates = Jinja2Templates(TEMPLATES_DIR)


@app.get("/", response_class=HTMLResponse, tags=["Root"])
async def home(request: Request):
    """
    Render home page (static template).
    """
    return templates.TemplateResponse(request=request, name="home.html")


@app.get("/list_files", tags=["Data Overview"])
async def list_files():
    """
    List all unique filenames stored in MongoDB.

    Returns:
        dict: Number of files + list of stored filenames.
    """
    collection = get_collection()
    files = await collection.distinct("files.file_name")

    return {"message": f"There are {len(files)} files stored.", "Files in directory": files}


@app.delete("/reset_files", tags=["Admin"])
def reset_datastore():
    """
    Reset datastore by deleting all documents and resetting the counter.
    """
    global counter
    counter = 0  # ⚠️ Resets only runtime counter, not DB IDs
    delete_collection()
    return {"message": "All the files and their records have been deleted successfully."}


# Attach router for file upload/update/delete APIs
app.include_router(router=router, prefix="/file", tags=["File Management"])


@app.get("/query/{id}", tags=["Chat with Files"])
async def query_file(id: int = Path(...), query: str = Query(default="")):
    """
    Query uploaded files via Google Gemini.

    Args:
        id (int): ID of the stored file group.
        query (str): User query text.

    Returns:
        dict: LLM response text.
    """
    verify_id(id=id)

    # Fetch combined content for this ID
    collection = get_collection()
    docs_data = await collection.find_one({"id": id})
    file_text = docs_data["combined_content"]

    # Get Gemini response
    response = await get_llm_response(context=file_text, query=query)
    return {"message": response.text}


@app.on_event("shutdown")
async def shutdown_session():
    """
    Cleanup task - drop collection on shutdown.
    ⚠️ This deletes all data permanently.
    """
    await delete_collection()


# Run app with Uvicorn (for local development)
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)