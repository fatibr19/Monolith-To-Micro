import os
import json
import javalang
from pathlib import Path
import numpy as np
import argparse
import subprocess
import sys

from unzip_project import unzip_java_project
from dep_graph_gen import SpringBootAnalyzer
from entrypointJsonGen import analyze_files, save_to_json
from extrac import load_json_data, analyze_project, save_analysis_to_json
from Gen_InheritanceMatrix_classNamesMapping import create_symmetric_inheritance_matrix
from Gen_updated_dep_graph import update_dependency_graph
from generate_X import remove_zero_rows
from graph_To_AdjacencyM import generate_adjacency_matrix, save_adjacency_matrix_as_csv
from inheritanceJson import InheritanceAnalyzer
from java_class_methodsJson import analyze_java_directory, save_results_to_json
from project_analysis_results_with_inheritanceJson import process_project_analysis
from cogcn.cogcn.vi_output import load_pickle, visualize_embeddings, visualize_outliers
from cogcn.cogcn.graph_visualisation import main_graph_visualisation

def main(uploaded_zip, k):
    # Current working directory operations
    base_project_dir = os.getcwd()  # Current project directory
    project_dir = unzip_java_project(uploaded_zip, base_project_dir)
    print(f"Project extracted to: {project_dir}")

    # Get project name from zip filename (without extension)
    project_name = os.path.splitext(os.path.basename(uploaded_zip))[0]
    project_path = os.path.join('springboot-projects', project_name)

    # Generate dependency graph
    analyzer = SpringBootAnalyzer(project_path)
    analyzer.save_to_file("dependency_graph.json")
    print("Dependency graph generated successfully!")

    # Update dependency graph
    PROJECT_PATH = os.path.join(project_path, 'src/main/java')
    JSON_FILEPATH = "dependency_graph.json"
    update_dependency_graph(PROJECT_PATH.replace("\\","/"), JSON_FILEPATH)
    print(f"depency graph updated successfully, project_path: {PROJECT_PATH}")

    # Generate entrypoints
    entrypoints = analyze_files(project_path)
    save_to_json(entrypoints, "entrypoints.json")
    print(f"Saved entrypoints to entrypoints.json")

    # Generate adjacency matrix
    dependency_graph_file = "dependency_graph.json"
    adjacency_matrix, nodes = generate_adjacency_matrix(dependency_graph_file)
    save_adjacency_matrix_as_csv(adjacency_matrix, "cogcn/cogcn/data/apps/acmeair/struct.csv")

    # Inheritance relations
    analyzer = InheritanceAnalyzer(project_path)
    analyzer.analyze()
    analyzer.save_to_file("inheritance_relations.json")

    # Inheritance matrix and class names mapping
    nodes_file = "dependency_graph.json"  
    with open(nodes_file, 'r') as f:
        nodes_data = json.load(f)
    
    inheritance_matrix, class_names = create_symmetric_inheritance_matrix(
        nodes_data, 
        "inheritance_relations.json"
    )
    np.savetxt('inheritance_matrix.csv', inheritance_matrix, delimiter=',', fmt='%d')    
    
    print(f"Matrix dimensions: {inheritance_matrix.shape}")
    print(f"Total relations (including symmetry): {np.sum(inheritance_matrix)}")
    print(f"Number of classes: {len(class_names)}")
    print("Symmetric inheritance matrix saved to 'inheritance_matrix.csv'")
    
    node_mapping = {str(i): name for i, name in enumerate(class_names)}
    with open('node_mapping.json', 'w') as f:
        json.dump(node_mapping, f, indent=4)
    print("Class list saved to 'node_mapping.json'")

    # Java class methods
    results = analyze_java_directory(project_path)
    save_results_to_json(results)

    # Project analysis with inheritance
    json_file_path = 'java_class_methods.json'
    inheritance_file = 'inheritance_relations.json'
    node_mapping_file = 'node_mapping.json'
    
    json_data = load_json_data(json_file_path)
    if json_data:
        project_analysis = analyze_project(json_data, inheritance_file, node_mapping_file)        
        output_file = 'project_analysis_results_with_inheritance.json'
        save_analysis_to_json(project_analysis, output_file)
        print(f"Analysis completed and saved to {output_file}")
    else:
        print("Failed to load or invalid JSON data.")

    # Updated project analysis
    process_project_analysis()

    # Generate X matrix
    EP_matrix = np.loadtxt('EP_matrix.csv', delimiter=',')
    C_matrix = np.loadtxt('C_matrix.csv', delimiter=',')
    In_matrix = np.loadtxt('inheritance_matrix.csv', delimiter=',')
    struct_matrix = np.loadtxt('cogcn/cogcn/data/apps/acmeair/struct.csv', delimiter=',')    
    X, index_mapping, struct_filtered = remove_zero_rows(EP_matrix, C_matrix, In_matrix, struct_matrix)    
    
    with open('index_mapping.json', 'w') as f:
        json.dump(index_mapping, f)    
    
    np.savetxt('cogcn/cogcn/data/apps/ECM/content.csv', X, delimiter=',', fmt='%.15f')
    np.savetxt('cogcn/cogcn/data/apps/ECM/struct.csv', struct_filtered, delimiter=',', fmt='%.15f')    
    
    print("X matrix dimensions:", X.shape)
    print("Struct matrix dimensions:", struct_filtered.shape)

    # Change to cogcn/cogcn directory for subsequent operations
    print("Changing directory to cogcn/cogcn")
    os.chdir('cogcn/cogcn')

    # Run training using subprocess
    training_cmd = [
        sys.executable, 'train.py', 
        '--dataset-str', 'data/apps/ECM', 
        '--k', f"{k}"
    ]
    
    try:
        print("Executing training command:", ' '.join(training_cmd))
        result = subprocess.run(training_cmd, check=True, capture_output=True, text=True)
        print("Training output:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("Training failed with error:")
        print(e.stderr)
        raise
    
    # Visualize embeddings
    
    # Path to your dataset directory
    dataset_dir = "data/apps/ECM"
    embeddings_file = os.path.join(dataset_dir, "embeddings.pkl")
    outliers_file = os.path.join(dataset_dir, "embeddings_outliers.pkl")
    membership_file = os.path.join(dataset_dir, "embeddings_membership.pkl")

    # Load embeddings
    embeddings = load_pickle(embeddings_file)
    print(f"Embeddings shape: {embeddings.shape}")

    # Load outlier scores
    outliers = load_pickle(outliers_file)
    o_1, o_2 = outliers
    print(f"Outlier scores (o_1): {o_1.shape}, (o_2): {o_2.shape}")

    # Load cluster memberships
    cluster_memberships = load_pickle(membership_file)
    print(f"Cluster memberships: {cluster_memberships}")

    if not os.path.exists('imgs'):
        os.makedirs('imgs')

    # Visualize embeddings and save as files
    visualize_embeddings(embeddings, labels=cluster_memberships, method='pca', output_file='imgs/pca_embeddings.png')
    visualize_embeddings(embeddings, labels=cluster_memberships, method='tsne', perplexity=10, output_file='imgs/tsne_embeddings.png')

    # Visualize outlier scores and save as file
    visualize_outliers(o_1, o_2, output_file='imgs/outlier_scores.png')

    # Graph decomposition visualization
    main_graph_visualisation()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process Java project ZIP file')
    parser.add_argument('zip_file', help='Path to the Java project ZIP file')
    parser.add_argument('-k', type=int, default=5, help='Value of k for the k-nearest neighbor algorithm')
    args = parser.parse_args()
    
    main(args.zip_file, args.k)