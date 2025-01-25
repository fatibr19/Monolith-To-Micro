import json
import numpy as np
import csv

def generate_adjacency_matrix(dependency_graph_file):
    with open(dependency_graph_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    nodes = data["nodes"]
    edges = data["edges"][0]["relationship"]

    # Create a mapping of class IDs to index in the matrix
    node_id_to_index = {node["id"]: idx for idx, node in enumerate(nodes)}

    # Initialize the adjacency matrix with zeros
    adjacency_matrix = np.zeros((len(nodes), len(nodes)), dtype=int)

    # Populate the adjacency matrix based on edges
    for edge in edges:
        start_idx = node_id_to_index[edge["properties"]["start"]]
        end_idx = node_id_to_index[edge["properties"]["end"]]
        adjacency_matrix[start_idx][end_idx] = 1
        adjacency_matrix[end_idx][start_idx] = 1  # If the relationship is undirected

    return adjacency_matrix, nodes

def save_adjacency_matrix_as_csv(adjacency_matrix, output_file):
    # Save adjacency matrix to a CSV file without class names in the first line
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Write matrix rows
        for row in adjacency_matrix:
            writer.writerow(row)

if __name__ == "__main__":
    dependency_graph_file = "dependency_graph.json"
    adjacency_matrix, nodes = generate_adjacency_matrix(dependency_graph_file)
    save_adjacency_matrix_as_csv(adjacency_matrix, "adjacency_matrix.csv")