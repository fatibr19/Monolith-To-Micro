import json


def load_data(file_path):
    """Charge les données JSON à partir d'un fichier spécifié."""
    with open(file_path, 'r') as file:
        return json.load(file)

def display_entrypoints_and_actions(data):
    """Affiche les identifiants d'entrée et lance un parcours des actions associées pour chaque méthode."""
    for class_path, class_details in data.items():
        for method_name, method_info in class_details.items():
            if isinstance(method_info, dict) and 'entrypoint_ids' in method_info:
                entrypoint_ids = method_info['entrypoint_ids']
                for entrypoint_id in entrypoint_ids:
                    print(f"Entrypoint {entrypoint_id} ->")
                    method_index = method_info.get('method_index')
                    if method_index:
                        display_actions_recursively(data, class_details.get("class_id", "unknown"), method_index)

def get_actions_for_method(data, class_id, method_id):
    """Retourne les actions associées à une méthode spécifique par son index dans une classe donnée."""
    for class_path, class_details in data.items():
        if class_details.get("class_id", "unknown") == class_id:
            for method_name, method_details in class_details.items():
                if method_details.get('method_index') == method_id:
                    actions = method_details.get('actions', [])
                    filtered_actions = [action for action in actions if 'unknown' not in action]
                    return [(action.split('.')[0], action.split('.')[1]) for action in filtered_actions if '.' in action]
    return []

def display_actions_recursively(data, class_id, method_id, depth=0):
    """Affiche récursivement toutes les actions et les sous-actions pour une méthode donnée."""
    actions = get_actions_for_method(data, class_id, method_id)
    indent = "  " * depth  # Indentation pour mieux visualiser la récursion
    for action_class_id, action_method_id in actions:
        print(f"{indent}Class {class_id}, Method {method_id} -> Action: ({action_class_id}, {action_method_id})")
        # Récursion pour suivre les actions de la méthode appelée
        display_actions_recursively(data, action_class_id, int(action_method_id), depth + 1)

# Utilisation des fonctions
data = load_data('updated_project_analysis_results.json')
display_entrypoints_and_actions(data)
 # type: ignore