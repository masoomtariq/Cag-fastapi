from fastapi import FastAPI, Request, Path, Query, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates 
from router import the_router, counter, data_store, data_path
from utils.llm_response import get_llm_response
import os, shutil


app = FastAPI(title="This is the cag project")

# Point to your templates directory
templates = Jinja2Templates(directory='/workspaces/Cag/src/templates')

@app.get('/', response_class=HTMLResponse, tags=['Root'])
def home(request: Request):
    return templates.TemplateResponse(request=request, name='home.html')

@app.get('/list_files')
def list_files():
    # list all files and directories
    all_items = os.listdir(data_path)

    # filter only files
    files = [f for f in all_items if os.path.isfile(os.path.join(data_path, f))]
    
    return {"message": f"There are {len(files)} files stored.", "Files in directory": files}

@app.delete('/reset_files')
def reset_datastore():

    global counter
    data_store.clear()
    counter = 0
    shutil.rmtree(data_path)

    return {"message": "All the files the and their records has been deleted successfully."}

app.include_router(router= the_router, prefix='/file', tags=["Data handling: uploading to deleting the files"])

@app.get('/query/{id}', tags=["Chat with Files"])
def query_file(id: int = Path(...), query: str = Query(default='')):
    if id not in data_store:
        raise HTTPException(status_code=401, detail=f"The given id '{id}' not exists.")
    file_content = data_store[id]

    response = get_llm_response(context=file_content, query=query)

    return {'message': response.text}

# Run the app using Uvicorn (used for local development)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)