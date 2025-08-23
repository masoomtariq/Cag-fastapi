from fastapi import FastAPI, HTTPException, File, UploadFile



app = FastAPI(title="THis is the cag project")

@app.get('/')
def home():
    return "Hellow"


# Run the app using Uvicorn (used for local development)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)