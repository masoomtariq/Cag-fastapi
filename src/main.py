from fastapi import FastAPI
from router import the_router, counter, data_store, data_path
import os, shutil


app = FastAPI(title="THis is the cag project")

@app.get('/')
def home():
    return {"content": "Hellow"}

app.include_router(router= the_router, prefix='/api/file')

@app.get('/list_files')
def list_files():
    # list all files and directories
    all_items = os.listdir(data_path)

    # filter only files
    files = [f for f in all_items if os.path.isfile(os.path.join(data_path, f))]
    '/n'.join(files)

    return {"message": f"There are {counter} files stored.", "Files in directory": files}

@app.delete('/reset_files')
def reset_datastore():

    global counter
    global data_store
    data_store.clear()
    counter = 0
    shutil.rmtree(data_path)

    return {"message": "All the files the and their records has been deleted successfully."}

# Run the app using Uvicorn (used for local development)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)