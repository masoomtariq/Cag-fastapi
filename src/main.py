from fastapi import FastAPI, Request, Path, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from router import the_router, counter
from utils.llm_response import get_llm_response
from utils.db import verify_id, list_files, delete_collection, get_text

app = FastAPI(title="This is the cag project")

# Point to your templates directory
templates = Jinja2Templates(directory='/workspaces/Cag/src/templates')

@app.get('/', response_class=HTMLResponse, tags=['Root'])
def home(request: Request):
    return templates.TemplateResponse(request=request, name='home.html')

@app.get('/list_files')
def list_files():
    # list all files and directories
    files = list_files
    
    return {"message": f"There are {len(files)} files stored.", "Files in directory": files}

@app.delete('/reset_files')
def reset_datastore():

    global counter
    delete_collection()
    counter = 0

    return {"message": "All the files the and their records has been deleted successfully."}

app.include_router(router= the_router, prefix='/file', tags=["Data handling: uploading to deleting the files"])

@app.get('/query/{id}', tags=["Chat with Files"])
def query_file(id: int = Path(...), query: str = Query(default='')):
    verify_id(id= id)
    
    file_content = get_text(id= id)

    response = get_llm_response(context=file_content, query=query)

    return {'message': response.text}


# Run the app using Uvicorn (used for local development)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)