import asyncio
import subprocess
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import shutil
import os
import zipfile
import json
import matplotlib.pyplot as plt
import networkx as nx

app = FastAPI()

# Configuration CORS
origins = ["http://localhost:3000", "http://127.0.0.1:3000"]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])



# Dossiers pour stockage des fichiers et des images générées
UPLOAD_DIRECTORY = "./uploaded_files"
IMAGE_DIRECTORY = "./generated_images"
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)
if not os.path.exists(IMAGE_DIRECTORY):
    os.makedirs(IMAGE_DIRECTORY)

app.mount("/static", StaticFiles(directory=IMAGE_DIRECTORY), name="static")
app.mount("/result", StaticFiles(directory="./cogcn/cogcn/imgs/"), name="result")

def unzip_file(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
        print(f"Contents extracted to {extract_to}")

def generate_graph(json_path):
    try:
        with open(json_path, 'r') as file:
            data = json.load(file)

        G = nx.DiGraph()

        for node in data["nodes"]:
            G.add_node(node["id"], label=node["label"])

        # Navigate the nested structure of relationships
        for edge_type in data["edges"]:
            for relationship in edge_type["relationship"]:
                start = relationship["properties"]["start"]
                end = relationship["properties"]["end"]
                G.add_edge(start, end, frequency=relationship["frequency"])

        return G
    except FileNotFoundError:
        print(f"File not found: {json_path}")
        raise HTTPException(status_code=404, detail=f"Dependency graph JSON file not found at {json_path}")
    except KeyError as e:
        print(f"Missing key in JSON data: {e}")
        raise HTTPException(status_code=500, detail=f"Missing key {e} in JSON data")
    except json.JSONDecodeError as err:
        print(f"Error parsing JSON: {err}")
        raise HTTPException(status_code=500, detail="Error parsing JSON")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


def save_graph_image(G, output_path):
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=700, node_color="skyblue")
    plt.savefig(output_path)
    plt.close()

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith('.zip'):
        raise HTTPException(status_code=400, detail="Only ZIP files are accepted.")
    
    zip_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
    extract_to = os.path.join(UPLOAD_DIRECTORY, file.filename.replace('.zip', ''))
    image_path = os.path.join(IMAGE_DIRECTORY, file.filename.replace('.zip', '.png'))

    
    with open(zip_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    unzip_file(zip_path, extract_to)

    json_path = os.path.join(extract_to, "dependency_graph.json")
    if not os.path.exists(json_path):
        raise HTTPException(status_code=404, detail="JSON file not found after extraction.")

    G = generate_graph(json_path)
    save_graph_image(G, image_path)

    return {"message": "File processed and graph generated.", "image_url": f"/static/{os.path.basename(image_path)}", "zip_path": zip_path}




@app.post("/set_microservices/")
async def set_microservices(config: dict):
    zip_file = config.get('zip_file', '')
    num_microservices = str(config.get('number_of_microservices', 0))

    if not zip_file:
        raise HTTPException(status_code=400, detail="Le nom du fichier ZIP est requis.")
    if not num_microservices.isdigit() or int(num_microservices) <= 0:
        raise HTTPException(status_code=400, detail="Le nombre de microservices doit être un nombre positif.")

    # Construction de la commande
    command = [
        "python", "pipeline.py",
        zip_file,  # Assurez-vous que le chemin d'accès est correct
        "-k", num_microservices
    ]

    # Exécution de la commande
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return {
            "message": "Le script a été exécuté avec succès!",
            "stdout": result.stdout,
            "stderr": result.stderr,
            "num_microservices": num_microservices
        }
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Erreur d'exécution du script: {e.stderr}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
