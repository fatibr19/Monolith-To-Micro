import os
import json
from pathlib import Path

def update_dependency_graph(project_path, json_filepath):
    """
    Met à jour les chemins relatifs des fichiers .java dans le fichier dependency_graph.json.
    
    Args:
        project_path (str): Le chemin vers le dossier contenant les fichiers Java du projet.
        json_filepath (str): Le chemin du fichier JSON à mettre à jour.
    """
    # Charger le fichier dependency_graph.json
    with open(json_filepath, "r", encoding="utf-8") as f:
        dependency_graph = json.load(f)

    # Créer un dictionnaire pour les nœuds
    nodes = {node["label"]: node for node in dependency_graph["nodes"]}

    # Parcourir tous les fichiers .java dans le dossier projet
    for root, _, files in os.walk(project_path):
        for file in files:
            if file.endswith(".java"):
                # Construire le chemin complet du fichier Java
                file_path = Path(root, file)
                relative_path = str(file_path).replace("\\", "/")

                # Extraire le label attendu depuis le chemin relatif
                package_path = relative_path.replace(f"{project_path}/", "").replace("/", ".").replace(".java", "")

                # Vérifier si le label existe dans le dependency_graph.json
                if package_path in nodes:
                    # Mettre à jour le label avec le chemin relatif complet
                    nodes[package_path]["label"] = relative_path

    # Mettre à jour le dependency_graph.json
    dependency_graph["nodes"] = list(nodes.values())

    # Sauvegarder le fichier modifié
    with open(json_filepath, "w", encoding="utf-8") as f:
        json.dump(dependency_graph, f, indent=2, ensure_ascii=False)

    print("Mise à jour du fichier dependency_graph.json terminée !")

# Permet d'appeler la fonction si ce script est exécuté directement
if __name__ == "__main__":
    PROJECT_PATH = "springboot-projects/projet_SI_gestion_ECM/src/main/java"
    JSON_FILEPATH = "dependency_graph.json"
    update_dependency_graph(PROJECT_PATH, JSON_FILEPATH)
