import numpy as np
import json

# Global variable
dependency_graph = None

def load_data(file_path):
   """Charge les données JSON à partir d'un fichier spécifié."""
   with open(file_path, 'r') as file:
       return json.load(file)

def get_class_index_map(dependency_graph):
   """Crée un dictionnaire pour mapper les IDs de classe à des indices de matrice."""
   return {node['id']: index for index, node in enumerate(dependency_graph['nodes'])}

def get_class_name_to_id_map(dependency_graph):
   """Crée un dictionnaire pour mapper les noms de classes à leurs IDs."""
   return {node['label'].split('/')[-1].replace('.java', ''): node['id'] 
           for node in dependency_graph['nodes']}

def get_entrypoint_index_map(entrypoints):
   """Crée un dictionnaire pour mapper les IDs d'entrée à des indices de colonnes de matrice."""
   return {str(entrypoint['id']): index for index, entrypoint in enumerate(entrypoints)}

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

def update_matrix_with_actions(data, matrix, class_index_map, entrypoint_index_map, class_name_to_id_map):
   """Mise à jour de la matrice en prenant en compte les actions des méthodes."""
   for class_details in data.values():
       class_id = class_details.get("class_id")
       if class_id in class_index_map:
           for method_details in class_details.values():
               if isinstance(method_details, dict) and 'entrypoint_ids' in method_details:
                   for entrypoint_id in method_details['entrypoint_ids']:
                       if str(entrypoint_id) in entrypoint_index_map:
                           ep_index = entrypoint_index_map[str(entrypoint_id)]
                           track_actions_recursively(data, class_id, method_details.get('method_index'), matrix, class_index_map, ep_index)

def track_actions_recursively(data, class_id, method_id, matrix, class_index_map, ep_index):
   """Suit récursivement les actions et met à jour la matrice."""
   global dependency_graph
   actions = get_actions_for_method(data, class_id, method_id)
   for action_class_id, action_method_id in actions:
       if action_class_id in class_index_map:
           matrix[class_index_map[action_class_id], ep_index] = 1
           
           # Ajouter la référence de Service interface,si ServiceImpl est référencé
           class_name_to_id = get_class_name_to_id_map(dependency_graph)
           for class_name, mapped_class_id in class_name_to_id.items():
               if action_class_id == mapped_class_id and class_name.endswith('ServiceImpl'):
                   service_interface = class_name.replace('ServiceImpl', 'Service')
                   interface_id = [id for name, id in class_name_to_id.items() if name == service_interface]
                   
                   if interface_id:
                       matrix[class_index_map[interface_id[0]], ep_index] = 1
           
           track_actions_recursively(data, action_class_id, int(action_method_id), matrix, class_index_map, ep_index)

def compute_cooccurrence_matrix(EP_matrix):
   num_classes = EP_matrix.shape[0]
   num_entrypoints = EP_matrix.shape[1]
   C = np.zeros((num_classes, num_classes), dtype=int)
   
   for i in range(num_classes):
       for j in range(num_classes):
           if i == j:
               C[i, i] = np.sum(EP_matrix[i, :])
           else:
               for k in range(num_entrypoints):
                   if EP_matrix[i, k] != 0 and EP_matrix[j, k] != 0:
                       C[i, j] += 1

   return C

def save_matrix_to_csv(matrix, filename):
   """Sauvegarde la matrice dans un fichier CSV."""
   np.savetxt(filename, matrix, fmt='%d', delimiter=",")

def main():
   global dependency_graph
   
   dependency_graph = load_data('dependency_graph.json')
   entrypoints = load_data('entrypoints.json')
   data = load_data('updated_project_analysis_results.json')
   inheritance_data = load_data('inheritance_relations.json')

   class_index_map = get_class_index_map(dependency_graph)
   class_name_to_id_map = get_class_name_to_id_map(dependency_graph)
   entrypoint_index_map = get_entrypoint_index_map(entrypoints)

   matrix = np.zeros((len(class_index_map), len(entrypoint_index_map)), dtype=int)

   update_matrix_with_actions(data, matrix, class_index_map, entrypoint_index_map, class_name_to_id_map)

   save_matrix_to_csv(matrix, "EP_matrix.csv")
   print("EP Matrix saved.")

   C_matrix = compute_cooccurrence_matrix(matrix)

   save_matrix_to_csv(C_matrix, "C_matrix.csv")
   print("C Matrix saved.")

   print("EP Matrix dimensions:", matrix.shape)
   print("C Matrix dimensions:", C_matrix.shape)

if __name__ == "__main__":
   main()