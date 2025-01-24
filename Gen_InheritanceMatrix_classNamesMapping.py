import json
import numpy as np
from pathlib import Path

def create_symmetric_inheritance_matrix(nodes_data, inheritance_file):
    # Extraire les noms des classes à partir des chemins de fichiers
    node_names = []
    for node in nodes_data["nodes"]:
        # Extraire le nom du fichier sans extension et chemin
        file_name = node["label"].split('/')[-1].replace('.java', '')
        node_names.append(file_name)

    # Créer un dictionnaire pour mapper les indices
    name_to_index = {name: i for i, name in enumerate(node_names)}
    n = len(node_names)

    # Initialiser la matrice avec des zéros
    matrix = np.zeros((n, n), dtype=int)

    # Charger les relations d'héritage depuis le fichier
    with open(inheritance_file, 'r') as f:
        inheritance_data = json.load(f)

    # Remplir la matrice de manière symétrique
    for relation in inheritance_data["inheritance_relations"]:
        child = relation["child"]
        parent = relation["parent"]
        print(f"Parent: {parent}, Child: {child}")
        
        # Trouver les indices correspondants
        child_matches = [i for i, name in enumerate(node_names) if child == name]
        parent_matches = [i for i, name in enumerate(node_names) if parent == name]
        print(f"child_matches: {child_matches}, parent_matches: {parent_matches}")
        
        if child_matches and parent_matches:
            child_idx = child_matches[0]
            parent_idx = parent_matches[0]
            # Rendre la matrice symétrique
            matrix[child_idx][parent_idx] = 1
            matrix[parent_idx][child_idx] = 1

    return matrix, node_names

def main():
    # Charger les données des nœuds depuis votre JSON
    nodes_file = "dependency_graph.json"  # Remplacer par le chemin de votre fichier de nœuds
    with open(nodes_file, 'r') as f:
        nodes_data = json.load(f)

    # Créer la matrice symétrique
    inheritance_matrix, class_names = create_symmetric_inheritance_matrix(
        nodes_data, 
        "inheritance_relations.json"
    )

    # Sauvegarder la matrice
    np.savetxt('inheritance_matrix.csv', inheritance_matrix, delimiter=',', fmt='%d')
    
    # Afficher quelques informations
    print(f"Dimensions de la matrice: {inheritance_matrix.shape}")
    print(f"Nombre total de relations (en comptant la symétrie): {np.sum(inheritance_matrix)}")
    print(f"Nombre de classes: {len(class_names)}")
    print("\nMatrice d'héritage symétrique sauvegardée dans 'inheritance_matrix.csv'")

    # Sauvegarder la liste des noms de classes pour référence
    node_mapping = {str(i): name for i, name in enumerate(class_names)}
    with open('node_mapping.json', 'w') as f:
        json.dump(node_mapping, f, indent=4)
    print("Liste des classes sauvegardée dans 'node_mapping.json'")

if __name__ == "__main__":
    main()
