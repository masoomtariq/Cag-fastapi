from fastapi import FastAPI, Request, Path, Query
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from file_router import router, counter
from utils.llm_response import get_llm_response
from helpers import verify_id
from pathlib import Path as path
from dotenv import load_dotenv
import os

load_dotenv()
connection_url = os.getenv('MONGO_URL')
db_name = os.getenv('DB_name')
collection_name = os.getenv('collection_name')

# Initialize FastAPI app
app = FastAPI(title="CAG Project - File Upload & Query System")

@app.on_event("startup")
async def startup():
    app.state.mongo_client = AsyncIOMotorClient(connection_url)
    app.state.db = app.state.mongo_client[db_name]
    app.state.collection = app.state.db[collection_name]

# Get the current directory of this file
BASE_DIR = path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"

# Jinja2 template directory (⚠️ Update path if running outside /workspaces)
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


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
    files = await app.state.collection.distinct("files.file_name")

    return {"message": f"There are {len(files)} files stored.", "Files in directory": files}


@app.delete("/reset_files", tags=["Admin"])
async def reset_datastore():
    global counter
    counter = 0
    await app.state.db.drop_collection(collection_name)
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
    verify_id(id=id, collection=app.state.collection)

    # Fetch combined content for this ID
    docs_data = await app.state.collection.find_one({"id": id})
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
    await app.state.db.drop_collection(collection_name)
    app.state.mongo_client.close()


# Run app with Uvicorn (for local development)
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)