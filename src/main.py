from fastapi import FastAPI, HTTPException, File, UploadFile
from router import file_router


app = FastAPI(title="THis is the cag project")

@app.get('/')
def home():
    return "Hellow"

app.include_router(file_router)

# Run the app using Uvicorn (used for local development)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)