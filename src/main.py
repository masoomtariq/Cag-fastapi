from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse 
from router import the_router, counter, data_store, data_path
import os, shutil


app = FastAPI(title="This is the cag project")

@app.get('/', response_class=HTMLResponse, tags=['Root'])
def home():
    return HTMLResponse(content=html_content, status_code=200)
@app.get('/my')
def tryapi(request: Request):
    return {'method': request.method, 'url': request.url, 'body': request.headers}

app.include_router(router= the_router, prefix='/file', tags=["Data handling: uploading to deleting the files"])

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

# Run the app using Uvicorn (used for local development)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)