# import os
# import json
# import pickle
# import networkx as nx
# import matplotlib.pyplot as plt
# import numpy as np

# def load_pickle(file_path):
#     with open(file_path, 'rb') as f:
#         return pickle.load(f)

# def load_index_mapping(file_path='../../index_mapping.json'):
#     with open(file_path, 'r') as f:
#         return json.load(f)

# def create_graph_from_embeddings(embeddings, cluster_memberships, outlier_scores, index_mapping):
#     """
#     Crée un graphe basé sur les embeddings avec les indices originaux.
#     """
#     similarity_matrix = np.dot(embeddings, embeddings.T)
    
#     # Mapper les nouveaux indices aux anciens indices
#     original_indices = list(index_mapping['rows'].values())
    
#     G = nx.Graph()
    
#     for i in range(len(embeddings)):
#         G.add_node(original_indices[i], 
#                    cluster=cluster_memberships[i], 
#                    outlier_structural=outlier_scores[0][i],
#                    outlier_attribute=outlier_scores[1][i])
    
#     threshold = np.percentile(similarity_matrix, 75)
#     for i in range(len(embeddings)):
#         for j in range(i+1, len(embeddings)):
#             if similarity_matrix[i, j] > threshold:
#                 G.add_edge(original_indices[i], original_indices[j], weight=similarity_matrix[i, j])
    
#     return G

# def visualize_graph(G):
#     """Visualise le graphe avec les indices originaux."""
#     plt.figure(figsize=(15, 12))
#     pos = nx.spring_layout(G, seed=42)
    
#     unique_clusters = set(nx.get_node_attributes(G, 'cluster').values())
#     color_map = plt.cm.get_cmap('tab10')
#     colors = [color_map(c/len(unique_clusters)) for c in nx.get_node_attributes(G, 'cluster').values()]
    
#     outlier_structural = nx.get_node_attributes(G, 'outlier_structural')
#     node_sizes = [1000 * (1 + outlier_structural[node]) for node in G.nodes()]
    
#     nx.draw_networkx_nodes(G, pos, node_color=colors, node_size=node_sizes, alpha=0.7)
#     nx.draw_networkx_edges(G, pos, alpha=0.2)
#     nx.draw_networkx_labels(G, pos, font_size=8)
    
#     plt.title("Graph of Nodes with Original Indices")
#     plt.axis('off')
#     plt.tight_layout()
#     plt.show()

# def main_graph_visualisation():
#     dataset_dir = "data/apps/acmeair"
#     embeddings_file = os.path.join(dataset_dir, "embeddings.pkl")
#     outliers_file = os.path.join(dataset_dir, "embeddings_outliers.pkl")
#     membership_file = os.path.join(dataset_dir, "embeddings_membership.pkl")

#     embeddings = load_pickle(embeddings_file)
#     outlier_scores = load_pickle(outliers_file)
#     cluster_memberships = load_pickle(membership_file)
#     index_mapping = load_index_mapping()

#     G = create_graph_from_embeddings(embeddings, cluster_memberships, outlier_scores, index_mapping)
#     visualize_graph(G)

# if __name__ == "__main__":
#     main_graph_visualisation()

import os
import json
import pickle
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def load_pickle(file_path):
    with open(file_path, 'rb') as f:
        return pickle.load(f)

def load_index_mapping(file_path='../../index_mapping.json'):
    with open(file_path, 'r') as f:
        return json.load(f)

def create_graph_from_embeddings(embeddings, cluster_memberships, outlier_scores, index_mapping):
    """
    Crée un graphe basé sur les embeddings avec les indices originaux.
    """
    similarity_matrix = np.dot(embeddings, embeddings.T)
   
    # Mapper les nouveaux indices aux anciens indices
    original_indices = list(index_mapping['rows'].values())
   
    G = nx.Graph()
   
    for i in range(len(embeddings)):
        G.add_node(original_indices[i],
                   cluster=cluster_memberships[i],
                   outlier_structural=outlier_scores[0][i],
                   outlier_attribute=outlier_scores[1][i])
   
    threshold = np.percentile(similarity_matrix, 75)
    for i in range(len(embeddings)):
        for j in range(i+1, len(embeddings)):
            if similarity_matrix[i, j] > threshold:
                G.add_edge(original_indices[i], original_indices[j], weight=similarity_matrix[i, j])
   
    return G

def visualize_graph(G, output_file=None):
    """Visualise le graphe avec les indices originaux."""
    plt.figure(figsize=(15, 12))
    pos = nx.spring_layout(G, seed=42)
   
    unique_clusters = set(nx.get_node_attributes(G, 'cluster').values())
    color_map = plt.cm.get_cmap('tab10')
    colors = [color_map(c/len(unique_clusters)) for c in nx.get_node_attributes(G, 'cluster').values()]
   
    outlier_structural = nx.get_node_attributes(G, 'outlier_structural')
    node_sizes = [1000 * (1 + outlier_structural[node]) for node in G.nodes()]
   
    nx.draw_networkx_nodes(G, pos, node_color=colors, node_size=node_sizes, alpha=0.7)
    nx.draw_networkx_edges(G, pos, alpha=0.2)
    nx.draw_networkx_labels(G, pos, font_size=8)
   
    plt.title("Graph of Nodes with Original Indices")
    plt.axis('off')
    plt.tight_layout()
    
    if output_file:
        plt.savefig(output_file)
        plt.close()
    else:
        plt.show()

def main_graph_visualisation(output_file='imgs/graph_decomposition.png'):
    dataset_dir = "data/apps/ECM"
    embeddings_file = os.path.join(dataset_dir, "embeddings.pkl")
    outliers_file = os.path.join(dataset_dir, "embeddings_outliers.pkl")
    membership_file = os.path.join(dataset_dir, "embeddings_membership.pkl")
    
    embeddings = load_pickle(embeddings_file)
    outlier_scores = load_pickle(outliers_file)
    cluster_memberships = load_pickle(membership_file)
    index_mapping = load_index_mapping()
    
    G = create_graph_from_embeddings(embeddings, cluster_memberships, outlier_scores, index_mapping)
    visualize_graph(G, output_file)

if __name__ == "__main__":
    main_graph_visualisation()