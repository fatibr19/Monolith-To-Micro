import javalang
from pathlib import Path
import json

# Initialiser endpoint_id à l'extérieur pour assurer un comptage global
endpoint_id = 1

def parse_java_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return javalang.parse.parse(file.read())

def extract_endpoints(tree, file_path, endpoint_counter):
    entrypoints = []
    global endpoint_id  # Utiliser le compteur global
    
    for _, class_decl in tree.filter(javalang.tree.ClassDeclaration):
        controller_path = extract_annotation_value(class_decl.annotations, "RequestMapping")
        for method in class_decl.methods:
            for annotation in method.annotations:
                if annotation.name in ["GetMapping", "PostMapping", "PutMapping", "DeleteMapping"]:
                    endpoint_path = extract_annotation_value(method.annotations, annotation.name)
                    
                    endpoint = {
                        "id": endpoint_id,
                        "controllerFilePath": str(file_path),  # Ajout du chemin du fichier du contrôleur
                        "classControllerPath": controller_path.strip('"'),  # Remove extra quotes
                        "endpointType": annotation.name.replace("Mapping", "").lower(),
                        "endpointPath": endpoint_path.strip('"'),  # Remove extra quotes
                        "methodName": method.name  # Ajout du nom de la méthode
                    }
                    entrypoints.append(endpoint)
                    endpoint_id += 1  # Incrémente l'ID globalement

    return entrypoints

def extract_annotation_value(annotations, annotation_name):
    for annotation in annotations:
        if annotation.name == annotation_name:
            if annotation.element:
                if isinstance(annotation.element, list):
                    return str(annotation.element[0].value)
                else:
                    return str(annotation.element.value)
            break
    return "/"

def save_to_json(entrypoints, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(entrypoints, f, indent=4)

def analyze_files(root_path):
    all_entrypoints = []
    global endpoint_id  # Déclare l'utilisation de la variable globale
    
    for java_file in Path(root_path).rglob('*.java'):
        tree = parse_java_file(java_file)
        entrypoints = extract_endpoints(tree, java_file, endpoint_id)
        all_entrypoints.extend(entrypoints)

    return all_entrypoints

if __name__ == "__main__":
    root_path = "projet_SI_gestion_ECM"
    output_file = "entrypoints.json"
    entrypoints = analyze_files(root_path)
    save_to_json(entrypoints, output_file)
    print(f"Saved entrypoints to {output_file}")
