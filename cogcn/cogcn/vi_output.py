# import os
# import pickle
# import numpy as np
# import matplotlib.pyplot as plt
# from sklearn.decomposition import PCA
# from sklearn.manifold import TSNE

# def load_pickle(file_path):
#     with open(file_path, 'rb') as f:
#         return pickle.load(f)

# def visualize_embeddings(embeddings, labels=None, method='pca', perplexity=10):
#     """
#     Visualize embeddings in 2D using PCA or t-SNE.
#     """
#     if method == 'pca':
#         reducer = PCA(n_components=2)
#     elif method == 'tsne':
#         reducer = TSNE(n_components=2, random_state=42, perplexity=perplexity)
#     else:
#         raise ValueError("Method should be either 'pca' or 'tsne'")

#     reduced_embeddings = reducer.fit_transform(embeddings)
#     plt.figure(figsize=(8, 6))

#     if labels is not None:
#         scatter = plt.scatter(reduced_embeddings[:, 0], reduced_embeddings[:, 1], c=labels, cmap='viridis', s=10)
#         plt.colorbar(scatter, label="Cluster Labels")
#     else:
#         plt.scatter(reduced_embeddings[:, 0], reduced_embeddings[:, 1], s=10)
    
#     plt.title(f"Visualization of Embeddings ({method.upper()})")
#     plt.xlabel("Component 1")
#     plt.ylabel("Component 2")
#     plt.show()

# def visualize_outliers(o_1, o_2):
#     """
#     Plot outlier scores for structural and attribute outliers.
#     """
#     plt.figure(figsize=(12, 6))
#     plt.plot(o_1, label='Structural Outlier Scores', alpha=0.8)
#     plt.plot(o_2, label='Attribute Outlier Scores', alpha=0.8)
#     plt.title("Outlier Scores")
#     plt.xlabel("Nodes")
#     plt.ylabel("Outlier Score")
#     plt.legend()
#     plt.show()

# if __name__ == "__main__":
#     # Path to your dataset directory
#     dataset_dir = "data/apps/acmeair"
#     embeddings_file = os.path.join(dataset_dir, "embeddings.pkl")
#     outliers_file = os.path.join(dataset_dir, "embeddings_outliers.pkl")
#     membership_file = os.path.join(dataset_dir, "embeddings_membership.pkl")

#     # Load embeddings
#     embeddings = load_pickle(embeddings_file)
#     print(f"Embeddings shape: {embeddings.shape}")

#     # Load outlier scores
#     outliers = load_pickle(outliers_file)
#     o_1, o_2 = outliers
#     print(f"Outlier scores (o_1): {o_1.shape}, (o_2): {o_2.shape}")

#     # Load cluster memberships
#     cluster_memberships = load_pickle(membership_file)
#     print(f"Cluster memberships: {cluster_memberships}")

#     # Visualize embeddings
#     visualize_embeddings(embeddings, labels=cluster_memberships, method='pca')
#     visualize_embeddings(embeddings, labels=cluster_memberships, method='tsne', perplexity=10)

#     # Visualize outlier scores
#     visualize_outliers(o_1, o_2)

import os
import pickle
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

def load_pickle(file_path):
    with open(file_path, 'rb') as f:
        return pickle.load(f)

def visualize_embeddings(embeddings, labels=None, method='pca', perplexity=10, output_file=None):
    """
    Visualize embeddings in 2D using PCA or t-SNE.
    """
    if method == 'pca':
        reducer = PCA(n_components=2)
    elif method == 'tsne':
        reducer = TSNE(n_components=2, random_state=42, perplexity=perplexity)
    else:
        raise ValueError("Method should be either 'pca' or 'tsne'")

    reduced_embeddings = reducer.fit_transform(embeddings)
    plt.figure(figsize=(8, 6))

    if labels is not None:
        scatter = plt.scatter(reduced_embeddings[:, 0], reduced_embeddings[:, 1], c=labels, cmap='viridis', s=10)
        plt.colorbar(scatter, label="Cluster Labels")
    else:
        plt.scatter(reduced_embeddings[:, 0], reduced_embeddings[:, 1], s=10)
    
    plt.title(f"Visualization of Embeddings ({method.upper()})")
    plt.xlabel("Component 1")
    plt.ylabel("Component 2")
    
    if output_file:
        plt.savefig(output_file)
        plt.close()
    else:
        plt.show()

def visualize_outliers(o_1, o_2, output_file=None):
    """
    Plot outlier scores for structural and attribute outliers.
    """
    plt.figure(figsize=(12, 6))
    plt.plot(o_1, label='Structural Outlier Scores', alpha=0.8)
    plt.plot(o_2, label='Attribute Outlier Scores', alpha=0.8)
    plt.title("Outlier Scores")
    plt.xlabel("Nodes")
    plt.ylabel("Outlier Score")
    plt.legend()
    
    if output_file:
        plt.savefig(output_file)
        plt.close()
    else:
        plt.show()

if __name__ == "__main__":
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

    # Visualize embeddings and save as files
    visualize_embeddings(embeddings, labels=cluster_memberships, method='pca', output_file='imgs/pca_embeddings.png')
    visualize_embeddings(embeddings, labels=cluster_memberships, method='tsne', perplexity=10, output_file='imgs/tsne_embeddings.png')

    # Visualize outlier scores and save as file
    visualize_outliers(o_1, o_2, output_file='imgs/outlier_scores.png')