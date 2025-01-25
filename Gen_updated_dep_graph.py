# import os
# import json
# from pathlib import Path

# # Chemin vers ton projet
# PROJECT_PATH = "projet_SI_gestion_ECM/src/main/java"

# # Charger le fichier dependency_graph.json
# with open("dependency_graph.json", "r", encoding="utf-8") as f:
#     dependency_graph = json.load(f)

# # Créer un dictionnaire pour les nœuds
# nodes = {node["label"]: node for node in dependency_graph["nodes"]}

# # Parcourir tous les fichiers .java dans le dossier projet
# for root, _, files in os.walk(PROJECT_PATH):
#     for file in files:
#         if file.endswith(".java"):
#             # Construire le chemin complet du fichier Java
#             file_path = Path(root, file)
#             relative_path = str(file_path).replace("\\", "/")

#             # Extraire le label attendu depuis le chemin relatif
#             package_path = relative_path.replace(f"{PROJECT_PATH}/", "").replace("/", ".").replace(".java", "")

#             # Vérifier si le label existe dans le dependency_graph.json
#             if package_path in nodes:
#                 # Mettre à jour le label avec le chemin relatif complet
#                 nodes[package_path]["label"] = relative_path

# # Mettre à jour le dependency_graph.json
# dependency_graph["nodes"] = list(nodes.values())

# # Sauvegarder le fichier modifié
# with open("dependency_graph.json", "w", encoding="utf-8") as f:
#     json.dump(dependency_graph, f, indent=2, ensure_ascii=False)

# print("Mise à jour du fichier dependency_graph.json terminée !")

import os
import json
from pathlib import Path

def update_dependency_graph(project_path):
    """
    Met à jour le dependency_graph.json avec les chemins relatifs corrects.
    
    Args:
        project_path (str): Chemin racine du projet Java
    """
    # Chemins standards des sources Java
    java_source_paths = [
        os.path.join(project_path, 'src', 'main', 'java'),
        os.path.join(project_path, 'src', 'java')
    ]
    
    # Trouver le chemin source Java correct
    PROJECT_PATH = None
    for path in java_source_paths:
        if os.path.exists(path):
            PROJECT_PATH = path
            break
    
    if not PROJECT_PATH:
        raise ValueError("Chemin source Java non trouvé")

    # Charger le fichier dependency_graph.json
    with open("dependency_graph.json", "r", encoding="utf-8") as f:
        dependency_graph = json.load(f)

    # Créer un dictionnaire pour les nœuds
    nodes = {node["label"]: node for node in dependency_graph["nodes"]}

    # Parcourir tous les fichiers .java dans le dossier projet
    for root, _, files in os.walk(PROJECT_PATH):
        for file in files:
            if file.endswith(".java"):
                # Construire le chemin complet du fichier Java
                file_path = Path(root, file)
                relative_path = str(file_path).replace("\\", "/")

                # Extraire le label attendu depuis le chemin relatif
                package_path = relative_path.replace(f"{PROJECT_PATH}/", "").replace("/", ".").replace(".java", "")

                # Vérifier si le label existe dans le dependency_graph.json
                if package_path in nodes:
                    # Mettre à jour le label avec le chemin relatif complet
                    nodes[package_path]["label"] = relative_path

    # Mettre à jour le dependency_graph.json
    dependency_graph["nodes"] = list(nodes.values())

    # Sauvegarder le fichier modifié
    with open("dependency_graph.json", "w", encoding="utf-8") as f:
        json.dump(dependency_graph, f, indent=2, ensure_ascii=False)

    print("Mise à jour du fichier dependency_graph.json terminée !")

# Exemple d'utilisation
if __name__ == "__main__":
    # Chemin vers le projet dézippé (à ajuster)
    project_base_path = os.path.join(os.getcwd(), 'springboot-projects', 'nom_projet')
    update_dependency_graph(project_base_path)