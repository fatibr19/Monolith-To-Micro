# main.py - Votre fichier FastAPI
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

UPLOAD_DIRECTORY = "./uploaded_files"
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

origins = [
    "http://localhost:3000",  # L'URL de votre front-end
    "http://127.0.0.1:3000"
]

# Configuration de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Les origines qui peuvent faire des requêtes
    allow_credentials=True,
    allow_methods=["*"],  # Autorise toutes les méthodes
    allow_headers=["*"],  # Autorise tous les headers
)


@app.post("/upload/")
async def create_upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith('.zip'):
        raise HTTPException(status_code=400, detail="Invalid file type, only ZIP files are allowed.")

    try:
        file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
        with open(file_location, "wb") as buffer:
            buffer.write(await file.read())

        return {"filename": file.filename, "filetype": file.content_type, "filesize": os.path.getsize(file_location)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
