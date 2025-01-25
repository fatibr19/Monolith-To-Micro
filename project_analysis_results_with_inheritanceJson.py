# import json

# def load_json(file_path: str) -> dict:
#     """Load and parse a JSON file."""
#     with open(file_path, 'r') as file:
#         return json.load(file)

# # Charger les données JSON à partir des fichiers
# data_classes = load_json('project_analysis_results_with_inheritance.json')
# data_structure = load_json('dependency_graph.json')
# entrypoints = load_json('entrypoints.json')

# # Créer un dictionnaire pour mapper les chemins complets aux IDs de nœud
# path_to_id = {node['label'].replace("/", "\\"): node['id'] for node in data_structure['nodes']}

# # Création des dictionnaires pour le mappage des noms de classe et des méthodes à leur class_id et indices de méthode
# class_to_details = {}

# global_method_index = 1  # Initialiser l'indice global des méthodes

# for path, details in data_classes.items():
#     class_id = path_to_id.get(path, "unknown")
#     class_name = path.split('\\')[-1].split('.')[0]  # Extraire le nom de classe sans extension
#     class_to_details[class_name] = {
#         "class_id": class_id,
#         "methods": {}
#     }
#     # Parcourir chaque méthode et les indexer par classe
#     for method in details:
#         if method not in ["class_id", "class_name"]:  # Ignorer les clés non-méthodes
#             class_to_details[class_name]["methods"][method] = global_method_index
#             global_method_index += 1

# print("class_to_details: ", class_to_details)
# # Mise à jour des classes et méthodes dans data_classes
# for path, details in data_classes.items():
#     class_name = path.split('\\')[-1].split('.')[0]
#     details['class_id'] = class_to_details[class_name]["class_id"]
#     details['class_name'] = class_name
#     for method, actions in list(details.items()):
#         if method not in ["class_id", "class_name"]:
#             updated_actions = []
#             for action in actions:
#                 parts = action.split('.')
#                 if len(parts) > 1:
#                     action_class, action_method = parts[0], parts[1]
#                     if action_class in class_to_details and action_method in class_to_details[action_class]["methods"]:
#                         print("class_to_details: ", class_to_details)
#                         print(f"class_to_details[action_class]: {class_to_details[action_class]['methods']}")
#                         action_class_id = class_to_details[action_class]["class_id"]
#                         action_method_index = class_to_details[action_class]["methods"][action_method]
#                         updated_actions.append(f"{action_class_id}.{action_method_index}")
#                     else:
#                         print("action_class: ", action_class)
#                         print("action_method: ", action_method)
#                         updated_actions.append("unknown.unknown")
#                 else:
#                     print("action_class: ", action_class)
#                     print("action_method: ", action_method)
#                     updated_actions.append("unknown.unknown")
#             details[method] = {"method_index": class_to_details[class_name]["methods"].get(method, "unknown"), "actions": updated_actions}

# for entry in entrypoints:
#     controller_path = entry["controllerFilePath"].replace("/", "\\")  # Uniformiser le chemin d'accès
#     method_name = entry["methodName"]
#     entrypoint_id = entry["id"]

#     if controller_path in data_classes:
#         # Vérifier si la méthode existe dans les données de classe
#         if method_name in data_classes[controller_path]:
#             # Associer l'entrypoint_id à la méthode correspondante
#             if 'entrypoint_ids' in data_classes[controller_path][method_name]:
#                 data_classes[controller_path][method_name]['entrypoint_ids'].append(entrypoint_id)
#             else:
#                 data_classes[controller_path][method_name]['entrypoint_ids'] = [entrypoint_id]

# def save_results_to_json(results, filename):
#     """Save the modified results with class IDs and method indices to a JSON file."""
#     with open(filename, 'w', encoding='utf-8') as f:
#         json.dump(results, f, indent=4)
#         print(f"Results saved to {filename}")

# # Sauvegarder les données mises à jour dans un nouveau fichier JSON
# save_results_to_json(data_classes, "updated_project_analysis_results.json")

import json
import os

def load_json(file_path: str) -> dict:
    """Load and parse a JSON file."""
    with open(file_path, 'r') as file:
        return json.load(file)

def process_project_analysis(
    project_analysis_path='project_analysis_results_with_inheritance.json',
    dependency_graph_path='dependency_graph.json', 
    entrypoints_path='entrypoints.json',
    output_path='updated_project_analysis_results.json'
):
    """
    Traite l'analyse de projet et génère un fichier de résultats mis à jour.
    
    Args:
        project_analysis_path (str): Chemin du fichier d'analyse de projet
        dependency_graph_path (str): Chemin du fichier de graphe de dépendances
        entrypoints_path (str): Chemin du fichier des points d'entrée
        output_path (str): Chemin de sortie pour les résultats
    
    Returns:
        dict: Résultats mis à jour de l'analyse de projet
    """
    # Charger les données JSON
    data_classes = load_json(project_analysis_path)
    data_structure = load_json(dependency_graph_path)
    entrypoints = load_json(entrypoints_path)

    # Créer un dictionnaire pour mapper les chemins complets aux IDs de nœud
    path_to_id = {node['label'].replace("/", "\\"): node['id'] for node in data_structure['nodes']}

    # Création des dictionnaires pour le mappage des noms de classe et des méthodes
    class_to_details = {}
    global_method_index = 1

    # Logique de traitement similaire à votre script original
    for path, details in data_classes.items():
        class_id = path_to_id.get(path, "unknown")
        class_name = path.split('\\')[-1].split('.')[0]
        class_to_details[class_name] = {
            "class_id": class_id,
            "methods": {}
        }
        
        for method in details:
            if method not in ["class_id", "class_name"]:
                class_to_details[class_name]["methods"][method] = global_method_index
                global_method_index += 1

    # Mise à jour des classes et méthodes
    for path, details in data_classes.items():
        class_name = path.split('\\')[-1].split('.')[0]
        details['class_id'] = class_to_details[class_name]["class_id"]
        details['class_name'] = class_name
        
        for method, actions in list(details.items()):
            if method not in ["class_id", "class_name"]:
                updated_actions = []
                for action in actions:
                    parts = action.split('.')
                    if len(parts) > 1:
                        action_class, action_method = parts[0], parts[1]
                        if (action_class in class_to_details and 
                            action_method in class_to_details[action_class]["methods"]):
                            action_class_id = class_to_details[action_class]["class_id"]
                            action_method_index = class_to_details[action_class]["methods"][action_method]
                            updated_actions.append(f"{action_class_id}.{action_method_index}")
                        else:
                            updated_actions.append("unknown.unknown")
                    else:
                        updated_actions.append("unknown.unknown")
                
                details[method] = {
                    "method_index": class_to_details[class_name]["methods"].get(method, "unknown"), 
                    "actions": updated_actions
                }

    # Traitement des points d'entrée
    for entry in entrypoints:
        controller_path = entry["controllerFilePath"].replace("/", "\\")
        method_name = entry["methodName"]
        entrypoint_id = entry["id"]

        if controller_path in data_classes:
            if method_name in data_classes[controller_path]:
                if 'entrypoint_ids' in data_classes[controller_path][method_name]:
                    data_classes[controller_path][method_name]['entrypoint_ids'].append(entrypoint_id)
                else:
                    data_classes[controller_path][method_name]['entrypoint_ids'] = [entrypoint_id]

    # Sauvegarder les résultats
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data_classes, f, indent=4)
    
    print(f"Results saved to {output_path}")
    return data_classes

def main():
    process_project_analysis()

if __name__ == "__main__":
    main()