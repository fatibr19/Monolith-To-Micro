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

def main():
    # Current working directory operations
    base_project_dir = os.getcwd()  # Current project directory
    uploaded_zip = "projet_SI_gestion_ECM.zip"
    project_dir = unzip_java_project(uploaded_zip, base_project_dir)
    print(f"Project extracted to: {project_dir}")

    # Generate dependency graph
    analyzer = SpringBootAnalyzer("springboot-projects/projet_SI_gestion_ECM")
    analyzer.save_to_file("dependency_graph.json")
    print("Dependency graph generated successfully!")

    # Update dependency graph
    PROJECT_PATH = "springboot-projects/projet_SI_gestion_ECM/src/main/java"
    JSON_FILEPATH = "dependency_graph.json"
    update_dependency_graph(PROJECT_PATH, JSON_FILEPATH)

    # Generate entrypoints
    root_path = "springboot-projects/projet_SI_gestion_ECM"
    output_file = "entrypoints.json"
    entrypoints = analyze_files(root_path)
    save_to_json(entrypoints, output_file)
    print(f"Saved entrypoints to {output_file}")

    # Generate adjacency matrix
    dependency_graph_file = "dependency_graph.json"
    adjacency_matrix, nodes = generate_adjacency_matrix(dependency_graph_file)
    save_adjacency_matrix_as_csv(adjacency_matrix, "cogcn/cogcn/data/apps/acmeair/struct.csv")

    # Inheritance relations
    analyzer = InheritanceAnalyzer("springboot-projects/projet_SI_gestion_ECM")
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
    directory = 'springboot-projects/projet_SI_gestion_ECM'
    results = analyze_java_directory(directory)
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
        '--k', '4'
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
    dataset_dir = "data/apps/ECM"
    embeddings_file = os.path.join(dataset_dir, "embeddings.pkl")
    outliers_file = os.path.join(dataset_dir, "embeddings_outliers.pkl")
    membership_file = os.path.join(dataset_dir, "embeddings_membership.pkl")
    
    embeddings = load_pickle(embeddings_file)
    print(f"Embeddings shape: {embeddings.shape}")
    
    outliers = load_pickle(outliers_file)
    o_1, o_2 = outliers
    print(f"Outlier scores (o_1): {o_1.shape}, (o_2): {o_2.shape}")
    
    cluster_memberships = load_pickle(membership_file)
    print(f"Cluster memberships: {cluster_memberships}")
    
    visualize_embeddings(embeddings, labels=cluster_memberships, method='pca')
    visualize_embeddings(embeddings, labels=cluster_memberships, method='tsne', perplexity=10)

    # Graph decomposition visualization
    main_graph_visualisation()

if __name__ == "__main__":
    main()